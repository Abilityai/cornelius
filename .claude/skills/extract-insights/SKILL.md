---
name: extract-insights
description: Extract unique insights and perspectives from personal content (conversations, transcripts, notes). Spawns insight-extractor subagent.
allowed-tools: [Task]
user-invocable: true
arg-description: "<file path or content description>"
---

# Extract Insights

Extract unique insights, original thinking, and distinctive perspectives from YOUR content.

## Purpose

User-invocable wrapper that spawns the `insight-extractor` subagent to:
- Extract personal theories, contrarian views, synthesis insights
- Preserve authentic voice and reasoning patterns
- Handle large files via chunking
- Deduplicate against existing knowledge base
- Save to `Brain/AI Extracted Notes/`

## When to Use

- Extracting insights from YOUR conversations, transcripts, journals
- Processing personal notes or reflections
- Capturing your unique perspectives from recorded content

**NOT for external research** - use `/extract-document-insights` for papers, books, articles.

## Usage

```
/extract-insights /path/to/transcript.md
/extract-insights "the conversation above about dopamine"
```

## Process

1. **Parse arguments** to identify source content
2. **Spawn insight-extractor subagent** in a fresh context. In Codex, follow the native delegation procedure in `docs/CODEX.md`: pass the source as data, require the child to read `.claude/agents/insight-extractor.md` and the shared rules, preserve `core,document-insights` duplicate checks, and wait for completion. If native delegation is unavailable, report `DELEGATION_UNAVAILABLE` without creating notes or switching runtimes. In Claude Code, use the Task tool with:
   ```
   Task(
     subagent_type="insight-extractor",
     prompt="Extract insights from: [source]. Follow your mandatory workflow - contextualize, search for duplicates, extract, create notes, update changelog."
   )
   ```
3. **Report results** - number of insights extracted, notes created

## Outputs

- Permanent notes in `Brain/AI Extracted Notes/`
- Session changelog in `Brain/05-Meta/Changelogs/`
- Summary of extracted insights
