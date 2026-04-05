---
name: compute-lifecycle
description: Compute lifecycle scores for all insight and framework notes - detect which notes are crystallizing or becoming generative
allowed-tools: [Bash, Read]
user-invocable: true
automation: gated
---

# Compute Lifecycle Scores

Computes lifecycle scores (0.0 reflective -> 1.0 generative) for all insight and framework notes based on behavioral signals: citation frequency, generative ratio, cross-domain reach, and temporal acceleration.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Enrichments | `resources/brain-graph/data/graph_enrichments.json` | ✓ | ✓ | Updated lifecycle scores |
| LBS Graph | `resources/local-brain-search/data/brain_graph.pkl` | ✓ | | NetworkX graph |
| Brain files | `Brain/**/*.md` | ✓ | | File mtimes for temporal signals |

## Process

### Step 1: Run lifecycle computation

```bash
cd resources/brain-graph
../local-brain-search/venv/bin/python cli.py lifecycle
```

For JSON output:
```bash
../local-brain-search/venv/bin/python cli.py lifecycle --json
```

### Step 2: Present transitions

Focus on notes that crossed phase boundaries:
- **Reflective -> Crystallizing**: Note is starting to generate its own connections
- **Crystallizing -> Generative**: Note has become a driver of new insights

For promotable notes, suggest:
- "Consider promoting to framework status"
- "This note drives connections across N domains"

## Lifecycle Phases

| Score Range | Phase | Meaning |
|---|---|---|
| 0.0 - 0.3 | Reflective | Tracks sources, sources win on conflict |
| 0.3 - 0.6 | Crystallizing | Generating own connections, authority contested |
| 0.6 - 1.0 | Generative | Drives downstream notes, this note wins on conflict |
