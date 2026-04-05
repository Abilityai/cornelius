---
name: learn-new-things
description: Continuous learning heartbeat - autonomously researches, extracts insights, and expands knowledge base
user-invocable: true
disable-model-invocation: true
argument-hint: "[interval-hours] [topic]"
automation: gated
allowed-tools: Task, Read, Write, Bash, Glob, Grep
---

# Learn New Things - Continuous Learning Heartbeat

Autonomous learning loop that periodically expands the knowledge base through research, extraction, and connection discovery. Runs locally using existing skills and sub-agents.

## Overview

This heartbeat skill implements a continuous learning cycle:
1. **Research** - Discover cutting-edge papers and developments
2. **Extract** - Pull unique insights into Document Insights
3. **Connect** - Map discoveries to existing knowledge base
4. **Commit** - Save results to dedicated git branch, return to main
5. **Rest** - Wait for next cycle

Each cycle is a complete learning session. The heartbeat never "completes" - it continuously learns.

**Git Workflow:** Each learning session commits to its own branch (`learning/YYYY-MM-DD-topic-slug`), then returns to `main`. This keeps main clean while preserving all learning for selective merging.

## Dependencies

- **Skills**: `/deep-research`, `/auto-discovery`, `/integrate-recent-notes`, `/refresh-index`
- **Sub-agents**: research-specialist, document-insight-extractor, connection-finder
- **Local Brain Search**: For semantic search and connection discovery

## Usage

```bash
/learn-new-things                    # Default: 8-hour interval, auto-select topic
/learn-new-things 4                  # 4-hour interval
/learn-new-things 8 "multi-agent systems"  # Specific topic
/learn-new-things stop               # Stop the learning loop
```

---

## State Tracking

Track learning progress in `resources/learn-new-things-log.md`:

```yaml
session_id: YYYY-MM-DD-HHMMSS
last_cycle: 2026-02-18T13:15:00
cycles_completed: 0
topics_researched: []
insights_extracted: 0
connections_discovered: 0
consecutive_errors: 0
phase: "running"  # running | paused | error
branches_created: []  # e.g., ["learning/2026-02-18-embodied-cognition"]
```

---

## STEP 1: Initialize State

Read or create state file:

```bash
cat resources/learn-new-things-log.md 2>/dev/null || echo "No existing state"
```

Parse arguments:
- `$ARGUMENTS[0]` - Interval in hours (default: 8)
- `$ARGUMENTS[1]` - Optional topic (default: auto-select)

If argument is "stop", set `phase: "paused"` and exit.

---

## STEP 2: Pre-Cycle Preparation

### Ensure Index is Fresh

Check when index was last updated:

```bash
ls -la resources/local-brain-search/data/brain.faiss
```

If older than 24 hours, refresh:

```bash
resources/local-brain-search/run_reindex.sh
```

### Check Knowledge Base State

Read current analysis:

```bash
head -100 knowledge-base-analysis.md
```

Note:
- Current note counts
- Identified gaps
- Recent research sessions

---

## STEP 3: Topic Selection

### If Topic Provided

Use the provided topic from `$ARGUMENTS[1]`.

### If Auto-Select (Default)

Select topic based on knowledge base gaps and rotation. Use these strategies:

**Strategy A: Gap-Filling**
Choose from underrepresented domains in knowledge-base-analysis.md:
- Systems thinking & complexity science (12 notes - gap)
- Embodiment & interoception (14 notes - gap)
- Creativity neuroscience
- Memory consolidation
- Collective intelligence

**Strategy B: Depth-Building**
Extend existing strong domains:
- AI agent architectures (latest 2025-2026 developments)
- Neuroscience of decision-making
- Buddhism-neuroscience bridges
- Identity and belief systems

**Strategy C: Emerging Trends**
Research cutting-edge developments:
- Latest AI safety research
- New consciousness research
- Recent dopamine/motivation findings
- Multi-agent coordination

