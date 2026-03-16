# Local Brain Search - Quick Reference Guide

**Status:** FULLY OPERATIONAL ✅  
**Index Age:** Fresh (updated Dec 13, 2025)  
**Coverage:** 1261 notes, 7726 chunks, 9300 connections

---

## One-Minute Setup

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search
source venv/bin/activate
```

## Common Commands

### Search
```bash
# Basic search
python search.py "dopamine"

# High-quality results (top 3 above 0.7 similarity)
python search.py "consciousness" --limit 3 --threshold 0.7

# Full content display
python search.py "Buddhism" --full

# Machine-readable JSON output
python search.py "AI agents" --json
```

### Connections
```bash
# Find what a note connects to
python connections.py "Dopamine"

# Only explicit wiki-links
python connections.py "Flow is a selfless state" --explicit-only

# Multi-hop connections (depth 2)
python connections.py "Identity" --depth 2

# Hub notes (most connected)
python connections.py --hubs

# Bridge notes (cross-domain connectors)
python connections.py --bridges

# Graph statistics
python connections.py --stats

# JSON for processing
python connections.py --hubs --json
```

## Real Examples

### Scenario 1: Explore a topic
```bash
# Find notes about dopamine
python search.py "dopamine reward learning" --limit 5

# See what notes connect to the top result
python connections.py "Dopamine"
```

### Scenario 2: Find cross-domain connections
```bash
# See bridge notes connecting different areas
python connections.py --bridges | head -10

# Explore one bridge in detail
python connections.py "MOC - AI and Agents"
```

### Scenario 3: Understand the knowledge graph
```bash
# Overall stats
python connections.py --stats

# Most important hubs
python connections.py --hubs | head -5

# Their incoming connections
python connections.py "Decision Making" --explicit-only
```

### Scenario 4: Batch process results
```bash
# Get JSON results, process with jq
python search.py "consciousness" --json | jq '.[].title'

# Find top bridges and get their details
python connections.py --bridges --json | jq '.[:3]'
```

## Key Concepts

### Similarity Scores
- **70-100%:** Highly relevant, core matches
- **50-70%:** Related, good context
- **<50%:** Tangential, less relevant

### Edge Types
- **[L]** = Explicit link (wiki-link in markdown)
- **[S]** = Semantic edge (computed similarity >0.65)

### Hub vs Bridge
- **Hubs:** Notes with most connections (centrality)
- **Bridges:** Notes connecting different clusters (betweenness)

## The Graph at a Glance

```
1261 notes
├── 97.9% in one main cluster
├── 2.1% isolated (metadata, drafts)
├── 9300 total connections
│   ├── 5201 explicit (wiki-links)
│   └── 4099 semantic (similarity)
└── 14.75 average connections per note
```

## Top 5 Hubs
1. **MOC - AI and Agents** - 184 connections (hub for AI cluster)
2. **Decision Making** - 140 connections (core decision science)
3. **Stumbling on Happiness** - 134 connections (influential source)
4. **Dopamine** - 126 connections (master concept hub)
5. **Superforecasting** - 98 connections (prediction framework)

## Top 5 Bridges
1. **MOC - AI and Agents** - Connects AI to all other domains
2. **The Uncertainty-Dopamine-Belief Loop** - Links domains
3. **Stumbling on Happiness** - Wide cross-domain influence
4. **Decision Making** - Referenced everywhere
5. **Confirmation Bias** - Multi-domain psychological concept

## Performance

| Operation | Time |
|-----------|------|
| First query (cold start) | 3.5 seconds |
| Subsequent queries | 1.0 second |
| Connection lookup | <100ms |
| Graph stats | <50ms |

## Maintenance

### After Adding New Notes
```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search
source venv/bin/activate
python index_brain.py  # Re-index once
```

### Verify Index Health
```bash
python connections.py --stats  # Should show all notes indexed
```

## Tips & Tricks

### Power User Workflows

**1. Find everything about a topic**
```bash
python search.py "attention" --limit 10 --json | jq '.[] | .title'
```

**2. Visualize a note's ecosystem**
```bash
python connections.py "Flow is a selfless state" --depth 2
```

**3. Find what connects two topics**
```bash
# Search both, then check their connections
python search.py "Buddhism" --json | jq '.[0].title'
python search.py "Neuroscience" --json | jq '.[0].title'
# Then check connections between them
```

**4. Export for external tools**
```bash
# Get all hub notes as JSON
python connections.py --hubs --json > hubs.json

# Process with jq or Python
cat hubs.json | jq '.[0:5]'
```

**5. Quality check a search**
```bash
# Low threshold finds everything
python search.py "dopamine" --threshold 0.3

# High threshold finds core matches only
python search.py "dopamine" --threshold 0.8
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Index not found" | Run `python index_brain.py` |
| Empty search results | Lower threshold or try different terms |
| No connections found | Note may be isolated or title exact match failed |
| Slow startup | First query loads model (~3.5s), subsequent queries are fast |
| Stale results | Run `python index_brain.py` to re-index |

## Settings You Can Change

Edit `config.py` to customize:

```python
SEMANTIC_EDGE_THRESHOLD = 0.65  # Higher = fewer edges, more selective
SEMANTIC_EDGE_TOP_K = 5         # Number of semantic edges per note
DEFAULT_SEARCH_LIMIT = 10       # Default results per search
DEFAULT_SIMILARITY_THRESHOLD = 0.5  # Default quality cutoff
```

## Files Generated

```
/Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search/
├── brain.faiss        # Vector index (11.3 MB)
├── brain_metadata.pkl # Chunk metadata (5.7 MB)
├── brain_graph.pkl    # Connection graph (0.7 MB)
└── brain_search       # Results in venv/bin/
```

---

**Last Updated:** December 13, 2025  
**Test Status:** FULLY OPERATIONAL ✅
