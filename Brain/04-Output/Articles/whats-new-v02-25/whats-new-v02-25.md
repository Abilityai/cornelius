---
created: 2025-02-13
updated: 2025-02-13
created_by: claude-opus-4-5-20251101
updated_by: claude-opus-4-5-20251101
agent_version: 02.25
---

# What's New in Cornelius v02.25

Project Cornelius has received its biggest update yet. This release fundamentally changes how the system works - moving from external dependencies to a fully local, modular architecture.

Here's everything that changed and why it matters for your second brain workflow.

## The Big Picture

Cornelius started as an experiment: could we turn Claude Code into a specialized knowledge management assistant? The answer was yes, but the original implementation had friction points. Smart Connections required Obsidian to be running. Commands were monolithic. Configuration was scattered.

v02.25 fixes all of that.

## Local Brain Search Replaces Smart Connections

The most significant change: **Smart Connections MCP is gone**. In its place is Local Brain Search - a FAISS-powered vector search system that runs entirely in Python.

**What this means for you:**

- No need to have Obsidian open for search to work
- Faster indexing and search (sub-second performance)
- Graph analytics you didn't have before (hubs, bridges, centrality)
- Clear distinction between explicit connections (your wiki-links) and semantic connections (similarity-based)

**The technical details:**

```bash
# Semantic search
./resources/local-brain-search/run_search.sh "query" --limit 10 --json

# Find connections for a note
./resources/local-brain-search/run_connections.sh "Note Name" --json

# Discover hub notes (most connected)
./resources/local-brain-search/run_connections.sh --hubs --json

# Find bridge notes (cross-domain connectors)
./resources/local-brain-search/run_connections.sh --bridges --json

# Graph statistics
./resources/local-brain-search/run_connections.sh --stats --json
```

The index uses `all-MiniLM-L6-v2` embeddings (384 dimensions) stored in FAISS. It's the same quality as cloud-based solutions, but everything stays on your machine.

**One trade-off:** You need to manually re-index when your vault changes. Run `./run_index.sh` or use the `/refresh-index` skill.

## Commands Become Skills

The entire command architecture has been refactored. Instead of 11 commands in `.claude/commands/`, there are now **19 skills** in `.claude/skills/`.

Why skills instead of commands?

1. **Modularity** - Each skill is self-contained with its own documentation, templates, and supporting files
2. **Composability** - Skills can reference other skills
3. **Discoverability** - Claude Code's skill system makes them easier to find and use

**New skills you'll want to try:**

| Skill | What it does |
|-------|--------------|
| `/auto-discovery` | Finds surprising connections across unrelated domains |
| `/deep-research` | Full research pipeline: web search → extract → integrate |
| `/create-article` | Synthesizes notes into articles with tone/structure guides |
| `/refresh-index` | Rebuilds the FAISS index after vault changes |
| `/self-diagnostic` | Health check for the entire Cornelius system |
| `/integrate-recent-notes` | Finds connections for notes created in last 14 days |

The elicitation techniques (cognitive interviewing, Socratic questioning, think-aloud protocol) are now properly documented skills you can invoke or learn from.

## Metadata Tracking

Every note Cornelius creates or updates now includes frontmatter metadata:

```yaml
---
created: 2025-02-13
updated: 2025-02-13
created_by: claude-opus-4-5-20251101
updated_by: claude-opus-4-5-20251101
agent_version: 02.25
---
```

This gives you:

- **Provenance** - Know which AI model created or modified a note
- **Timeline** - Track when changes happened
- **Version tracking** - See which Cornelius version was used

The system is smart about updates: it only changes `updated_by` for substantial changes, not typo fixes.

## What Got Removed

Some features didn't make the cut:

**`/switch-brain` command** - The multi-vault switching feature is gone. The added complexity wasn't worth it for most users. If you work with multiple vaults, you can still configure them manually in `settings.md`.

**`memory/` folder** - Session memory is now handled through Claude Code's native systems rather than custom files.

**Smart Connections references** - All documentation has been updated. If you see mentions of Smart Connections anywhere, that's a bug.

## Trinity Platform Compatibility

Cornelius now includes a `template.yaml` that makes it compatible with the Trinity agent orchestration platform. This is optional - you don't need Trinity to use Cornelius - but if you want to deploy Cornelius as a managed agent, the configuration is ready.

## Getting Started with v02.25

If you're upgrading from a previous version:

```bash
# Pull the latest changes
cd /path/to/cornelius
git pull origin main

# Set up Local Brain Search
cd resources/local-brain-search
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Index your vault
./run_index.sh

# Start Claude Code
cd ../..
claude
```

If you're starting fresh, follow the [QUICKSTART.md](../../QUICKSTART.md) guide.

## What's Next

The foundation is now solid. Future updates will focus on:

- **Better graph analytics** - Cluster detection, path finding, temporal analysis
- **Scheduled operations** - Run auto-discovery on a cron schedule
- **Integration patterns** - Working with other AI tools and agents

The goal remains the same: make your second brain genuinely useful, not just a graveyard of notes you'll never read again.

---

*Cornelius v02.25 - Released February 2025*
