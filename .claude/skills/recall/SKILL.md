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
BRAIN_READ_SCOPE=@lookup resources/local-brain-search/run_search.sh "query" --limit 10 --json

# Spreading activation search (follows graph connections)
BRAIN_READ_SCOPE=@lookup resources/local-brain-search/run_search.sh "query" --mode spreading --limit 10 --json

# Find connections
BRAIN_READ_SCOPE=@lookup resources/local-brain-search/run_connections.sh "Note Name" --json

# Find hubs
resources/local-brain-search/run_connections.sh --hubs --json
```

## Search Query
$ARGUMENTS

## Step 0 — Who is asking, and is there anything to search?

- **Agent mode** — another agent asked (an agent-to-agent call, an MCP or API trigger, a scheduled or headless run, or no person in the chat). Run Layer 1 only and answer in the short form under **Output Format** below. Never ask a question.
- **Person mode** — a person is in the chat: the three layers and the full format below are unchanged.

Check the brain before searching:
```bash
INDEX=resources/local-brain-search/data/brain.faiss
# real notes only: skip READMEs, changelogs, indexes, templates and _SAMPLE files
NOTES=$(find Brain -name '*.md' ! -name 'README.md' ! -name 'CHANGELOG.md' ! -name '*INDEX*.md' \
  ! -name '_*' ! -path '*/Templates/*' 2>/dev/null | head -1)
[ -f "$INDEX" ] && [ -n "$NOTES" ] || echo "EMPTY"
```
`EMPTY` (a fresh brain: no notes, or the index not built yet) → answer `nothing on record for "<topic>"` and stop; add `(search index not built yet)` when notes exist but the index does not. This is the answer, not an error. The same line answers a search that returns no results after the thin-read retry. If notes and an index exist but the search itself fails, say `search unavailable: <one line>` - never claim "nothing on record" for a brain you could not read.

## Instructions

**Read role: lookup** (contract: `scope-mount`, decided 2026-09-04): every search and neighbourhood call runs at the reasoning mount `@lookup`, so recall answers "what do I *know* about X", and the output is **grouped by scope** so "what do I *think* about X" stays legible (the core group). Run the `scope-mount` trigger check on the query first; a hit appends `,company` / `,thinkers` / `,Books/<slug>` for this run. `--scope core` (or "only my notes") pins the read to `core`; `--hubs` stays `core` always (fingerprint).

1. **First Layer - Initial Search**:
   - Use spreading activation for better context:
     ```bash
     BRAIN_READ_SCOPE=@lookup resources/local-brain-search/run_search.sh "$ARGUMENTS" --mode spreading --limit 5 --json
     ```
   - Use `Read` tool to read the full content of the top 2 results

2. **Second Layer - Direct Associations**:
   - For the top result from layer 1, get connections:
     ```bash
     BRAIN_READ_SCOPE=@lookup resources/local-brain-search/run_connections.sh "Top Result Note" --json
     ```
   - Use `Read` tool to read the full content of the top 2 connected notes

3. **Third Layer - Extended Network**:
   - For additional context, check hub notes and bridges:
     ```bash
     resources/local-brain-search/run_connections.sh --hubs --json
     ```
   - This reveals deeper conceptual connections

## Output Format

**Agent mode — the short form** (a few lines, no headings):
```text
recall: <topic>
- <one-line finding> [<path from the repo root>] (<your thinking | read, not endorsed | record>)
- ...
sources: <the notes read, paths from the repo root>
```
or the single line `nothing on record for "<topic>"`. At most 5 findings. Material the user has read but not endorsed is labelled as read, never as their view. The label is the result's own `source_kind` field (`your thinking` · `read, not endorsed` · `record`).

**Person mode** — present the findings in this structured format:

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
- If search returns fewer than 3 results, apply the `scope-mount` thin-read rule (re-run at `--threshold 0.3`), then try broader terms or related concepts

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | Search permanent notes, sources, MOCs |
| Local Brain Search index | `resources/local-brain-search/` | X | | Vector index for semantic search |
| Memory config | `resources/local-brain-search/memory_config.py` | X | | Tunable memory parameters |

## Completion Checklist

- [ ] Step 0 done: agent vs person mode decided; empty brain answered `nothing on record`
- [ ] Layer 1 search executed (spreading mode for synthesis queries)
- [ ] Layer 2 connections retrieved for top result (person mode)
- [ ] Layer 3 hub notes checked for context (person mode)
- [ ] Key insights synthesized from findings
- [ ] Relevant excerpts included in output
