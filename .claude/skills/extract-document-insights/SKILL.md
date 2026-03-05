---
name: extract-document-insights
description: Extract insights from external documents (research papers, books, articles). Spawns document-insight-extractor subagent. Requires session name.
allowed-tools: [Task]
user-invocable: true
arg-description: "<session name> <file path or content description>"
---

# Extract Document Insights

Extract insights from EXTERNAL documents with proper epistemic classification.

## Purpose

User-invocable wrapper that spawns the `document-insight-extractor` subagent to:
- Extract research findings, theoretical frameworks, hypotheses
- Classify epistemic status (confirmed, theoretical, speculative)
- Store in session-based folders
- Deduplicate against existing knowledge base
- Save to `Brain/Document Insights/[session]/`

## When to Use

- Analyzing research papers, academic articles
- Processing books or book chapters
- Extracting insights from web articles, reports
- Any EXTERNAL content (not your personal thoughts)

**NOT for personal content** - use `/extract-insights` for your conversations, transcripts.

## Usage

```
/extract-document-insights "2025-02-21 Ancient Wisdom Research" /path/to/document.md
/extract-document-insights "AI Agent Papers" "the transcript above"
```

**Session name is REQUIRED** - describes the research session for organization.

## Process

1. **Parse arguments** to extract session name and source
2. **Spawn document-insight-extractor subagent** via Task tool with:
   ```
   Task(
     subagent_type="document-insight-extractor",
     prompt="Extract insights from: [source] into session '[session-name]'. Follow your mandatory workflow - contextualize, classify epistemically, search duplicates, create notes, update changelog."
   )
   ```
3. **Report results** - number of insights extracted, session folder path

## Outputs

- Insight notes in `Brain/Document Insights/[session]/`
- Session changelog in same folder
- Summary with epistemic breakdown (confirmed vs hypothetical)
