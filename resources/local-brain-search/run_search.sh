#!/bin/bash
# Wrapper script for semantic search
# Usage: ./run_search.sh "query" [--limit N] [--threshold 0.X] [--json]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/search.py" "$@"
