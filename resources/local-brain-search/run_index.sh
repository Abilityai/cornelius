#!/bin/bash
# Wrapper script for re-indexing the Brain
# Usage: ./run_index.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# -u forces unbuffered stdout/stderr. Without it Python block-buffers when its
# output is piped (not a tty), so the indexer's progress prints don't appear
# until the process exits — which reads as a silent multi-minute Bash call and
# trips the platform's 300s stall watchdog. See .claude/skills/refresh-index.
"$SCRIPT_DIR/venv/bin/python" -u "$SCRIPT_DIR/index_brain.py" "$@"
rc=$?

# A rebuilt brain.faiss invalidates the running daemon (the wrappers' build-id
# guard then routes every read to the ~4.5s cold path). Re-point the daemon at
# the new index in the background; harmless when no daemon is in use.
[ $rc -eq 0 ] && "$SCRIPT_DIR/run_daemon.sh" ensure > /dev/null 2>&1
exit $rc
