#!/bin/bash
# First-boot bootstrap for a fresh Cornelius on Trinity - the detached half of
# the /first-run playbook. Launched by .trinity/setup.sh in the background on every
# container start until ~/.trinity-bootstrap.done exists; never blocks startup.
#
# RESUMABLE (2026-11-27). The platform restarts a new instance's container a few
# minutes after its first start, to apply the person's Claude credential - which
# cuts this script off wherever it is (seen: the log stopped at "reindex start",
# no marker, a stale lock). So:
#   - a lock is honoured only while its pid is alive AND is this script (pid +
#     start time recorded; after a restart pids are reused, and a bare kill -0 on
#     a reused pid would block every later boot);
#   - each finished step is stamped in ~/.trinity-bootstrap.steps and skipped on
#     the next run (the venv step re-checks its imports instead - a half-done pip
#     is redone, a done one costs a second);
#   - the next boot's setup.sh starts it again, and /first-run runs it in the
#     foreground to finish and write the marker.
# The orphan sweep does not kill it: .trinity/persistent-processes.allow lists it.
#
# Steps: venv -> pip (CPU torch + intake converters, no cache) -> reindex until
# remaining=0 (fix stored paths) -> daemon (ensure, one starter) -> smoke search -> marker.
# Log: ~/.trinity-bootstrap.log
#
# Usage: bootstrap.sh            run / resume (idempotent)
#        bootstrap.sh --status   print done | running (pid N) | interrupted after <step> | not started
#                                (clears a stale lock as a side effect; changes nothing else)

set -u
AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LBS="$AGENT_DIR/resources/local-brain-search"
LOG="$HOME/.trinity-bootstrap.log"
LOCK="$HOME/.trinity-bootstrap.lock"
DONE="$HOME/.trinity-bootstrap.done"
STEPS="$HOME/.trinity-bootstrap.steps"

log(){ echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
starttime(){ awk '{print $22}' "/proc/$1/stat" 2>/dev/null; }
# A lock is live only if its pid runs, is a bootstrap.sh, and started when the lock says.
lock_live(){
  [ -f "$LOCK" ] || return 1
  local pid st
  read -r pid st < "$LOCK" 2>/dev/null || return 1
  [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null || return 1
  tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null | grep -q "bootstrap.sh" || return 1
  [ -z "${st:-}" ] || [ "$(starttime "$pid")" = "$st" ] || return 1
  return 0
}
clear_stale_lock(){
  if [ -f "$LOCK" ] && ! lock_live; then
    log "stale lock cleared ($(tr '\n' ' ' < "$LOCK"); its process is gone or is no longer this script - an interrupted run, e.g. a container restart)"
    rm -f "$LOCK"
  fi
}
step_done(){ grep -qx "$1" "$STEPS" 2>/dev/null; }
mark_step(){ step_done "$1" || echo "$1" >> "$STEPS"; }

if [ "${1:-}" = "--status" ]; then
  clear_stale_lock
  if [ -f "$DONE" ]; then echo "done ($(cat "$DONE"))"
  elif lock_live; then echo "running (pid $(awk '{print $1}' "$LOCK"))"
  elif [ -s "$STEPS" ]; then echo "interrupted after: $(paste -sd, "$STEPS") - run: bash .trinity/bootstrap.sh"
  elif [ -f "$LOG" ]; then echo "interrupted before any step finished - run: bash .trinity/bootstrap.sh"
  else echo "not started"; fi
  exit 0
fi

if [ -f "$DONE" ]; then log "already done ($(cat "$DONE")); nothing to do"; exit 0; fi
clear_stale_lock
if lock_live; then log "another bootstrap is running (pid $(awk '{print $1}' "$LOCK"))"; exit 0; fi
echo "$$ $(starttime $$)" > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

[ -s "$STEPS" ] && log "resuming - already finished: $(paste -sd, "$STEPS")"
log "bootstrap start in $AGENT_DIR"
cd "$LBS" || { log "FAIL: $LBS missing"; exit 1; }

# 1. Python environment
#    The same venv carries the document converters /intake uses (markitdown,
#    pymupdf, trafilatura) - no uv, no second toolchain.
if ./venv/bin/python -c "import faiss, sentence_transformers, networkx, markitdown, pymupdf, trafilatura" >/dev/null 2>&1; then
  log "venv ok"
else
  log "building venv (CPU torch, no cache - a few minutes)"
  # a venv cut off while being created has a python but no pip: recreate it
  if [ ! -x ./venv/bin/python ] || [ ! -x ./venv/bin/pip ]; then
    python3 -m venv --clear venv >> "$LOG" 2>&1 || { log "FAIL: venv create"; exit 1; }
  fi
  ./venv/bin/pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt >> "$LOG" 2>&1 \
    || { log "FAIL: pip install (see above)"; exit 1; }
  log "venv built"
fi
mark_step venv

# 2. Reindex so stored paths match this machine (also downloads the embedding
#    model on first use; no daemon needed). The indexer embeds at most 500 notes
#    per call, so repeat until remaining=0. Stamped when complete; skipped on resume.
if step_done reindex && [ -f data/brain.faiss ]; then
  log "reindex: done in an earlier run - skipped"
else
  log "reindex start"
  ok=""
  for i in 1 2 3 4 5 6; do
    BRAIN_DAEMON_AUTOSTART=0 ./run_index.sh >> "$LOG" 2>&1; rc=$?   # streams to the log: a cut-off run leaves its trace
    [ $rc -eq 0 ] || { log "warn: reindex returned $rc"; break; }
    last=$(tail -5 "$LOG" | grep "^RESULT" | tail -1)
    case "$last" in *remaining=0*|"") ok=1; break ;; esac           # no counter printed: one pass is all
  done
  if [ -n "$ok" ]; then mark_step reindex; log "reindex ok"; else log "warn: reindex not complete - the next run resumes it"; fi
fi

# 3. Daemon - ONE starter (ensure is lock-guarded; a separate `start` raced the
#    ensure that run_index.sh used to fire, and two daemons loaded the model at once).
#    Bounded: a fresh model load can keep /health silent for a while.
if [ -f data/brain.faiss ]; then
  log "daemon start"
  timeout 120 ./run_daemon.sh ensure --wait >> "$LOG" 2>&1 || log "warn: daemon not fresh in time (search falls back to the CLI path)"
else
  log "daemon: skipped - no index yet (the next run builds it first)"
fi

# 4. Smoke search. An unattended start never adds the seed library (#21): the
#    brain starts empty, so "0 results + the empty-vault hint" is a pass too.
#    Bring the library in later with /first-run --with-library.
N=$(BRAIN_READ_SCOPE=@lookup ./run_search.sh "decision under uncertainty" --limit 3 --json 2>/dev/null | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); r=d.get('results',d); print(len(r) if r else ('empty' if d.get('hint') else 0))
except Exception: print(0)")
log "smoke search: $N results"
if [ "$N" = "empty" ]; then
  mark_step smoke; date -u +%FT%TZ > "$DONE"; log "bootstrap DONE - empty brain (seed library not added; /first-run --with-library adds it)"
elif [ "${N:-0}" -gt 0 ] 2>/dev/null; then
  mark_step smoke; date -u +%FT%TZ > "$DONE"; log "bootstrap DONE"
else
  log "bootstrap finished but the smoke search returned 0 - run /first-run to diagnose"
fi
