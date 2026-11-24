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
source "$SCRIPT_DIR/wrapper_common.sh" || exit 1

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
    ENCODED_SCOPE=$(url_encode "$SCOPE") || {
        echo "Failed to encode connection scope" >&2
        exit 1
    }
    if [ "$STATS" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/stats")
    elif [ "$HUBS" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/hubs?scope=$ENCODED_SCOPE")
    elif [ "$BRIDGES" = "true" ]; then
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections/bridges?scope=$ENCODED_SCOPE")
    else
        ENCODED_Q=$(url_encode "$QUERY") || {
            echo "Failed to encode connection query" >&2
            exit 1
        }
        RESULT=$(curl -s --max-time 30 "$DAEMON_URL/connections?q=$ENCODED_Q&depth=$DEPTH&semantic_only=$SEMANTIC_ONLY&explicit_only=$EXPLICIT_ONLY&scope=$ENCODED_SCOPE")
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
