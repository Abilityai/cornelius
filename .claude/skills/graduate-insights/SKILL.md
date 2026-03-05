---
name: graduate-insights
description: Review and graduate notes to permanent status using Zettelkasten principles. Consolidates AI extractions and document insights into curated permanent notes.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Task]
user-invocable: true
---

# Graduate Insights

Review candidate notes from holding areas and promote valuable ones to permanent note status following Zettelkasten principles.

## Purpose

The knowledge base accumulates insights in multiple holding areas:
- **AI Extracted Notes/** - Personal insights from conversations (177 notes)
- **Document Insights/** - Research findings from external sources (1,608 notes across 89 sessions)
- **00-Inbox/** - Raw captures and staging notes (27 notes)

Without periodic graduation, these insights remain unintegrated. This skill provides a structured review process to:
1. Surface high-value candidates based on retrieval frequency and age
2. Present each for human judgment (the essential step)
3. Graduate worthy notes to `02-Permanent/` with proper formatting
4. Maintain knowledge graph integrity

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Q-values | `resources/local-brain-search/data/q_values.json` | Yes | No |
| AI Extracted | `Brain/AI Extracted Notes/` | Yes | Move |
| Document Insights | `Brain/Document Insights/*/` | Yes | Move |
| Inbox | `Brain/00-Inbox/` | Yes | Move |
| Permanent Notes | `Brain/02-Permanent/` | No | Yes |
| Changelog | `Brain/CHANGELOG.md` | Yes | Yes |

## Process

### Step 1: Load State and Find Candidates

```bash
# Get Q-values for retrieval frequency signals
cat resources/local-brain-search/data/q_values.json
```

Find candidate notes prioritized by:
1. **Q-value > 0** - Notes that have been retrieved and used
2. **Age > 14 days** - Notes that have had time to prove value
3. **Has connections** - Notes with wiki-links to permanent notes

Collect up to **5 candidates** per session from:
- `Brain/AI Extracted Notes/*.md`
- `Brain/Document Insights/**/*.md` (exclude CHANGELOG files)
- `Brain/00-Inbox/*.md`

### Step 2: For Each Candidate

Present the following information:

```
## Candidate [N/5]: [Note Title]

**Source:** AI Extracted Notes | Document Insights ([Session Name]) | Inbox
**Created:** [date from frontmatter or file mtime]
**Age:** [X days]
**Q-Value:** [value or "not tracked"]

### Content Preview
[First 500 characters of note content]

### Existing Connections
[List wiki-links found in the note, indicate which link to permanent notes]

### Semantic Neighbors (if available)
[Run quick search to show 3 most similar permanent notes]
```

Ask user:

**Decision for "[Note Title]":**
1. **Promote** - Graduate to permanent notes
2. **Skip** - Review again later (note stays in place)
3. **Delete** - Remove entirely (rare, for duplicates/errors)

### Step 3: Handle Promotion

When user chooses **Promote**:

1. **Check for duplicates** in `02-Permanent/`:
   ```bash
   # Search for similar titles
   grep -r "similar keywords" Brain/02-Permanent/
   ```

2. **Prepare note for graduation**:
   - Ensure frontmatter includes:
     ```yaml
     ---
     created: [original date]
     updated: [today]
     created_by: [original model if present]
     updated_by: [current model]
     agent_version: 01.25
     graduated_from: [original path]
     graduated_date: [today]
     ---
     ```
   - Verify atomic insight format (single clear idea)
   - Ensure wiki-links use `[[Note Title]]` format
   - Remove source-specific metadata (session info, extraction date)

3. **Optionally refine**:
   Ask user: "Refine title/content before promoting? (or press Enter to keep as-is)"

4. **Move to permanent**:
   - Generate clean filename: `Brain/02-Permanent/[Title].md`
   - Move file (not copy - maintains git history)
   - Verify move succeeded

### Step 4: Handle Skip

Note remains in original location. No action needed.

### Step 5: Handle Delete

Confirm before deleting:
```
Are you sure you want to DELETE "[Note Title]"?
This cannot be undone. Type 'yes' to confirm.
```

If confirmed, remove file.

### Step 6: Session Summary

After processing all candidates:

```
## Graduation Session Complete

**Reviewed:** 5 notes
**Promoted:** X notes
**Skipped:** Y notes
**Deleted:** Z notes

### Promoted Notes:
- [[New Permanent Note 1]] (from AI Extracted Notes)
- [[New Permanent Note 2]] (from Document Insights/Session Name)

### Remaining Candidates
- AI Extracted Notes: [count] notes
- Document Insights: [count] notes
- Inbox: [count] notes

Run `/graduate-insights` again to continue review.
```

### Step 7: Update Changelog

Append to `Brain/CHANGELOG.md`:

```markdown
## [DATE] - Insight Graduation Session

**Promoted to Permanent:**
- [[Note 1]] - graduated from AI Extracted Notes
- [[Note 2]] - graduated from Document Insights/[Session]

**Session Stats:** Reviewed 5, Promoted X, Skipped Y
```

## Zettelkasten Graduation Criteria

When reviewing candidates, consider these principles:

### Promote If:
- **Atomic** - Contains ONE clear idea (not a list or summary)
- **Evergreen** - Will remain true/relevant over time
- **Connected** - Links meaningfully to existing permanent notes
- **Original** - Adds unique perspective not already captured
- **Actionable** - Can inform thinking or decisions

### Skip If:
- **Ephemeral** - Time-sensitive or will become outdated
- **Compound** - Contains multiple ideas (may need splitting)
- **Duplicate** - Similar insight exists in permanent notes
- **Unripe** - Not yet clear how it connects or matters

### Delete If:
- **Exact duplicate** - Same content exists elsewhere
- **Error** - Extraction mistake or corrupted content
- **Obsolete** - Information proven wrong or superseded

## Outputs

1. Promoted notes in `Brain/02-Permanent/` with graduation metadata
2. Updated `Brain/CHANGELOG.md` with session record
3. Session summary showing graduation statistics

## Notes

- **Human judgment is essential** - This skill surfaces candidates, humans decide
- **No automated promotion** - Every graduation requires explicit approval
- **Batch size is 5** - Keeps sessions focused and completable
- **Priority by Q-value** - Notes that have been retrieved rank higher
- **Recommend weekly cadence** - Prevents backlog accumulation

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could error handling, step ordering, or instructions be clearer?
- [ ] **Scope check**: Only tactical/execution changes - NOT changes to core purpose or goals
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control** (if in a git repository):
  - [ ] Stage: `git add .claude/skills/graduate-insights/SKILL.md`
  - [ ] Commit: `git commit -m "refactor(graduate-insights): <brief improvement description>"`