**Rotation Logic:**
```
cycle_num = cycles_completed % 3
if cycle_num == 0: Strategy A (gap-filling)
if cycle_num == 1: Strategy B (depth-building)
if cycle_num == 2: Strategy C (emerging)
```

Document selected topic and rationale.

---

## STEP 4: Execute Deep Research

Launch the deep-research skill with selected topic:

Use Task tool with subagent_type='research-specialist':

```
TOPIC: [Selected topic]

Conduct comprehensive research on [topic] focusing EXCLUSIVELY on the most recent research and developments (2025-2026).

SEARCH STRATEGY:
- Prioritize papers from last 12-18 months
- Search for "2025", "2026", "recent", "latest" in queries
- Check arXiv preprints, major conferences (NeurIPS, ICML, ICLR)
- Look for industry whitepapers and blog posts

OUTPUT REQUIREMENTS:
- 15-25 major papers/developments
- Full citations with DATES
- Key findings and novel contributions
- Save to: resources/[Topic-Slug]-Research-YYYY-MM-DD.md
```

**On Success:** Continue to Step 5
**On Failure:** Log error, increment `consecutive_errors`, check threshold

---

## STEP 5: Extract Insights

### Create Session Folder

Format: `YYYY-MM-DD [Topic Description]`

```bash
date '+%Y-%m-%d'
# Create: Brain/Document Insights/YYYY-MM-DD [Topic]/
```

### Launch Document Insight Extractor

Use Task tool with subagent_type='document-insight-extractor':

```
Extract unique insights from the research report for the knowledge base.

SOURCE DOCUMENT: [Path to research report from Step 4]
SESSION FOLDER: [Session folder name]

EXTRACTION GUIDELINES:
1. Focus on novel insights (paradigm shifts, counter-intuitive findings)
2. Bridge to existing hubs: Consciousness, Dopamine, Decision-Making, Identity, AI Agents, Flow
3. Quality > Quantity: 15-25 high-value insights
4. ALWAYS search for duplicates before creating notes
5. Create changelog in session folder
```

**On Success:** Count insights extracted, continue to Step 6
**On Failure:** Log error, continue to Step 6 (partial success is OK)

---

## STEP 6: Discover Connections

### Launch Connection Finder

Use Task tool with subagent_type='connection-finder':

```
Discover connections between newly extracted insights and existing knowledge base.

STARTING POINTS: All notes in session folder: [Session folder path]

CONNECTION DISCOVERY GOALS:
1. Bridge to existing 530+ permanent notes
2. Link to 6 primary thematic hubs
3. Find cross-domain consilience opportunities
4. Similarity thresholds: 0.65-0.85

OUTPUT:
- Connection map for new insights
- Synthesis opportunities identified
- Changelog: CHANGELOG - Connection Discovery Session YYYY-MM-DD.md in Brain/05-Meta/Changelogs/
```

**On Success:** Count connections, continue to Step 7
**On Failure:** Log error, continue to Step 7

---

## STEP 7: Update State & Log

### Update State File

Write to `resources/learn-new-things-log.md`:

```markdown
# Learn New Things - Session Log

**Session ID:** [session_id]
**Last Updated:** [timestamp]
**Phase:** running

## Statistics
- Cycles completed: [N]
- Topics researched: [list]
- Total insights extracted: [N]
- Total connections discovered: [N]
- Consecutive errors: [N]

## Latest Cycle
- **Started:** [timestamp]
- **Topic:** [topic]
- **Research report:** [path]
- **Session folder:** [path]
- **Insights extracted:** [N]
- **Connections found:** [N]
- **Status:** [success/partial/error]

## Cycle History
| Date | Topic | Insights | Connections | Status |
|------|-------|----------|-------------|--------|
| YYYY-MM-DD | [topic] | [N] | [N] | [status] |
```

### Log to Master Changelog

Add entry to `Brain/CHANGELOG.md`:

```markdown
## YYYY-MM-DD - Learning Heartbeat Cycle [N]

- **Topic:** [topic]
- **Insights extracted:** [N]
- **Connections discovered:** [N]
- **Session folder:** [[Document Insights/YYYY-MM-DD Topic]]
```

