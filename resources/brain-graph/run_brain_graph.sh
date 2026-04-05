#!/bin/bash
# Brain Dependency Graph - CLI Wrapper
#
# Usage:
#   ./run_brain_graph.sh bootstrap [--force]
#   ./run_brain_graph.sh status [--json]
#   ./run_brain_graph.sh inspect "Note Name" [--json]
#   ./run_brain_graph.sh propagate "Note Name" [--magnitude 0.8] [--json]
#   ./run_brain_graph.sh lifecycle [--json]
#   ./run_brain_graph.sh tensions [--similarity 0.75] [--divergence 0.3] [--json]
#   ./run_brain_graph.sh coherence [--days 7] [--tensions] [--json]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/../local-brain-search/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Python venv not found at $VENV_DIR" >&2
    echo "Set up local-brain-search first." >&2
    exit 1
fi

# Activate venv and run CLI
source "$VENV_DIR/bin/activate"
cd "$SCRIPT_DIR"
python cli.py "$@"
