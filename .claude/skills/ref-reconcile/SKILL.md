---
name: ref-reconcile
description: Keep a reference scope canonical and internally consistent. SENSE phase (auto) detects issues by invoking ref-audit; FIX phase (human-gated) resolves conflicts, repairs bidirectional link integrity (A cites [[B]] as client → does B back-link?), fixes/removes dangling links, and MERGES duplicate entities into one canonical note. Every write is human-gated — merge and delete stay human even in market/. Company is the default scope.
automation: gated
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Skill]
user-invocable: true
argument-hint: "[scope=Company] [--issue links|duplicates|conflicts|all]"
metadata:
  version: "1.1"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.2: Two fixes (validated 2026-07-08) — (a) the Step 1 relation-verb grep was case-sensitive with a 5-verb space-only set and matched 4 of ~28 real mutual relations (the family uses lowercase colon-form: `client:`, `Partner of:`, `Security vendor for:`); replaced with a case-insensitive, connector-agnostic, BSD-portable regex. (b) Step 2 merge could self-inflict a dangling link — a `## Change Log` line naming the hard-removed duplicate as `[[wiki-link]]` dangles; now plain-text the merged name (or use the tombstone path)."
    - "1.1: Fix — Step 1 wrongly attributed conflict + back-link-asymmetry detection to ref-audit (which computes neither); those now detected in-skill, with a relations-vs-references scope so directional links aren't false-flagged"
    - "1.0: Initial version — sense (composes ref-audit) + gated fix (back-link repair, dangling-link fix, duplicate merge); reindex after writes"
---

# Ref Reconcile

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-reconcile v1.0 — recent: initial version`. Then proceed.

The **act** on top of `ref-audit`'s **report**. `ref-audit` senses (read-only, autonomous); `ref-reconcile` fixes (human-gated). It protects the property that makes a reference scope a *source of truth*: **one canonical note per real-world entity**, with consistent bidirectional links and no dangling references.

**Read first:** `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` → "Canonical source of truth" + "The update model"; `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md`.

## Composes

- `/ref-audit` — the sense/detection pass (do not re-implement the scan here).

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/*/*.md` | ✓ | ✓ (gated) | Entity notes reconciled |
| Audit report | `resources/company-brain/reports/` | ✓ | | Consumed for detection |
| LBS index | `resources/local-brain-search/data/` | ✓ | ✓ (reindex) | Rebuilt after any write |

## Process

### Step 1 — SENSE (auto)

Detection has two sources — don't attribute to `ref-audit` what it doesn't compute:

**From `/ref-audit` (structural, single-authored there — do not re-implement):** dangling links, orphan entities, duplicate candidates, plus the frontmatter/provenance/enum/partition/`as_of` violations. Invoke it (or read its latest report).

**In this skill (relational, needs the references-vs-relations judgment `ref-audit` deliberately avoids):**
- **Conflicts** — two notes asserting contradictory facts about one entity. Read the duplicate/near-name clusters `ref-audit` flags and compare their bodies.
- **Bidirectional-link asymmetry** — but **only for *relation* links, never *reference* links.** A `## Relations` entry that names a mutual tie (`client: [[B]]`, `Partner of: [[B]]`, `Engagement: [[B]]`) should reciprocate; a directional *reference* (`built on [[Trinity]]`, `competitor of [[X]]`, `runs on [[Y]]`) must **not** be forced to back-link. `ref-audit` reports the family CLEAN despite dozens of such directional links precisely because a blanket A→B⇒B→A check would be almost all false positives — so scope the reciprocity check to relation verbs only:
  ```bash
  (
  cd Brain/Company
  # Mutual-tie relation links whose reciprocal is worth checking.
  # Case-insensitive (-i) and connector-agnostic: matches BOTH "Client of [[..]]" and the colon
  # form "client: [[..]]" the migrated notes actually use. The verb must LEAD the label (~12 chars)
  # so prose bullets that merely contain a verb word (e.g. "…problem owners…") aren't flagged.
  # No \b — BSD/macOS grep does not support it. TUNE THE VERB SET to the scope's real vocabulary.
  grep -rniE '^- [^[]{0,12}(client|partner|vendor|counsel|owner|owns|engagement|collaborat|advis)[^[]*\[\[' */*.md
  )
  ```
  (The old space-only, capitalized set — `Client of|Vendor to|…` — matched only 4 of the family's ~28 mutual relations; the family is predominantly lowercase colon-form.) For each match, confirm the named target carries the reciprocal relation; if not, it's a repair candidate (Step 2).

### Step 2 — FIX (every write gated)

For each issue, **propose the concrete edit, show the before/after, and get explicit approval** (`AskUserQuestion`) before writing. CRM and market alike — merge/delete are human in every scope.

- **Bidirectional link repair:** if `A` lists `[[B]]` (e.g. "Client of [[Ability AI]]") but `B` has no reciprocal relation, propose adding the back-link to `B`'s `## Relations`. Append a `## Change Log` line on the edited note.
- **Dangling link:** the target note doesn't exist → propose either (a) correct the link to the real entity, or (b) remove it, or (c) create the missing entity via `/ref-ingest`. Ask which.
- **Conflict:** two notes assert contradictory facts about one entity → present both, ask which is current; the loser is either corrected (overwrite via the note body) or, if a validity window closed, handed to `/ref-supersede`.
- **Duplicate MERGE (the canonical act):** two notes are the same real-world entity →
  1. choose the canonical note (usually the better-linked / more complete),
  2. fold the duplicate's unique facts + `[[relations]]` into it,
  3. **repoint every inbound link:** `grep -rl "\[\[<Duplicate Name>\]\]" Brain/Company/` → rewrite each to `[[<Canonical Name>]]`,
  4. remove the duplicate note **only after step 3 leaves zero inbound `[[links]]` to it**; if history or lingering references matter, keep a `status: superseded` + `superseded_by: [[Canonical]]` tombstone instead (which keeps the name resolvable),
  5. append a `## Change Log` line on the canonical note noting the merge + source — **name the merged duplicate as plain text, NOT a `[[wiki-link]]`.** A wiki-link to a hard-removed note is itself a fresh dangling link (it would fail the very check this skill enforces); a `[[Duplicate]]` reference may remain *only* on the tombstone path, where the note still exists.

### Step 3 — Reindex after any write

```bash
(cd resources/local-brain-search && ./run_index.sh && ./run_daemon.sh restart)   # :7437, RESTART not reload
```
(No BDG bootstrap — reference notes are BDG-excluded.) If nothing was written (all issues declined), skip.

## Verification

- After a merge: `grep -ril "<duplicate name>" Brain/Company/` returns **only** the canonical note (or a tombstone); **no inbound `[[link]]`** still points at the removed duplicate — **including the canonical note's own Change Log line** (reference the merged name as plain text, so the merge does not re-introduce the dangling link it just resolved).
- After a back-link repair: the reciprocal relation exists on both notes.
- Re-running `/ref-audit` shows the fixed issues cleared and **no new** dangling links introduced by the edits.
- Every edited note carries a new `## Change Log` line.

## This skill must refuse to

- Write **any** fix without explicit human approval of that specific edit (sense is auto; every fix is gated).
- Merge/delete on a hunch — a merge requires confirmed same-entity identity.
- Set any provenance but `reference`, or crystallize/lifecycle-classify/promote a record into a cognitive insight.
