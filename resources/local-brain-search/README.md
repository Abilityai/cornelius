# Local Brain Search

Local vector search and connection discovery for the Brain folder, independent of Smart Connections plugin.

**Tech Stack:** FAISS + sentence-transformers + NetworkX

## Features

- **Semantic search** - Find notes by meaning, not just keywords
- **Connection graph** - Discover explicit links AND semantic relationships
- **Hub detection** - Find most connected notes
- **Bridge detection** - Find notes connecting different topics
- **Multi-hop paths** - Discover paths between distantly related notes
- **Fully local** - No cloud APIs, all data stays on your machine
- **Fast** - Sub-100ms queries, 14s indexing for 1200+ notes

## Current Stats (Dec 2025)

```
Notes indexed: 1261
Total chunks: 7726
Graph nodes: 1261
Graph edges: 9300
  - Explicit (wiki-links): 5201
  - Semantic (similarity): 4099
```

## Setup

```bash
cd ./resources/local-brain-search

# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Index the Brain folder (first time - takes ~15 seconds)
python index_brain.py

# Re-index after changes
python index_brain.py

# Force full re-index
python index_brain.py --force
```

## Usage

### Search

```bash
# Activate venv first
source venv/bin/activate

# Basic search
python search.py "dopamine reward prediction"

# Limit results
python search.py "consciousness" --limit 5

# Set similarity threshold (0-1)
python search.py "meditation" --threshold 0.7

# Show full content
python search.py "belief systems" --full

# JSON output (for scripting)
python search.py "AI agents" --json
```

### Connections

```bash
# Find connections for a note (searches by title/filename)
python connections.py "Dopamine"

# Multi-hop connections (depth 2)
python connections.py "Dopamine" --depth 2

# Only semantic connections
python connections.py "Flow states" --semantic-only

# Only explicit links
python connections.py "Buddhism" --explicit-only

# Graph statistics
python connections.py --stats

# Find hub notes (most connected)
python connections.py --hubs

# Find bridge notes (connect communities)
python connections.py --bridges

# JSON output
python connections.py "Dopamine" --json
```

## How It Works

### Indexing (`index_brain.py`)

1. **Collect notes** - Scans all .md files in Brain folder
2. **Chunk content** - Splits notes by headings for better granularity
3. **Generate embeddings** - Uses `all-MiniLM-L6-v2` (384 dimensions, normalized)
4. **Store vectors** - FAISS IndexFlatIP for cosine similarity search
5. **Build graph** - NetworkX DiGraph with explicit links + semantic edges

### Search (`search.py`)

1. Encode query with same embedding model
2. Find nearest neighbors in FAISS index
3. Return results above similarity threshold

### Connection Discovery (`connections.py`)

1. Load graph from pickle
2. Find note by name/title/path
3. Traverse explicit edges (wiki-links)
4. Include semantic edges (similarity > 0.65)
5. Compute multi-hop paths if requested

## Data Storage

All data stored in `./data/`:

```
data/
├── brain.faiss        # FAISS vector index
├── brain_metadata.pkl # Chunk metadata (titles, content, paths)
└── brain_graph.pkl    # NetworkX graph (nodes + edges)
```

Total size: ~50MB

## Configuration

Edit `config.py` to customize:

```python
# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384d, fast

# Semantic edge threshold (0-1)
SEMANTIC_EDGE_THRESHOLD = 0.65  # Notes with similarity > this get connected

# Number of semantic edges per note
SEMANTIC_EDGE_TOP_K = 5

# Search defaults
DEFAULT_SEARCH_LIMIT = 10
DEFAULT_SIMILARITY_THRESHOLD = 0.5

# Excluded folders
EXCLUDED_FOLDERS = ["templates", ".obsidian", ".trash"]
```

## Performance

For ~1200 notes / 7700 chunks:
- Initial indexing: ~15 seconds
- Search latency: <100ms (including model load)
- Connection lookup: <50ms
- Storage: ~50MB

## Integration Ideas

### As MCP Server

This can be wrapped as an MCP server. Tools would be:
- `search_brain(query, limit, threshold)` - Semantic search
- `get_connections(note_name, depth)` - Connection discovery
- `get_graph_stats()` - Graph statistics
- `find_hubs(top_n)` - Find hub notes
- `find_bridges(top_n)` - Find bridge notes

### With Claude Bash Tool

```bash
# Search from Claude
cd ./resources/local-brain-search && \
source venv/bin/activate && \
python search.py "your query" --json
```

### With Scripts

All scripts output JSON with `--json` flag:

```bash
# Pipe to jq for processing
python search.py "query" --json | jq '.[].title'
python connections.py --hubs --json | jq '.[0:5]'
```

## Differences from Smart Connections

| Feature | Smart Connections | Local Brain Search |
|---------|-------------------|-------------------|
| Embedding model | BGE-micro-v2 | all-MiniLM-L6-v2 |
| Vector DB | Custom | FAISS |
| Interface | Obsidian plugin | CLI/Python |
| Portability | Obsidian-only | Any environment |
| MCP integration | Yes (built-in) | Can be added |
| Graph persistence | Yes | Yes (pickle) |
| Scriptable | No | Yes |

## Troubleshooting

**"Error: Index not found"**
- Run `python index_brain.py` first

**"ModuleNotFoundError"**
- Activate venv: `source venv/bin/activate`

**Slow search**
- Model loads on each query (~1s). For batch queries, use Python API directly.

**Memory issues**
- FAISS IndexFlatIP loads full index to memory. For very large vaults (10k+ notes), consider IndexIVF.