---

## STEP 8: Git Commit & Branch Management

After completing the learning cycle, commit all changes to a dedicated branch, then return to main.

### Create Branch Name

Generate branch name from topic and date:

```bash
# Get current date
DATE=$(date '+%Y-%m-%d')

# Create topic slug (lowercase, hyphens, no special chars)
# Example: "Multi-Agent Systems" → "multi-agent-systems"
TOPIC_SLUG=$(echo "[topic]" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')

BRANCH_NAME="learning/${DATE}-${TOPIC_SLUG}"
```

### Ensure Clean State on Main

Before creating the learning branch, ensure we're on main:

```bash
cd "$(git rev-parse --show-toplevel)"
git stash --include-untracked -m "Pre-learning stash $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
git checkout main
git pull origin main 2>/dev/null || true
git stash pop 2>/dev/null || true
```

### Create and Switch to Learning Branch

```bash
git checkout -b "$BRANCH_NAME"
```

### Stage Learning Results

Stage all files created during this cycle:

```bash
# Research report
git add "resources/[Topic-Slug]-Research-*.md"

# Document Insights session folder
git add "Brain/Document Insights/[Session-Folder]/"

# Changelogs
git add "Brain/05-Meta/Changelogs/CHANGELOG - *.md"
git add "Brain/CHANGELOG.md"

# State file
git add "resources/learn-new-things-log.md"

# Local Brain Search index updates (if any)
git add "resources/local-brain-search/data/" 2>/dev/null || true
```

### Commit with Descriptive Message

```bash
git commit -m "$(cat <<'EOF'
Learning: [Topic] - Cycle [N]

Research & Extraction Session:
- Topic: [topic]
- Papers analyzed: [N]
- Insights extracted: [N]
- Connections discovered: [N]

Session folder: Brain/Document Insights/[Session-Folder]/
Research report: resources/[filename]

Generated by /learn-new-things heartbeat
EOF
)"
```

### Push Branch to Remote

```bash
git push -u origin "$BRANCH_NAME"
```

### Create Pull Request

Create a PR for review and selective merging:

```bash
gh pr create --title "Learning: [Topic] - Cycle [N]" --body "$(cat <<'EOF'
## Learning Session Summary

**Topic:** [topic]
**Date:** YYYY-MM-DD
**Cycle:** [N]

### Research Results
- Papers analyzed: [N]
- Insights extracted: [N]
- Connections discovered: [N]

### Files Added
- Research report: `resources/[filename]`
- Session folder: `Brain/Document Insights/[Session-Folder]/`
- Changelogs updated

### Key Discoveries
1. [Most significant insight]
2. [Cross-domain connection found]
3. [Synthesis opportunity identified]

### Review Checklist
- [ ] Insights are high quality and non-redundant
- [ ] Connections to existing notes are valid
- [ ] No sensitive or incorrect information

---
🤖 Generated by `/learn-new-things` heartbeat
EOF
)"
```

**Store PR URL** in state file for reference:

```markdown
## Latest Cycle
...
- **Pull Request:** https://github.com/[repo]/pull/[N]
```

**If PR creation fails:**
- Branch still exists on remote
- PR can be created manually later
- Continue to next cycle

### Return to Main Branch

```bash
git checkout main
```

### Verify Clean State

```bash
git status
# Should show: "On branch main, nothing to commit, working tree clean"
# Or show unrelated pending changes (not from learning cycle)
```

### Log Branch Info

Update state file with branch information:

```markdown
## Latest Cycle
...
- **Git branch:** learning/YYYY-MM-DD-topic-slug
- **Branch pushed:** yes/no
- **Main restored:** yes
```

### Git Error Handling

**If branch creation fails:**
- Log error, continue on main
- Learning results remain uncommitted
- Flag for manual review

**If push fails:**
- Branch exists locally
- Can be pushed manually later
- Continue to next cycle

**If checkout main fails:**
- CRITICAL: Do not proceed to next cycle
- Increment `consecutive_errors`
- Manual intervention required

---

