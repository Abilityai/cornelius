---
name: git-commit-push
description: Stage, commit, and push changes to remote repository with approval gate
automation: gated
allowed-tools: [Bash, AskUserQuestion]
user-invocable: true
---

# Git Commit and Push

Commit and push changes to the remote repository. Shows diff for approval before committing.

## Purpose

Safely commit and push all staged and unstaged changes to the remote repository. Presents changes for review before committing to prevent accidental commits.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Git status | `.git/` | X | | Current repo state |
| Working directory | `./` | X | | Modified files |
| Remote repository | origin | | X | Push destination |

## Prerequisites

- Git repository initialized
- Remote origin configured
- Changes to commit (untracked or modified files)

## Process

### Step 1: Check Repository State

```bash
# Show current branch
git branch --show-current

# Check if there are changes to commit
git status --short
```

If no changes, inform user and exit.

### Step 2: Review Changes (APPROVAL GATE)

Present the changes for review:

```bash
# Show summary of changes
git status

# Show detailed diff of modified files (not untracked)
git diff

# Show staged changes if any
git diff --cached
```

**Ask user**:
1. Show the list of files that will be committed
2. Ask for commit message (suggest based on changes)
3. Confirm before proceeding

Use AskUserQuestion with options:
- "Commit all changes" (Recommended)
- "Select specific files"
- "Cancel"

### Step 3: Stage and Commit

Based on user choice:

**If "Commit all changes":**
```bash
# Stage all changes
git add -A

# Commit with user-provided message
git commit -m "$(cat <<'EOF'
[commit message here]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

**If "Select specific files":**
- Ask which files to stage
- Stage only those files
- Commit

### Step 4: Push to Remote

```bash
# Push to current branch's upstream
git push

# If no upstream, push with -u flag
git push -u origin $(git branch --show-current)
```

### Step 5: Verify

```bash
# Confirm push succeeded
git log --oneline -1

# Show remote status
git status
```

## Completion Checklist

- [ ] Repository state checked
- [ ] Changes reviewed by user
- [ ] Commit message approved
- [ ] Changes committed
- [ ] Pushed to remote
- [ ] Push verified

## Error Recovery

| Error | Recovery |
|-------|----------|
| No changes to commit | Inform user, exit gracefully |
| No remote configured | Ask user to configure: `git remote add origin <url>` |
| Push rejected (non-fast-forward) | Suggest `git pull --rebase` first |
| Authentication failed | Check SSH keys or credentials |
| Branch protection | Inform user, suggest PR workflow |

## Usage Examples

**Basic usage:**
```
/git-commit-push
```

**After a work session:**
```
User: commit and push my changes
Agent: [runs this skill]
```

## Notes

- Always shows diff before committing (safety gate)
- Adds Co-Authored-By trailer for AI contributions
- Does NOT use `--force` push (safety)
- Does NOT amend existing commits (safety)
