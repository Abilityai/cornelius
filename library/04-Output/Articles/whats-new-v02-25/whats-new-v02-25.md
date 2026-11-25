---
created: 2025-02-13
updated: 2025-02-13
created_by: claude-opus-4-5-20251101
updated_by: claude-opus-4-5-20251101
agent_version: 02.25
---

# What's New in Cornelius v02.25

Project Cornelius has received its biggest update yet. This release fundamentally changes how the system works - moving from external dependencies to a fully local, modular architecture with proper orchestration patterns.

Here's everything that changed and why it matters for your second brain workflow.

## The Big Picture

Cornelius started as an experiment: could we turn Claude Code into a specialized knowledge management assistant? The answer was yes, but the original implementation had friction points. Smart Connections required Obsidian to be running. Commands were monolithic scripts. Configuration was scattered. There was no clear way to deploy or share the agent.

v02.25 fixes all of that with three major architectural shifts:

1. **Local Brain Search** replaces Smart Connections (fully local FAISS)
2. **Playbook-style skills** replace simple commands (structured workflows)
3. **Trinity compatibility** enables deployment as a managed agent

---

## Local Brain Search Replaces Smart Connections

The most significant infrastructure change: **Smart Connections MCP is gone**. In its place is Local Brain Search - a FAISS-powered vector search system that runs entirely in Python.

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

---

## Skills as Playbooks: A New Architecture

The entire command architecture has been refactored. Instead of 11 commands in `.claude/commands/`, there are now **19 skills** in `.claude/skills/`.

But this isn't just a rename. Skills in v02.25 are structured as **playbooks** - multi-phase workflows with clear inputs, outputs, state dependencies, and completion criteria.

### What Makes a Playbook Different from a Command?

**Old commands** were simple prompts. They told Claude what to do but left execution details implicit.

**Playbook-style skills** are structured workflows with:

1. **Frontmatter metadata** - Name, description, allowed tools, argument hints
2. **Phased execution** - Clear stages (e.g., Research → Extract → Connect)
3. **State dependencies** - Explicit documentation of what files are read/written
4. **Completion checklists** - Verification that all steps completed
5. **Error handling** - What to do when things go wrong
6. **Supporting files** - Templates, examples, and configuration

### Example: The Deep Research Playbook

Look at `/deep-research` - it's not just "do some research." It's a 5-phase autonomous pipeline:

```
Phase 1: Topic Selection & Research Planning
  ├── Parse input (directed vs autonomous mode)
  ├── Analyze knowledge base gaps (if autonomous)
  └── Select 1-3 research topics with rationale

Phase 2: Execute Research
  ├── Launch research-specialist sub-agent(s)
  ├── Generate comprehensive reports (15-25 papers each)
  └── Save to /resources/ with citations

Phase 3: Extract Insights
  ├── Create session folder in Document Insights
  ├── Launch document-insight-extractor
  ├── Deduplicate against existing knowledge
  └── Create extraction changelog

Phase 4: Connection Discovery
  ├── Launch connection-finder agent
  ├── Map to existing knowledge base hubs
  ├── Identify consilience zones
  └── Create discovery changelog

Phase 5: Summary & Recommendations
  ├── Generate comprehensive session report
  ├── Identify synthesis opportunities
  └── Recommend next actions
```

Each phase has explicit state dependencies:

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Knowledge base analysis | `knowledge-base-analysis.md` | ✓ | | Current KB state |
| Document Insights | `Brain/Document Insights/` | ✓ | ✓ | Session folders |
| Research reports | `resources/` | ✓ | ✓ | Generated reports |
| Changelogs | `Brain/05-Meta/Changelogs/` | ✓ | ✓ | Session logs |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Deduplication |

And a completion checklist:

- [ ] Execution mode determined
- [ ] Topics selected with rationale
- [ ] Research reports saved to /resources/
- [ ] Session folder created in Document Insights
- [ ] Insights extracted with deduplication
- [ ] Changelogs created
- [ ] Master CHANGELOG.md updated
- [ ] Synthesis opportunities identified

This structure means the skill can run autonomously end-to-end, or you can intervene at any phase.

### Skills with Supporting Files

Some skills include their own supporting resources:

**`/create-article`** includes:
- `SKILL.md` - Main playbook
- `tone-of-voice.md` - Writing style guidelines
- `article-structure.md` - Structure templates
- `metadata-template.md` - Article metadata format

**`/elicitation-techniques`** includes:
- `SKILL.md` - Overview and selection guide
- `cognitive-interviewing.md` - Memory activation techniques
- `socratic-questioning.md` - Critical inquiry methods
- `think-aloud.md` - Process transparency techniques
- `specialized-techniques.md` - Laddering, repertory grid, concept mapping

**`/nano-banana-image-generator`** includes:
- `SKILL.md` - Usage instructions
- `best_practices.md` - Image generation guidelines
- `scripts/generate.sh` - Shell wrapper
- `scripts/generate_image.py` - Python generation script
- `scripts/generate_thumbnail.py` - Thumbnail variant

This modular structure means skills can be complex without being monolithic.

### New Skills in v02.25

| Skill | Type | What it does |
|-------|------|--------------|
| `/auto-discovery` | Playbook | Cross-domain connection hunting with random sampling |
| `/deep-research` | Playbook | Full research pipeline: web search → extract → integrate |
| `/create-article` | Playbook | Synthesize notes into articles with tone/structure guides |
| `/integrate-recent-notes` | Playbook | Find connections for notes created in last 14 days |
| `/refresh-index` | Utility | Rebuild the FAISS index after vault changes |
| `/self-diagnostic` | Utility | Health check for the entire Cornelius system |
| `/changelog-protocol` | Protocol | Standard for creating dated changelog files |
| `/epistemic-classification` | Framework | Classify claims as research/hypothesis/speculation |
| `/insight-capture-format` | Template | Standard format for capturing insights |