## STEP 9: Error Handling

### Check Error Threshold

If `consecutive_errors >= 3` OR git checkout main failed:

```markdown
## LEARNING HEARTBEAT PAUSED

**Error:** 3 consecutive cycles failed
**Last topic:** [topic]
**Last error:** [error description]

Manual intervention required. Check:
1. Network connectivity for research
2. Local Brain Search index health
3. Disk space for new notes

To resume: `/learn-new-things`
```

Set `phase: "error"` and stop.

### Reset on Success

If cycle completes successfully:
- Set `consecutive_errors = 0`
- Increment `cycles_completed`
- Add topic to `topics_researched`

---

## STEP 10: Cycle Summary

Display cycle summary:

```markdown
## Learning Cycle [N] Complete

**Topic:** [topic]
**Duration:** [time]

### Results
- Research papers analyzed: [N]
- Unique insights extracted: [N]
- Connections discovered: [N]

### Key Discoveries
1. [Most significant insight]
2. [Cross-domain connection]
3. [Synthesis opportunity]

### Files Created
- Research report: `resources/[filename]`
- Session folder: `Brain/Document Insights/[folder]`
- Changelogs updated

### Git
- **Branch:** `learning/YYYY-MM-DD-topic-slug`
- **Pushed to remote:** yes
- **Pull Request:** [PR URL]
- **Returned to main:** yes

### Next Cycle
- Scheduled in: [interval] hours
- Suggested topic: [next topic based on rotation]
```

---

## STEP 11: Schedule Next Cycle

Set timer for next learning cycle:

```bash
INTERVAL_HOURS=${1:-8}
INTERVAL_SECONDS=$((INTERVAL_HOURS * 3600))
sleep $INTERVAL_SECONDS && echo "HEARTBEAT: learn-new-things ready for next cycle"
```

Run with `run_in_background: true`.

**Important:** The heartbeat only continues if you respond to "HEARTBEAT: learn-new-things" prompt.

---

## Stopping the Loop

**Automatic pause:**
- 3+ consecutive errors

**Manual stop:**
- Run `/learn-new-things stop`
- Don't respond to "HEARTBEAT:" prompts
- Say "stop learning"

**Resume:**
- Run `/learn-new-things` again

---

## Configuration

### Modifiable Parameters

Edit this skill to adjust:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `interval_hours` | 8 | Hours between cycles |
| `max_errors` | 3 | Consecutive errors before pause |
| `insights_per_cycle` | 15-25 | Target insight count |
| `connection_threshold` | 0.65-0.85 | Similarity range |

### Topic Rotation

The rotation pattern can be customized:

```
Cycle 0, 3, 6, 9... → Gap-filling (underrepresented domains)
Cycle 1, 4, 7, 10... → Depth-building (strong domains)
Cycle 2, 5, 8, 11... → Emerging trends (cutting-edge)
```

---

## Examples

### Example 1: Start with Defaults

```
/learn-new-things

→ Starts 8-hour learning loop
→ Auto-selects topic based on gaps
→ Runs research → extract → connect
→ Schedules next cycle in 8 hours
```

### Example 2: Specific Topic, Faster Cycle

```
/learn-new-things 4 "embodied cognition"

→ 4-hour interval
→ Researches embodied cognition specifically
→ Useful for filling known gap quickly
```

### Example 3: Check Status

```
cat resources/learn-new-things-log.md

→ See cycles completed, topics covered
→ Review error history
→ Check next scheduled cycle
```

### Example 4: Stop Learning

```
/learn-new-things stop

→ Pauses the heartbeat
→ Preserves state for later resume
→ No new cycles scheduled
```

---

## Managing Learning Branches & Pull Requests

Each learning cycle creates a branch (`learning/YYYY-MM-DD-topic-slug`) and opens a Pull Request. This provides a formal review workflow for learning results.

### List Open Learning PRs

```bash
gh pr list --search "Learning:" --state open
```

### Review a Learning PR

