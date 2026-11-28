---
name: ref-supersede
description: Handle a validity transition on a reference entity — a contract renewal, role change, or re-termed price where a full prior snapshot matters. Creates the new status:active note (with valid_from/valid_until), marks the old note status:superseded + superseded_by:[[New]], keeps both for history, and reindexes. Human-gated. Distinct from ref-ingest overwrite (which replaces the body + logs one line); use supersede only when the prior snapshot must be preserved. Company is the default scope.
automation: gated
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
user-invocable: true
argument-hint: "[scope=Company] <entity or engagement being superseded>"
metadata:
  version: "1.0"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.0: Initial version — validity-transition supersede: new active note + old superseded + superseded_by chain, valid_from/until, Change Log both, reindex"
---

# Ref Supersede

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-supersede v1.0 — recent: initial version`. Then proceed.

A **validity transition** with history preserved. Overwrite-in-place (`ref-ingest`) is right when the latest fact simply *replaces* the old one. Supersede is right when the **old snapshot itself matters** — you want to be able to answer "what was the term of the *2026* Acme Corp engagement?" after the 2027 renewal exists. It keeps both notes: old `superseded`, new `active`, linked by `superseded_by:`.

**Read first:** `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` → "Canonical source of truth" (overwrite body vs. supersede-with-snapshot) + "The temporal model"; `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md` → "History".

**Human-gated in every scope.** Even in `market/`, a supersede (a structural, two-note change) is a human act — the autonomous market path *overwrites*, it never supersedes (`ref-ingest` flags such cases here instead).

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/*/*.md` | ✓ | ✓ (gated) | Old + new entity notes |
| LBS index | `resources/local-brain-search/data/` | ✓ | ✓ (reindex) | Rebuilt after the write |

## Process

### Step 1 — Identify the transition

Resolve the note being superseded (Grep by name/alias). Confirm it is a **validity transition** (a term/window closed, a role or price was re-termed) and that a **prior snapshot is worth keeping** — otherwise this is an overwrite; route to `/ref-ingest` instead.

### Step 2 — Draft both notes + get approval

Present the before/after and get explicit approval (`AskUserQuestion`) before writing:
- **New note** (`status: active`): the current fact, with `valid_from:` (and `valid_until:` if it has a term), fresh `as_of`/`updated`, `provenance: reference`, and the entity's relations. Give it a name that disambiguates the window when needed (e.g. `Acme Corp - Trinity Enterprise Build 2027`).
- **Old note** (`status: superseded`): add `superseded_by: "[[<New note title>]]"`; leave its body as the historical snapshot; re-stamp `updated` only.

### Step 3 — Write + chain + log

Write the new note; edit the old note to `status: superseded` + the `superseded_by:` link. Append a `## Change Log` line to **both**:
```markdown
## Change Log
- 2026-07-08 — superseded by [[<New>]] on renewal (source: <...>)   # on the old note
- 2026-07-08 — supersedes [[<Old>]]; new term 2027-01 → 2027-12 (source: <...>)   # on the new note
```

### Step 4 — Reindex

```bash
(cd resources/local-brain-search && ./run_index.sh && ./run_daemon.sh restart)   # :7437, RESTART not reload
```
(No BDG bootstrap — reference notes are BDG-excluded.)

## Verification

- Two notes now exist: the old one `status: superseded` with a resolving `superseded_by:`, the new one `status: active`.
- `/ref-query` for the entity returns the **new** (active) fact by default and can surface the old on "what changed?".
- Both notes carry a `## Change Log` line describing the transition; the old body is intact as the snapshot.
- `/ref-audit` reports no `status/superseded_by` integrity violation for the pair.

## This skill must refuse to

- Write without explicit approval of the specific transition (human-gated in every scope, including `market/`).
- Delete or overwrite the old snapshot (supersede **keeps** it — that is the whole point).
- Set any provenance but `reference`, or crystallize/lifecycle-classify/promote a record into a cognitive insight.
