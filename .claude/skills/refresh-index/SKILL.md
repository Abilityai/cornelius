---
name: refresh-index
description: Rebuild the Local Brain Search FAISS index to reflect vault changes
automation: autonomous
schedule: "0 5 * * *"
allowed-tools: Bash
---

# Refresh Index

Rebuild the Local Brain Search vector index to ensure semantic search reflects current vault state.

## Purpose

The FAISS index is not auto-updated. This playbook rebuilds it so semantic search stays accurate.

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

### Step 2: Run Indexer

```bash
resources/local-brain-search/run_index.sh
```

### Step 3: Verify Index

Confirm index works:
```bash
resources/local-brain-search/run_connections.sh --stats --json
```

Should return valid JSON with note count > 0.

### Step 4: Re-bootstrap Brain Dependency Graph

The BDG enrichments depend on the LBS graph. After reindexing, re-classify nodes and edges:

```bash
resources/brain-graph/run_brain_graph.sh bootstrap --force
```

Verify:
```bash
resources/brain-graph/run_brain_graph.sh status
```

Should show enriched nodes matching the new index count.

## Outputs

- Rebuilt FAISS index at `resources/local-brain-search/data/`
- Refreshed BDG enrichments at `resources/brain-graph/data/graph_enrichments.json`
- Stats output confirming note count

## Error Handling

| Error | Recovery |
|-------|----------|
| Script missing | Abort - check Local Brain Search installation |
| Index fails | Check Python env, disk space |
| Stats return 0 notes | Re-run indexer, check Brain path |
| BDG bootstrap fails | Non-critical - LBS index still works without BDG |

## Completion Checklist

- [ ] Indexer script exists
- [ ] Index rebuilt without errors
- [ ] Stats query returns valid JSON
- [ ] Note count > 0
- [ ] BDG re-bootstrapped
