---
name: ref-audit
description: Integrity report for a reference scope — the reference-scope analog of /coherence-sweep. Scans every entity note for provenance violations (any note not provenance:reference), type/relationship enum violations, missing/invalid as_of, status/superseded_by integrity, dangling wiki-links, orphan entities, and duplicate-entity candidates. READ-ONLY — it reports, it never fixes (fixes are ref-reconcile). Company is the default scope. Safe to run unattended.
automation: autonomous
schedule: "15 11 * * 1"
allowed-tools: [Read, Write, Bash, Glob, Grep]
user-invocable: true
argument-hint: "[scope=Company] [--json]"
metadata:
  version: "1.1"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.1: Report template now includes the Freshness (vs SLA) section it already emitted; explicit audit/reconcile boundary note (structural links only — relational asymmetry/conflicts are ref-reconcile's, not a CLEAN-verdict gap)"
    - "1.0: Initial version — read-only integrity report (provenance/enum/as_of/status/dangling-link/orphan/duplicate) to resources/company-brain/reports/"
---

# Ref Audit

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-audit v1.0 — recent: initial version`. Then proceed.

The **integrity health check** for a reference scope. It answers "is the source of truth still canonical, well-formed, and honestly stamped?" It is **read-only**: it produces a report and prints a summary. It never edits (repairs/merges are `/ref-reconcile`, which is human-gated) — that is exactly what makes it autonomous-safe.

**Read first:** `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` (the enum + temporal contract) and `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md` (the reference-kind contract). This skill checks notes against those docs.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/{people,orgs,products,engagements,market}/*.md` | ✓ | | Entity notes audited |
| Reports | `resources/company-brain/reports/` | | ✓ | `ref-audit-YYYY-MM-DD.md` |

## The contract this audits

- **provenance:** every note must be `provenance: reference`. Anything else = a leak (a cognitive note crept in, or an insight was mis-filed here).
- **type ∈** `person · organization · product · agent · engagement · interaction`.
- **relationship ∈** (by `type`) person: `self-team·client-contact·counsel·prospect·partner-contact`; organization: `self·client·prospect·partner·vendor·competitor·investor`; product: `own·competitor`. `agent`/`engagement`/`interaction` carry **no** `relationship`.
- **as_of:** present + a valid `YYYY-MM-DD`.
- **status ∈** `active · superseded`; a `superseded` note MUST have a `superseded_by: "[[...]]"` that resolves.
- **partition rule:** a `relationship: competitor` note belongs in `market/`; a transacted entity does not.
- **links:** every `[[wiki-link]]` resolves to an existing note; every entity has at least one relation (no orphans).

## Process

### Step 1 — Collect the family + frontmatter

```bash
cd $PROJECT_ROOT
SCOPE="${scope:-Company}"
ls Brain/$SCOPE/*/*.md | wc -l          # total entity notes
```

### Step 2 — Run the checks (read-only)

Scan every `Brain/$SCOPE/*/*.md`. Use grep sweeps as the fast path, then Read the flagged notes to confirm:
```bash
cd Brain/Company
# provenance violations
for f in */*.md; do grep -qE '^provenance: reference$' "$f" || echo "PROVENANCE  $f"; done
# type enum violations
grep -rhoE '^type: .*' */*.md | sort -u        # eyeball against the allowed set
# missing as_of / bad date
for f in */*.md; do grep -qE '^as_of: [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$f" || echo "AS_OF       $f"; done
# superseded without a superseded_by
for f in */*.md; do grep -qE '^status: superseded' "$f" && ! grep -qE '^superseded_by:' "$f" && echo "SUPERSEDED  $f"; done
# competitor sitting outside market/
grep -rlE '^relationship: competitor' */*.md | grep -v '^market/' | sed 's/^/PARTITION   /'
```
For **dangling links** and **orphans**, extract `[[...]]` targets across the family, resolve each against existing note basenames, and list unresolved targets + notes with zero in/out links:
```bash
# every wiki-link target used
grep -rhoE '\[\[[^]]+\]\]' */*.md | sed -E 's/\[\[([^]|#]+).*/\1/' | sort -u
# every existing entity basename
for f in */*.md; do basename "$f" .md; done | sort -u
# a target in the first list but not the second = dangling
```
For **duplicate candidates**, flag near-identical display names / aliases across sub-scopes (fuzzy) for `/ref-reconcile` to judge — do NOT merge here.

### Step 3 — Write the report + summarise

Write `resources/company-brain/reports/ref-audit-YYYY-MM-DD.md` (create the dir if absent):
```markdown
# Ref Audit — Company — YYYY-MM-DD
Total entity notes: N  (people · orgs · products · engagements · market)

## Violations
- Provenance: <count> [list]
- Type/relationship enum: <count> [list]
- Missing/invalid as_of: <count> [list]
- Status/superseded integrity: <count> [list]
- Partition (competitor outside market/): <count> [list]

## Link integrity
- Dangling links: <count> [note → missing target]
- Orphan entities (no relations): <count> [list]

## Duplicate candidates (for ref-reconcile)
- [[A]] ↔ [[B]] — same entity?

## Freshness (vs per-type SLA)
- Over SLA: <count> [note — as_of N days old vs Xd SLA]
- Next cohort to stale: <sub-scope> on <date>

## Verdict: CLEAN | N issues (M require ref-reconcile)
```
Print a one-screen summary + the report path. **Do not fix anything.**

**Scope note (the audit/reconcile boundary):** this skill checks **structural link integrity only** — every `[[link]]` resolves, no orphan. It deliberately does **not** flag *relational asymmetry* (A names `[[B]]` as client but B doesn't back-link) or *conflicts* (two notes contradict): most A→B links here are legitimately directional *references* (`built on [[Trinity]]`, `competitor of [[X]]`), so a blanket reciprocity check would be almost all false positives. That judgment — relation vs reference — lives in `/ref-reconcile` Step 1, not here. A CLEAN verdict therefore means "well-formed and canonical," not "every link is mutual."

## Verification

- Run against the live family → the total matches `ls Brain/Company/*/*.md | wc -l` (expect 53), and on the current data expect **0 provenance violations, 0 enum violations, 0 missing as_of** (all 53 are `provenance: reference`, `status: active`, `as_of`-stamped).
- Any dangling links / orphans it finds are **listed with the offending note and target**.
- A report file exists at `resources/company-brain/reports/ref-audit-<today>.md`; **no entity note was modified** (`git status` shows only the new report).

## This skill must refuse to

- Edit, merge, delete, or repair any entity note (report-only; hand fixes to `/ref-reconcile`).
- Write anything outside `resources/company-brain/reports/`.
- Crystallize, lifecycle-classify, or promote a record into a cognitive insight.
