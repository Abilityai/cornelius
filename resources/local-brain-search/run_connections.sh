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

# Try daemon first (fast path)
if curl -s --max-time 0.2 "$DAEMON_URL/health" > /dev/null 2>&1; then
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

    # Route to correct endpoint
    if [ "$STATS" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/stats")
    elif [ "$HUBS" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/hubs")
    elif [ "$BRIDGES" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/bridges")
    else
        ENCODED_Q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections?q=$ENCODED_Q&depth=$DEPTH&semantic_only=$SEMANTIC_ONLY&explicit_only=$EXPLICIT_ONLY")
    fi

    if [ "$JSON_OUT" = "true" ]; then
        echo "$RESULT"
    else
        echo "$RESULT" | python3 -m json.tool
    fi
    exit 0
fi

# Fallback: direct Python (original behavior)
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/connections.py" "$@"
