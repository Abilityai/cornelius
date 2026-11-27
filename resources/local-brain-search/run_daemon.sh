#!/bin/bash
# Brain Search Daemon management
# Usage: ./run_daemon.sh start|stop|restart|reload|status|fresh|ensure [--wait]|watchdog [stop]
#
#   fresh    exit 0 iff a daemon answers /health AND loaded the on-disk index
#            (build_id == brain.faiss mtime) AND resolves role aliases. Silent.
#   ensure   make it so: nothing if fresh; otherwise (re)start the daemon in the
#            BACKGROUND and return at once (the caller's current query falls back to
#            the cold CLI path; the next one is warm). `--wait` blocks until healthy
#            (<= 90s). Lock-guarded, so N parallel reads on a miss start ONE daemon.
#            Disabled by BRAIN_DAEMON_AUTOSTART=0 (tests, e2e). Fails soft when the
#            venv is not bootstrapped. Called by run_search.sh / run_connections.sh on
#            a daemon miss, by run_index.sh after a rebuild, and by /refresh-index.
#   watchdog detached loop that calls `ensure` every 120s so a crash between reads
#            heals without waiting for the next query. .daemon-watchdog.lock holds the
#            loop pid (stale when dead); `watchdog stop` kills it. Disabled by
#            BRAIN_DAEMON_AUTOSTART=0. Started by .trinity/setup.sh on container boot.
#
# Log: daemon.log is append-only (preserves crash evidence across restarts); rotated
# to daemon.log.1 at ~5 MB (one generation kept). start case writes a banner line.
#
# Why ensure exists (2026-11-06): the daemon had no supervisor, the daily reindex
# invalidated it through the wrapper's build-id guard, and the wrapper's silent
# fallback hid both - every read paid a ~4.5s torch import. See ARCHITECTURE.md
# -> "Search daemon liveness".

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/daemon.pid"
PORT="${BRAIN_DAEMON_PORT:-7437}"
PYTHON="$SCRIPT_DIR/venv/bin/python"
LOG_FILE="$SCRIPT_DIR/daemon.log"
FAISS_FILE="$SCRIPT_DIR/data/brain.faiss"
HEALTH_URL="http://127.0.0.1:$PORT/health"
ENSURE_LOCK="$SCRIPT_DIR/.daemon-ensure.lock"

get_pid() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo "$pid"
            return 0
        fi
        rm -f "$PID_FILE"
    fi
    # No pid file but something owns the port (daemon started by another path):
    # adopt it so stop/restart never leave a zombie holding :$PORT.
    # lsof is not in the Trinity base image, so fall back to the pid the daemon
    # itself reports on /health. Without this, a daemon started by `ensure` (e.g.
    # from run_index.sh) while a second `start` lost the port race was left with
    # daemon.pid naming the dead loser - "the daemon is gone" while it was serving.
    local port_pid
    port_pid=$(lsof -nP -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -1)
    if [ -z "$port_pid" ]; then
        port_pid=$(curl -s --max-time 0.5 "$HEALTH_URL" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('pid') or '')" 2>/dev/null)
        kill -0 "$port_pid" 2>/dev/null || port_pid=""
    fi
    if [ -n "$port_pid" ]; then
        echo "$port_pid" > "$PID_FILE"
        echo "$port_pid"
        return 0
    fi
    return 1
}

