# Similarity Calibration - the metric contract

**Status:** canonical method. This file is the single source of truth for what a similarity number MEANS in this system. Skills state their threshold and cite this file; they do not re-derive bands in their own prose.
**Reproduce on your vault:** `resources/local-brain-search/venv/bin/python calibrate_similarity.py --session "<session folder>"`

> The figures below are **indicative**, taken from a reference instance (several thousand notes, `cosine_ip` index, the default embedding model). Your vault will differ - **re-measure before trusting any band**, and again after any large ingestion wave, embedding-model change, or chunking change.

---

## The one rule

> **A similarity score has no meaning without its population.** The same 0.75 is routine in one measurement space, reachable-but-rare in a second, and physically unreachable in a third. A threshold written against one space and copied into another silently means something else.

---

## The measurement spaces

### Space 1 - chunk <-> chunk cosine (what the GRAPH is built from)

`add_semantic_edges()` in `index_brain.py` embeds each note's **representative chunk** and links it to the top-k most similar chunks above `semantic_edge_threshold`. Indicative median ~0.78. Space-1 numbers are **not** comparable to query-space scores; residual `1.000`s are genuine duplicate content (e.g. near-identical changelogs).

### Space 2 - query -> vault (what `/recall`, `/search-vault`, `/find-connections` see)

A note title encoded as a query, searched against the vault. Indicative: a note's score against **itself** has a median ~0.8, and its **best other** neighbour a median ~0.7 - the margin is thin, and a large share of notes have *some other* note above 0.75. "Scores above 0.75 are near-duplicates" is false. High scores here are often shared boilerplate (changelogs, READMEs), not insight relationships.

**Scoped reads are their own populations.** Under the `scope-mount` contract, `core` (voice reads) is the tightest population - its best-other scores run noticeably lower than the reasoning mount (`core,Books,document-insights`) or the whole vault, so a fixed `0.5` threshold drops the tail at `core`. Bands do not transfer between mounts.

### Space 3 - new external material -> core (what INGESTION and auto-linking see)

Freshly ingested notes queried against `core`. Indicative median ~0.47, **ceiling ~0.56**. **This is the operative space for every ingestion, dedup, and unhookedness check.** A threshold >= 0.65 here is not "strict" - it is unreachable, and it fails silently by returning nothing, which reads identically to "no connections exist."

### Space 4 - near-duplicate probe (what the DEDUP gate sees)

Approximated by querying a note with its own title / first sentence. A true duplicate scores ~0.70-0.75 median - but the best *unrelated* neighbour scores almost the same. **No score-only gate separates duplicates from neighbours.** Gate on **rank** (always read the top 3) plus a **raw-cosine tail** (`raw_similarity >= 0.60` anywhere in the list); on the reference instance that caught ~80-90% of simulated duplicates at a bounded cost.

---

## Threshold inventory - the space each threshold runs in

| Threshold | Where | Runs against | Guidance |
|---|---|---|---|
| `AUTO_LINK_THRESHOLD` 0.45 | `ingest-source` | Space 3 | Sits near the Space-3 median. Conceptual filter mandatory; false friends are common. |
| `semantic_edge_threshold` 0.65 | `memory_config.py` | Space 1 | A floor on what may enter; the top-k quota is what actually decides. |
| `default_threshold` 0.5 (search) | `memory_config.py` | all | Harmful in Space 3, tight at `core`. Ingestion/dedup paths must pass an explicit lower `--threshold`. |
| strong/moderate/weak layers | `find-connections` | Space 2 | Read as percentiles, not quality grades. Unreachable if pointed at new material. |
| auto-discovery band ~0.45-0.70 | `auto-discovery` | Space 2 | A *candidate pool* - the reasoning grades the connection, not the score. |
| dedup read-gate | `document-insight-extractor` | Space 4 | Top-3 by rank + `raw_similarity >= 0.60`. |
| unhooked `< 0.40` / hooked `>= 0.45` | `domain-watch` | Space 3 (core) | Concepts a KB is built on can score as low as ~0.45 against core; foreign nouns ~0.2-0.4. |

---

## Trap 1: the reported `similarity` is not raw cosine

`static_search()` applies a Q-value learning adjustment that **overwrites `similarity` in place and re-sorts**. Consequences:

- The headline number is a **ranking score**, not cosine. Never quote it as a measurement.
- **Ranking is unstable in `--limit`**: a larger limit can admit boosted notes that push the true nearest neighbour out of view.
- The `--threshold` filter is applied to raw cosine *before* adjustment.

Every static result also carries **`raw_similarity`** (printed as `Raw cosine:`). **Any skill that compares a score to a threshold must use `raw_similarity`.**

## Trap 2: `build_scope_selector` takes RESOLVED folders, not scope tokens

```python
build_scope_selector(metadata, ['core'])                       # WRONG - matches nothing
build_scope_selector(metadata, resolve_read_scope('core'))     # right
```

Unresolved, `'core'` is treated as a literal folder name, matches zero rows, and the fail-safe path returns an empty result set - indistinguishable from "no matches in scope."

## Trap 3: the frontmatter collision

If a note's first chunk is nothing but its YAML frontmatter, notes created the same day by the same model get **byte-identical** representative text, and the graph fills with cosine-1.000 edges between unrelated notes. Because most notes sit at the top-k edge cap, these artifacts **displace** real neighbours rather than adding noise.

**Fixed in `index_brain.py`** (`is_meaningless_chunk()`): frontmatter-only chunks, empty stub notes, and chunks shorter than `min_chunk_length` are excluded both as a note's representative and as an edge target. `tension.py` uses the same representative-chunk rule. After upgrading, **rebuild the index** and re-run `/detect-tensions` - tension candidates detected under an older index are suspect.

`redundancy.py` averages *all* of a note's chunks straight from the index (frontmatter included), so the fix does not move its series. If you ever exclude frontmatter there, re-baseline its history in the same change.

---

## When to re-run

Re-run `calibrate_similarity.py` and update this file after an embedding-model change, an index-builder version bump, a chunking change, or any ingestion wave large enough to move the population. Treat every band in every skill as **provisional until re-measured**.
