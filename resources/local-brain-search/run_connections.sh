#!/bin/bash
# Wrapper script for connection discovery
# Usage: ./run_connections.sh "note name" [--semantic-only] [--explicit-only] [--json]
# Usage: ./run_connections.sh --hubs [--json]
# Usage: ./run_connections.sh --stats [--json]
# Usage: ./run_connections.sh --bridges [--json]
#
# If the daemon is running, queries go via HTTP (fast).
# If not, falls back to direct Python invocation (original behavior).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${BRAIN_DAEMON_PORT:-7437}"
DAEMON_URL="http://127.0.0.1:$PORT"
FAISS_FILE="$SCRIPT_DIR/data/brain.faiss"
SCOPE="${BRAIN_READ_SCOPE:-core}"   # fail-closed default; widen by exporting BRAIN_READ_SCOPE

# A daemon is usable only if its loaded index matches the on-disk index; a stale
# daemon fails over to the fresh-process CLI path below. (See run_search.sh.)
daemon_fresh() {
    local health build_id on_disk
    health=$(curl -s --max-time 0.2 "$DAEMON_URL/health" 2>/dev/null) || return 1
    [ -n "$health" ] || return 1
    build_id=$(printf '%s' "$health" | python3 -c "import sys,json; d=json.load(sys.stdin); v=d.get('build_id'); print(v if v is not None else '')" 2>/dev/null) || return 1
    [ -n "$build_id" ] || return 1
    [ -f "$FAISS_FILE" ] || return 1
    on_disk=$(python3 -c "import os;print(int(os.path.getmtime('$FAISS_FILE')))" 2>/dev/null) || return 1
    [ "$build_id" = "$on_disk" ] || return 1
    # a role alias (@reasoning/@lookup) needs a daemon whose code resolves it; an older
    # daemon would read "@reasoning" as a folder and silently return nothing
    case "$SCOPE" in *@*) printf '%s' "$health" | grep -q '"role_aliases": *true' || return 1 ;; esac
}

# Try daemon first (fast path)
if daemon_fresh; then
    # Parse args
    QUERY=""
    DEPTH="1"
    SEMANTIC_ONLY="false"
    EXPLICIT_ONLY="false"
    STATS="false"
    HUBS="false"
    BRIDGES="false"
    JSON_OUT="false"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --depth|-d)        DEPTH="$2"; shift 2 ;;
            --semantic-only)   SEMANTIC_ONLY="true"; shift ;;
            --explicit-only)   EXPLICIT_ONLY="true"; shift ;;
            --stats)           STATS="true"; shift ;;
            --hubs)            HUBS="true"; shift ;;
            --bridges)         BRIDGES="true"; shift ;;
            --json|-j)         JSON_OUT="true"; shift ;;
            *)
                if [ -z "$QUERY" ]; then
                    QUERY="$1"
                fi
                shift ;;
        esac
    done

    # Route to correct endpoint. scope is forwarded to every /connections*
    # endpoint for URL uniformity; hubs/bridges/stats ignore it (fingerprint /
    # whole-graph), the traversal endpoint honors it under enforcement.
    ENCODED_SCOPE=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$SCOPE")
    if [ "$STATS" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/stats")
    elif [ "$HUBS" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/hubs?scope=$ENCODED_SCOPE")
    elif [ "$BRIDGES" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/bridges?scope=$ENCODED_SCOPE")
    else
        ENCODED_Q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections?q=$ENCODED_Q&depth=$DEPTH&semantic_only=$SEMANTIC_ONLY&explicit_only=$EXPLICIT_ONLY&scope=$ENCODED_SCOPE")
    fi

    if [ "$JSON_OUT" = "true" ]; then
        echo "$RESULT"
    else
        echo "$RESULT" | python3 -m json.tool
    fi
    exit 0
fi

# Daemon miss (down, stale after a reindex, or old code): start/restart it in the
# background so the NEXT read is warm, then serve THIS read from the cold CLI path.
# One starter at a time (lock in run_daemon.sh); BRAIN_DAEMON_AUTOSTART=0 disables.
"$SCRIPT_DIR/run_daemon.sh" ensure > /dev/null 2>&1

# Fallback: direct Python (original behavior)
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/connections.py" "$@"