# Mirrors daemon_fresh() in run_search.sh / run_connections.sh (keep in sync).
# Prints a reason on stdout when NOT fresh; prints nothing when fresh.
freshness() {
    local health build_id on_disk
    health=$(curl -s --max-time 0.5 "$HEALTH_URL" 2>/dev/null) || { echo "down"; return 1; }
    [ -n "$health" ] || { echo "down"; return 1; }
    build_id=$(printf '%s' "$health" | python3 -c "import sys,json; d=json.load(sys.stdin); v=d.get('build_id'); print(v if v is not None else '')" 2>/dev/null) || { echo "no-build-id"; return 1; }
    [ -n "$build_id" ] || { echo "no-build-id"; return 1; }
    [ -f "$FAISS_FILE" ] || { echo "no-index"; return 1; }
    on_disk=$(python3 -c "import os;print(int(os.path.getmtime('$FAISS_FILE')))" 2>/dev/null) || { echo "no-index"; return 1; }
    [ "$build_id" = "$on_disk" ] || { echo "stale (daemon build_id $build_id, on-disk $on_disk)"; return 1; }
    printf '%s' "$health" | grep -q '"role_aliases": *true' || { echo "old-code (no role aliases)"; return 1; }
    return 0
}

wait_healthy() {   # $1 = seconds
    local i
    for i in $(seq 1 "${1:-30}"); do
        if curl -s --max-time 1 "$HEALTH_URL" > /dev/null 2>&1; then return 0; fi
        sleep 1
    done
    return 1
}

