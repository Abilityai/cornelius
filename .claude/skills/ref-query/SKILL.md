---
name: ref-query
description: Structured, temporal lookup against a reference scope — "what do we know about Acme Corp as of today?", "which engagements are active and expiring in 90 days?", "list our competitors". Respects status (active over superseded), validity windows, and as_of freshness, and ALWAYS prints the as_of date so staleness is legible. Distinct from /recall, which searches cognitive insights. Company is the default scope. Read-only.
automation: autonomous
allowed-tools: [Read, Bash, Glob, Grep]
user-invocable: true
argument-hint: "[scope=Company] <entity name | filter, e.g. 'engagements active expiring 90d' | 'competitors'>"
metadata:
  version: "1.2"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.2: Agent callers get a few lines with sources; an empty or missing reference scope answers 'nothing on record', never an error; unconfirmed offers are shown as unconfirmed"
    - "1.1: Declared automation: autonomous - read-only, no gates, no interactive prompt, so it is fleet-callable per protocols/playbook-call.md obligation 7 (published 2026-08-22 in docs/cognition-query-interface.md)"
    - "1.0: Initial version — deterministic frontmatter scan + fuzzy fallback with read-time interpretation (active>superseded, valid_until, as_of discount vs per-type SLA, always print as_of)"
---

# Ref Query

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-query v1.0 — recent: initial version`. Then proceed.

Answer a **structured question about reference records** with the temporal contract applied. This is **not** `/recall` — `/recall` searches the user's cognitive insights; `ref-query` reads the CRM/market source of truth and honours `status`/validity/`as_of`.

**Read first:** `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` → "The temporal model" (read-time interpretation + the per-type Freshness SLA). This skill enforces those rules.

## Step 0 — Who is asking, and is there anything on record?

- **Agent mode** — another agent asked (an agent-to-agent call, an MCP or API trigger, a scheduled or headless run, or no person in the chat). Skip the version line and answer in the short form of Step 4.
- **Person mode** — a person is in the chat: everything below is unchanged.

Before any search, check the scope has records:
```bash
SCOPE_DIR="Brain/${scope:-Company}"
[ -d "$SCOPE_DIR" ] && find "$SCOPE_DIR" -name '*.md' ! -name 'README.md' ! -name '_*' | head -1 | grep -q . || echo "EMPTY"
```
`EMPTY` (a fresh brain, or a scope nobody has written yet) → answer `nothing on record for "<question>"` and stop. That is the answer, not an error. The same applies when the search finds no matching note.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/{people,orgs,products,engagements,market}/*.md` | ✓ | | Entity notes + frontmatter |
| Search wrapper | `resources/local-brain-search/run_search.sh` | ✓ | | Fuzzy "tell me about X" under a `core,Company` mount |

## Process

### Step 1 — Classify the question

- **Entity lookup** ("what do we know about X *as of today*?") → resolve the note (Grep by name/alias, or a mounted search) and read it.
- **Filtered list** (by `type`/`relationship`/`status`/expiry window) → **deterministic frontmatter scan** (below), not semantic search — the answer must be exact and reproducible.
- **Fuzzy / exploratory** ("who might overlap with X?") → mounted semantic search:
  ```bash
  BRAIN_READ_SCOPE=core,Company resources/local-brain-search/run_search.sh "<query>" --limit 10 --json
  ```

### Step 2 — Scan (deterministic filters)

Frontmatter is the query surface. Examples:
```bash
cd Brain/Company
# all active competitors
grep -rlE '^relationship: competitor' */*.md | while read f; do grep -qE '^status: active' "$f" && echo "$f"; done
# active engagements + their as_of
for f in engagements/*.md; do grep -qE '^status: active' "$f" && printf "%s  as_of=%s valid_until=%s\n" \
  "$(basename "$f" .md)" "$(grep -m1 '^as_of:' "$f" | cut -d' ' -f2)" "$(grep -m1 '^valid_until:' "$f" | cut -d' ' -f2)"; done
```
For an "expiring in N days" filter, compare `valid_until` to today + N. Note: notes that predate incremental `valid_until` adoption have no window — report them as "no recorded term" rather than dropping them.

### Step 3 — Apply read-time interpretation (mandatory)

Before presenting any fact:
1. Prefer **`status: active`** over `superseded` (a superseded note is history — show it only if asked "what changed?").
2. A fact past its **`valid_until`** is **stale-unless-renewed** — say so.
3. **Discount by `as_of` age** against the per-type Freshness SLA (COMPANY-BRAIN-SCHEMA): `market` product/pricing ~14d · `engagement` ~30d · client `organization` ~90d · `person` ~180d · own `product` on-change. Over SLA → tag `⚠ stale (as_of N days old)`.
4. **Always print the `as_of` date** next to each fact ("Trinity pricing *as of 2026-06-13*").

### Step 4 — Answer

**Agent mode — the short form** (at most ~6 lines, no headings, no preamble):
```text
ref-query: <question>
- <entity> - <key fact> (as_of YYYY-MM-DD [· ⚠ stale] [· unconfirmed, offered by <agent>]) [<path from the repo root>]
- ...
sources: <the notes read, paths from the repo root>
```
or, when nothing matches, the single line `nothing on record for "<question>"`. A fact under `## Offered by agents (unconfirmed)` or in a note with `confirmation: unconfirmed` is always labelled `unconfirmed`, never presented as confirmed.

**Person mode:** compact, sourced, staleness-legible. One line per record: `name — key fact (as_of YYYY-MM-DD [· ⚠ stale] · status)`. For an entity lookup, summarise the body + list its `[[relations]]` + the freshness verdict.

## Verification

- A real entity question ("what do we know about Acme Corp as of today?") returns the note's facts **with the `as_of` date printed** and a freshness verdict.
- A real filter ("which engagements are `active`?") returns exactly the notes whose frontmatter matches (cross-check the count against `grep -rlE '^status: active' engagements/*.md | wc -l`).
- Nothing is written; `git status` is unchanged after a query.
- On a fresh brain (no `Brain/Company/`), an agent-mode query returns `nothing on record for "<question>"` and no error.

## This skill must refuse to

- Write or mutate any note (read-only).
- Present a `superseded` fact as current, or a fact without its `as_of` date.
- Present an unconfirmed (agent-offered) fact as confirmed.
- Answer an empty scope with an error or a stack trace instead of `nothing on record`.
- Set/alter provenance, crystallize, lifecycle-classify, or promote a record into a cognitive insight.
