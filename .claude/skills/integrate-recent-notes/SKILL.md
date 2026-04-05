---
name: integrate-recent-notes
description: Find notes created in the last 14 days and discover their connections to the knowledge base
automation: autonomous
schedule: "0 19 1,15 * *"
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Integrate Recent Notes

Find recently created notes and map their connections to the existing knowledge base.

## Purpose

New notes often sit unconnected. This playbook identifies notes from the last 14 days and discovers how they integrate with existing knowledge.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Permanent Notes | `Brain/02-Permanent/` | ✓ | | Recent notes source |
| AI Extracted Notes | `Brain/AI Extracted Notes/` | ✓ | | Recent notes source |
| Document Insights | `Brain/Document Insights/` | ✓ | | Recent notes source |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Connection discovery |
| Session Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Integration report |

## Prerequisites

- Local Brain Search index up-to-date (`/refresh-index`)

## Process

### Step 1: Find Recent Notes

Find notes modified in the last 14 days:

```bash
find Brain/02-Permanent -name "*.md" -mtime -14 -type f
find Brain/AI\ Extracted\ Notes -name "*.md" -mtime -14 -type f
find Brain/Document\ Insights -name "*.md" -mtime -14 -type f
```

Compile list of recent notes.

### Step 2: Get Current Date

```bash
date '+%Y-%m-%d'
```

### Step 3: Analyze Connections for Each

For each recent note:

1. Extract note title from filename
2. Run connection discovery:
   ```bash
   resources/local-brain-search/run_connections.sh "Note Title" --json
   ```
3. Record top 5 connections with similarity scores
4. Check BDG layer classification:
   ```bash
   resources/brain-graph/run_brain_graph.sh inspect "Note Title" --json
   ```

### Step 4: Identify Integration Opportunities

For each note, categorize:

- **Well-connected** (3+ connections > 0.70): Already integrated
- **Partially connected** (1-2 connections > 0.70): Needs attention
- **Isolated** (0 connections > 0.70): Priority for integration

### Step 5: Create Integration Report

Write to `Brain/05-Meta/Changelogs/CHANGELOG - Note Integration YYYY-MM-DD.md`:

```markdown
## Note Integration Report: YYYY-MM-DD

### Recent Notes Analyzed
Total: [N] notes from last 14 days

### Integration Status

**Well-Connected** ([N]):
- [[Note A]] - 5 connections

**Partially Connected** ([N]):
- [[Note B]] - 2 connections
  - Suggested: Link to [[X]], [[Y]]

**Isolated - Priority** ([N]):
- [[Note C]] - 0 connections
  - Top semantic matches: [[X]] (0.65), [[Y]] (0.62)
  - Integration suggestion: [brief recommendation]

### Suggested Actions
1. [specific linking recommendations]
2. [synthesis opportunities]
```

## Outputs

- Integration report in `Brain/05-Meta/Changelogs/`
- List of isolated notes needing attention
- Suggested connections for each

## Error Handling

| Error | Recovery |
|-------|----------|
| No recent notes | Log "no notes in period" and exit |
| Connection search fails | Note error, continue with next note |
| Index outdated | Run `/refresh-index` first |

## Completion Checklist

- [ ] Recent notes identified (last 14 days)
- [ ] Connections analyzed for each note
- [ ] Notes categorized (well-connected, partial, isolated)
- [ ] Integration suggestions provided for isolated notes
- [ ] Report created in `Brain/05-Meta/Changelogs/`