case "${1:-status}" in
    start)
        if pid=$(get_pid); then
            echo "Daemon already running (PID $pid)"
            exit 0
        fi
        if [ ! -x "$PYTHON" ]; then
            echo "Daemon not started: venv missing at $PYTHON (reads fall back to the CLI path)"
            exit 0
        fi
        # Rotate log at ~5 MB, keep one generation so crash evidence survives restart
        if [ -f "$LOG_FILE" ] && [ "$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)" -gt 5242880 ]; then
            mv "$LOG_FILE" "${LOG_FILE}.1"
        fi
        echo "Starting brain search daemon on port $PORT..."
        setsid nohup "$PYTHON" "$SCRIPT_DIR/daemon.py" >> "$LOG_FILE" 2>&1 < /dev/null &
        daemon_pid=$!
        disown 2>/dev/null
        echo $daemon_pid > "$PID_FILE"
        printf '=== start %s pid %s ===\n' "$(date -u +%FT%TZ)" "$daemon_pid" >> "$LOG_FILE"
        if wait_healthy 60; then
            # The pid that answers is the one that owns the port - if another
            # start won the bind race, ours has exited; record the winner.
            served=$(curl -s --max-time 1 "$HEALTH_URL" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('pid') or '')" 2>/dev/null)
            [ -n "$served" ] && kill -0 "$served" 2>/dev/null && echo "$served" > "$PID_FILE"
            echo "Daemon started (PID $(cat "$PID_FILE"))"
            exit 0
        fi
        echo "Daemon started but not yet responding (check $LOG_FILE)"
        ;;

    stop)
        if pid=$(get_pid); then
            echo "Stopping daemon (PID $pid)..."
            kill "$pid"
            # wait for the port to free so an immediate start can bind
            for i in $(seq 1 20); do
                kill -0 "$pid" 2>/dev/null || break
                sleep 0.25
            done
            rm -f "$PID_FILE"
            echo "Stopped."
        else
            echo "Daemon not running."
        fi
        ;;

    restart)
        "$0" stop
        sleep 1
        "$0" start
        ;;

    reload)
        if pid=$(get_pid); then
            echo "Reloading brain data..."
            kill -SIGHUP "$pid"
            echo "Reload signal sent to PID $pid"
        else
            echo "Daemon not running."
            exit 1
        fi
        ;;

    status)
        if pid=$(get_pid); then
            echo "Daemon running (PID $pid)"
            curl -s "$HEALTH_URL" 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "(not responding yet)"
            reason=$(freshness) && echo "Fresh: yes" || echo "Fresh: NO - $reason"
        else
            echo "Daemon not running."
        fi
        ;;

    fresh)
        freshness > /dev/null
        ;;

    ensure)
        [ "${BRAIN_DAEMON_AUTOSTART:-1}" = "0" ] && exit 0
        if reason=$(freshness); then exit 0; fi
        [ -x "$PYTHON" ] || exit 0           # fail soft: no venv, nothing to start
        # One starter at a time. The lock holds the worker's pid: a dead worker
        # (on Trinity the orphan sweep can kill it mid-start, cornelius#17) means a
        # stale lock, cleared now rather than blocking restarts. A lock with no pid
        # yet older than 3 minutes is a starter that crashed before writing it.
        if [ -d "$ENSURE_LOCK" ]; then
            lock_pid=$(cat "$ENSURE_LOCK/pid" 2>/dev/null)
            if { [ -n "$lock_pid" ] && ! kill -0 "$lock_pid" 2>/dev/null; } \
               || [ -n "$(find "$ENSURE_LOCK" -maxdepth 0 -mmin +3 2>/dev/null)" ]; then
                rm -rf "$ENSURE_LOCK"
            fi
        fi
        if mkdir "$ENSURE_LOCK" 2>/dev/null; then
            echo "$(date -u +%FT%TZ) ensure: daemon $reason - (re)starting" >> "$LOG_FILE"
            # Detached worker: restart if a (stale/old) daemon is up, else start; then drop the lock.
            nohup bash -c "
                echo \$\$ > '$ENSURE_LOCK/pid'
                if curl -s --max-time 0.5 '$HEALTH_URL' > /dev/null 2>&1; then '$0' stop; sleep 1; fi
                '$0' start
                rm -rf '$ENSURE_LOCK'
            " > /dev/null 2>&1 < /dev/null &
            disown 2>/dev/null
        fi
        if [ "$2" = "--wait" ]; then
            for i in $(seq 1 90); do
                freshness > /dev/null && { echo "Daemon fresh."; exit 0; }
                sleep 1
            done
            echo "Daemon not fresh after 90s: $(freshness)"
            exit 1
        fi
        ;;

    watchdog)
        WATCHDOG_LOCK="$SCRIPT_DIR/.daemon-watchdog.lock"
        if [ "${2:-}" = "stop" ]; then
            if [ -f "$WATCHDOG_LOCK" ]; then
                wdog_pid=$(cat "$WATCHDOG_LOCK" 2>/dev/null)
                if [ -n "$wdog_pid" ] && kill -0 "$wdog_pid" 2>/dev/null; then
                    kill "$wdog_pid" && echo "Watchdog stopped (PID $wdog_pid)."
                else
                    echo "Watchdog not running (stale lock)."
                fi
                rm -f "$WATCHDOG_LOCK"
            else
                echo "Watchdog not running."
            fi
            exit 0
        fi
        # watchdog start (default subcommand)
        [ "${BRAIN_DAEMON_AUTOSTART:-1}" = "0" ] && exit 0
        # One watchdog per checkout: lock file holds loop pid, stale when pid is dead
        if [ -f "$WATCHDOG_LOCK" ]; then
            wdog_pid=$(cat "$WATCHDOG_LOCK" 2>/dev/null)
            if [ -n "$wdog_pid" ] && kill -0 "$wdog_pid" 2>/dev/null; then
                echo "Watchdog already running (PID $wdog_pid)."
                exit 0
            fi
            rm -f "$WATCHDOG_LOCK"
        fi
        setsid bash -c "
            echo \$\$ > '$WATCHDOG_LOCK'
            while true; do
                sleep 120
                [ \"\${BRAIN_DAEMON_AUTOSTART:-1}\" = \"0\" ] && exit 0
                if ! '$SCRIPT_DIR/run_daemon.sh' fresh > /dev/null 2>&1; then
                    printf '=== watchdog: daemon not fresh - (re)starting %s ===\n' \"\$(date -u +%FT%TZ)\" >> '$LOG_FILE'
                    '$SCRIPT_DIR/run_daemon.sh' ensure
                fi
            done
        " > /dev/null 2>&1 < /dev/null &
        disown 2>/dev/null
        echo "Watchdog started."
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|reload|status|fresh|ensure [--wait]|watchdog [stop]}"
        exit 1
        ;;
esac
