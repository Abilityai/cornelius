---
name: ref-ingest
description: The single entry point for incoming information of ANY kind about a reference entity (a person, org, product, engagement, or watched competitor). Extracts entity facts, RESOLVES them to the one existing canonical note (never duplicating), reconciles new-vs-old, and upserts (overwrite body, re-stamp as_of, append Change Log), then reindexes. Extends manage-reference-data with entity resolution + reconciliation + the market-vs-CRM automation split. Company is the default scope. NEVER writes any provenance but reference; NEVER crystallizes/lifecycle-classifies/promotes a record into an insight.
automation: gated
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Skill]
user-invocable: true
argument-hint: "[scope=Company] <entity name or the incoming info> [--source <where it came from>] [--from-agent <name>] [--no-reindex]"
metadata:
  version: "1.3"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.3: Decisions with no named person or organisation are kept, not dropped. They go to a dated decisions record, Brain/Company/decisions/Decisions YYYY-MM.md - what was decided, the reason (or \"reason not stated\"), who decided when named, source, date, offered by, unconfirmed. Agent mode and person mode alike. Origin: first-boot test 2026-11-27 dropped \"warehouse move confirmed for 2 February\" as `no entity named`."
    - "1.2: Agent offers - when another agent sends facts (headless, no person in the chat) the skill never asks: it keeps work facts as unconfirmed offers with source and date, drops personal / health / an individual's money with a reason, and replies with a short receipt. A person in the chat keeps the gated flow."
    - "1.1: Fix — Step 3 named a phantom agents-as-product/ sub-scope; type: agent notes live in products/. Corrected."
    - "1.0: Initial version — extract→resolve→reconcile→gate→upsert entry point for the Company reference family; overwrite-only market branch invariant; composes ref-supersede; grows manage-reference-data"
---

# Ref Ingest

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-ingest v1.0 — recent: initial version`. Then proceed. (In agent mode, below, the receipt's `skill:` line carries the version instead.)

## Step 0 — Who is asking? (person mode vs agent mode)

Decide this first; it changes Steps 4-6 and the reply.

- **Person mode** — a person is in this conversation and can answer a question now. Everything below applies unchanged: CRM writes are gated, ambiguity is asked.
- **Agent mode** — anything else: another agent sent the facts (an agent-to-agent call, an MCP or API trigger, a scheduled or headless run, `--from-agent <name>` passed, or the message says it comes from an agent). **Nobody can answer, so this run never asks a question** (no `AskUserQuestion`, no "shall I?", no waiting). Follow **Agent mode** below in place of the gates.
- **Can't tell?** Use agent mode. A question nobody answers is worse than a marked, reversible offer.

## Agent mode — offers from another agent

An offer is a set of facts another agent believes are true. They are kept as **offers**: written with their source and date and marked unconfirmed until a person confirms them. They never overwrite what is already on record.

### A1 — Sort each fact: keep or drop

**Keep** facts about work:
- who someone is at work and their role, team, employer, or work relationship to us;
- a decision and its stated reason (who decided, what, why, when);
- a stated preference of a customer or partner (how they want to work, buy, be contacted at work);
- the same kinds of facts about an organisation, product or engagement (what it does, a deal stage, a term, a date).

**Drop** (never written, not even marked):
- anything personal about an individual — family, home life, relationships, beliefs, private contact details or address;
- health of an individual — conditions, leave reasons, wellbeing;
- money of an individual — pay, personal finances, debts, personal spending (company money such as a deal size or a price is a work fact and is kept);
- a fact with no entity it is about (`no entity named`) - **except a decision**, which is kept (see A3a);
- a fact with no source — neither its own nor `--source` (`no source`);
- a fact whose entity matches two or more existing notes (`ambiguous: <A> or <B> - resend naming one`). Never guess, never create a new note to dodge the choice.

When a fact mixes both (e.g. "Dana moved to the platform team after her surgery"), keep the work part and drop the rest, and say so. When unsure whether something is personal, drop it — the caller can resend.

### A2 — Date every kept fact

Use the fact's own date if it has one; otherwise the date the offer arrived, written `received <YYYY-MM-DD>`. The source is the fact's own source, else `--source`.

### A3 — Write kept facts as unconfirmed offers

Route (Step 3) and resolve (Step 4, without asking) as usual, then:
- **Existing note** — do **not** overwrite the body. Append each fact under a `## Offered by agents (unconfirmed)` section (create it above `## Change Log` if missing). If a fact contradicts the body, keep it anyway and add `contradicts: <the current line>`; a person decides later.
- **No note yet** — create it with the normal reference frontmatter plus `confirmation: unconfirmed` and `offered_by: <agent>` (`as_of` = the day the offer arrived); the body holds only the offered section, plus a `## Relations` wiki-link when a kept fact names another entity (e.g. a person's employer). A person confirming the note later removes those two fields.
- Fact line format, one per fact:
  ```markdown
  - <fact> (source: <source>; date: <YYYY-MM-DD | received YYYY-MM-DD>; offered by: <agent or "an agent">; unconfirmed)
  ```
- Append one `## Change Log` line per note: `- <today> - <N> fact(s) offered by <agent>, unconfirmed (source: <source>)`.
- This applies to every sub-scope, `market/` included: an offer never overwrites and never calls `/ref-supersede`.
- Then Step 7 (reindex) as usual. If the reindex fails, the facts are still kept; say so in the receipt.

### A3a — Decisions with no named person or organisation: the decisions record

A decision is kept even when it names no person, organisation, product or engagement ("warehouse move confirmed for 2 February, old site closes in March because the lease ends"). Decisions and their reasons are the most valuable thing a meeting produces; dropping them for want of an entity loses exactly that. Its home is a dated record, one file per month, chosen by the decision's date (else the date the offer arrived):

`Brain/Company/decisions/Decisions YYYY-MM.md`

- **No record for that month yet** - create it:
  ```markdown
  ---
  type: decision-record
  provenance: reference
  status: active
  as_of: <today>
  period: YYYY-MM
  confirmation: unconfirmed
  ---
  # Decisions YYYY-MM

  Decisions recorded for this month, newest last. A line marked `unconfirmed` was offered by an agent and not yet confirmed by a person.

  ## Decisions

  ## Change Log
  ```
- Append one line per decision under `## Decisions` (never rewrite an existing line):
  ```markdown
  - <date> - <what was decided>. Reason: <the stated reason | reason not stated>. Decided by: <name | not stated>. (source: <source>; date: <YYYY-MM-DD | received YYYY-MM-DD>; offered by: <agent or "an agent">; unconfirmed)
  ```
  `<date>` is the day the decision was made, not a date inside it (the warehouse decision above taken at a 27 November meeting is dated 2026-11-27; "2 February" stays in the text). When it does name an entity that has a note, add a `[[wiki-link]]` to it in the line; the entity note gets the fact as usual (A3).
- Re-stamp `as_of: <today>`, keep `confirmation: unconfirmed` while any line is unconfirmed, and append one `## Change Log` line: `- <today> - <N> decision(s) offered by <agent>, unconfirmed (source: <source>)`.
- The same line already present (same decision, same date) is not added twice; count it as kept and say `(already on record)` in the receipt.
- The A1 drops still apply: a decision about a person's health, family or pay is dropped like any other personal fact, and a decision with no source is dropped `no source`.

In **person mode** the same record is the home for an entity-less decision, gated like the CRM sub-scopes: show the line, write it on approval, without `unconfirmed` and with `offered by: <the person>`.

### A4 — Reply with a receipt, nothing else

The whole reply is this block, so the caller can log it:

```text
ref-ingest receipt
skill: ref-ingest v1.3
mode: agent-offer
caller: <agent name | unknown>
kept: <N>
dropped: <N>
dropped-reasons:
- "<first ~60 chars of the fact>" - <one or more of: personal, health, individual money, no entity named, no source, ambiguous: A or B>
written:
- <path from the repo root, e.g. Brain/Company/people/<name>.md> (+<N> facts, new | existing)
- <e.g. Brain/Company/decisions/Decisions 2026-11.md> (+<N> decisions, new | existing)
status: unconfirmed - a person confirms later
reindex: done | skipped (--no-reindex) | failed: <one line>
```

With nothing kept, `written:` is `- none`. Never include the dropped text beyond its first ~60 characters.

The **one operation every input funnels through** for a reference scope: `incoming info → resolve → reconcile → upsert`. It grows the manual single-upsert `manage-reference-data` with the two load-bearing hard parts — **entity resolution** (is this new "Reply" the existing `Reply.io`?) and **reconciliation** (new fact contradicts old → overwrite / supersede-with-history / flag) — plus the **automation split by scope**.

**Read first (authoritative — this skill enforces, does not restate):**
- `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` → "The update model", "The two axes" (sub-scope routing + `type:`/`relationship:` enums), "Automation boundary — split by scope".
- `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md` → the reference-kind frontmatter contract.
- `.claude/skills/manage-reference-data/SKILL.md` → the seed upsert (Step 0 scope check + the frontmatter template). This skill is its richer successor; it does not duplicate the contract.

## Composes

- `/ref-supersede` — when reconciliation finds a **validity transition** that needs a prior snapshot (contract renewal, role/price change), hand off instead of overwriting. **Never invoked on the market/autonomous branch** (see the invariant).

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/{people,orgs,products,engagements,market}/*.md` | ✓ | ✓ | Entity notes (one note = one entity) |
| Scope registry | `resources/local-brain-search/memory_config.py` | ✓ | | Confirm reference-kind |
| LBS index | `resources/local-brain-search/data/` | ✓ | ✓ (reindex) | FAISS + graph; reindexed after a write |
| Search wrappers | `resources/local-brain-search/run_search.sh` | ✓ | | Entity-resolution search under a `core,Company` mount |

## The automation split (load-bearing)

| Sub-scope | Writer | This skill |
|-----------|--------|------------|
| `market/` (watched competitors/ecosystem) | autonomous | **auto-overwrite, no gate** — reference facts sit outside the `encountered→endorsed` gate |
| `people/ orgs/ products/ engagements/` (transacted CRM) | curated | **human-gated** — present the diff, get approval before writing |

**Invariant (what makes any autonomous caller safe):** the `market/` branch is **overwrite-only** — it never opens an approval gate and **never calls `/ref-supersede`**. A validity transition in `market/` that would need a snapshot is *flagged for a human `ref-supersede`*, not auto-run. So a scheduled caller (e.g. `ref-refresh`, or domain-watch in 9e) that routes market items here always takes a gate-free path.

---

## Process

### Step 1 — Resolve the scope + confirm reference-kind

```bash
cd resources/local-brain-search
SCOPE="${scope:-Company}"
./venv/bin/python - "$SCOPE" <<'PY'
import sys, memory_config as mc
f = sys.argv[1]
print("kind:", mc.scope_kind(f), "| is_reference:", mc.is_reference_scope(f))
PY
```
If `is_reference` is False → **stop** (this skill only writes reference scopes). See the schema doc's "Adding a new reference scope".

### Step 2 — Extract candidate entity facts

From the incoming info (the user in conversation · a document/contract/deck/call · a domain-watch market signal · another agent's report), pull the **atomic facts about one real-world entity**: display name + aliases, `type:`, the relation to us (`relationship:`), body facts, and any term-bearing fact (a contract window, a role start, a price effective date).

### Step 3 — Route to the sub-scope (watch vs transact)

Apply the partition rule from COMPANY-BRAIN-SCHEMA "The two axes":
- an entity you **watch** (competitor, competitor product, ecosystem player) → `market/`
- an entity you **own or transact with** (self, client, prospect, partner, vendor, your offering, internal agent, a deal) → `people/ orgs/ products/ engagements/` by `type:`. The internal agent workforce (`type: agent`) lives in `products/` alongside own products — there is no separate `agents/` sub-scope.
- a **decision that names no entity** → `decisions/`, the dated monthly record (`type: decision-record`, format in A3a). A decision that names an entity goes to that entity's note as usual.
- `type:`/`relationship:` values MUST come from the schema doc's enum (person·organization·product·agent·engagement·interaction·decision-record × the relationship axis). Never invent a value.

### Step 4 — ENTITY RESOLUTION (never duplicate)

Find the one canonical note this fact belongs to before writing:
```bash
# semantic: does an entity like this already exist in the family?
BRAIN_READ_SCOPE=core,Company resources/local-brain-search/run_search.sh "<entity name + a distinctive fact>" --limit 8 --json
# exact/alias: title + body match
grep -rilE "<name>|<alias1>|<alias2>" Brain/Company/
```
- **Match found** → this is an *update* to that note. Use its exact path.
- **Ambiguous** (2+ plausible matches, e.g. "Reply" vs "Reply.io") → present the candidates and ask which entity this is (`AskUserQuestion`); do NOT guess a new note into existence. *(Agent mode: do not ask — drop the fact as `ambiguous`, see A1.)*
- **No `Brain/Company/` yet** (a fresh brain) → there is nothing to resolve against; every entity is new. Create the sub-scope folder when you write the first note.
- **No match** → genuinely new entity → *add*.

### Step 5 — RECONCILIATION (new fact vs old)

Compare the incoming fact to the note's current body:
| Situation | Action |
|-----------|--------|
| New fact **corrects/refreshes** an existing fact (same validity window) | **overwrite** the body (Step 6) |
| A **validity window closed** and a full prior snapshot matters (contract renewed, role changed, price re-termed) | hand to **`/ref-supersede`** — *CRM only; on `market/` flag for a human instead* |
| New fact **contradicts** old with no clear winner | **flag** — surface both, ask; do not silently overwrite |

### Step 6 — Automation gate + upsert

- **`market/`** → proceed (no gate). **CRM sub-scopes** → show the before/after diff and get explicit approval (`AskUserQuestion`) before writing. *(Agent mode replaces this gate with A3: no question, facts written as unconfirmed offers, body untouched.)*
- Write the note with the reference frontmatter contract (copy the template from `manage-reference-data` Step 2 — do not restate it here). On update: **overwrite the body** (current truth), preserve `created`/`created_by`, re-stamp `as_of` + `updated` to today, bump `updated_by` to your model. Append a `## Change Log` line:
  ```markdown
  ## Change Log
  - 2026-07-08 — <what changed> (source: <where it came from>)
  ```
- **Going forward only:** for a term-bearing fact, add `valid_from:`/`valid_until:`. **Do NOT** backfill these onto notes that lack them — incremental adoption.

### Step 7 — Reindex (unless deferred)

```bash
cd resources/local-brain-search && ./run_index.sh && ./run_daemon.sh restart   # daemon on :7437, RESTART not reload
```
Content-hash detection → a changed note triggers a **full FAISS rebuild** (minutes). Reference notes are **BDG-excluded**, so **no `run_brain_graph.sh bootstrap` is needed**. If invoked with `--no-reindex` (batch mode, e.g. by `ref-refresh` over many market items), **skip this step** and let the batch caller reindex once at the end.

---

## Verification

- **Round-trip:** after an add/overwrite + reindex, the entity **surfaces under a mount** and is **absent unmounted**:
  ```bash
  BRAIN_READ_SCOPE=core,Company resources/local-brain-search/run_search.sh "<entity>" --limit 5 --json   # present
  resources/local-brain-search/run_search.sh "<entity>" --limit 5 --json                                  # absent (core default)
  ```
- **Learn-gate held:** `md5 resources/local-brain-search/data/q_values.json` is byte-identical before and after (a mounted read trains nothing).
- **Audit trail:** the note has a new `## Change Log` line; the body is the current truth (no append-only drift); `as_of` = today.
- **Decision with no entity:** a headless offer of "warehouse move confirmed for 2 February, old site closes in March because the lease ends" (source: meeting notes) is kept, not dropped: the receipt lists `Brain/Company/decisions/Decisions <YYYY-MM>.md (+1 decisions, new)`, the line carries the reason, the source, the date, the offering agent and `unconfirmed`, and `/ref-query "what did we decide about the warehouse"` finds it.
- **Agent offer:** a headless run with one work fact and one personal fact returns a receipt with `kept: 1`, `dropped: 1` and the reason, asks nothing, leaves the existing body unchanged, and adds one `(unconfirmed)` line under `## Offered by agents (unconfirmed)`.
- **No duplicate:** exactly one note exists for the entity (`grep -ril "<name>" Brain/Company/` returns one canonical file).

## This skill must refuse to

- Write into a non-reference / core / cognitive folder, or set any `provenance` but `reference`.
- **Create a duplicate** entity note when resolution finds (or is unsure of) an existing one.
- **Auto-supersede or gate-skip on a CRM sub-scope**, or run `/ref-supersede` on the `market/` branch. (Agent mode is not a gate-skip: it never changes what is on record, it only adds marked offers.)
- **Ask a question in agent mode**, or write a fact it dropped under A1.
- Crystallize, lifecycle-classify, synthesis-pulse, or **promote a record into an endorsed cognitive insight** — that crossing stays the human `encountered → endorsed` act.
