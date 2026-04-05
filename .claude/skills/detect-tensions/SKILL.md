---
name: detect-tensions
description: Detect productive contradictions between notes - high semantic similarity with opposing conclusions that represent synthesis opportunities
allowed-tools: [Bash, Read]
user-invocable: true
automation: gated
---

# Detect Productive Tensions

Scans the knowledge base for productive contradictions: note pairs with high semantic similarity but opposing conclusions. These tension zones are where the most valuable articles and frameworks emerge.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Enrichments | `resources/brain-graph/data/graph_enrichments.json` | ✓ | ✓ | Tension records saved |
| FAISS Index | `resources/local-brain-search/data/brain.faiss` | ✓ | | Similarity search |
| Metadata | `resources/local-brain-search/data/brain_metadata.pkl` | ✓ | | Note content |

## Process

### Step 1: Run tension detection

Default thresholds (similarity > 0.75, divergence > 0.3):
```bash
cd resources/brain-graph
../local-brain-search/venv/bin/python cli.py tensions
```

Broader search (more results, lower quality):
```bash
../local-brain-search/venv/bin/python cli.py tensions --similarity 0.70 --divergence 0.2
```

### Step 2: Present synthesis opportunities

For each tension, explain:
- What the two notes assert
- Why they contradict
- What synthesis opportunity exists (article topic, framework potential)

### Step 3: Track existing tensions

```bash
../local-brain-search/venv/bin/python cli.py status --json
```

Check `tension_count` for total tracked tensions.

## Key Principle

Tensions are features, not bugs. The system NEVER auto-resolves tensions. It surfaces them as the most productive intellectual territory in the vault.
