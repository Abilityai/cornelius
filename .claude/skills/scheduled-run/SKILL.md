---
name: scheduled-run
description: Wrapper for scheduled playbooks - handles git sync before and after execution
argument-hint: <playbook-name>
automation: autonomous
allowed-tools: Bash, Skill
user-invocable: true
---

# Scheduled Run

Wrapper that runs any playbook with git sync. Use this for all scheduled executions to ensure:
- Latest changes pulled before running
- All changes committed and pushed after running

## Purpose

Ensures scheduled playbooks on Trinity stay in sync with the GitHub repository.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Git repo | `.git/` | ✓ | ✓ | Pull before, commit+push after |
| Playbook output | varies | | ✓ | Whatever the playbook produces |

## Arguments

`$ARGUMENTS` = The playbook name to run (e.g., `refresh-index`, `coherence-sweep`)

## Process

### Step 1: Pull Latest Changes

```bash
git pull --rebase
```

If conflicts, abort and log error. Do NOT run the playbook on a dirty tree.

### Step 2: Run the Playbook

Invoke the specified playbook using the Skill tool:

```
Skill: $ARGUMENTS
```

Wait for completion.

### Step 3: Check for Changes

```bash
git status --porcelain
```

If no changes, skip to completion.

### Step 4: Commit Changes

```bash
git add -A && git commit -m "$(cat <<'EOF'
Scheduled: $ARGUMENTS $(date '+%Y-%m-%d %H:%M')

Automated execution via /scheduled-run

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 5: Push to Remote

```bash
git push
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Pull fails (conflicts) | Abort, log error, do not run playbook |
| Playbook fails | Still attempt commit/push of partial changes |
| Push fails | Log error, changes remain local |

## Autonomy Guide

**What should be scheduled (mechanical, no creative decisions):**

| Schedule | Command | Cron | Purpose |
|----------|---------|------|---------|
| Refresh Index | `/scheduled-run refresh-index` | `0 5 * * *` | FAISS + BDG bootstrap (daily) |
| GJ Open Refresh | `/scheduled-run gjopen-refresh` | `0 6 * * *` | External forecasting data (daily) |
| Coherence Sweep | `/scheduled-run coherence-sweep` | `0 6 * * 1` | Weekly Monday report: staleness, health, transitions |

**What should NOT be scheduled (requires human judgment):**

| Skill | Why manual |
|-------|-----------|
| `/auto-discovery` | Generates new connections - that's intellectual work |
| `/deep-research` | Creates new content from external sources |
| `/detect-tensions` | Productive contradictions need human interpretation |
| `/compute-lifecycle` | Promotions to framework status need human decision |
| `/integrate-recent-notes` | Integration choices are creative decisions |
| `/analyze-kb` | Useful on-demand, not worth weekly automation |

**The principle:** Automate measurement and maintenance. Never automate creation or judgment.

The coherence sweep is the one weekly artifact that earns automation - it's a Monday briefing that says "here's what changed, here's what might be stale, here's what's evolving." You glance at it, act on what matters, ignore the rest.

## Completion Checklist

- [ ] Git pull completed successfully
- [ ] Playbook executed
- [ ] Changes detected and committed (if any)
- [ ] Changes pushed to remote
