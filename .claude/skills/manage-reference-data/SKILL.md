---
name: manage-reference-data
description: Upsert and maintain entity notes in a REFERENCE-kind scope (external facts/records), then reindex so they become connection/insight targets. Generic across reference scopes; Company is the default. The scope's entity taxonomy (type/relationship) lives in that scope's own schema doc (Company's is COMPANY-BRAIN-SCHEMA.md). NEVER crystallizes, lifecycle-classifies, or trains on reference data.
automation: manual
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
user-invocable: true
argument-hint: "[add|update|supersede|list|mount-help] [scope=Company] [entity name]"
metadata:
  version: "1.0"
  created: 2026-06-26
  author: Cornelius
---

# Manage Reference Data

Maintain a **reference-kind scope** — a non-core Brain/ layer of *external facts/records* the personal brain discovers bridges to, not a query store (a CRM owns queries). This skill upserts entity notes (overwrite-in-place), stamps the reference contract, and reindexes. It is **generic**: pass `scope=<Folder>` for any registered reference scope; `Company` is the default.

**Read first:** `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md` (the generic kind contract: frontmatter + linking + privacy) **and the target scope's own schema doc** for its `type:`/`relationship:` enum + structure (Company → `COMPANY-BRAIN-SCHEMA.md`, which also defines the family sub-scopes and the `ref-*` playbook suite this skill is the seed of). This skill *enforces* those docs; it does not restate them.

**Hard rules (non-negotiable — these are what make it a reference scope):**
- Every note gets `provenance: reference`. Never `originated`/`endorsed`/`encountered`/`ai-inferred`.
- Reference notes are **never** crystallized, lifecycle-classified, or used as a synthesis-pulse source.
- Reference scopes are non-core → they never train q-values (the engine learn-gate already guarantees this; do not bypass it).
- Default read scope is unchanged. Reference data surfaces only under an explicit `BRAIN_READ_SCOPE=core,<Scope>` mount.

---

## Step 0 — Resolve the scope and confirm it is registered + reference-kind

```bash
(
cd resources/local-brain-search
SCOPE="${1:-Company}"   # or parse scope=<Folder> from args
./venv/bin/python - "$SCOPE" <<'PY'
import sys, memory_config as mc
folder = sys.argv[1]
print("kind         :", mc.scope_kind(folder))
print("is_reference :", mc.is_reference_scope(folder))
print("is_core      :", folder in mc.CORE_FOLDERS)
PY
)
```

- If `is_reference` is **False**: the scope is not registered as reference. Stop and either (a) add a `ScopeDef(..., SCOPE_KIND_REFERENCE, False, (...))` to `SCOPE_REGISTRY` in `memory_config.py`, or (b) `register_scope("<Folder>", kind="reference", slugs=(...))`. See the schema doc → "Adding a new reference scope". Do **not** write entity notes into a non-reference folder.

## Step 1 — Privacy (settled: private agent, no gate)

Cornelius is a fully private agent on a private remote, so reference data is **committed/synced by default** — no per-scope gate to clear. Just populate.

The only exception: if *this specific scope* must be host-local (e.g. third-party data you've agreed not to sync), add `Brain/$SCOPE/` to `.gitignore` first. Default is to commit.

## Step 2 — Upsert the entity note (overwrite-in-place)

One note = one entity. Path: `Brain/<Scope>/<entity-name>.md` for a flat scope; **for a family scope, route into the correct child folder** per that scope's schema doc (e.g. `Brain/Company/people/<name>.md`, `Company/market/<name>.md` — never loose at the family root). Apply the frontmatter contract exactly — `type:`/`relationship:` values come from the scope's schema doc:

```yaml
---
type: <per the scope's schema doc — Company's enum is in COMPANY-BRAIN-SCHEMA.md>
relationship: <per the scope's schema doc, when the scope uses the axis>
provenance: reference
scope: <Scope>
status: active
as_of: <today YYYY-MM-DD>
updated: <today>
created: <today, or preserve existing>
created_by: <your model name>
updated_by: <your model name>
agent_version: 01.25
---

# <Entity display name>

<concise factual body>

## Relations
- <relation>: [[Other Entity]]

## Change Log
- <today> — <what changed and the source>
```

- **add**: create the file. **update**: overwrite-in-place (re-stamp `as_of:`/`updated:`, preserve `created`/`created_by`). Reference data is mutable — overwriting is correct, not destructive.
- **supersede**: set the old note `status: superseded` + `superseded_by: "[[New Entity]]"`; create the new note `status: active`. Keep both (history).
- Relations are `[[wiki-links]]` (explicit edges, traversed by connection-finder). Use a `contract`/`engagement` note as the join for many-to-many (Client × Product × owner × dates × value).

## Step 3 — Reindex (so the note becomes a connection target)

```bash
(cd resources/local-brain-search && ./run_index.sh)        # then, if the daemon is running:
./run_daemon.sh restart                                   # daemon is long-lived: RESTART, never reload
```

`index_brain.py` uses **content-hash change detection**: if nothing changed it skips; if any note changed it does a **full rebuild** (FAISS has no good incremental append). So an add/overwrite triggers a full reindex of the vault — expect minutes on the full Brain. After it completes, the reference note exists in the index as a non-core node — invisible to default (core) readers, surfaced only when mounted. **Restart the daemon** afterward so the long-lived process serves the new note (the wrapper's stale-guard only checks index mtime, not whether new scope tokens were added to the code).

## Step 4 — Mount for discovery (opt-in, per-invocation)

To let the personal brain find bridges to these entities, run a discovery pass with the scope mounted:

```bash
BRAIN_READ_SCOPE=core,<Scope> resources/local-brain-search/run_connections.sh --note "<a core note>"
# or auto-discovery / connection-finder with the same env var
```

Unset, the scope stays absent from every reader. The mounted (non-pure-core) read trains no q-values — verify `data/q_values.json` is byte-unchanged after a mounted discovery pass (existing learn-gate; this is the positive safety control).

---

## Acceptance (matches Phase 6 in SCOPE-IMPLEMENTATION-PLAN.md)

1. `BRAIN_READ_SCOPE` unset → reference notes absent from recall/search/connections; `q_values.json` byte-unchanged.
2. `=core,<Scope>` → entities surface and link to core notes via wiki-links; the mounted read trains no q-values.
3. Editing a note in place + reindex re-embeds it and drops the old content (content-hash diff).
4. Reference notes never appear in `--hubs` / lifecycle / tension output (non-core, fingerprint-excluded), and are never crystallized.

## What this skill must refuse

- Writing into a non-reference (cognitive/core) folder.
- Setting any provenance other than `reference`.
- Any crystallize / graduate / lifecycle / synthesis-pulse action on a reference note (route those to cognitive scopes only).
