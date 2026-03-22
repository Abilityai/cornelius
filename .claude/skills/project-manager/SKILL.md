---
name: project-manager
description: Lightweight project management - create, track, update, and archive projects with folder-based structure
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
user-invocable: true
---

# Project Manager

Lightweight, file-based project management. Each project is a folder in `projects/` with a `project.md` file and any related files. Syncs via git between local and remote.

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Projects | `projects/*/project.md` | Yes | Yes |
| Archive | `projects/archive/*/project.md` | Yes | Yes (on archive) |

## Statuses

| Status | Meaning |
|--------|---------|
| `planning` | Scoping, not yet started |
| `active` | In progress |
| `blocked` | Waiting on something specific |
| `on-hold` | Paused intentionally |
| `completed` | Done - ready to archive |
| `cancelled` | Abandoned - ready to archive |

## Priorities

`high` | `medium` | `low`

## Project File Structure

```
projects/
├── project-name/
│   ├── project.md       # Required - status, description, next steps
│   └── ...              # Any related files (research, drafts, data, scripts)
├── another-project/
│   └── project.md
└── archive/             # Completed/cancelled projects
    └── old-project/
        └── project.md
```

## project.md Template

```markdown
---
status: planning
priority: medium
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Project Name

One-paragraph description of what this project is and why it matters.

## Next Steps
- First concrete action
- Second concrete action

## Blockers
- None

## Notes
Context, decisions, links, references.
```

## Commands

Parse the argument to determine which command to run:

### `/project-manager` or `/project-manager list`

Scan all `projects/*/project.md` files (excluding `archive/`). Parse frontmatter from each. Display as table:

```
| Project | Status | Priority | Updated | Next Step |
|---------|--------|----------|---------|-----------|
| treasury-agent | active | high | 2026-03-20 | Design escrow interface |
| moltbook-growth | planning | medium | 2026-03-18 | Analyze top posts |
```

Sort by: priority (high first), then status (active/blocked first), then updated (recent first).

If no projects exist, say so and suggest `/project-manager create <name>`.

### `/project-manager create <name>`

1. Sanitize name to kebab-case (lowercase, hyphens)
2. Check `projects/<name>/` doesn't already exist (check archive too)
3. Create directory: `projects/<name>/`
4. Get today's date via `date '+%Y-%m-%d'`
5. Ask user for:
   - One-line description
   - Initial status (default: `planning`)
   - Priority (default: `medium`)
6. Create `projects/<name>/project.md` from template with provided details
7. Confirm creation

### `/project-manager update <name>`

1. Find project: `projects/<name>/project.md`
   - If not found, list available projects and ask which one
2. Read current project.md
3. Ask user what to update (or infer from conversation context):
   - Status change
   - Priority change
   - Add/remove next steps
   - Add/remove blockers
   - Add notes
4. Edit the file - update frontmatter `updated` date to today
5. Show summary of changes

### `/project-manager archive <name>`

1. Find project: `projects/<name>/`
   - If not found, list available projects
2. Read current status
3. If status is not `completed` or `cancelled`, ask user to confirm and set final status
4. Update `project.md`: set final status, update date
5. Move folder: `mv projects/<name>/ projects/archive/<name>/`
6. Confirm archive

### `/project-manager review`

Full review for session startup or periodic check-in:

1. Run `list` to show all active projects
2. For each project with status `active` or `blocked`:
   - Show full next steps and blockers
   - Flag if `updated` date is older than 7 days (may be stale)
3. Check archive for recently archived projects (last 14 days)
4. Summary: "X active, Y blocked, Z on-hold, W in planning"
5. Ask: "Want to update any project?"

## Error Handling

- **Project not found**: List available projects, suggest closest match
- **Duplicate name**: Warn and suggest alternative name
- **No projects directory**: Create it automatically
- **Malformed frontmatter**: Read what's there, suggest fix

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could error handling, step ordering, or instructions be clearer?
- [ ] **Scope check**: Only tactical/execution changes - NOT changes to core purpose or goals
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control** (if in a git repository):
  - [ ] Stage: `git add .claude/skills/project-manager/SKILL.md`
  - [ ] Commit: `git commit -m "refactor(project-manager): <brief improvement description>"`
