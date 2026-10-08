#!/bin/bash
# Wrapper script for benchmark-memory
# Uses the local-brain-search venv for dependencies

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate from scripts -> benchmark-memory -> skills -> .claude -> project root
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
VENV_PYTHON="$PROJECT_DIR/resources/local-brain-search/venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: venv Python not found at $VENV_PYTHON"
    echo "Run 'python -m venv venv && pip install -r requirements.txt' in resources/local-brain-search/"
    exit 1
fi

cd "$SCRIPT_DIR"
"$VENV_PYTHON" run_benchmark.py "$@"
