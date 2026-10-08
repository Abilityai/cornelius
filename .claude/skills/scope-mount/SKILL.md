---
name: scope-mount
description: Shared read-scope contract - which scopes a knowledge-base read mounts, decided by the read's ROLE (voice / reasoning / lookup / perception-ingestion-maintenance), plus question-triggered reference mounts (Company, Canon, Thinkers, one book), the never-mount list, the core-first/wide-second retrieval shape and the scope-grouped output format. Every read skill references this file and never copies it. Invoke directly to resolve the mount for a question.
automation: autonomous
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
argument-hint: "[role=voice|reasoning|lookup] [the question or topic, for the conditional reference mounts]"
metadata:
  version: "1.0"
  created: 2026-09-04
  updated: 2026-09-04
  author: Ability.ai
  changelog:
    - "1.0: Initial contract - four read roles with standing mounts (voice=core; reasoning and lookup=core,Books,document-insights), question-triggered reference mounts, never-mount list, two-pass retrieval shape, scope-grouped output. Origin: the user 2026-09-04 ('only core is not enough') + the audit that found eleven read skills inheriting the fail-closed engine default as their retrieval policy. Enabled by the per-note learn-gate (learning.py trains(), Phase 10a)."
---

# Scope Mount

> ℹ️ **First, set expectations:** print one line with this skill's version and its most recent change - the top of `metadata.changelog` - e.g. `scope-mount v1.0 — recent: initial four-role contract`. Then proceed. (Skip the banner when applied silently inside a consuming skill.)

## Purpose

The scope primitive (`ARCHITECTURE.md` → "Scope") was built for **hygiene**: keep the core fingerprint and q-learning clean of encountered material. Its engine default is fail-closed - `unset BRAIN_READ_SCOPE` → `core`. That default is correct for the *engine* and wrong as a *retrieval policy*, and until 2026-09-04 it was the retrieval policy for every everyday read: `/recall`, `/advise`, `/decide` and eight other skills carried no mount and so read 1,187 of ~6,800 notes. Everything the user has read (Books, Document Insights) and every reference record was invisible to advice and recall. Nobody chose that.

This file is the **policy of record for what a read mounts** (`ARCHITECTURE.md` → "Scope Mount Policy"). The engine keeps failing closed; the mount is declared in the playbook, per read, by **role**.

**Contract rule (the `reasoning-checks` / `SOURCE-AUTHORITY.md` pattern):** this file is the single source of truth. Consuming skills reference it and put the mount inline on their search commands; they never copy the tables. Change a mount here, not in consumers.

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Scope registry | `resources/local-brain-search/memory_config.py` → `SCOPE_REGISTRY` (tokens: `core`, `books`, `document-insights`, `company`, `canon`, `thinkers`, `meta`, `inbox`, `output`; families accept `Books/<slug>`, `Company/<sub>`) | ✓ | |
| Company record titles | `Brain/Company/**/*.md` | ✓ | |
| Thinker roster | `Brain/Thinkers/THINKERS-INDEX.md` | ✓ | |
| Book shelf | `Brain/Books/<slug>/` | ✓ | |
| Similarity contract | `resources/local-brain-search/SIMILARITY-CALIBRATION.md` | ✓ | |

**Never writes.** Never changes the engine default.

## The four read roles

| Role | The read is for | Standing mount | Consumers |
|---|---|---|---|
| **voice** | the user's fingerprint IS the product; the answer must be attributable to him | `BRAIN_READ_SCOPE=core` (declared explicitly, never inherited) | `/get-perspective-on`, `/create-article` (source pass), `/synthesize-insights` in "my thoughts on X" mode |
| **reasoning** | the best-grounded answer, every source attributed | `BRAIN_READ_SCOPE=core,Books,document-insights` - the **reasoning mount** | `/advise`, `/decide`, `/think-about-it`, `/dialectic` (monk grounding), `/abstraction-ladder` (rungs), `/synthesize-insights` (pattern mode), `/talk` → `thinking-partner`, incubation-loop evidence pass |
| **lookup** | "what do I have on X" | the reasoning mount, output **grouped by scope** | `/recall`, `/search-vault`, `/quick-search`, `/find-connections` (anchor + neighbourhood) |
| **perception / ingestion / maintenance** | see everything new · dedup against the write target · measure the fingerprint | unchanged and already declared: wide (`core,Books,document-insights,meta,inbox,output`) / the write target / `core` | domain-watch, auto-discovery, worldview-refresh, integrate-recent-notes, the extractors, `/ingest-source`, analyze-kb, coherence, lifecycle |

**Lookup semantics.** "What do I *think* about X" is answered by the core group; "what do I *know* about X" by all groups. The user narrows on demand: `--scope core` (or "only my notes") pins the read to `core`; `--scope <token>` mounts exactly that.

**`/talk` is reasoning, not voice** (the user, 2026-09-04): the thinking partner speaks *from* the whole knowledge base, including what the user has read; it still labels what it cites.

## Conditional reference mounts (reasoning + lookup only; never standing)

| Trigger in the question | Add | Detect |
|---|---|---|
| a person / org / product / deal name | `company` | a Company record title appears in the question |
| a named external thinker | `thinkers` | a roster name from `THINKERS-INDEX.md` appears |
| a book title or author already on the shelf | an **extra precision pass** at `core,Books/<slug>` - the wide pass keeps the whole shelf | a `Brain/Books/` slug matches |
| direction / strategy / "should we" about the org | `canon` - but the *route* is `/canon-advise`; inside `/advise` mount Canon only to surface disagreement **as dissent, never as direction** | the `canon-advise` trigger vocabulary |

