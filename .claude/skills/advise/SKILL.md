---
name: advise
description: Solve problems using knowledge base insights - extracts search terms, runs parallel KB queries, synthesizes advice grounded in your own frameworks
automation: autonomous
argument-hint: <describe your problem or question in natural language>
allowed-tools: [Bash, Read]
user-invocable: true
metadata:
  version: "1.2"
  updated: 2026-07-31
  author: Ability.ai
  changelog:
    - "1.2: Route structured decisions to the new /decide sibling (rule-matched choice vs framework map)"
    - "1.1: Wire in the reasoning-checks contract (Step 5) - epistemic inversion, attractor check (hubs fetched inside the Step 2 parallel batch, so still 2 tool rounds), provenance base, conditional reference-class; blocks appended to the output"
    - "1.0: Initial version - fast-path KB-grounded advice (no subagents, parallel search + read)"
---

# Advise

Help solve problems by grounding advice in your accumulated knowledge and frameworks.

## Purpose

Turn natural language problems into KB-grounded advice. Fast path: no subagents, no changelogs, no multi-layer expansion.

**Routing:** if the problem is a structured decision between courses of action ("X or Y?", go/no-go, "is it worth") → use `/decide` instead: it applies an explicit decision rule (ergodic filter, EV, robustness, value-of-information) and delivers tripwires, not just frameworks. `/advise` is for framing, understanding, and open problems.

## Problem

$ARGUMENTS

## Process

### Step 1: Extract Search Terms (no tool calls - just reasoning)

From the problem description, identify 3-4 keyword clusters that would match relevant KB content:
- Core concepts (what domain is this?)
- Related frameworks (what mental models apply?)
- Analogous patterns (what similar problems exist?)

**Example:**
- Problem: "Should I focus on fundraising or product development?"
- Search terms: `decision making tradeoffs`, `explore exploit`, `focus prioritization`, `opportunity cost`

### Step 2: Parallel Knowledge Retrieval

**Read role: reasoning** (contract: `scope-mount` - never copy its tables, never run a bare search). Two passes per term in the same batch: `core` is the spine (the user's thinking), the reasoning mount is the evidence layer (what he has read). Before the batch, run the `scope-mount` trigger check on the problem text; a hit appends `,company` / `,thinkers` / `,Books/<slug>` to the wide pass for this run only. Direction questions about the org are not yours - route to `/canon-advise`.

Run the searches **in parallel** (single message, multiple Bash calls):

```bash
BRAIN_READ_SCOPE=core                          resources/local-brain-search/run_search.sh "search term 1" --limit 3 --json
BRAIN_READ_SCOPE=core,Books,document-insights  resources/local-brain-search/run_search.sh "search term 1" --limit 5 --json
BRAIN_READ_SCOPE=core                          resources/local-brain-search/run_search.sh "search term 2" --limit 3 --json
BRAIN_READ_SCOPE=core,Books,document-insights  resources/local-brain-search/run_search.sh "search term 2" --limit 5 --json
BRAIN_READ_SCOPE=core                          resources/local-brain-search/run_search.sh "search term 3" --limit 3 --json
BRAIN_READ_SCOPE=core,Books,document-insights  resources/local-brain-search/run_search.sh "search term 3" --limit 5 --json
resources/local-brain-search/run_connections.sh --hubs --json   # fingerprint - always core; for Step 5's attractor check, same batch
```

### Step 3: Read Top Insights

From the search results, read 2-3 of the most relevant note files **in parallel** - when both passes returned, read at least one from each. A `Books/` or `Document Insights/` note is *encountered* material: cite it as what the user has read, never as his view (Check 3 in Step 5 enforces this):

```bash
# Use Read tool on the top-scoring, most relevant files
```

### Step 3.5: Check BDG Context (optional, if top results are frameworks)

For any top result that looks like a framework or key insight, check its BDG context:
```bash
resources/brain-graph/run_brain_graph.sh inspect "Top Result Name" --json
```

This reveals: lifecycle phase (is it generative?), staleness (is it still fresh?), and typed edges (what does it drive?). Prioritize generative frameworks over reflective notes. Warn if citing a stale note.

### Step 4: Synthesize Advice

Combine the retrieved insights to address the original problem:
- Apply frameworks from the notes to the specific situation
- Cite specific notes: [[Note Title]]
- Highlight tensions or tradeoffs the KB reveals
- Give concrete recommendations grounded in your own thinking
- Prioritize generative notes (lifecycle > 0.6) - these are the user's strongest frameworks

### Step 5: Reasoning Checks (required)

Apply the shared contract in `.claude/skills/reasoning-checks/SKILL.md` before finalizing:
- **Epistemic Inversion** (always) - specific falsifier required; a generic hedge means redo it
- **Attractor Check** (always) - against the hubs fetched in Step 2; ≥2 top-10 hubs load-bearing → generate one non-attractor framing
- **Provenance Base** (always) - tally from the frontmatter of the notes read in Step 3; unendorsed synthesis must be labelled as such
- **Reference Class** (only if the advice hinges on a forecast, magnitude, or probability)

Append the resulting blocks after the Bottom line.

## Output Format

```markdown
## [Problem summary - one line]

**Relevant frameworks from your KB:**
- [[Note 1]] - [how it applies]
- [[Note 2]] - [how it applies]
- [[Note 3]] - [how it applies]

**My take (grounded in your insights):**

[2-4 paragraphs synthesizing advice, citing notes, applying frameworks to the specific problem]

**Key tradeoffs to consider:**
- [Tradeoff 1]
- [Tradeoff 2]

**Bottom line:** [One clear recommendation or framing]

[reasoning-checks blocks: Epistemic Inversion · Attractor Check · Provenance Base · Reference Class (when quantitative)]
```

## Rules

- **NO subagent spawning** - all work happens inline
- **NO changelog creation** - this is conversational, not archival
- **NO spreading activation** - use static search for speed
- **Parallel execution** - run all searches in one message, all reads in the next
- **Maximum 2 rounds of tool calls** - searches + hubs (parallel) + reads (parallel); the reasoning checks reuse those results, no extra round
- **Cite your sources** - always reference the specific notes used
- **Be actionable** - don't just dump knowledge, apply it to the problem
- If KB lacks relevant content, say so honestly and offer general reasoning instead
