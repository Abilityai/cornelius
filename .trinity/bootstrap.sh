#!/bin/bash
# First-boot bootstrap for a fresh Cornelius on Trinity - the detached half of
# the /first-run playbook. Launched by .trinity/setup.sh in the background the
# first time a container starts without a working search venv; never blocks
# startup. Idempotent: every step checks before it acts.
#
# Steps: venv -> pip (CPU torch, no cache) -> daemon -> reindex (fix stored
# paths) -> daemon reload -> smoke search -> marker. Log: ~/.trinity-bootstrap.log

set -u
AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LBS="$AGENT_DIR/resources/local-brain-search"
LOG="$HOME/.trinity-bootstrap.log"
LOCK="$HOME/.trinity-bootstrap.lock"
DONE="$HOME/.trinity-bootstrap.done"

log(){ echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }

if [ -f "$DONE" ]; then log "already done ($(cat "$DONE")); nothing to do"; exit 0; fi
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then log "another bootstrap is running (pid $(cat "$LOCK"))"; exit 0; fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

log "bootstrap start in $AGENT_DIR"
cd "$LBS" || { log "FAIL: $LBS missing"; exit 1; }

# 1. Python environment
if ./venv/bin/python -c "import faiss, sentence_transformers, networkx" >/dev/null 2>&1; then
  log "venv ok"
else
  log "building venv (CPU torch, no cache - a few minutes)"
  python3 -m venv venv >> "$LOG" 2>&1 || { log "FAIL: venv create"; exit 1; }
  ./venv/bin/pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt >> "$LOG" 2>&1 \
    || { log "FAIL: pip install (see above)"; exit 1; }
  log "venv built"
fi

# 2. Daemon
./run_daemon.sh start >> "$LOG" 2>&1 || log "warn: daemon start returned non-zero"

# 3. Reindex once so stored paths match this machine, then reload the daemon
log "reindex start"
./run_index.sh >> "$LOG" 2>&1 && log "reindex ok" || log "warn: reindex returned non-zero"
./run_daemon.sh reload >> "$LOG" 2>&1 || ./run_daemon.sh restart >> "$LOG" 2>&1 || true

# 4. Smoke search
N=$(BRAIN_READ_SCOPE=core,books,document-insights ./run_search.sh "decision under uncertainty" --limit 3 --json 2>/dev/null | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); r=d.get('results',d); print(len(r))
except Exception: print(0)")
log "smoke search: $N results"
if [ "${N:-0}" -gt 0 ]; then
  date -u +%FT%TZ > "$DONE"; log "bootstrap DONE"
else
  log "bootstrap finished but the smoke search returned 0 - run /first-run to diagnose"
fi
