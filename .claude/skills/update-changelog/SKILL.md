---
name: update-changelog
description: Update Knowledge Graph Changelog
---

# Update Knowledge Graph Changelog

You are updating the Brain vault changelog to track recent modifications to the knowledge graph.

## Your Task

1. **Identify Recent Changes** - Review the session history to identify:
   - New notes created
   - New connections/links added between existing notes
   - Significant edits to note content
   - Focus only on changes made during THIS session

2. **Read Existing Changelog** - Read `$VAULT_BASE_PATH/Brain/CHANGELOG.md` to see the current state

3. **Append New Entry** - Add a new dated entry at the TOP of the changelog with:
   - Date and session identifier
   - List of changes in format: `- [ACTION] Note Title: Brief description (→ Connected to: [[Other Note]])`
   - Keep each entry to 1-2 sentences maximum
   - Use action verbs: CREATED, CONNECTED, UPDATED, LINKED

## Format Example

```markdown
## 2025-10-24 - Session [Brief Description]

- CONNECTED [[Psychological Safety]] → [[Flow is impossible without Autonomy]]: Psychological safety creates autonomy prerequisite for flow by removing fear-based constraints.
- CONNECTED [[Radical Ownership]] → [[Flow is impossible without Autonomy]]: True ownership requires autonomy; permission-seeking eliminates both.
- CONNECTED [[Flow is a selfless state]] ↔ [[In Buddhism - Self is an Illusion]]: Flow provides empirical validation of Buddhist insight through performance.
- CONNECTED [[Entrepreneurship is de-risking]] → [[Belief deals with Uncertainty]]: Entrepreneurs hold beliefs about uncertain futures without eliminating uncertainty.
- CONNECTED [[Taking on external obligations]] → [[Radical Ownership]]: Obligations stem from permission-seeking rather than ownership.
```

## Important Guidelines

- Only document changes from THIS session
- Be concise - max 2 sentences per change
- Use bidirectional arrows (↔) for mutual connections, directional (→) for one-way
- Group related changes together
- Focus on WHAT was connected and WHY it matters (the insight)
- If no changelog exists, create it with a header explaining its purpose

## Output

After updating, show the user:
1. Number of changes logged
2. The new entry you added
3. Confirmation that CHANGELOG.md was updated

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Master changelog | `Brain/CHANGELOG.md` | X | X | Main change log to update |
| Session history | Current conversation | X | | Changes made this session |

## Completion Checklist

- [ ] Session changes identified (notes created, connections made, edits)
- [ ] Existing CHANGELOG.md read
- [ ] New dated entry added at TOP of changelog
- [ ] Action verbs used (CREATED, CONNECTED, UPDATED, LINKED)
- [ ] Entries concise (max 2 sentences each)
- [ ] Arrow notation correct (→ for one-way, ↔ for bidirectional)
- [ ] Number of changes reported to user
- [ ] Confirmation provided that CHANGELOG.md was updated
