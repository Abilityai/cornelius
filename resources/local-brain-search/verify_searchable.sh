#!/bin/bash
# Prove that notes just written are findable by search - the last check of every
# ingestion before its summary is written (/ingest-source Step 3b, /intake Step 6).
#
# Usage: verify_searchable.sh <scope mount> <notes dir | note.md>...
#   e.g. verify_searchable.sh core,document-insights "Brain/Document Insights/<session>"
#        verify_searchable.sh core,Books "Brain/Books/<slug>"
#
# For each note (changelogs, READMEs and _book.md hubs skipped) it searches the
# note's title through run_search.sh - the same path every playbook reads through,
# daemon or CLI - in the given mount, and passes the note only if the note itself
# comes back. Prints one line per miss, then exactly one summary line:
#   searchable: 4/4
#   searchable: 1/4 - index older than the notes (refresh not run or not finished)
# Exit 0 only when every note was found. Read-only: never reindexes by itself.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCOPE="${1:?usage: verify_searchable.sh <scope mount> <notes dir | note.md>...}"; shift
[ $# -gt 0 ] || { echo "usage: verify_searchable.sh <scope mount> <notes dir | note.md>..."; exit 2; }
cd "$ROOT" || exit 2

notes=()
for a in "$@"; do
  if [ -d "$a" ]; then
    while IFS= read -r f; do notes+=("$f"); done < <(find "$a" -maxdepth 1 -name '*.md' | sort)
  elif [ -f "$a" ]; then notes+=("$a")
  else echo "missing path: $a"; fi
done

total=0; found=0; newer=0
FAISS="$SCRIPT_DIR/data/brain.faiss"
for f in "${notes[@]}"; do
  b=$(basename "$f" .md)
  case "$b" in CHANGELOG*|README|_book|_metadata) continue ;; esac
  total=$((total+1))
  nid="${f#Brain/}"; nid="${nid#./Brain/}"
  [ -f "$FAISS" ] && [ "$f" -nt "$FAISS" ] && newer=$((newer+1))
  if BRAIN_READ_SCOPE="$SCOPE" "$SCRIPT_DIR/run_search.sh" "$b" --mode static --limit 20 --threshold 0.1 --json --no-track 2>/dev/null \
     | python3 -I -c "
import sys, json
nid = sys.argv[1]
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(1)
ids = {r.get('note_id') or '' for r in d.get('results', [])} | {(r.get('filepath') or '').split('Brain/', 1)[-1] for r in d.get('results', [])}
sys.exit(0 if nid in ids else 1)
" "$nid"; then
    found=$((found+1))
  else
    echo "not found: $b"
  fi
done

if [ "$total" -eq 0 ]; then echo "searchable: 0/0 - no notes given"; exit 2; fi
if [ "$found" -eq "$total" ]; then echo "searchable: $found/$total"; exit 0; fi
why="search did not return them (check the mount: $SCOPE)"
[ -f "$FAISS" ] || why="no index (run /first-run)"
[ "$newer" -gt 0 ] && why="index older than $newer of the notes (refresh not run or not finished)"
echo "searchable: $found/$total - $why"
exit 1
