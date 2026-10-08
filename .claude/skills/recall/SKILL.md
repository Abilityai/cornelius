---
name: recall
description: Retrieve relevant knowledge from Obsidian vault using 3-layer semantic search based on conversation context
automation: autonomous
argument-hint: <search query or topic>
allowed-tools: Read, Bash, Grep
---

# Semantic Knowledge Retrieval

You are tasked with retrieving relevant knowledge from the Obsidian vault using multi-layer semantic search.

## Local Brain Search

Use Local Brain Search for all semantic search operations. **Spreading activation mode recommended for synthesis queries.**

**Scripts:**
```bash
# Static search (fast, exact matches)
BRAIN_READ_SCOPE=core,Books,document-insights resources/local-brain-search/run_search.sh "query" --limit 10 --json

# Spreading activation search (follows graph connections)
BRAIN_READ_SCOPE=core,Books,document-insights resources/local-brain-search/run_search.sh "query" --mode spreading --limit 10 --json

# Find connections
BRAIN_READ_SCOPE=core,Books,document-insights resources/local-brain-search/run_connections.sh "Note Name" --json

# Find hubs
resources/local-brain-search/run_connections.sh --hubs --json
```

## Search Query
$ARGUMENTS

## Instructions

**Read role: lookup** (contract: `scope-mount`, decided 2026-09-04): every search and neighbourhood call runs at the reasoning mount `core,Books,document-insights`, so recall answers "what do I *know* about X", and the output is **grouped by scope** so "what do I *think* about X" stays legible (the core group). Run the `scope-mount` trigger check on the query first; a hit appends `,company` / `,thinkers` / `,Books/<slug>` for this run. `--scope core` (or "only my notes") pins the read to `core`; `--hubs` stays `core` always (fingerprint).

1. **First Layer - Initial Search**:
   - Use spreading activation for better context:
     ```bash
     BRAIN_READ_SCOPE=core,Books,document-insights resources/local-brain-search/run_search.sh "$ARGUMENTS" --mode spreading --limit 5 --json
     ```
   - Use `Read` tool to read the full content of the top 2 results

2. **Second Layer - Direct Associations**:
   - For the top result from layer 1, get connections:
     ```bash
     BRAIN_READ_SCOPE=core,Books,document-insights resources/local-brain-search/run_connections.sh "Top Result Note" --json
     ```
   - Use `Read` tool to read the full content of the top 2 connected notes

3. **Third Layer - Extended Network**:
   - For additional context, check hub notes and bridges:
     ```bash
     resources/local-brain-search/run_connections.sh --hubs --json
     ```
   - This reveals deeper conceptual connections

## Output Format

Present the findings in this structured format:

```markdown
# Knowledge Recall: [Query Topic]

## Layer 1: Direct Matches
### Your thinking (core: 02-Permanent · 03-MOCs · AI Extracted Notes · 01-Sources)
[notes found, with key excerpts]
### What you have read (Books · Document Insights) - encountered, not endorsed
[notes found, with key excerpts - never presented as "your view"]
### Records (Company · Canon · Thinkers) - only when a trigger mounted them
[facts, `provenance: reference`]

## Layer 2: First-Degree Associations
[List connected notes with their relationships and excerpts]

## Layer 3: Extended Network
[Show hub notes and bridge connections]

## Key Insights
[Synthesize the main themes and connections discovered]

## Relevant Content
[Include the most pertinent excerpts from the retrieved notes]
```

## Important Notes
- Use `--mode spreading` for synthesis and connection-finding queries
- Use static mode for exact factual lookups
- Focus on quality over quantity
- Highlight unexpected connections
- Provide enough context for the user to understand the relevance
- If search returns no results, try broader terms or related concepts
- **Learning active**: Searches are tracked and rankings improve over time based on usage

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | Search permanent notes, sources, MOCs |
| Local Brain Search index | `resources/local-brain-search/` | X | | Vector index for semantic search |
| Memory config | `resources/local-brain-search/memory_config.py` | X | | Tunable memory parameters |

## Completion Checklist

- [ ] Layer 1 search executed (spreading mode for synthesis queries)
- [ ] Layer 2 connections retrieved for top result
- [ ] Layer 3 hub notes checked for context
- [ ] Key insights synthesized from findings
- [ ] Relevant excerpts included in output
