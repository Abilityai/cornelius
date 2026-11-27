#!/bin/bash
# Step 4 helper: for every new note in a book scope, query the index by TITLE ONLY,
# read raw_similarity (not the Q-adjusted `similarity`), drop same-scope + changelog +
# index-artifact hits, dedupe by note, and print the top-8 per note at raw cosine >= 0.44.
# Usage (from the agent root): resources/local-brain-search/score_neighbours.sh <Brain/Books/<slug>> <scope-token-for-exclusion e.g. Books/<slug>> > connections.txt
# Non-book sessions (added 2026-10-23): SCOPE=core,document-insights score_neighbours.sh "<Brain/Document Insights/<session>>" "Document Insights/<session>"
set -u
# Agent root = two levels up from this script; no git needed (a fresh copy may not be a clone).
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || exit 2
DIR="$1"; EXCL="$2"; SCOPE="${SCOPE:-core,Books}"
[ -d "$DIR" ] || { echo "no such folder: $DIR" >&2; exit 2; }
for f in "$DIR"/*.md; do
  b=$(basename "$f" .md)
  case "$b" in _book|CHANGELOG*) continue;; esac
  echo "### $b"
  BRAIN_READ_SCOPE="$SCOPE" resources/local-brain-search/run_search.sh "$b" --mode static --limit 100 --threshold 0.44 --json --no-track 2>/dev/null \
  | python3 -I -c "
import sys, json
excl = sys.argv[1]
d = json.load(sys.stdin)
best = {}
for r in d.get('results', []):
    nid = r.get('note_id', '')
    if nid.startswith(excl) or 'CHANGELOG' in nid or nid.endswith('/README.md') or nid.endswith('/_book.md'):
        continue
    s = r.get('raw_similarity')
    if s is None: continue
    if s > best.get(nid, 0): best[nid] = s
for nid, s in sorted(best.items(), key=lambda x: -x[1])[:8]:
    if s >= 0.44: print(f'  {s:.3f}\t{nid}')
" "$EXCL"
done
