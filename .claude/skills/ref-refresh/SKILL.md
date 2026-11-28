---
name: ref-refresh
description: Mechanical staleness sweep over a reference scope. Scans every note's as_of age against the per-type Freshness SLA, builds an overdue-sorted refresh queue, then splits by scope — market/ stale items are handed to ref-ingest (the gate-free overwrite branch) for autonomous re-verification; CRM stale items are report-only (never auto-written). Safe to run unattended. Company is the default scope.
automation: autonomous
allowed-tools: [Read, Write, Bash, Glob, Grep, Skill]
user-invocable: true
argument-hint: "[scope=Company] [--market-only]"
metadata:
  version: "1.0"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.0: Initial version — as_of-vs-SLA staleness sweep → refresh queue; market→ref-ingest (ungated overwrite), CRM→report-only; single batch reindex"
---

# Ref Refresh

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-refresh v1.0 — recent: initial version`. Then proceed.

The **temporal maintenance** loop: which records have gone stale, and which can be autonomously refreshed. Reference facts have a freshness half-life; this skill enforces the per-type SLA and routes the stale ones. It is the reference analog of a scheduled coherence job — mechanical, no judgment.

**Read first:** `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` → "The temporal model" → the per-type Freshness SLA and "Automation boundary — split by scope".

## Composes

- `/ref-ingest` — for **`market/` stale items only**, invoked with `--no-reindex` (batch); this skill reindexes once at the end. Because it only ever takes `ref-ingest`'s **gate-free, overwrite-only market branch**, the whole path is autonomous-safe.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/*/*.md` | ✓ | ✓ (market, via ref-ingest) | Entity notes swept |
| Refresh report | `resources/company-brain/reports/` | | ✓ | `ref-refresh-YYYY-MM-DD.md` (the queue + what was done) |
| LBS index | `resources/local-brain-search/data/` | ✓ | ✓ (one batch reindex) | Rebuilt once after market writes |

## The Freshness SLA (drives the sweep)

| Type / relationship | Stale after |
|---------------------|-------------|
| `market/` competitor product/pricing | ~14 days |
| `engagement` (active deal) | ~30 days |
| `organization` (client) | ~90 days |
| `person` (bio/role) | ~180 days |
| `product` (own) | on-change (no age SLA — skip) |
| `decision-record` | never (historical record — skip) |

## Process

### Step 1 — Sweep as_of vs SLA

For every `Brain/Company/*/*.md`, read `type`/`relationship`/`status`/`as_of`, compute `today − as_of` in days, and compare to the SLA for that type. Collect the overdue notes; sort by how far over SLA they are. Skip `status: superseded`, own-`product` (on-change) and `decision-record` (historical).
```bash
(
cd $PROJECT_ROOT/Brain/Company
# example: market notes older than 14 days (compute days-since in the agent; illustrative)
for f in market/*.md; do a=$(grep -m1 '^as_of:' "$f" | cut -d' ' -f2); echo "$a  $f"; done | sort
)
```

### Step 2 — Split the queue by scope

- **`market/` stale** → the **auto-refresh** set (Step 3).
- **CRM stale** (`people/orgs/products(own)/engagements`) → the **report-only** set. Never auto-write CRM — list them for a human to refresh via `/ref-ingest`.

### Step 3 — Refresh market/ (autonomous, batched)

For each stale `market/` item, hand it to `/ref-ingest` with the fresh signal and `--no-reindex`:
> re-verify the current competitor fact (pricing/positioning/shipped features), overwrite the body if changed, always re-stamp `as_of` to today, append a Change Log line.

In **9d** the fetch source is whatever the invoker supplies; the **autonomous web re-fetch is wired in 9e** (domain-watch feeding `market/` through `ref-ingest`). If no fresh signal is available this run, record the item as "queued, awaiting signal" rather than restamping a fact you did not actually re-verify. After all market items, reindex **once**:
```bash
(cd resources/local-brain-search && ./run_index.sh && ./run_daemon.sh restart)
```

### Step 4 — Report

Write `resources/company-brain/reports/ref-refresh-YYYY-MM-DD.md`: the full overdue queue, what was auto-refreshed (market), and the CRM items awaiting human refresh. Print a summary.

## Verification

- The sweep flags exactly the notes whose `as_of` age exceeds their type's SLA (spot-check one market note ≥14d old and one client org <90d — the first is queued, the second is not).
- **No CRM note is auto-written** — only market notes appear in the "refreshed" list; CRM appears only under "awaiting human refresh".
- If any market note was refreshed: exactly **one** reindex ran for the whole batch, and each refreshed note has a new `## Change Log` line + today's `as_of`.
- A report exists at `resources/company-brain/reports/ref-refresh-<today>.md`.

## This skill must refuse to

- Auto-write any CRM sub-scope (`people/orgs/products/engagements`) — report-only.
- Restamp `as_of` on a fact it did not actually re-verify (staleness laundering).
- Invoke `/ref-supersede` or open any approval gate on the autonomous path (market is overwrite-only).
- Crystallize, lifecycle-classify, or promote a record into a cognitive insight.
