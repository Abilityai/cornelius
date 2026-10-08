---
name: refresh-index
description: Rebuild the Local Brain Search FAISS index to reflect vault changes
automation: autonomous
schedule: "30 3 * * *"
allowed-tools: Bash
---

# Refresh Index

Rebuild the Local Brain Search vector index to ensure semantic search reflects current vault state.

## Purpose

The FAISS index is not auto-updated. This playbook refreshes it so semantic
search (and the BDG enrichment layer the Brain Orb reads) reflect the current
vault. The indexer is incremental — it re-embeds only changed/new notes — so a
daily refresh is a matter of seconds and never a long-running job.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | ✓ | | Source content to index |
| Index script | `resources/local-brain-search/run_index.sh` | ✓ | | Indexer |
| FAISS index | `resources/local-brain-search/brain_index/` | | ✓ | Output index |

## Prerequisites

- Local Brain Search installed at `resources/local-brain-search/`
- Python environment with FAISS dependencies

## Process

### Step 1: Verify Prerequisites

Check indexer exists:
```bash
test -f resources/local-brain-search/run_index.sh && echo "OK" || echo "MISSING"
```

If missing, abort.

### Step 2: Run the Indexer (incremental, short, resumable)

The indexer is **incremental**: it reuses the embedding of every note whose
content is unchanged and re-embeds only the delta. A normal daily run touches a
handful of notes and finishes in **seconds** — there is no long-running job here
anymore. Run it, then read the LAST line of its output:

```bash
resources/local-brain-search/run_index.sh
```

The final line is machine-readable:

```
RESULT reused=<N> embedded=<N> remaining=<N>
```

- **`remaining=0`** → the index is complete; go to Step 3.
- **`remaining>0`** → a large (cold/forced) rebuild was split into short,
  Trinity-safe batches (default cap: 500 notes/run). **Run the exact same command
  again** — each call reuses what's already indexed and embeds the next batch.
  Repeat until `remaining=0`. Daily runs are always a single pass.

**Execution rules — each call is short (seconds to ~2 min) and must STREAM:**

- **Run it in the foreground and let its heartbeat lines stream.** Do NOT pipe it
  through `tail`/`head`/`grep` — they buffer to EOF, so the call looks silent and
  the **300s stall watchdog can SIGKILL it**. And do NOT background it and end the
  turn to "await a completion notification" — a scheduled turn ending kills the
  child, so the job never finishes (this is exactly what made this skill silently
  skip for days). Loop short foreground calls instead; that is the sanctioned
  Trinity pattern for work that would otherwise be long.
- **Do not stop after the indexer** — Steps 3 and 4 MUST run in the same turn,
  once `remaining=0`.

The indexer writes the FAISS index, the connection graph, and a build manifest
(`data/manifest.json`, stamping the `cosine_ip` edge formula + `builder_version`)
— the manifest is written only on the final pass (`remaining=0`).

**Full rebuild after an indexing/edge-logic change** (e.g. the semantic-edge
formula): bump `BUILDER_VERSION` in `memory_config.py`, then force every note to
re-embed by removing the stale index and running the normal resumable loop, so
every call stays short:

```bash
rm -f resources/local-brain-search/data/brain.faiss resources/local-brain-search/data/brain_metadata.pkl
# then loop Step 2 until remaining=0
```

(`run_index.sh --force` also re-embeds everything, but in ONE unbounded pass —
use it only for an attended manual rebuild, never on a Trinity schedule.)

### Step 3: Verify Index

Confirm index works:
```bash
resources/local-brain-search/run_connections.sh --stats --json
```

Should return valid JSON with note count > 0.

### Step 4: Re-bootstrap Brain Dependency Graph (MANDATORY — do not defer)

**This is the step the whole pipeline exists for.** It writes
`resources/brain-graph/data/graph_enrichments.json` — the enrichment layer that
the Brain Orb and every coherence/lifecycle skill read. If the run ends before
this step (backgrounded indexer, watchdog kill, "I'll finish later"), the index
may be fresh but the enrichment layer stays stale and the orb graph stops
updating. Run it in the SAME turn as Steps 2-3, as a foreground call:

```bash
resources/brain-graph/run_brain_graph.sh bootstrap --force
```

Verify:
```bash
resources/brain-graph/run_brain_graph.sh status
```

Should show enriched nodes matching the new index count. The run is only
complete once this reports a node count close to the indexer's — a fresh FAISS
index with a stale `graph_enrichments.json` is a FAILED run, not a partial
success, even though the index step "succeeded."

### Step 5: Recompute lifecycle with the full engine (MANDATORY — must follow Step 4)

`bootstrap --force` stamps every *new* node with `compute_initial_lifecycle`, a
crude structural proxy (`0.5·citation-signal + 0.5·out/in-ratio`) whose ratio term
is suppressed by high in-degree, so it almost never clears the 0.6 generative
threshold. The full engine (`lifecycle.py`) computes the real behavioral signals —
citation frequency, generative ratio over typed edges, cross-domain reach — and
stamps `lifecycle_source: engine`, which bootstrap then preserves across future
re-bootstraps the way it preserves tensions and dismissals.

