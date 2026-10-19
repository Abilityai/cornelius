---
name: search-vault
description: Quick search across Obsidian vault using keywords or semantic similarity
automation: autonomous
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
   BRAIN_READ_SCOPE=core,Books,document-insights resources/local-brain-search/run_search.sh "$ARGUMENTS" --limit 5 --json

   # For finding connections, use spreading mode
   BRAIN_READ_SCOPE=core,Books,document-insights resources/local-brain-search/run_search.sh "$ARGUMENTS" --mode spreading --limit 5 --json
   ```
   **Read role: lookup** (contract: `scope-mount`): the reasoning mount, output grouped as *your thinking* (core) · *what you have read* (Books / Document Insights) · *records* (a reference scope, only if a trigger mounted it); `--scope core` pins to your own notes.

2. **Keyword Search** - Search only the same read scope as semantic search.
   Run from the repository root, using the same `BRAIN_PATH` and
   `BRAIN_READ_SCOPE` environment for both searches. Select the mount through
   the `scope-mount` lookup contract above; translate a user `--scope` request
   into that environment for every command rather than passing it to the search
   wrapper. An unset engine environment defaults to core, not the playbook's
   reasoning mount. Set the chosen scope explicitly for the enumeration too. Unknown
   scope names do not mean "all"; use the names in `memory_config.py`.

   First list eligible note paths using the existing scope API:

   ```bash
   python3 - <<'PY'
   import json
   import sys

   sys.path.insert(0, "resources/local-brain-search")
   from memory_config import BRAIN_PATH, in_read_scope, resolve_read_scope

   read_scope = resolve_read_scope()
   if not BRAIN_PATH.is_dir():
       raise SystemExit(f"Vault not found: {BRAIN_PATH}")
   paths = [str(path) for path in sorted(BRAIN_PATH.rglob("*.md"))
            if not path.is_symlink() and path.is_file()
            and in_read_scope(path.relative_to(BRAIN_PATH).as_posix(), read_scope)]
   print(json.dumps(paths, ensure_ascii=False, indent=2))
   PY
   ```

   Note symlinks are excluded, even when their targets are in scope. The
   recursive enumeration does not descend into directory symlinks; a symlink
   used as the configured vault root is supported. Do not resolve an excluded
   alias and treat that alias as eligible. This is a current-filesystem read
   guard, not a validation of content already stored in the semantic index.

   Then use `Grep` only on those exact file paths:
   - Pattern: supplied $ARGUMENTS, passed as data rather than shell code
   - Path: each eligible file, never the whole `Brain/` directory
   - Output mode: "files_with_matches" to get the matching file list
   - Then use output mode: "content" with -C flag for context
   - An empty eligible list means no keyword matches; do not broaden the scope

   Report invalid patterns, unreadable files or missing vaults as errors; do
   not substitute a whole-vault search. Scope filtering controls retrieval,
   not filesystem permissions.

3. **Retrieve Content** - For the top result from semantic search:
   - Use `Read` tool to get full content

## Output Format

```markdown
# Search Results: "$ARGUMENTS"

## Semantic Matches
[Top 5 notes with similarity/activation scores]

## Keyword Matches
[Top 5 notes with context snippets]

## Top Result Content
[Full content of the most relevant note]
```

Keep results concise and actionable. Highlight the most relevant findings.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | Notes in the selected read scope |
| Local Brain Search index | `resources/local-brain-search/` | X | | Vector index for semantic search |
| Memory config | `resources/local-brain-search/memory_config.py` | X | | Tunable memory parameters |

## Completion Checklist

- [ ] Semantic search executed with top 5 results
- [ ] Keyword search executed with file matches
- [ ] Top result full content retrieved and displayed
- [ ] Results formatted and highlighted
