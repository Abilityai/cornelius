---
name: refresh-index
description: Rebuild both qmd and FAISS indexes to reflect vault changes
automation: autonomous
schedule: "0 5 * * *"
allowed-tools: Bash
---

# Refresh Indexes

Rebuild both search indexes to ensure they reflect the current vault state.

## Purpose

Two indexes must be maintained:
- **qmd index** - Powers all search/retrieval (BM25 + vector + reranking)
- **FAISS index** - Powers graph analytics (connections, hubs, bridges, stats)

Neither index auto-updates. This skill rebuilds both.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | Source content to index |
| qmd CLI | `qmd` (global) | X | X | Search index (SQLite + vectors) |
| FAISS index script | `resources/local-brain-search/run_index.sh` | X | | Graph indexer |
| FAISS index | `resources/local-brain-search/data/` | | X | Graph index output |

## Prerequisites

- qmd installed globally (`npm install -g @tobilu/qmd`)
- Brain collection configured in qmd (`qmd collection list` shows "brain")
- Local Brain Search installed at `resources/local-brain-search/`
- Python environment with FAISS dependencies

## Process

### Step 1: Verify Prerequisites

```bash
which qmd && echo "qmd OK" || echo "qmd MISSING"
test -f resources/local-brain-search/run_index.sh && echo "FAISS OK" || echo "FAISS MISSING"
```

If either is missing, abort.

### Step 2: Rebuild qmd Index (Search)

```bash
qmd update && qmd embed
```

### Step 3: Rebuild FAISS Index (Graph)

```bash
resources/local-brain-search/run_index.sh
```

### Step 4: Verify Both Indexes

Verify qmd:
```bash
qmd status
```
Should show collection "brain" with file count > 0.

Verify FAISS graph:
```bash
resources/local-brain-search/run_connections.sh --stats --json
```
Should return valid JSON with note count > 0.

## Outputs

- Rebuilt qmd index at `~/.cache/qmd/index.sqlite`
- Rebuilt FAISS index at `resources/local-brain-search/data/`
- Stats output confirming both indexes are healthy

## Error Handling

| Error | Recovery |
|-------|----------|
| qmd not found | Install: `npm install -g @tobilu/qmd` |
| qmd collection missing | Re-add: `qmd collection add ./Brain --name brain --mask "{[0-9]*,AI*,Document*,CHANGELOG.md,README.md}/**/*.md"` |
| FAISS script missing | Check Local Brain Search installation |
| FAISS index fails | Check Python env, disk space |
| Stats return 0 notes | Re-run indexers, check Brain path |

## Completion Checklist

- [ ] qmd CLI exists
- [ ] FAISS indexer script exists
- [ ] qmd index rebuilt without errors
- [ ] FAISS index rebuilt without errors
- [ ] qmd status shows brain collection with files > 0
- [ ] FAISS stats query returns valid JSON with notes > 0
