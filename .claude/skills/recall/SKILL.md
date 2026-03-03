---
name: recall
description: Retrieve relevant knowledge from Obsidian vault using 3-layer semantic search based on conversation context
argument-hint: <search query or topic>
allowed-tools: Read, Bash, Grep, mcp__qmd__qmd_deep_search, mcp__qmd__qmd_get
---

# Semantic Knowledge Retrieval

You are tasked with retrieving relevant knowledge from the Obsidian vault using multi-layer search combining qmd hybrid search and graph analytics.

## Search Tools

### qmd Search (for finding notes by topic)
- `qmd_deep_search` - Hybrid search with BM25 + vector + reranking (primary search tool)
- `qmd_get` - Retrieve full document content by path

### Graph Analytics (for connections and topology)
```bash
# Find connections for a specific note
resources/local-brain-search/run_connections.sh "Note Name" --json

# Find hub notes (most connected)
resources/local-brain-search/run_connections.sh --hubs --json
```

## Search Query
$ARGUMENTS

## Instructions

1. **First Layer - Initial Search**:
   - Call `qmd_deep_search` with query "$ARGUMENTS", collection "brain", limit 5
   - Use `Read` tool to read the full content of the top 2 results

2. **Second Layer - Direct Associations**:
   - For the top result from layer 1, get graph connections:
     ```bash
     resources/local-brain-search/run_connections.sh "Top Result Note" --json
     ```
   - Use `Read` tool to read the full content of the top 2 connected notes

3. **Third Layer - Extended Network**:
   - For additional context, check hub notes:
     ```bash
     resources/local-brain-search/run_connections.sh --hubs --json
     ```
   - This reveals deeper conceptual connections

## Output Format

Present the findings in this structured format:

```markdown
# Knowledge Recall: [Query Topic]

## Layer 1: Direct Matches
[List notes found with relevance scores and key excerpts]

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
- Focus on quality over quantity
- Highlight unexpected connections
- Provide enough context for the user to understand the relevance
- If search returns no results, try broader terms or related concepts

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | Search permanent notes, sources, MOCs |
| qmd index | `~/.cache/qmd/index.sqlite` | X | | Hybrid search index |
| FAISS graph | `resources/local-brain-search/data/` | X | | Graph for connections and hubs |

## Completion Checklist

- [ ] Layer 1 qmd search executed and top results read
- [ ] Layer 2 graph connections retrieved for top result
- [ ] Layer 3 hub notes checked for context
- [ ] Key insights synthesized from findings
- [ ] Relevant excerpts included in output