---

## Sub-Agent Architecture Changes

Sub-agents haven't just been updated - their interaction patterns have changed.

### Clear Separation of Concerns

Each sub-agent now has a focused responsibility:

| Agent | Responsibility | Invokes |
|-------|---------------|---------|
| `vault-manager` | CRUD operations on notes | Local Brain Search |
| `connection-finder` | User-directed exploration | Local Brain Search |
| `auto-discovery` | Autonomous pattern mining | Local Brain Search |
| `insight-extractor` | Extract from YOUR content | Local Brain Search (dedup) |
| `document-insight-extractor` | Extract from EXTERNAL content | Local Brain Search (dedup) |
| `thinking-partner` | Brainstorming dialogue | Local Brain Search |
| `research-specialist` | Web research with Gemini | WebSearch, WebFetch |
| `diagram-generator` | Mermaid visualizations | Mermaid MCP |
| `local-brain-search` | Vector search & graph analytics | FAISS index |

### Orchestration Patterns

Skills now orchestrate sub-agents in defined patterns:

**Sequential orchestration** (`/deep-research`):
```
research-specialist → document-insight-extractor → connection-finder
```

**Parallel orchestration** (multiple topics):
```
research-specialist(topic1) ─┐
research-specialist(topic2) ─┼→ document-insight-extractor → connection-finder
research-specialist(topic3) ─┘
```

**Conditional orchestration** (`/auto-discovery`):
```
local-brain-search (sample notes)
    │
    ├─→ [if patterns found] → connection-finder (deep dive)
    │
    └─→ [if consilience zone] → thinking-partner (synthesis)
```

### Changelog Protocol

All agents now follow a standardized changelog protocol:

1. **Get timestamp** at session start: `date '+%Y-%m-%d %H:%M:%S %Z'`
2. **Create dated changelog** in `Brain/05-Meta/Changelogs/`
3. **Format**: `CHANGELOG - [Session Type] YYYY-MM-DD.md`
4. **Update master** `CHANGELOG.md` with summary

This creates an audit trail of what changed, when, and why.

---

## Trinity Platform Compatibility

Cornelius is now a **Trinity-compatible agent**, ready to be deployed on the [Trinity Deep Agent Orchestration Platform](https://github.com/AbilityAI/trinity).

### What is Trinity?

Trinity is an open-source platform for deploying and orchestrating AI agents. It provides:

- **Container-based deployment** - Each agent runs in isolation
- **Inter-agent communication** - Agents can delegate tasks to each other
- **Credential management** - Secure handling of API keys and secrets
- **Scheduling** - Run agents on cron schedules
- **Monitoring** - Track agent performance and costs
- **Skill libraries** - Share skills across agents

### The template.yaml File

Cornelius includes a `template.yaml` that declares everything Trinity needs:

```yaml
name: cornelius
display_name: "Cornelius"
description: |
  AI Insight Harvester and Second Brain Partner...

resources:
  cpu: "2"
  memory: "4g"

capabilities:
  - semantic_search
  - insight_extraction
  - connection_discovery
  - knowledge_synthesis
  - content_generation

sub_agents:
  - name: vault-manager
    description: "CRUD operations on Obsidian vault notes"
  - name: connection-finder
    description: "Discover hidden connections between notes"
  # ... more agents

skills:
  - name: recall
    description: "3-layer semantic search"
  - name: deep-research
    description: "Autonomous research pipeline"
  # ... more skills

mcp_servers:
  - name: mermaid-diagram
  - name: ebook-mcp

credentials:
  env_file:
    - VAULT_BASE_PATH
    - DOCUMENT_INSIGHTS_PATH

metrics:
  - name: notes_total
    type: gauge
  - name: insights_extracted
    type: counter
  - name: connections_discovered
    type: counter
```

### Deploying to Trinity

If you have Trinity running:

```bash
# From your Trinity instance
trinity agent create --template github:AbilityAI/cornelius --name my-cornelius

# Or deploy from local
cd /path/to/cornelius
trinity deploy
```

Trinity will:
1. Build a container from the template
2. Inject credentials from your vault
3. Start the agent with configured resources
4. Make it available for scheduling and orchestration

### Local-Remote Pairing

A powerful pattern: run Cornelius locally for development, deploy to Trinity for automation.

- **Local**: Interactive sessions, testing, development
- **Remote**: Scheduled `/auto-discovery`, background `/deep-research`

The same skills work in both environments.

---

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

---

## What Got Removed

Some features didn't make the cut:

**`/switch-brain` command** - The multi-vault switching feature is gone. The added complexity wasn't worth it for most users. If you work with multiple vaults, configure them manually in `settings.md`.

**`memory/` folder** - Session memory is now handled through Claude Code's native systems rather than custom files.

**Smart Connections references** - All documentation has been updated. If you see mentions of Smart Connections anywhere, that's a bug.

---

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

---

## What's Next

The foundation is now solid. Future updates will focus on:

- **Better graph analytics** - Cluster detection, path finding, temporal analysis
- **Scheduled operations** - Run auto-discovery on a cron schedule via Trinity
- **Integration patterns** - Working with other AI tools and agents
- **Skill library expansion** - More playbooks for common knowledge workflows

The goal remains the same: make your second brain genuinely useful, not just a graveyard of notes you'll never read again.

---

## Links

- **Cornelius Repository**: [github.com/AbilityAI/cornelius](https://github.com/AbilityAI/cornelius)
- **Trinity Platform**: [github.com/AbilityAI/trinity](https://github.com/AbilityAI/trinity)

---

*Cornelius v02.25 - Released February 2025*
