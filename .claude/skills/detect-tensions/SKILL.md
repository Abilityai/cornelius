---
name: detect-tensions
description: Detect productive contradictions between notes - high semantic similarity with opposing conclusions that represent synthesis opportunities
allowed-tools: [Bash, Read]
user-invocable: true
automation: gated
metadata:
  version: "1.3"
  updated: 2026-09-02
  changelog:
    - "1.3: The 1.2 caveat was wrong in the reassuring direction - the index rebuild never reached this detector, which picks its own representative chunk straight from the FAISS metadata (first chunk = frontmatter for 83% of notes) and was therefore mostly blind for those notes (measured on 293 of them: 121 usable pair hits and 3 in 4 notes with none, vs 765 hits with the representative mapping; different-text frontmatter never lands in [0.75, 0.93)). tension.py now uses the first MEANINGFUL chunk (_representative_chunks / _is_boilerplate_chunk, mirroring index_brain.is_meaningless_chunk). Candidates tracked before 2026-09-02 are suspect (64% had frontmatter first chunks on both sides locally)"
    - "1.2: Label the measurement space. The detector's 0.75/0.70 floors are graph-space (chunk-to-chunk) numbers, NOT comparable to the Q-adjusted scores /recall prints; and until the index is rebuilt with the frontmatter fix a large share of top-scoring pairs are same-date boilerplate twins. See resources/local-brain-search/SIMILARITY-CALIBRATION.md"
    - "1.1: Document detector blind spots - filter the false-positive flood (boilerplate/near-duplicate pairs) and probe manually for cross-vocabulary tensions the similarity+keyword detector cannot see (output is candidates, not proof of absence)."
    - "1.0: Initial version"
---

# Detect Productive Tensions

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change - the top entry of `metadata.changelog` above - e.g. `detect-tensions vX.Y - recent: <summary>`. Then proceed.

Scans the knowledge base for productive contradictions: note pairs with high semantic similarity but opposing conclusions. These tension zones are where the most valuable articles and frameworks emerge.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Enrichments | `resources/brain-graph/data/graph_enrichments.json` | ✓ | ✓ | Tension records saved |
| FAISS Index | `resources/local-brain-search/data/brain.faiss` | ✓ | | Similarity search |
| Metadata | `resources/local-brain-search/data/brain_metadata.pkl` | ✓ | | Note content |

## Process

### Step 1: Run tension detection

Default thresholds (similarity > 0.75, divergence > 0.3). **These are graph-space (chunk-to-chunk) numbers and are NOT comparable to the scores `/recall` or `/search-vault` print** - see `resources/local-brain-search/SIMILARITY-CALIBRATION.md`. **Fixed 2026-09-02 (v1.3):** the detector now queries with each note's first *meaningful* chunk instead of its first chunk (bare frontmatter for 83% of notes) - before that it returned nothing usable for 3 in 4 of those notes, and the graph rebuild did not help because `tension.py` picks its chunk itself. Expect the candidate set to change shape on the first post-fix scan, and treat pairs tracked before 2026-09-02 as suspect (see `SIMILARITY-CALIBRATION.md` -> Trap 3):
```bash
cd $PROJECT_ROOT/resources/brain-graph
../local-brain-search/venv/bin/python cli.py tensions
```

Broader search (more results, lower quality):
```bash
../local-brain-search/venv/bin/python cli.py tensions --similarity 0.70 --divergence 0.2
```

### Step 2: Filter false positives, then present synthesis opportunities

The raw count is dominated by false positives - discard them before presenting:
- **Boilerplate / near-duplicate pairs.** The signature is high similarity with maximal divergence (e.g. sim ≈ 1.00, divergence ≈ 1.00), and pairs where both notes are changelogs, registries, or near-identical restatements of one principle. These are detector artifacts, not contradictions.

Keep only pairs that assert genuinely **opposing conclusions about the same question**. For each surviving tension, explain:
- What the two notes assert
- Why they contradict
- What synthesis opportunity exists (article topic, framework potential)

### Step 3: Track existing tensions

```bash
../local-brain-search/venv/bin/python cli.py status --json
```

Check `tension_count` for total tracked tensions.

### Step 4: Probe for cross-vocabulary tensions the detector cannot see

The detector pairs notes by cosine similarity (floor ~0.70, measured **note-to-note in graph space** - not the query space that `/recall` reports, see `resources/local-brain-search/SIMILARITY-CALIBRATION.md`) and scores opposition with a keyword heuristic (negation vs. assertion words). It is therefore **structurally blind to the most valuable tensions**: genuine contradictions are usually *cross-vocabulary* - two frameworks reaching opposite conclusions in different language - which fall BELOW the similarity floor and read too assertively for the keyword check. **A thin or empty result does NOT mean no tensions exist; this tool surfaces candidates, it does not certify absence.**

Compensate by manually checking known opposing-framework pairs even when they score below threshold, e.g.:
- loss aversion (prospect theory) ↔ ergodicity / Kelly  (bias vs. correct policy)
- Bayesian/Brier "assign a probability" ↔ "There Is No Bayesian Dial" / radical uncertainty
- heuristics-and-biases ↔ ecological / evolutionary rationality
- expert failure as psychological ↔ expert failure as structural

Treat these as candidate `tension` edges regardless of the detector's similarity score.

> **Root-cause fix (code, out of scope for this playbook):** durable precision needs `resources/brain-graph/tension.py` to replace the keyword stance heuristic with an LLM stance-classifier on a shared proposition, lower the similarity floor with theme/MOC-anchored cross-cluster pairing, and exclude index/changelog-layer nodes from the scan.

## Key Principle

Tensions are features, not bugs. The system NEVER auto-resolves tensions. It surfaces them as the most productive intellectual territory in the vault.
