# Company-Brain Schema Convention

**What this is:** the structure, entity/relationship model, temporal model, and playbook suite for the **Company brain** - a reference-kind scope *family* holding the canonical, mutable, date-interpreted source of truth about the people, organizations, offerings, and deals that matter to the business, plus an autonomously-maintained competitive/market layer.

**Status:** **9a-9d SHIPPED + COMMITTED 2026-07-08** (`83d5b5939` + validation/fixes `c2859086c`, `d51efa186`). Structural slice 9a-9c (family flag + 53 notes migrated + reindex/BDG/daemon + 18 family tests, 102/102 green) **plus the seven `ref-*` playbooks (9d), built + live-verified** (ref-audit CLEAN on the 53; ref-ingest round-trip byte-clean on the learn-gate; no engine edits). **All seven then validated one-by-one 2026-07-08** — every skill passes its own Verification section; three hardening fixes applied from that pass: `ref-bridge` v1.2 (run static+spreading, static-primary — spreading drifts to the KB's densest hub and mis-bridges cross-cluster agent entities), `ref-reconcile` v1.2 (relation-asymmetry grep rewritten case-insensitive/colon-form/BSD-portable — the old one matched 4 of ~28 mutual relations; and the duplicate-merge no longer self-inflicts a dangling link via a `[[wiki-link]]` to the removed note). **9e (autonomy wiring) SHIPPED 2026-09-13** — `ref-refresh` (Mon 10:15 UTC) and `ref-audit` (Mon 11:15 UTC, after the sweep) scheduled, and domain-watch wired to `Company/market/` as a **dispatch** (Step 6.6 → `resources/company-brain/inbound/` → `ref-refresh` Step 0 → `/ref-receive-batch` → `/ref-ingest`), with the boundaries enforced mechanically in `resources/diagnostics/effects.yaml`. **Phase 9 is complete** — see item 6 below and `SCOPE-IMPLEMENTATION-PLAN.md` → Phase 9. Builds directly on the shipped reference-scope primitive.
**Base contract:** `REFERENCE-SCOPE-SCHEMA.md` (the reference-kind frontmatter + linking + privacy contract - this doc *extends* it, does not restate it).
**Design of record:** `TARGET-ARCHITECTURE.md` -> Direction B ("Scope kinds") + the Books family precedent ("Scope families").
**Playbook:** the `manage-reference-data` skill (existing) + the six new `ref-*` skills defined below.

---

## Why this is a *family*, not the flat `Company` scope

The reference-kind primitive already gives us read-isolation, learn-gating, fingerprint-exclusion, and the epistemic opt-out (no lifecycle, no crystallization, `provenance: reference`) for free. What the flat `Company/` folder does NOT give:

1. **Separately-mountable sub-scopes** ("load just my clients", "load just competitive intel").
2. **A MECE entity taxonomy** - today `type: vendor` conflates competitors with suppliers, and `type: product` conflates sellable products with the internal agent workforce.
3. **A place to interpret facts by date** beyond a bare `as_of:` stamp.

A **scope family** (the `Books/` mechanism) solves #1 with one code change: each `Brain/Company/<sub>/` folder becomes its own pluggable, separately-mountable reference scope, while `scope_of()` still resolves the top folder -> the reference kind -> the epistemic opt-out stays intact for every child.

```python
# memory_config.py — the ONLY engine change
ScopeDef("Company", SCOPE_KIND_REFERENCE, False, ("company",), family=True)
#                                                                ^^^^^^^^^^^ added
```

Verified against `scope_of` / `scope_id` / `in_read_scope` / `is_reference_scope` / `core_subgraph`: a reference family composes with no other engine change. `scope_id("Company/clients/genesis10.md") == "Company/clients"` (fine mount); `scope_of(...) == "Company"` -> reference kind (opt-out); `core_subgraph` untouched (Company is non-core, fingerprint stays clean); BDG `classify.bootstrap` skips it (`is_reference_scope`).

---

## The two axes

The model is two orthogonal axes. Do not collapse them (collapsing them is the current bug).

### Axis 1 — SCOPE (the mount boundary = who owns the writes)

| Sub-scope | Holds | Writer | Mount |
|-----------|-------|--------|-------|
| `Company/people/` | humans | **curated** (human write) | `core,Company/people` |
| `Company/orgs/` | organizations you own or transact with | **curated** | `core,Company/orgs` |
| `Company/products/` | your offerings + internal agent workforce | **curated** | `core,Company/products` |
| `Company/engagements/` | deals/contracts (join-nodes) | **curated** | `core,Company/engagements` |
| `Company/market/` | competitors, their products, ecosystem you **watch** | **autonomous** (domain-watch overwrites) | `core,Company/market` |
| whole brain | all of the above | — | `core,Company` |

**The partition rule: watch vs. transact.** `market/` holds what you *watch* (competitors, competitor products, ecosystem players). `orgs/` + `products/` hold what you *own or transact with* (self, clients, prospects, partners, vendors, your offerings). A competitor org lives in `market/`, not `orgs/`, because `market/` is the autonomously-maintained scope and an org you compete with is watched, not transacted with.

`people/ · orgs/ · products/ · engagements/` are partitioned **by entity type** (the CRM you curate). `market/` is carved out **by relationship** because it has a different writer (the perception loop) and a different cadence (web-signal-driven).

### Axis 2 — TYPE + RELATIONSHIP (frontmatter, applies inside every scope)

`type:` = **what the entity is**. `relationship:` = **how it relates to us**. Decoupling these is the fix for the `vendor`/`product` overload.

| `type:` | Is | `relationship:` values |
|---------|-----|------------------------|
| `person` | a human | `self-team` · `client-contact` · `counsel` · `prospect` · `partner-contact` |
| `organization` | a company | `self` · `client` · `prospect` · `partner` · `vendor` · `competitor` · `investor` |
| `product` | an offering | `own` · `competitor` |
| `agent` | an internal AI worker (first-class: the business *is* agents) | — |
| `engagement` | a deal/contract **join-node** (client × product × owner × dates × value) | — |
| `interaction` | *(optional)* an atomic dated event: meeting, milestone, signal | — |

"List my competitors" = `type: organization AND relationship: competitor` (or simply: everything in `market/` with `relationship: competitor`). The taxonomy no longer lies.

---

## The temporal model — "interpret by creation / update date"

Three layers. Two are buildable now at the convention/playbook level; the third is the deferred engine feature this workload finally motivates.

### 1. Fact-level frontmatter (playbook-enforced, now)

```yaml
type: organization
relationship: client
provenance: reference          # ALWAYS reference (base contract)
scope: Company                 # top folder (family); scope_id resolves the child
status: active                 # active | superseded
as_of: 2026-06-13              # when this fact was last VERIFIED true (freshness)
valid_from: 2026-01-01         # validity window — for facts with a term (contract, role, price)
valid_until: 2026-12-31        # omit for facts with no natural expiry
superseded_by: "[[Acme Engagement 2027]]"   # only on superseded rows
created: 2026-06-26
updated: 2026-07-08
created_by: [model-name]
updated_by: [model-name]
agent_version: 01.25
```

### 2. Read-time interpretation (agent-level, now)

Any playbook that surfaces a reference fact MUST:
- prefer `status: active` over `superseded`;
- respect `valid_until` (a fact past its window is stale unless renewed);
- **discount by `as_of` age** against the per-type freshness SLA (below);
- **always print the `as_of` date** so staleness is legible to the reader ("Trinity pricing *as of 2026-06-13*").

This is the near-term form of "interpret by date" - the reading agent does it, the vector engine does not yet.

### 3. Engine-level recency (deferred — C-Phase 7)

True recency-weighted retrieval (newer edges automatically beat older) is **C-Phase 7 bi-temporal edges** (`valid_from`/`valid_until` on BDG edges), designed-not-built. `TARGET-ARCHITECTURE.md` already names a regularly-updated reference/company scope as C-7's motivating workload - **this brain is that workload.** Until C-7 ships, layers 1-2 carry recency at the convention level.

### Freshness SLA (per type — drives `ref-refresh`)

| Type / relationship | Stale after | Rationale |
|---------------------|-------------|-----------|
| `market/` competitor product/pricing | ~14 days | moves fast; autonomously refreshed |
| `engagement` (active deal) | ~30 days | status/stage changes |
| `organization` (client) | ~90 days | slower-moving facts |
| `person` (bio/role) | ~180 days | rarely changes |
| `product` (own) | on-change | you know when it changes |

---

## Canonical source of truth — one note per real-world entity

The property that makes this a *source of truth*: for any business fact there is exactly **one authoritative, mutable, freshness-stamped note**. This is enforced by:
- **overwrite-in-place** (the latest content *is* the index — no append-only drift);
- **entity resolution on every write** (an incoming fact is matched to the existing entity, never duplicated) — `ref-reconcile` hunts and merges duplicates;
- **the change log** — because overwrite-in-place would otherwise lose the audit trail, every note carries a `## Change Log` appended-to section:

```markdown
## Change Log
- 2026-07-08 — pricing updated to $500/mo floor (source: domain-watch, competitor page)
- 2026-06-13 — license position corrected to Apache 2.0 + SaaS restriction
```

Overwrite the *body* (the current truth); append the *change log* (the history of truth). Validity transitions that need a full prior snapshot (contract renewal) use `status: superseded` + `superseded_by:` instead.

---

## The update model — "updated based on incoming information of different kinds"

Every input funnels through one operation: **upsert-by-entity-resolution.**

```
incoming info (any kind)             →  resolve  →  reconcile  →  upsert
──────────────────────────────          ───────      ─────────     ──────
· the user, in conversation                match name/  new fact vs.   overwrite body,
· a document (contract, deck, call)      aliases →    old fact:      re-stamp as_of,
· perception (domain-watch: a            existing     overwrite /    append change log,
  competitor shipped X)  →  market/      note or new  supersede /    supersede if a
· another agent (a content agent, Atlas report)                  flag           validity window closed
```

The load-bearing hard parts are **entity resolution** (is this new "Reply" the existing `Reply.io`?) and **reconciliation** (new fact contradicts old -> overwrite vs. supersede-with-history vs. flag). Both live in the playbooks.

---

## The playbook suite

The existing `manage-reference-data` skill is a single manual upsert. The company brain needs the full lifecycle: **ingest -> resolve -> reconcile -> maintain -> activate -> audit.**

| # | Playbook | Path | Does | Automation |
|---|----------|------|------|------------|
| 1 | **`ref-ingest`** (extends `manage-reference-data`) | write | Incoming info of any kind -> extract entity facts -> resolve to existing entity (dedup/alias) -> upsert (overwrite body, re-stamp `as_of`, append change log). The single entry point for incoming information. | assisted (CRM) / **auto (market)** |
| 2 | **`ref-supersede`** | write | Validity transitions: contract renewal, role change, price change. New `active` note + old `superseded` + `superseded_by:` chain. | human-gated |
| 3 | **`ref-reconcile`** | consistency | Conflict resolution + bidirectional link integrity (A lists `[[B]]` as client -> does B back-link?) + dangling-link detection + **duplicate-entity detection** (what keeps it canonical). | sense auto / **merge human** |
| 4 | **`ref-refresh`** | temporal | Staleness sweep: scan `as_of` ages vs. the per-type SLA -> refresh queue -> (market) hand to `ref-ingest`. | **auto** - live weekly **Mon 10:15 UTC** since 2026-09-13 (`template.yaml` id `ref-refresh`). Was declared "auto (scheduled)" from 2026-07-08 but never wired; 53/55 notes sat 79 days stale in the gap. |
| 5 | **`ref-query`** | read | Structured temporal lookup: "what do we know about Acme Corp *as of today*?", "which engagements are active and expiring in 90 days?" Respects active/`as_of`. Distinct from `/recall` (which searches insights). | auto |
| 6 | **`ref-bridge`** (thin mode over `connection-finder`) | activate | The reason reference data lives *in the brain*: "this client maps to that insight you had." connection-finder with `core,Company/<sub>` mounted -> bridge entities to the cognitive KB. Makes it more than a CRM. | auto (sense) |
| 7 | **`ref-audit`** | consistency | Integrity report: orphan entities, dangling links, provenance violations (any non-`reference` leaked in), type/relationship-enum violations, missing `as_of`. The reference-scope analog of `/coherence-sweep`. | **auto** - live weekly **Mon 11:15 UTC** since 2026-09-13 (`template.yaml` id `ref-audit`), placed **after** `ref-refresh` so it audits the post-sweep state. Read-only: repairs stay `ref-reconcile`. |

### Automation boundary — split by scope

Reference records sit **outside** the `encountered -> endorsed` gate (they are mutable facts that never claim to be the user's thinking), so more is safe to automate here than for insights. The boundary splits by scope:

| | Autonomous | Human-gated |
|--|-----------|-------------|
| **`market/`** (watched) | competitor/ecosystem facts auto-**overwrite** (with `as_of` + change-log entry) - since 2026-09-13 along the wired path *domain-watch Step 6.6 dispatch -> `resources/company-brain/inbound/` -> `ref-refresh` Step 0 -> `/ref-receive-batch` -> `/ref-ingest`*; domain-watch itself never writes `Brain/Company/**`. Plus `ref-refresh`, `ref-audit`, `ref-bridge` | entity **merge / delete**; promoting a market fact into a **cognitive insight** (the guarded boundary, unchanged) |
| **`people/orgs/products/engagements/`** (transacted) | `ref-refresh`, `ref-audit`, `ref-bridge` (sense only) | every **upsert, supersede, merge, delete** |

What NEVER automates, in any scope: **promotion of a reference fact into an endorsed cognitive insight.** That crossing stays the human `encountered -> endorsed` act. A record informing a thought is fine; a record *becoming* the user's `originated`/`endorsed` thought is the one line the reference kind exists to hold.

---

## Relations — wiki-links, not new edge types (unchanged from base)

Model relationships with `[[wiki-links]]`; a link is already an `explicit` edge (weight 1.0) that connection-finder and spreading traverse. The `engagement` note is the **join** for many-to-many (Client × Product × owner × dates × value). Typed relational BDG edges (`employed-by`, `contract-for`) stay **deferred** - taken only if untyped links prove insufficient.

```markdown
# Acme Corp - Trinity Enterprise Build        (engagement)
joins: [[Acme Corp]] (client) × [[Trinity]] × [[Your Name]] (owner)
value: $130k + $20k license · term: 2026-.. → .. · status: active
```

---

## Build sequence

1. **Engine (1 line):** `family=True` on the Company `ScopeDef`. ✅ **DONE 2026-07-08.**
2. **Migration:** sort the flat notes into `people/ orgs/ products/ engagements/ market/`; split `agent` out of `product`; replace the `vendor`/`client`/`employee` types with `type:` + `relationship:`; move competitors/ecosystem into `market/`. Loose files at the family root degrade to singleton scopes, so they MUST move into a sub-folder. ✅ **DONE 2026-07-08 — 53 notes** (people 3 · orgs 8 · products 16 · engagements 12 · market 14); `valid_from/until` + `## Change Log` deferred to incremental adoption; `as_of` preserved (not re-verified).
3. **Reindex + daemon restart** (content-hash change detection -> full rebuild). ✅ **DONE 2026-07-08** (+ BDG bootstrap: `reference-kind excluded: 53`).
4. **Schema/convention:** this doc (canonical). ✅ **DONE.**
5. **Playbooks:** extend `manage-reference-data` -> `ref-ingest`; build `ref-reconcile`, `ref-refresh`, `ref-query`, `ref-bridge`, `ref-audit`, `ref-supersede`. ✅ **DONE (9d) 2026-07-08** — seven `.claude/skills/ref-*/SKILL.md`, each with a procedure + verification + refusal block; automation per this doc's "Automation boundary"; live-verified (ref-audit 0 violations on the 53; tests 102/102; no engine edits). Reports → `resources/company-brain/reports/`. **Validated one-by-one 2026-07-08** (each skill exercised against the live 53, all test writes reverted): all seven pass. Fixes from that pass — `ref-bridge` → v1.2 (static-primary bridge search; spreading-mode hub-drift documented), `ref-reconcile` → v1.2 (portable colon-form relation-asymmetry grep; merge no longer emits a `[[wiki-link]]` to the hard-removed duplicate). Open (not blocking, logged for later): entity-resolution should rank title over body-mention (`ref-ingest`/`ref-query`); `ref-audit` by-type relationship check is eyeball-only and its dangling check resolves against family basenames only; `valid_from/until` still 0-adopted so temporal filters are unexercised.
6. **Autonomy wiring:** point domain-watch at `Company/market/` via `ref-ingest`; schedule `ref-refresh` + `ref-audit` (mechanical, like coherence-sweep). ✅ **DONE 2026-09-13** (the last open item of Phase 9 — 9a–9e now complete). Three parts, all live: (a) **`ref-refresh` scheduled** weekly Mon 10:15 UTC (`claude-sonnet-5`, 45m, id `4iuPcjdZ9qT5y4pA6uPgVA`) after a measured 79-day staleness gap — this doc had called it "auto (scheduled)" while it had never been scheduled, and 53 of 55 notes sat at `as_of: 2026-06-26`; (b) **`ref-audit` scheduled** weekly Mon 11:15 UTC (`claude-sonnet-5`, 20m, id `RduWZc--u1E5yw_1S1sVVQ`), deliberately **after** the sweep so it audits the post-write state — sense-after-write, since the thing most likely to break an enum is `ref-refresh`'s own autonomous `market/` overwrite; (c) **domain-watch → `market/`** wired as a **dispatch**, not a write: domain-watch **Step 6.6** appends frozen-schema-v1 batch items to `resources/company-brain/inbound/domain-watch-queue.yaml` and never touches `Brain/Company/**`, and `ref-refresh` **Step 0** drains that queue through `/ref-receive-batch` → `/ref-ingest` before measuring staleness. The dispatch-not-write shape is deliberate: it keeps the single write funnel intact, isolates the perception layer's search budget, avoids three reindexes a day, and means the CRM gate is enforced by the receiver rather than trusted to the caller. Four dispatch refusals are contractual (no decided direction — that is canon; no discovery-tier source — it may raise a question, never settle one; CRM facts dispatch but stage `flagged`; a record is never an insight). All three are declared in `template.yaml`, mirrored in `CLAUDE.md`, and made **mechanical** in `resources/diagnostics/effects.yaml`: `ref-audit` carries a read-only contract, `ref-refresh`'s `never_touch` covers the four CRM sub-scopes, and `domain-watch`'s `never_touch` now covers `Brain/Company/**` — so a boundary crossing trips the diagnostics instead of relying on a doc promise.
7. **(Later) C-Phase 7 bi-temporal edges** — promote read-time recency into the engine; this brain is its motivating workload. ⬜ deferred.

Steps 1-4 are the structural slice (**shipped**; reversible: unset `family=True` + move files back). Steps 5-6 are the operational layer. Step 7 is the long arc.

---

## What the Company brain must NEVER do (inherits base + adds)

- Never be **crystallized / lifecycle-classified / synthesis-pulsed** (base contract; `is_reference_scope` guard).
- Never acquire `provenance` other than `reference`.
- Never **train q-values** (non-core by construction).
- Never be the **default read scope** (mounted on demand only).
- Never let a **market fact auto-promote into a cognitive insight** — autonomous overwrite of a *record* is fine; autonomous creation of an *endorsed belief* is not.

---

## References

- `REFERENCE-SCOPE-SCHEMA.md` — the reference-kind base contract (this doc extends it).
- `BOOK-SCOPE-SCHEMA.md` — the scope-family precedent (same mechanism, cognitive kind).
- `TARGET-ARCHITECTURE.md` -> Direction B ("Scope kinds", "Scope families") + Direction C-Phase 7 (bi-temporal edges).
- `.claude/skills/manage-reference-data/SKILL.md` — the existing upsert playbook (extends to `ref-ingest`).
- `resources/local-brain-search/memory_config.py` — `SCOPE_REGISTRY`, `ScopeDef(family=)`, `scope_id`, `in_read_scope`, `is_reference_scope`.