**Both halves are required.** Preservation alone (shipped earlier) only protects
scores that already exist; without this step new notes stay on the proxy forever
and the distribution drifts back toward the artifact. Skipping it is what made
"generative" read 13-14 when the true engine figure was ~161.

```bash
resources/brain-graph/run_brain_graph.sh lifecycle
```

Verify engine coverage is non-zero and preserved:
```bash
resources/local-brain-search/venv/bin/python -c "
import json, collections
d = json.load(open('resources/brain-graph/data/graph_enrichments.json'))
src = collections.Counter(v.get('lifecycle_source') for v in d['nodes'].values())
print(dict(src))"
```

Expect a substantial `engine` count (insight + framework layers; other layers
correctly stay `proxy` — the engine does not target them). **If `engine` is 0,
the lifecycle numbers in every downstream report are the proxy artifact — say so
rather than reporting them as health.**

### Step 6: Record the redundancy ("crowding") metric

Tracks whether notes are spreading out or piling onto the same ideas — the
early-warning signal for accumulating without digesting. Appends one line to
`data/redundancy_history.jsonl`; the value is the time series, so run it every
rebuild.

```bash
resources/local-brain-search/venv/bin/python resources/local-brain-search/redundancy.py
```

> **The 2026-09-02 frontmatter fix does not touch this metric's input, so the series is continuous.**
> The fix changed which chunk represents a note in the *graph*; `redundancy.py` averages *all* of a
> note's chunks straight from the FAISS index, which still holds every frontmatter chunk. (The first
> post-fix note claimed the boilerplate was "diluted" and the bias "did not materialize" - wrong reason:
> measured directly, frontmatter chunks add a constant **+0.034** to core NN1, driven by one-body-chunk
> notes.) Constant offset = comparable series: **no re-baseline needed** and pre-2026-09-02 samples stay
> valid - *unless* someone later excludes frontmatter from `note_vectors()`, which must re-baseline
> `data/redundancy_history.jsonl` in the same change. Background:
> `resources/local-brain-search/SIMILARITY-CALIBRATION.md` -> Trap 3.

Report any **ALARM** line (a scope that both grew and got more crowded) in the
run summary. Compare only the matched-n column — raw NN1 rises with note count
for free and is not comparable across scopes or dates.

### Step 7: Restart the search daemon (MANDATORY after a rebuild)

The daemon serves the index it loaded at start. After a rebuild its `build_id` no
longer matches the files on disk, `run_search.sh` refuses the stale daemon and falls
back to the CLI path, which loads the embedding model on **every** search - a
`/advise` with six searches goes from seconds to ten minutes. Restart it:

```bash
cd resources/local-brain-search && ./run_daemon.sh restart && sleep 3 && curl -s --max-time 3 http://127.0.0.1:7437/health
```

Expect `{"status":"ok", ... "build_id": <n>, "chunks": <n>}`. If the daemon will not
come up, say so in the report: searches still work, only slower.

## Outputs

- Rebuilt FAISS index at `resources/local-brain-search/data/`
- Refreshed BDG enrichments at `resources/brain-graph/data/graph_enrichments.json`
- Engine-computed lifecycle scores (`lifecycle_source: engine`), preserved across re-bootstrap
- Appended redundancy sample at `resources/local-brain-search/data/redundancy_history.jsonl`
- Stats output confirming note count

## Error Handling

| Error | Recovery |
|-------|----------|
| Script missing | Abort - check Local Brain Search installation |
| Index fails | Check Python env, disk space |
| Stats return 0 notes | Re-run indexer, check Brain path |
| `remaining>0` after a run | Expected for a cold/forced rebuild - just run Step 2 again; repeat until `remaining=0`. If `remaining` is not decreasing across runs, the partial index isn't persisting (check disk space / write perms on `data/`) |
| Indexer killed ~300s with no output | The stall watchdog fired - you piped/buffered or backgrounded it. Re-run per Step 2's execution rules: a foreground call, output streaming, no `tail`/pipe, no backgrounding |
| BDG bootstrap fails | Retry once. If it still fails, the LBS index is fresh but the orb/coherence enrichment layer is stale - report it; this is NOT a clean run |
| Lifecycle engine fails | Retry once. If it still fails, report that lifecycle figures are the bootstrap proxy, NOT health data - do not cite generative counts from this run |
| Redundancy script fails | Non-critical - the index and BDG are still valid. Log and continue; the metric is a trend signal, one missing sample is harmless |

## Completion Checklist

- [ ] Search daemon restarted and `/health` reports the new `build_id`

- [ ] Indexer script exists
- [ ] Index rebuilt without errors
- [ ] Stats query returns valid JSON
- [ ] Note count > 0
- [ ] BDG re-bootstrapped
- [ ] Lifecycle engine run after bootstrap; `lifecycle_source: engine` count > 0
- [ ] Redundancy sample appended; any ALARM reported
