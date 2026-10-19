#!/bin/bash
# Wrapper script for semantic search
# Usage: ./run_search.sh "query" [options]
#
# Options:
#   --limit N           Maximum results (default: 10)
#   --threshold 0.X     Similarity threshold 0-1 (default: 0.5)
#   --mode MODE         Search mode: static or spreading (default: spreading)
#   --intent INTENT     Override detected intent: factual/conceptual/synthesis/temporal
#   --explain           Show activation traces (for spreading mode)
#   --json              Output as JSON
#   --full              Show full content instead of preview
#   --no-track          Disable usage tracking for this search (Phase 4 learning)
#
# If the daemon is running, queries go via HTTP (fast).
# If not, falls back to direct Python invocation (original behavior).
#
# Examples:
#   ./run_search.sh "dopamine and motivation"
#   ./run_search.sh "connect Buddhism and AI" --mode spreading
#   ./run_search.sh "recent notes about agents" --mode spreading --intent temporal
#   ./run_search.sh "what is spreading activation" --mode spreading --explain --json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${BRAIN_DAEMON_PORT:-7437}"
DAEMON_URL="http://127.0.0.1:$PORT"
FAISS_FILE="$SCRIPT_DIR/data/brain.faiss"
SCOPE="${BRAIN_READ_SCOPE:-core}"   # fail-closed default; widen by exporting BRAIN_READ_SCOPE

# A daemon is usable only if the index it loaded matches the on-disk index. A
# stale daemon (reindex without restart, or a pre-scope build that has no
# build_id) is failed over to the fresh-process CLI path below, which always
# reads the current index + code - never serving a wrongly-scoped result.
source "$SCRIPT_DIR/wrapper_common.sh" || exit 1

# Try daemon first (fast path)
if daemon_fresh; then
    # Parse args into URL params
    QUERY=""
    LIMIT="10"
    THRESHOLD="0.5"
    MODE=""
    INTENT=""
    EXPLAIN="false"
    NO_TRACK="false"
    FULL="false"
    JSON_OUT="false"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --limit|-n)   LIMIT="$2"; shift 2 ;;
            --threshold|-t) THRESHOLD="$2"; shift 2 ;;
            --mode|-m)    MODE="$2"; shift 2 ;;
            --intent|-i)  INTENT="$2"; shift 2 ;;
            --explain|-e) EXPLAIN="true"; shift ;;
            --no-track)   NO_TRACK="true"; shift ;;
            --full|-f)    FULL="true"; shift ;;
            --json|-j)    JSON_OUT="true"; shift ;;
            *)
                if [ -z "$QUERY" ]; then
                    QUERY="$1"
                fi
                shift ;;
        esac
    done

    # URL-encode query + scope
    ENCODED_Q=$(url_encode "$QUERY") || {
        echo "Failed to encode search query" >&2
        exit 1
    }
    ENCODED_SCOPE=$(url_encode "$SCOPE") || {
        echo "Failed to encode search scope" >&2
        exit 1
    }

    URL="$DAEMON_URL/search?q=$ENCODED_Q&limit=$LIMIT&threshold=$THRESHOLD&explain=$EXPLAIN&no_track=$NO_TRACK&full=$FULL&scope=$ENCODED_SCOPE"
    [ -n "$MODE" ] && URL="$URL&mode=$MODE"
    [ -n "$INTENT" ] && URL="$URL&intent=$INTENT"

    RESULT=$(curl -s --max-time 30 "$URL")

    if [ "$JSON_OUT" = "true" ]; then
        echo "$RESULT"
    else
        # Pretty-print for human consumption
        echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('results', [])
mode = data.get('mode', 'static')
meta = data.get('metadata', {})

if not results:
    print(f\"No results found for: {data.get('query', '')}\")
    sys.exit(0)

print(f\"\nFound {len(results)} results for: {data.get('query', '')}\")
print(f\"(mode: {mode}, via daemon)\")

if 'intent' in meta:
    print(f\"Intent: {meta['intent']} ({meta.get('confidence', 0):.0%} confidence)\")

for r in results:
    score = r.get('activation', r.get('similarity', 0))
    label = 'activation' if 'activation' in r else 'similarity'
    print(f\"\n{'='*60}\")
    print(f\"[{score:.1%} {label}] {r['title']}\")
    heading = r.get('heading', '')
    if heading and heading != r['title']:
        print(f\"  Section: {heading}\")
    filepath = r.get('filepath', '')
    if filepath:
        print(f\"  Path: {filepath}\")
    content = r.get('content', '')
    if content:
        preview = content[:300]
        if len(content) > 300:
            preview += '...'
        print(f\"\n{preview}\")

print(f\"\n{'='*60}\")
print(f\"Mode: {mode.upper()} (via daemon)\")
"
    fi
    exit 0
fi

# Fallback: direct Python (original behavior)
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/search.py" "$@"
