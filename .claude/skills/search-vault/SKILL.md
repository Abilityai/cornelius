---
name: search-vault
description: Quick search across Obsidian vault using keywords or semantic similarity
argument-hint: <search query>
allowed-tools: Read, Grep, Bash, mcp__qmd__qmd_search, mcp__qmd__qmd_deep_search, mcp__qmd__qmd_get
---

# Quick Vault Search

Search the Obsidian vault using qmd hybrid search (BM25 keyword + vector semantic + LLM reranking).

## Search Tools

### qmd Search (Primary - for finding notes)
Use qmd MCP tools for all search operations:
- `qmd_deep_search` - Hybrid search with reranking (recommended for most queries)
- `qmd_search` - Fast BM25 keyword search (when exact terms matter)
- `qmd_get` - Retrieve full document content by path

### Grep (Supplementary)
Use `Grep` only for structural queries (finding wikilinks, frontmatter fields, specific patterns) - not for general search.

## Query
$ARGUMENTS

## Instructions

1. **Search** - Use qmd hybrid search:
   - Call `qmd_deep_search` with query "$ARGUMENTS", collection "brain", limit 5
   - This combines keyword matching, semantic similarity, and LLM reranking in one call

2. **Retrieve Content** - For the top result:
   - Use `Read` tool to get full content of the highest-scoring note
   - Or use `qmd_get` with the file path from search results

## Output Format

```markdown
# Search Results: "$ARGUMENTS"

## Results
[Top 5 notes with relevance scores and snippets from qmd]

## Top Result Content
[Full content of the most relevant note]
```

Keep results concise and actionable. Highlight the most relevant findings.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | All vault notes for search |
| qmd index | `~/.cache/qmd/index.sqlite` | X | | Hybrid search index |

## Completion Checklist

- [ ] qmd search executed with top 5 results
- [ ] Top result full content retrieved and displayed
- [ ] Results formatted and highlighted
