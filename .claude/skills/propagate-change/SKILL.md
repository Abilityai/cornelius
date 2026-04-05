---
name: propagate-change
description: Propagate staleness from a changed note through the Brain Dependency Graph - shows which downstream notes need review
argument-hint: <note name>
allowed-tools: [Bash, Read]
user-invocable: true
automation: gated
---

# Propagate Framework/Note Change

When a note is substantially edited, this skill computes which downstream notes may be stale and need review. Uses the Brain Dependency Graph's staleness propagation engine with edge-type decay, distance decay, and hub dampening.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Enrichments | `resources/brain-graph/data/graph_enrichments.json` | ✓ | ✓ | Updated staleness scores |
| LBS Graph | `resources/local-brain-search/data/brain_graph.pkl` | ✓ | | NetworkX graph |

## Process

### Step 1: Run propagation

```bash
cd resources/brain-graph
../local-brain-search/venv/bin/python cli.py propagate "<NOTE_NAME>"
```

Optional: specify change magnitude (0.0-1.0) for partial changes:
```bash
../local-brain-search/venv/bin/python cli.py propagate "<NOTE_NAME>" --magnitude 0.5
```

### Step 2: Present affected notes

Show the user which notes are flagged for review, sorted by staleness score.

For each affected note, explain:
- Why it's flagged (which upstream change, through what edge type)
- Suggested action: review, update, or mark as OK

### Step 3: Offer to inspect specific notes

If the user wants details on any affected note:
```bash
../local-brain-search/venv/bin/python cli.py inspect "<NOTE_NAME>"
```

## When to Use

- After substantially editing a framework or key insight note
- When the user says they've updated their thinking on a topic
- After ingesting new source material that contradicts existing notes
