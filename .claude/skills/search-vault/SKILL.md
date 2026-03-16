---
name: search-vault
description: Quick search across Obsidian vault using keywords or semantic similarity
argument-hint: <search query>
allowed-tools: Read, Grep, Bash
---

# Quick Vault Search

Search the Obsidian vault using both semantic and keyword-based search.

## Local Brain Search

Use Local Brain Search for all semantic search operations. Supports two modes:
- **static**: Fast vector similarity (default)
- **spreading**: SYNAPSE-inspired graph traversal (better for connections)

**Note:** Usage-based learning is active - searches are tracked and rankings improve over time.

## Query
$ARGUMENTS

## Instructions

1. **Semantic Search** - Use Local Brain Search:
   ```bash
   # For quick lookups, use static mode
   /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search/run_search.sh "$ARGUMENTS" --limit 5 --json

   # For finding connections, use spreading mode
   /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search/run_search.sh "$ARGUMENTS" --mode spreading --limit 5 --json
   ```

2. **Keyword Search** - Use `Grep`:
   - Pattern: $ARGUMENTS
   - Path: `Brain/`
   - Output mode: "files_with_matches" to get file list
   - Then use output mode: "content" with -C flag for context

3. **Retrieve Content** - For the top result from semantic search:
   - Use `Read` tool to get full content

## Output Format

```markdown
# Search Results: "$ARGUMENTS"

## Semantic Matches
[Top 5 notes with similarity/activation scores]

## Keyword Matches
[Top 5 notes with context snippets from Grep]

## Top Result Content
[Full content of the most relevant note]
```

Keep results concise and actionable. Highlight the most relevant findings.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | All vault notes for search |
| Local Brain Search index | `resources/local-brain-search/` | X | | Vector index for semantic search |
| Memory config | `resources/local-brain-search/memory_config.py` | X | | Tunable memory parameters |

## Completion Checklist

- [ ] Semantic search executed with top 5 results
- [ ] Keyword search executed with file matches
- [ ] Top result full content retrieved and displayed
- [ ] Results formatted and highlighted