Detection is a cheap title match, run once before the searches (no LLM call, ~50 ms) by the resolver shipped with this skill:

```bash
.claude/skills/scope-mount/resolve_mount.sh <voice|reasoning|lookup> "<the question>"
# BRAIN_READ_SCOPE=core,Books,document-insights,company      <- use verbatim on the wide pass
# # trigger company: Trinity
# # extra pass: BRAIN_READ_SCOPE=core,Books/black-swan-taleb  <- a book hit adds a THIRD, precision pass
```

Rules (whole-word matching; a false positive costs one slightly wider read, nothing else): a **Company** record title appears *whole* in the question (single-word titles such as `Trinity` match as words - `agent` in a question never mounts `BDR agent`); any **Thinkers** name token of 5+ characters appears (the surname is the natural trigger); a **Books** slug has one distinctive token of 6+ characters or two tokens present, with a stoplist that keeps generic words (*thinking*, *guide*, *science*, *agent*, ...) from mounting anything. `voice` always answers `core` and runs no detector.

A hit adds the token to the mount for that read only (a book hit adds a pass instead). No hit, no mount. A question that is *about* the org's direction leaves `/advise` for `/canon-advise` (dispatch rule in `CLAUDE.md`).

## Never in a reasoning or lookup mount

| Scope | Why |
|---|---|
| `05-Meta` | operational exhaust - changelogs are 88% of the residual cosine-1.000 edges; thinking/watch files are read by grep where a skill needs them (incubation-loop does) |
| `00-Inbox` | unprocessed captures |
| `04-Output` | derivative of core - it would return the user's own articles as evidence for the user's views |
| `DemoCRM` | demo data |
| `Company`, `Canon`, `Thinkers` as *standing* mounts | reference records are facts, not thinking; they enter only on a trigger |

These stay perception-only (domain-watch, auto-discovery, integrate-recent-notes already mount them for that purpose).

## Retrieval shape: core-first, wide-second

Document Insights alone is 2.3x core, so one wide search with a small `--limit` can push core out of the top-k. Run **two passes in the same parallel batch** - core as the spine, wide as the evidence layer:

```bash
# one query, two populations, one parallel batch
BRAIN_READ_SCOPE=core                          resources/local-brain-search/run_search.sh "<term>" --limit 3 --json
BRAIN_READ_SCOPE=core,Books,document-insights  resources/local-brain-search/run_search.sh "<term>" --limit 5 --json
```

Neighbourhood calls follow the same mount as the search that found the anchor (`run_connections.sh "<note>"` at the reasoning mount reaches Books/DI neighbours). **`--hubs` / `--bridges` / `--stats` stay `core` always** - they are the fingerprint, not a read.

Autonomous loops keep `--no-track` (learning hygiene is about *who* is reading, not what is mounted).

## Output: group by scope, label by provenance

Scope is the `note_id` folder prefix - no engine change:

| Group | Prefix | Present as |
|---|---|---|
| **your thinking** | `02-Permanent/` `03-MOCs/` `AI Extracted Notes/` `01-Sources/` | core - the fingerprint |
| **what you have read** | `Books/` `Document Insights/` | encountered, not endorsed - never phrased as "your view" |
| **records** | `Company/` `Canon/` `Thinkers/` | facts (`provenance: reference`), not thinking |

Load-bearing sources in a *conclusion* additionally pass `reasoning-checks` **Check 3 - Provenance Weighting**, already wired into `/advise`, `/decide` and both crystallization paths. Under the reasoning mount that check is the load-bearing voice guard: it is what keeps a wider read from becoming a wider voice.

## What the mount does NOT change

- **Learning.** Since Phase 10a (2026-09-04) the learn-gate is **per note** (`learning.py` → `trains()`): the core hits of a mixed read train q-values and get the q-boost, non-core hits never do. Mounting never switches learning off. (Before 10a any mixed read disabled learning - the "landmine" that kept every read at `core`.)
- **The fingerprint.** Hubs, bridges, lifecycle, redundancy: `core`, by construction.
- **The engine default.** Unset scope → `core`, never "all". The policy lives here and in the playbooks.
- **The endorsement boundary.** Reading wider changes what the agent can *see*, never what it may *endorse*. `encountered → endorsed` remains the human act.
- **Thresholds are population-bound.** The reasoning mount is its own population; its row lives in `SIMILARITY-CALIBRATION.md` (Space 2, scoped). Do not carry a `core` band to the mount or back.

## Direct invocation

`/scope-mount role=<voice|reasoning|lookup> <question>` → runs `resolve_mount.sh` with those arguments and prints its output: the mount line to use verbatim, the triggers that fired, and any extra precision pass. Useful when writing or debugging a consumer.

## Consumers (who declares which role)

`/advise` · `/decide` · `/think-about-it` · `/dialectic` · `/abstraction-ladder` · `/synthesize-insights` · `/talk` (via `thinking-partner`) · incubation-loop → **reasoning**. `/recall` · `/search-vault` · `/quick-search` · `/find-connections` (+ `connection-finder` when called from them) → **lookup**. `/get-perspective-on` · `/create-article` → **voice** (explicit `core`). Perception, ingestion and maintenance skills keep their existing declared mounts. A consumer with a bare (unmounted) search command is a defect: diagnostics check D3.6 lints for it.
