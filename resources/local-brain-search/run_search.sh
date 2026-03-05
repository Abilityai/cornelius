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
# Examples:
#   ./run_search.sh "dopamine and motivation"
#   ./run_search.sh "connect Buddhism and AI" --mode spreading
#   ./run_search.sh "recent notes about agents" --mode spreading --intent temporal
#   ./run_search.sh "what is spreading activation" --mode spreading --explain --json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/search.py" "$@"
