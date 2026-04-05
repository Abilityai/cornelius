#!/bin/bash
# Brain Search Daemon management
# Usage: ./run_daemon.sh start|stop|restart|reload|status

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/daemon.pid"
PORT="${BRAIN_DAEMON_PORT:-7437}"
PYTHON="$SCRIPT_DIR/venv/bin/python"
LOG_FILE="$SCRIPT_DIR/daemon.log"

get_pid() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo "$pid"
            return 0
        fi
        rm -f "$PID_FILE"
    fi
    return 1
}

case "${1:-status}" in
    start)
        if pid=$(get_pid); then
            echo "Daemon already running (PID $pid)"
            exit 0
        fi
        echo "Starting brain search daemon on port $PORT..."
        nohup "$PYTHON" "$SCRIPT_DIR/daemon.py" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        # Wait for it to be ready
        for i in $(seq 1 30); do
            if curl -s "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
                echo "Daemon started (PID $(cat "$PID_FILE"))"
                exit 0
            fi
            sleep 1
        done
        echo "Daemon started but not yet responding (check $LOG_FILE)"
        ;;

    stop)
        if pid=$(get_pid); then
            echo "Stopping daemon (PID $pid)..."
            kill "$pid"
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
            curl -s "http://127.0.0.1:$PORT/health" 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "(not responding yet)"
        else
            echo "Daemon not running."
        fi
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|reload|status}"
        exit 1
        ;;
esac