```bash
# View PR details
gh pr view [PR-NUMBER]

# See files changed
gh pr diff [PR-NUMBER]

# View in browser
gh pr view [PR-NUMBER] --web
```

### Merge Valuable Learning

When learning results look good:

```bash
# Merge via CLI
gh pr merge [PR-NUMBER] --merge

# Or merge via GitHub web interface for more control
gh pr view [PR-NUMBER] --web
```

### Close Without Merging

If a learning session produced low-quality results:

```bash
# Close PR without merging
gh pr close [PR-NUMBER]

# Optionally delete the branch too
gh pr close [PR-NUMBER] --delete-branch
```

### Bulk Operations

```bash
# List all open learning PRs
gh pr list --search "Learning:" --state open

# List all learning branches (including those without PRs)
git branch -r | grep "learning/"

# Delete all merged learning branches (cleanup)
git branch -r --merged main | grep "learning/" | xargs -I {} git push origin --delete {}
```

### Why This Pattern?

- **Formal review**: PRs provide structured review with descriptions and checklists
- **Main stays clean**: Learning only enters main after explicit approval
- **Easy comparison**: GitHub diff view shows exactly what was learned
- **Discussion**: Can comment on specific insights or flag issues
- **Audit trail**: PR history shows decisions about what was accepted/rejected
- **Notifications**: Get notified when learning sessions complete

---

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `/deep-research` | Core research engine (called each cycle) |
| `/auto-discovery` | Can run separately for connection-only cycles |
| `/integrate-recent-notes` | Runs after learning to connect new notes |
| `/refresh-index` | Called before each cycle |
| `/analyze-kb` | Run periodically to update gap analysis |

---

## The Learning Pattern

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          LEARNING HEARTBEAT                                 │
│                                                                             │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌─────────┐   ┌─────┐ │
│  │ SELECT │──▶│RESEARCH│──▶│EXTRACT │──▶│CONNECT │──▶│ COMMIT  │──▶│ PR  │ │
│  │ TOPIC  │   │ PAPERS │   │INSIGHTS│   │ TO KB  │   │ BRANCH  │   │     │ │
│  └────────┘   └────────┘   └────────┘   └────────┘   └─────────┘   └──┬──┘ │
│       │                                                               │     │
│       │                                                       ┌───────▼───┐ │
│       │                                                       │ RETURN TO │ │
│       │                                                       │   MAIN    │ │
│       │                                                       └─────┬─────┘ │
│       │                                                             │       │
│       └─────────────────────SLEEP 8hrs──────────────────────────────┘       │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘

Each cycle:
1. Check gaps in knowledge base
2. Select topic (gap-fill / depth / emerging)
3. Research latest papers (15-25)
4. Extract unique insights (15-25)
5. Discover connections to existing notes
6. Commit to learning/YYYY-MM-DD-topic branch
7. Push branch, create Pull Request
8. Return to main, schedule next cycle

Continuous learning → Ever-expanding knowledge base
PRs enable formal review → Selective merging via GitHub
```

---

## Completion Checklist

Each cycle should complete:

- [ ] Topic selected with rationale
- [ ] Research report generated (15-25 papers)
- [ ] Session folder created in Document Insights
- [ ] Insights extracted with deduplication
- [ ] Connections discovered to existing notes
- [ ] State file updated with cycle results
- [ ] Master changelog updated
- [ ] Learning branch created and pushed
- [ ] Pull request created
- [ ] Returned to main branch
- [ ] Next cycle scheduled (if continuing)

---

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| State file | `resources/learn-new-things-log.md` | ✓ | ✓ | Cycle tracking |
| KB analysis | `knowledge-base-analysis.md` | ✓ | | Gap identification |
| Research reports | `resources/` | | ✓ | Generated reports |
| Document Insights | `Brain/Document Insights/` | | ✓ | Extracted insights |
| Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Session logs |
| Master changelog | `Brain/CHANGELOG.md` | ✓ | ✓ | Summary entries |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Index, search |

---

**Remember:** This is a continuous learning engine. Each cycle makes the knowledge base smarter. The goal is not completion - it's perpetual growth and integration.
