---
name: scheduled-run
description: Wrapper for scheduled playbooks - handles git sync before and after execution
argument-hint: <playbook-name>
automation: autonomous
allowed-tools: Bash, Skill
---

# Scheduled Run

Wrapper that runs any playbook with git sync. Use this for all scheduled executions to ensure:
- Latest changes pulled before running
- All changes committed and pushed after running

## Purpose

Ensures scheduled playbooks on Trinity stay in sync with the GitHub repository.

## Arguments

`$ARGUMENTS` = The playbook name to run (e.g., `auto-discovery`, `analyze-kb`)

## Process

### Step 1: Pull Latest Changes

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius && git pull --rebase
```

If conflicts, abort and log error.

### Step 2: Run the Playbook

Invoke the specified playbook using the Skill tool:

```
Skill: $ARGUMENTS
```

Wait for completion.

### Step 3: Check for Changes

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius && git status --porcelain
```

If no changes, skip to completion.

### Step 4: Commit Changes

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius && git add -A && git commit -m "$(cat <<'EOF'
Scheduled: $ARGUMENTS $(date '+%Y-%m-%d %H:%M')

Automated execution via /scheduled-run

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 5: Push to Remote

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius && git push
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Pull fails (conflicts) | Abort, log error, do not run playbook |
| Playbook fails | Still attempt commit/push of partial changes |
| Push fails | Log error, changes remain local |

## Usage

**Schedule format:**
```
Daily 5am → /scheduled-run refresh-index
Sunday 8pm → /scheduled-run auto-discovery
Sunday 10pm → /scheduled-run analyze-kb
1st & 15th → /scheduled-run integrate-recent-notes
```

## Completion Checklist

- [ ] Git pull completed successfully
- [ ] Playbook executed
- [ ] Changes detected and committed (if any)
- [ ] Changes pushed to remote
