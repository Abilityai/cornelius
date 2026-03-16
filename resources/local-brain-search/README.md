# Local Brain Search

Local vector search and connection discovery for the Brain folder with **SYNAPSE-inspired spreading activation**.

**Tech Stack:** FAISS + sentence-transformers + NetworkX

## Features

- **Semantic search** - Find notes by meaning, not just keywords
- **Spreading activation** - SYNAPSE-inspired memory retrieval that follows graph connections
- **Intent classification** - Automatically adapts search based on query type
- **Connection graph** - Discover explicit links AND semantic relationships
- **Hub detection** - Find most connected notes
- **Bridge detection** - Find notes connecting different topics
- **Lateral inhibition** - Prevents hub dominance in results
- **Fully local** - No cloud APIs, all data stays on your machine

## Current Stats (Feb 2026)

```
Notes indexed: 1531
Graph edges: 10,870
  - Explicit (wiki-links): 5,983
  - Semantic (similarity): 4,887
```

## Quick Start

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Basic search (static mode)
./run_search.sh "dopamine and motivation"

# Spreading activation search (recommended)
./run_search.sh "connect Buddhism and neuroscience" --mode spreading

# Force specific intent
./run_search.sh "recent AI agent notes" --mode spreading --intent temporal

# JSON output
./run_search.sh "query" --mode spreading --json
```

## Search Modes

### Static Mode (default)
Traditional vector similarity search. Fast, good for exact lookups.

```bash
./run_search.sh "dopamine" --mode static
```

### Spreading Mode (SYNAPSE-inspired)
Propagates activation through the graph, finding contextually relevant notes.

```bash
./run_search.sh "relationship between identity and belief" --mode spreading
```

**When to use spreading mode:**
- Finding cross-domain connections
- Synthesis and pattern discovery
- Exploring conceptual neighborhoods
- Avoiding "contextual tunneling" (topically similar but contextually wrong results)

## Intent Classification

Queries are automatically classified into four types:

| Intent | Description | Search Behavior |
|--------|-------------|-----------------|
| **factual** | Looking for specific info | Minimal spreading (2 iterations) |
| **conceptual** | Exploring a topic | Broad spreading (5 iterations) |
| **synthesis** | Finding connections | Maximum spreading (7 iterations) |
| **temporal** | Recent/historical focus | Time-weighted search |

Override with `--intent`:
```bash
./run_search.sh "dopamine" --mode spreading --intent synthesis
```

## Configuration

**All memory parameters in one file:** `memory_config.py`

Key tunable parameters:
```python
MEMORY_CONFIG = {
    "spreading": {
        "max_iterations": 5,
        "temporal_decay": 0.9,
        "inhibition_strength": 0.3,
        "decay_factors": {
            "explicit": 0.8,  # Wiki-links
            "semantic": 0.5,  # Similarity edges
        },
    },
    "search": {
        "default_threshold": 0.5,
        "default_mode": "static",  # Change to "spreading" for default
    },
}
```

## Setup

```bash
# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Index the Brain folder
python index_brain.py

# Re-index after vault changes
python index_brain.py --force
```

## Data Storage

```
data/
├── brain.faiss        # FAISS vector index
├── brain_metadata.pkl # Chunk metadata
└── brain_graph.pkl    # NetworkX graph
```

## Implementation Status

Based on [UPGRADE-REQUIREMENTS.md](UPGRADE-REQUIREMENTS.md):

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Intent Classification | ✅ Complete |
| 2 | Extended Graph (temporal/causal edges) | ⏳ Not started |
| 3 | Spreading Activation | ✅ Complete |
| 4 | Usage-Based Learning | ✅ Complete |
| 5 | Foresight Signals | ⏳ Not started |

## Research Foundation

- SYNAPSE (arXiv:2601.02744) - Spreading activation for LLM memory
- SimpleMem (arXiv:2601.02553) - Intent-aware retrieval
- Collins & Loftus (1975) - Original spreading activation theory
