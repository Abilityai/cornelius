---
name: quick-search
description: Fast knowledge base retrieval - single FAISS search + graph connections, no subagents or LLM orchestration
argument-hint: <search query>
allowed-tools: [Bash, Read]
user-invocable: true
---

# Quick Search

Fastest possible knowledge base retrieval. No subagents, no multi-layer orchestration, no changelogs.

## Purpose

Return relevant notes and their graph neighborhood in minimal tool calls. Designed for speed over thoroughness.

## Query

$ARGUMENTS

## Process

**Execute these two commands in parallel (single message, two Bash calls):**

```bash
# 1. Semantic search (6-14s - the unavoidable cost)
/Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search/run_search.sh "$ARGUMENTS" --limit 5 --json

# 2. Graph connections for likely top hit (0.3s - nearly free)
/Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search/run_connections.sh "$ARGUMENTS" --json
```

**Then read the top result file using Read tool.**

That's it. Three tool calls. Present results and stop.

## Output Format

Keep it brief:

```
## [Query]

**Top matches:**
1. [[Note Title]] (0.XX) - [one-line summary from content]
2. [[Note Title]] (0.XX) - [one-line summary]
3. [[Note Title]] (0.XX) - [one-line summary]

**Graph neighborhood** (for top hit):
- Outgoing: [[Note]], [[Note]], ...
- Incoming: [[Note]], [[Note]], ...

**Top result content:**
[First ~30 lines of the highest-scoring note]
```

## Rules

- **NO subagent spawning** - do everything inline
- **NO changelog creation** - this is a read-only lookup
- **NO multi-layer expansion** - one search, one connection call, done
- **NO spreading activation** - use static mode (faster for simple lookups)
- **Parallel execution** - run search and connections in the same message
- **Maximum 3 tool calls** - search + connections + read top file
- If the user wants deeper analysis, tell them to use `/recall` or `/find-connections`
