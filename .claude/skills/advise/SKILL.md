---
name: advise
description: Solve problems using knowledge base insights - extracts search terms, runs parallel KB queries, synthesizes advice grounded in your own frameworks
argument-hint: <describe your problem or question in natural language>
allowed-tools: [Bash, Read]
user-invocable: true
---

# Advise

Help solve problems by grounding advice in your accumulated knowledge and frameworks.

## Purpose

Turn natural language problems into KB-grounded advice. Fast path: no subagents, no changelogs, no multi-layer expansion.

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

Run 3-4 searches **in parallel** (single message, multiple Bash calls):

```bash
resources/local-brain-search/run_search.sh "search term 1" --limit 3 --json
resources/local-brain-search/run_search.sh "search term 2" --limit 3 --json
resources/local-brain-search/run_search.sh "search term 3" --limit 3 --json
```

### Step 3: Read Top Insights

From the search results, read 2-3 of the most relevant note files **in parallel**:

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
```

## Rules

- **NO subagent spawning** - all work happens inline
- **NO changelog creation** - this is conversational, not archival
- **NO spreading activation** - use static search for speed
- **Parallel execution** - run all searches in one message, all reads in the next
- **Maximum 2 rounds of tool calls** - searches (parallel) + reads (parallel)
- **Cite your sources** - always reference the specific notes used
- **Be actionable** - don't just dump knowledge, apply it to the problem
- If KB lacks relevant content, say so honestly and offer general reasoning instead
