#!/bin/bash
# Wrapper script for connection discovery
# Usage: ./run_connections.sh "note name" [--semantic-only] [--explicit-only] [--json]
# Usage: ./run_connections.sh --hubs [--json]
# Usage: ./run_connections.sh --stats [--json]
# Usage: ./run_connections.sh --bridges [--json]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/connections.py" "$@"
