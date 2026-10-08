#!/usr/bin/env bash
# scope-mount resolver - print the BRAIN_READ_SCOPE line for a read role + question.
#   Usage: .claude/skills/scope-mount/resolve_mount.sh <voice|reasoning|lookup> "<question>"
# Contract: .claude/skills/scope-mount/SKILL.md. Pure read, no LLM call, ~50 ms.
# Output: line 1 = the mount for the wide pass; "# trigger ..." lines say why; a book hit
# adds "# extra pass: BRAIN_READ_SCOPE=core,Books/<slug>" (a THIRD, precision pass - the
# wide pass keeps the whole shelf).
set -euo pipefail
ROLE="${1:?role: voice|reasoning|lookup}"; shift || true
Q="${*:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
case "$ROLE" in
  voice) echo "BRAIN_READ_SCOPE=core"; echo "# voice read: pinned to core, no conditional mounts"; exit 0 ;;
  reasoning|lookup) MOUNT="core,Books,document-insights" ;;
  *) echo "unknown role: $ROLE (voice|reasoning|lookup)" >&2; exit 2 ;;
esac
if [ -z "$Q" ]; then echo "BRAIN_READ_SCOPE=$MOUNT"; exit 0; fi
notes=()
# generic tokens that must never trigger a mount on their own
STOP=" thinking guide brief smart science theory power world history business design model models agent agents human mind brain book life work small great little simple thing things people making decision decisions behavior behaviour principles rules laws story stories secret secrets future modern complete essential practical introduction handbook manual "

# Company: a record title appears WHOLE in the question (records are named precisely;
# single-word titles such as "Trinity" match as whole words).
hit=""
while IFS= read -r t; do
  [ -n "$t" ] || continue
  if grep -qiwF -- "$t" <<<"$Q"; then hit="$t"; break; fi
done < <(find "$ROOT/Brain/Company" -name '*.md' ! -name '_*' ! -iname 'README*' 2>/dev/null | sed 's#.*/##; s/\.md$//')
[ -n "$hit" ] && { MOUNT="$MOUNT,company"; notes+=("# trigger company: $hit"); }

# Thinkers: any name token of 5+ chars appears as a whole word (the surname is the natural trigger).
hit=""
while IFS= read -r name; do
  for tok in $name; do
    if [ ${#tok} -ge 5 ] && grep -qiw -- "$tok" <<<"$Q"; then hit="$name"; break 2; fi
  done
done < <(find "$ROOT/Brain/Thinkers" -name '*.md' ! -name 'THINKERS-INDEX.md' ! -name '_*' 2>/dev/null | sed 's#.*/##; s/\.md$//')
[ -n "$hit" ] && { MOUNT="$MOUNT,thinkers"; notes+=("# trigger thinkers: $hit"); }

# Books: one distinctive slug token of 6+ chars (not in STOP) as a whole word, or two tokens.
hit=""
for slug in $(ls "$ROOT/Brain/Books" 2>/dev/null); do
  n=0; strong=0
  for tok in ${slug//-/ }; do
    lc="$(tr '[:upper:]' '[:lower:]' <<<"$tok")"
    case "$STOP" in *" $lc "*) continue;; esac
    if [ ${#tok} -ge 4 ] && grep -qiw -- "$tok" <<<"$Q"; then n=$((n+1)); [ ${#tok} -ge 6 ] && strong=1; fi
  done
  if [ $strong -eq 1 ] || [ $n -ge 2 ]; then hit="$slug"; break; fi
done
[ -n "$hit" ] && notes+=("# trigger book: $hit" "# extra pass: BRAIN_READ_SCOPE=core,Books/$hit")

echo "BRAIN_READ_SCOPE=$MOUNT"
for n in ${notes[@]+"${notes[@]}"}; do echo "$n"; done   # bash 3.2 + set -u: safe on an empty array
