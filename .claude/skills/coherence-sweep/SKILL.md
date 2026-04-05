---
name: coherence-sweep
description: Run a full coherence sweep across the Brain Dependency Graph - computes staleness, lifecycle transitions, structural health, and generates a report
argument-hint: [--days N] [--tensions] [--json]
allowed-tools: [Bash, Read, Write]
user-invocable: true
automation: gated
---

# Brain Coherence Sweep

Run a full coherence analysis of the knowledge base using the Brain Dependency Graph engine. Identifies stale notes, lifecycle transitions, structural issues, and optionally productive tensions.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| LBS Graph | `resources/local-brain-search/data/brain_graph.pkl` | ✓ | | NetworkX graph |
| Enrichments | `resources/brain-graph/data/graph_enrichments.json` | ✓ | ✓ | Node/edge enrichments |
| Reports | `resources/brain-graph/reports/` | | ✓ | Generated reports |

## Prerequisites

- Brain Dependency Graph must be bootstrapped (`run_brain_graph.sh bootstrap`)
- Local Brain Search index must exist

## Process

### Step 1: Check bootstrap status

```bash
cd resources/brain-graph
../local-brain-search/venv/bin/python cli.py status
```

If not bootstrapped, run bootstrap first:
```bash
../local-brain-search/venv/bin/python cli.py bootstrap
```

### Step 2: Run coherence sweep

Default (7-day lookback, lifecycle included, no tensions):
```bash
../local-brain-search/venv/bin/python cli.py coherence
```

With options:
```bash
# Include tension detection (slower)
../local-brain-search/venv/bin/python cli.py coherence --tensions

# Custom lookback period
../local-brain-search/venv/bin/python cli.py coherence --days 14

# JSON output
../local-brain-search/venv/bin/python cli.py coherence --json
```

### Step 3: Present results

Read the generated report and present key findings to the user:

1. **Staleness alerts** - Notes that need review due to upstream changes
2. **Lifecycle transitions** - Notes crossing phase boundaries (reflective -> crystallizing -> generative)
3. **Structural health** - Orphans, overloaded hubs, missing MOCs
4. **Tensions** (if enabled) - Productive contradictions for synthesis

Report is saved to: `resources/brain-graph/reports/coherence-report-YYYY-MM-DD.md`

## Output Format

Present a concise summary with:
- Count of stale notes with top 5 most affected
- Notable lifecycle transitions (especially new generative notes)
- Structural issues requiring attention
- Path to full report
