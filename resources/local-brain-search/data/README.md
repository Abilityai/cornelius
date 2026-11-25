# Search index (built on your machine)

No index ships with the template. `/first-run` (or `run_index.sh`) builds it from
whatever is in the vault - a few templates on a fresh, empty brain; about 6,600
chunks once the seed library is added with `/first-run --with-library`.

| File | What it is |
|------|------------|
| `brain.faiss` | FAISS vector index (384-dim, `all-MiniLM-L6-v2` embeddings) |
| `brain_metadata.pkl` | Per-chunk metadata (vault-relative paths) |
| `brain_graph.pkl` | NetworkX graph: explicit wiki-link edges + semantic-similarity edges |
| `manifest.json` | Build provenance (model, edge formula, counts) |

All of these are gitignored. Rebuild after notes change:

```bash
resources/local-brain-search/run_index.sh      # or /refresh-index
```
