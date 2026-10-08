# Project Cornelius

**Compounding intelligence your company owns** - the cognitive architecture that makes your work compound, built on Claude Code + Obsidian and run on [Trinity](https://github.com/Abilityai/trinity), the operating system for AI-native companies.

Cornelius turns what you and your company do into knowledge you keep and build on - without retraining a model. It captures *your* thinking in your own voice, finds the connections you missed, works on open questions on a schedule, and stops every conclusion at one human gate before it becomes part of what you believe.

> **Compounds, with receipts.** Every note records who authored the thinking (you, an external source, or the AI). Nothing the AI concludes becomes endorsed knowledge without your explicit act, and every change leaves a git trail. Adaptive improvement inside strict governance - growth is a dial, with your hand on it.

**Where this comes from.** [Ability AI](https://ability.ai) is the lab for AI-native companies, and Cornelius is our cognitive architecture for making a company's work compound. It runs in production on our own work. This repository is its open template: the memory engine, the governance contracts, and the everyday thinking tools ship here as they stabilize; components of the autonomous loop are released once they have soaked in production.

**Why it is yours.** It runs on your machine or your own Trinity server, on plain Markdown files, against any model - export it and walk away. The more a system improves itself, the more it matters who owns it: compounding intelligence on rented ground compounds for the landlord.

### Built for Trinity: the compounding intelligence engine

Cornelius is designed to be the **compounding intelligence engine** inside **[Trinity](https://github.com/Abilityai/trinity)** - the operating system for AI-native companies, where agents and workflows run with permissions, state, governance, and receipts. Open source and self-hosted. On Trinity, Cornelius becomes a persistent brain rather than a chat session:

- 🏢 **A company brain** - the place your organization's experience accumulates and stays: decisions, research, records of people, clients, and competitors, and the reasoning behind them. Other agents in your Trinity fleet consult it, so what one agent records, the others can build on - and it does not walk out the door when a person does.
- 🧠 **A personal brain** - your own thinking, captured in your own voice, connected across everything you read, and kept working on your open questions while you are away.

Trinity supplies what a compounding brain needs and a laptop does not: always-on scheduled loops (incubation, domain watch, research), agent-to-agent delegation, an isolated container with your data on your infrastructure, the live Brain Orb visualization, and receipts - git history, audit logs, and human gates on every change.

Cornelius works standalone in Claude Code for exploration and development. **It is meant to be run on Trinity** - see [Deploy to Trinity](#recommended-deploy-to-trinity-for-autonomous-operation) below.

![How Cornelius works - animated architecture explainer](docs/cornelius-explainer.gif)

*The whole system in one ~3-minute loop: notes become a graph → connection discovery proposes cross-domain bridges → extractors source-tier and provenance-stamp everything at the door → the domain watch fires signals → the incubation loop argues hypotheses with rotating analytical moves → conclusions stop at the one human endorsement gate → pluggable scopes mount and unmount → the BDG answers queries by spreading activation → Trinity runs it all autonomously.*

> 🌱 **Ships pre-seeded.** This isn't an empty template - it comes with a working knowledge graph of **~1,000 interlinked notes** on decision-making, judgment, and cognitive science (distilled from published research and books, ~5,000 edges). Clone it and `/advise`, `/recall`, or `/find-connections` work immediately. Start at [`Brain/03-MOCs/MOC - Knowledge Base.md`](Brain/03-MOCs/MOC%20-%20Knowledge%20Base.md), then layer your own thinking on top. See [knowledge-base-analysis.md](knowledge-base-analysis.md) for what's inside.

## What's New in v10.26

- **`/decide` - decisions, not just advice** - when the question is "X or Y?", "go/no-go", or "is it worth it", `/decide` expands the real option set (status quo, defer, pilot, hybrids), classifies the decision (reversible or one-way door, one-shot or repeated, ruin exposure, risk vs radical uncertainty), applies the *matching* rule (ergodic filter first, then expected value, robustness / minimax regret, or value of information), and closes with tripwires. A recommendation with no named rule is advice wearing a costume.
- **Reasoning checks** - a shared discipline contract (`reasoning-checks`) that `/advise`, `/decide`, and crystallization run before concluding: an epistemic inversion (pre-mortem with a concrete falsifier), an attractor check (is this conclusion just the gravity of your most-linked notes?), provenance weighting, and a reference-class anchor for any estimate.
- **Read roles (`scope-mount`)** - every knowledge-base read now declares *why* it reads: **voice** reads (your perspective, your articles) see only your own thinking; **reasoning** and **lookup** reads also see what you have read, grouped as *your thinking · what you have read · records*. Reference scopes (records, per-book shelves) mount only when the question names them. No more silent reads of the wrong slice of the vault.
- **Similarity scores you can trust** - [`SIMILARITY-CALIBRATION.md`](resources/local-brain-search/SIMILARITY-CALIBRATION.md): a score means nothing without its population, so every threshold in the system is now stated against the space it actually runs in. Search results carry `raw_similarity` next to the learning-adjusted ranking score, and `calibrate_similarity.py` re-measures the bands on *your* vault.
- **Graph fix - rebuild your index** - identical YAML frontmatter blocks made unrelated notes look like perfect twins (cosine 1.000), crowding real neighbours out of the semantic graph. `index_brain.py` now skips frontmatter-only and empty chunks when choosing a note's representative; `tension.py` uses the same rule. **Run `./run_index.sh` and `/detect-tensions` after upgrading.**
- **Source authority** - [`resources/SOURCE-AUTHORITY.md`](resources/SOURCE-AUTHORITY.md) is one template for what to trust at ingestion: a tier model (`primary` · `credible-interpreter` · `discovery-tier` · `rejected`), a web allowlist, and reject patterns. `discovery-tier` lets an off-list source *raise* a question but never *settle* one.
- **Skills ship with their scripts** - the book extractors (`multi-format-book-extractor`, `epub-chapter-extractor`) and `benchmark-memory` now include the Python they call.
- **60 skills** - plus refreshed `advise`, `recall`, `find-connections`, `dialectic`, `ingest-source`, `create-article`, `refresh-index`, and the extraction agents.

<details>
<summary>v07.26 changes</summary>

- **Animated architecture explainer** - the film at the top of this README: the full pipeline from capture to autonomous operation in ~3 minutes (`docs/cornelius-explainer.gif`)
- **Reference scopes - a CRM layer inside the brain** - `manage-reference-data` plus seven `ref-*` skills (`ingest`, `query`, `audit`, `reconcile`, `refresh`, `supersede`, `bridge`) maintain mutable, freshness-stamped entity records - people, organizations, products, engagements, watched competitors - in separately mountable sub-scopes under `Brain/Company/`. Records carry `provenance: reference`, temporal validity, and per-type freshness SLAs; `ref-bridge` surfaces which of your insights an entity is a live instance of. A guarded boundary keeps records from ever auto-promoting into endorsed insights. Conventions: `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md` + `COMPANY-BRAIN-SCHEMA.md`
- **Incremental indexing** - `run_index.sh` now reuses the embedding of every unchanged note (content-hash matching) and splits cold rebuilds into short resumable batches; a daily refresh takes seconds instead of a 15-20 minute full re-embed
- **Tension detection v2** - structural-artifact filters (index/changelog noise, near-duplicates, same-source pairs), persistent dismissals that survive re-scans, and curated tensions that survive graph re-bootstrap
- **Hardened autonomous thinking** - `incubation-loop` v1.22 and `domain-watch` v1.18 codify evidence discipline learned from months of autonomous operation: stale-wire dating, primary-source pinning, pre-registered triggers, injection-not-spawn, framework-exhaustion guards
- **Live orb freshness** - the Brain Orb exporter overlays notes captured since the last reindex, so capture → refresh → appears holds without waiting for the nightly rebuild
- **57 skills** for insight capture, autonomous thinking, connection discovery, reference data, research, and content creation
</details>

<details>
<summary>v06.26 changes</summary>

- **Seeded public knowledge base (1,031 notes)** - The template now ships with a real, fully-indexed library instead of a few showcase notes: 1,031 decision-science notes distilled from 57 research sessions and 6 books, spanning decision-making, judgment, behavioral economics, and the cognitive science beneath good decisions
- **11 new Maps of Content** - Topic-level navigation across decision-making, cognitive biases, risk and antifragility, neuroscience, consciousness, learning and memory, motivation, social cognition, embodied cognition, and meaning and wisdom
- **Portable prebuilt index** - The FAISS + graph index was rebuilt over the new corpus with vault-relative paths, so semantic search, recall, and connection discovery work on any clone immediately - no indexing required before you start exploring
- **Neutral, provenance-tagged notes** - External research distilled into atomic notes (provenance: encountered), navigated via the MOCs; only the foundation tier is published (agent-research and private tiers withheld)
</details>

<details>
<summary>v05.26 changes</summary>

- **Incubation loop** - Autonomous iterative thinking engine; each run applies a rotating analytical move (ACH, Bayesian update, steelman, cross-domain bridge, implication check) and persists reasoning state across scheduled runs
- **Domain watch** - Autonomous perception layer that scans the KB for new notes matching configured domains, checks gap resonance, and probes external signals to auto-activate topics for the incubation loop
- **Insight interview** - KB-grounded Socratic dialogue; searches existing notes on a topic then runs a one-question-at-a-time session to surface and sharpen your thinking, saving results as permanent notes
- **YouTube transcript** - Extract transcripts from any YouTube video for processing into the knowledge base
- **deep-research Phase 4** - Optional insight interview step before connection discovery, capturing your personal angles alongside extracted research
- **45 skills** for insight capture, autonomous thinking, connection discovery, research, and content creation
</details>

<details>
<summary>v04.26 changes</summary>

- **Brain Dependency Graph (BDG)** - Directed, mode-aware dependency graph layered on Local Brain Search. Seven semantic layers (signal -> synthesis), staleness propagation, lifecycle tracking, and tension detection
- **Staleness propagation** - `/propagate-change` traces which downstream notes need review when a framework changes
- **Lifecycle scoring** - `/compute-lifecycle` detects reflective -> crystallizing -> generative transitions
- **Tension detection** - `/detect-tensions` finds productive contradictions (high similarity + opposing conclusions)
- **Coherence sweeps** - `/coherence-sweep` runs full structural health analysis with staleness and lifecycle reports
- **Brain merge** - `/brain-merge` compares and selectively merges Brain directories across agent instances
- **Explanatory images** - `/create-explanatory-image` generates AI diagrams via Nano Banana (Gemini 2.5 Flash)
- **LBS daemon** - Background search daemon for persistent vector search
- **36 skills** for insight capture, connection discovery, research, and content creation
- **10 specialized sub-agents** for different knowledge tasks
</details>

<details>
<summary>v03.26 changes</summary>

- **SYNAPSE-inspired memory** - Spreading activation search with intent classification and usage-based learning
- **Dialectic engine** - Two sub-agents argue committed positions while orchestrator synthesizes
- **Autonomous research** - `/learn-new-things` runs full research cycles with git branching
- **Insight graduation** - `/graduate-insights` promotes draft notes to permanent status with Zettelkasten criteria
- **Q-value learning** - Search rankings improve over time based on actual usage patterns
- **Trinity-compatible** - Can be deployed to the Trinity agent orchestration platform
</details>

---

## TL;DR

**Project Cornelius** = Claude Code + Custom Agents + Obsidian + FAISS Vector Search + a governed autonomous thinking loop

It's like having a highly specialized AI research assistant that:
- **Finds hidden connections** in your notes you didn't know existed
- **Writes articles** from your accumulated insights
- **Captures unique thoughts** while preserving your voice
- **Discovers patterns** across different domains of knowledge
- **Decides, not just advises** - `/decide` structures real choices with a named decision rule and tripwires
- **Keeps you the author** - provenance on every note; AI conclusions never become your beliefs without your explicit act
- **Researches autonomously** - can run research cycles and expand your knowledge base
- **Thinks while you sleep** - runs scheduled reasoning loops on open questions via [Trinity](https://github.com/Abilityai/trinity)
- **Evolves with you** through Git-tracked configurations

---

## What is Project Cornelius?

Project Cornelius is a **multi-layered knowledge management system** that creates an intelligent bridge between your thinking and AI assistance. It's an agent-within-an-agent architecture that transforms Claude Code into a specialized second brain operator.

### The Layer Cake Architecture

```
┌─────────────────────────────────────────┐
│         Human (You)                     │
├─────────────────────────────────────────┤
│         Claude Code                     │ ← General AI assistant
├─────────────────────────────────────────┤
│     Project Cornelius Agent             │ ← Specialized for knowledge work
│     (Defined by CLAUDE.md)              │
├─────────────────────────────────────────┤
│     Specialized Sub-Agents              │ ← Task-specific capabilities
│  (vault-manager, connection-finder...)  │
├─────────────────────────────────────────┤
│  Brain Dependency Graph (BDG)           │ ← Directed graph with staleness,
│  (7 semantic layers, lifecycle)         │   lifecycle, and tension tracking
├─────────────────────────────────────────┤
│     Local Brain Search (FAISS)          │ ← Vector search + memory engine
├─────────────────────────────────────────┤
│         Your Knowledge Base             │ ← Your actual "brain"
│        (Obsidian Vault/Brain)           │
└─────────────────────────────────────────┘
```

### Key Features

**Insight Capture**
- Extract unique insights from books, articles, and conversations
- Preserve your authentic voice and reasoning patterns
- Distinguish between your original thinking and borrowed ideas

**Connection Discovery**
- Find non-obvious relationships between notes
- Identify consilience zones where multiple domains converge
- Surface cross-domain bridges and synthesis opportunities

**Content Generation**
- Synthesize notes into articles and frameworks
- Generate talking points and outlines
- Create content from your accumulated knowledge

**SYNAPSE-Inspired Memory Search**
- FAISS-powered semantic search (fast, local, no API calls)
- Incremental indexing - only changed notes re-embed; daily refresh in seconds
- Intent-aware query classification (factual/conceptual/synthesis/temporal)
- Spreading activation with lateral inhibition
- Usage-based Q-value learning (experimental - rankings can adapt to use; `raw_similarity` always shows the unadjusted score)
- Graph analytics: hubs, bridges, centrality
- Explicit (wiki-links) and semantic edge distinction

**Reference Layer (CRM in the brain)**
- Freshness-stamped entity records (clients, competitors, products, engagements) in mountable scopes
- Temporal queries that always print data age; validity windows with kept history
- Entity ↔ insight bridging - see which of your insights an entity is a live instance of
- Guarded boundary: reference records never auto-promote into endorsed insights

---

## Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/Abilityai/cornelius.git
cd cornelius

# 2. Configure your vault path
cp .claude/settings.md.template .claude/settings.md
# Edit .claude/settings.md and set your vault path:
# VAULT_BASE_PATH=./Brain  (or absolute path to your vault)

# 3. Set up Local Brain Search
cd resources/local-brain-search
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 4. Index your vault
./run_index.sh

# 5. Start Claude Code
cd ../..
claude
```

**Detailed guides:**
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
- [INSTALL.md](INSTALL.md) - Detailed installation
- [MCP-SETUP.md](MCP-SETUP.md) - MCP server configuration (optional)

---

## Recommended: Deploy to Trinity for Autonomous Operation

Running locally is fine for development. Cornelius becomes a compounding intelligence engine - your company brain or your personal brain - when it runs persistently on **[Trinity](https://github.com/Abilityai/trinity)**: scheduled research, incubation loops, domain watching, and the rest of your agent fleet consulting it.

Trinity is the operating system for AI-native companies - open source and self-hosted; compounding intelligence your company owns. Each agent runs in an isolated Docker container with cron scheduling, real-time monitoring, and agent-to-agent delegation.

On Trinity, Cornelius also gets the **Brain Orb** - a live 3D visualization of this knowledge base on the agent's Brain tab, with scope mounting (per-book sub-scopes included), voice-drivable KB search, and capture/link/refresh actions that write back into the vault. The seeded KB renders out of the box (`data.seed.json`); the hook contract ships in `.trinity/brain-orb/` (requires a Trinity base image from 2026-07 or later, with the platform's Brain Orb flags enabled).

**Fastest path:** Use the `trinity` plugin from the [Abilities marketplace](https://github.com/Abilityai/abilities):

```bash
# Install the plugin
claude plugin add abilityai/abilities

# Then from inside Cornelius:
/trinity:connect    # one-time auth
/trinity:onboard    # deploy
```

**Documentation:** [docs.ability.ai](https://docs.ability.ai)

### Abilities Plugin Marketplace

The [Abilities marketplace](https://github.com/Abilityai/abilities) provides Claude Code plugins for the full agent lifecycle:

| Plugin | What it does |
|--------|-------------|
| `create-agent` | Scaffold new agents from domain-specific wizards |
| `agent-dev` | Extend agents with skills, memory systems, and backlogs |
| `trinity` | Deploy and sync agents to Trinity |
| `dev-methodology` | Documentation-driven development framework |
| `utilities` | Ops tools - incident investigation, deployment rollback |

Install all at once: `/plugin marketplace add abilityai/abilities`
Docs: [docs.ability.ai/cloud-code-plugins](https://docs.ability.ai/cloud-code-plugins)

---

## What's Included

### Sub-Agents (`.claude/agents/`)

| Agent | Purpose |
|-------|---------|
| `vault-manager` | Create, read, update, delete notes with proper metadata |
| `connection-finder` | Find hidden relationships between notes (user-directed) |
| `auto-discovery` | Autonomous cross-domain connection hunter |
| `insight-extractor` | Extract insights from YOUR content (conversations, transcripts) |
| `document-insight-extractor` | Extract insights from EXTERNAL content (papers, books) |
| `thinking-partner` | Brainstorming and ideation support |
| `diagram-generator` | Create Mermaid visualizations |
| `local-brain-search` | FAISS-powered semantic search and graph analytics |
| `research-specialist` | Deep research with web search |
| `epub-chapter-extractor` | Extract content from ebooks |

### Skills (`.claude/skills/`)

**Search & Discovery**

| Skill | Command | Purpose |
|-------|---------|---------|
| `recall` | `/recall <topic>` | 3-layer semantic search with spreading activation |
| `search-vault` | `/search-vault <query>` | Quick semantic + keyword search |
| `quick-search` | `/quick-search <query>` | Fastest lookup - top hits with excerpts |
| `find-connections` | `/find-connections <note>` | Map conceptual network |
| `auto-discovery` | `/auto-discovery` | Run cross-domain connection discovery |
| `detect-tensions` | `/detect-tensions` | Find productive contradictions between notes |

**Insight Management**

| Skill | Command | Purpose |
|-------|---------|---------|
| `extract-insights` | `/extract-insights <file>` | Extract insights from YOUR content |
| `extract-document-insights` | `/extract-document-insights <file>` | Extract insights from external documents |
| `ingest-source` | `/ingest-source <file or url>` | One entry point for books, papers, documents, and videos - routes and links them |
| `graduate-insights` | `/graduate-insights` | Promote notes to permanent status |
| `integrate-recent-notes` | `/integrate-recent-notes` | Connect recent notes to knowledge base |
| `insight-interview` | `/insight-interview <topic>` | KB-grounded Socratic dialogue to surface and sharpen your thinking |

**Content & Synthesis**

| Skill | Command | Purpose |
|-------|---------|---------|
| `advise` | `/advise <problem>` | Advice grounded in your own frameworks - parallel KB queries, synthesized |
| `decide` | `/decide <choice>` | Structure a decision - option set, decision type, matching rule, tripwires |
| `think-about-it` | `/think-about-it <topic>` | Consider a topic through successive distinct KB lenses |
| `create-article` | `/create-article <topic>` | Write article from notes |
| `get-perspective-on` | `/get-perspective-on <topic>` | Extract unique perspective |
| `synthesize-insights` | `/synthesize-insights` | Combine insights into narrative |
| `dialectic` | `/dialectic <question>` | Stress-test ideas with opposing positions |
| `create-explanatory-image` | `/create-explanatory-image` | Generate AI diagrams via Nano Banana |

**Research & Learning**

| Skill | Command | Purpose |
|-------|---------|---------|
| `deep-research` | `/deep-research <topic>` | Autonomous research pipeline |
| `learn-new-things` | `/learn-new-things [topic]` | Full research cycle with git branching |
| `get-youtube-transcript` | `/get-youtube-transcript <url>` | Extract transcript from YouTube video |

**System & Maintenance**

| Skill | Command | Purpose |
|-------|---------|---------|
| `analyze-kb` | `/analyze-kb` | Generate structure report |
| `refresh-index` | `/refresh-index` | Rebuild FAISS index |
| `self-diagnostic` | `/self-diagnostic` | Health check |
| `git-commit-push` | `/git-commit-push` | Stage, commit, push with approval gate |
| `talk` | `/talk` | Conversational partner mode |
| `update-changelog` | `/update-changelog` | Update master CHANGELOG.md |
| `benchmark-memory` | `/benchmark-memory` | Benchmark search system |
| `test-memory-system` | `/test-memory-system` | Test memory improvements |
| `scheduled-run` | `/scheduled-run <skill>` | Wrapper for cron automation |
| `update-dashboard` | `/update-dashboard` | Update Trinity dashboard metrics |

**Autonomous Thinking**

| Skill | Command | Purpose |
|-------|---------|---------|
| `incubation-loop` | `/incubation-loop` | Iterative thinking engine - applies rotating analytical moves to active topics |
| `manage-thinking-topics` | `/manage-thinking-topics` | Seed, review, crystallize, and retire thinking loop topics |
| `domain-watch` | `/domain-watch` | Autonomous KB scanning - detects new signals and activates thinking topics |
| `manage-watching-domains` | `/manage-watching-domains` | Configure domain-watch surveillance and review proposals |

**Reasoning Contracts** (shared rules other skills follow - not invoked directly)

| Skill | Purpose |
|-------|---------|
| `scope-mount` | Which slice of the vault a read sees, decided by the read's role (voice / reasoning / lookup) |
| `reasoning-checks` | Pre-conclusion checks - epistemic inversion, attractor check, provenance weighting, reference class |
| `epistemic-classification` | Truth-status and source-tier tagging at ingestion |

**Brain Dependency Graph**

| Skill | Command | Purpose |
|-------|---------|---------|
| `coherence-sweep` | `/coherence-sweep` | Full BDG health analysis - staleness, lifecycle, structure |
| `propagate-change` | `/propagate-change <note>` | Trace which notes need review after a change |
| `compute-lifecycle` | `/compute-lifecycle` | Detect reflective -> crystallizing -> generative transitions |
| `detect-tensions` | `/detect-tensions` | Find productive contradictions for synthesis |
| `brain-merge` | `/brain-merge` | Compare and merge Brain directories across instances |

**Reference Data (entities & CRM)**

| Skill | Command | Purpose |
|-------|---------|---------|
| `manage-reference-data` | `/manage-reference-data` | Upsert entity notes in a reference scope (base playbook) |
| `ref-ingest` | `/ref-ingest <facts>` | Entry point for incoming entity info - resolve, reconcile, upsert |
| `ref-query` | `/ref-query <question>` | Temporal lookup that always prints `as_of` freshness |
| `ref-audit` | `/ref-audit` | Read-only integrity report for a reference scope |
| `ref-reconcile` | `/ref-reconcile` | Gated integrity fixes and duplicate-entity merges |
| `ref-refresh` | `/ref-refresh` | Staleness sweep against per-type freshness SLAs |
| `ref-supersede` | `/ref-supersede <entity>` | Validity transitions that keep the old snapshot |
| `ref-bridge` | `/ref-bridge <entity>` | Surface entity ↔ insight bridges into the cognitive KB |

### Sample Vault (`Brain/`)

Complete Zettelkasten structure with templates:

```
Brain/
├── 00-Inbox/              # Quick capture, unprocessed notes
├── 01-Sources/            # Literature notes, references
├── 02-Permanent/          # Atomic, evergreen notes (CORE)
├── 03-MOCs/               # Maps of Content
├── 04-Output/             # Articles, frameworks, insights
│   └── Articles/          # Each article in own folder
├── 05-Meta/               # System notes, changelogs
├── AI Extracted Notes/    # AI-extracted from YOUR content
├── Company/               # Reference scopes - entity records (created by ref-* skills)
└── Document Insights/     # AI-extracted from external content
```

### Local Brain Search (`resources/local-brain-search/`)

FAISS-powered vector search with SYNAPSE-inspired memory architecture:

```bash
# Semantic search (static mode - fast)
./run_search.sh "dopamine motivation" --limit 10 --json

# Spreading activation search (better for synthesis queries)
./run_search.sh "how does dopamine relate to decision making" --mode spreading --json

# Find connections
./run_connections.sh "Note Name" --json

# Graph analytics
./run_connections.sh --hubs --json    # Most connected notes
./run_connections.sh --bridges --json  # Cross-domain connectors
./run_connections.sh --stats --json    # Graph statistics

# Learning system status
./run_learning.sh status              # Q-value stats
./run_learning.sh top                 # Top notes by learned relevance

# Re-index after changes
./run_index.sh
```

**Memory Architecture:**
- **Intent Classification** - Routes queries as factual/conceptual/synthesis/temporal
- **Spreading Activation** - Propagates relevance through graph with lateral inhibition
- **Usage-Based Learning** - Q-values adjust rankings based on what you actually use
- **Configuration** - Single source of truth in `memory_config.py`

### Brain Dependency Graph (`resources/brain-graph/`)

A directed, mode-aware dependency graph layered on top of Local Brain Search. Every relationship has **direction** (who's authoritative), **mode** (generative vs reflective), and **type** (derives-from, instantiates, references, associates, tension, supersedes).

**Seven Semantic Layers:** signal (1) -> impression (2) -> insight (3) -> framework (4) -> lens (5) -> synthesis (6) -> index (7)

```bash
# Bootstrap the graph from your vault
./run_brain_graph.sh bootstrap

# Check graph status
./run_brain_graph.sh status --json

# Inspect a specific note's dependencies
./run_brain_graph.sh inspect "Note Name" --json

# Propagate staleness from a changed note
./run_brain_graph.sh propagate "Note Name" --json

# Compute lifecycle scores (reflective -> crystallizing -> generative)
./run_brain_graph.sh lifecycle --json

# Find productive contradictions
./run_brain_graph.sh tensions --json

# Full coherence report
./run_brain_graph.sh coherence --days 7 --tensions --json
```

**Key Behaviors:**
- When a framework note changes, staleness propagates downstream with attenuation
- Notes transition from reflective -> crystallizing -> generative based on citation patterns
- Productive contradictions (tension edges) are immune to staleness - surfaced as synthesis opportunities
- Authority is edge-local, not node-global

**Architecture details:** See `resources/brain-graph/BRAIN-DEPENDENCY-GRAPH-ARCHITECTURE.md`

---

## Documentation

| File | Purpose |
|------|---------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup |
| [INSTALL.md](INSTALL.md) | Detailed installation & troubleshooting |
| [EXAMPLES.md](EXAMPLES.md) | Sample notes, MOCs, workflows |
| [FOLDER-STRUCTURE.md](FOLDER-STRUCTURE.md) | Vault organization guide |
| [MCP-SETUP.md](MCP-SETUP.md) | MCP server configuration |
| [Brain/README.md](Brain/README.md) | Sample vault guide |

---

## Use Cases

**Capture**: Extract insights from books and articles while reading
**Connect**: Find non-obvious relationships between ideas from different domains
**Create**: Synthesize notes into articles, frameworks, and presentations
**Discover**: Let AI find patterns you didn't know existed
**Research**: Autonomous research cycles that expand your knowledge base
**Evolve**: Track how your thinking changes over time

---

## Core Principles

**Atomic notes** - One idea per note, well-linked
**Your words** - Not copy-paste from sources
**Rich links** - Connect everything with `[[wiki-links]]`
**Regular discovery** - Run connection finder and auto-discovery
**Active synthesis** - Create content from your connections

---

## Requirements

- [Claude Code](https://claude.ai/claude-code) (CLI)
- [Obsidian](https://obsidian.md/) (for viewing/editing vault)
- Python 3.10+ (for Local Brain Search)
- Node.js 18+ (optional, for MCP servers)

---

## Architecture Overview

```mermaid
graph TB
    subgraph "User Space"
        User[User]
    end

    subgraph "Claude Code Layer"
        CC[Claude Code IDE]
        CLAUDE[CLAUDE.md System Prompt]
    end

    subgraph "Project Cornelius"
        CONFIG[.claude Config]
        AGENTS[Sub-Agents]
        SKILLS[Skills]
        SEARCH[Local Brain Search]
    end

    subgraph "Memory Engine"
        INTENT[Intent Classifier]
        SPREAD[Spreading Activation]
        LEARN[Q-Value Learning]
    end

    subgraph "Dependency Graph"
        BDG[Brain Dependency Graph]
        LIFE[Lifecycle Scoring]
        TENSION[Tension Detection]
        STALE[Staleness Propagation]
    end

    subgraph "Knowledge Layer"
        BRAIN[Brain / Obsidian Vault]
        FAISS[FAISS Index]
        GRAPH[Knowledge Graph]
    end

    User --> CC
    CC --> CLAUDE
    CLAUDE --> CONFIG
    CONFIG --> AGENTS
    CONFIG --> SKILLS
    AGENTS --> SEARCH
    SKILLS --> SEARCH
    SEARCH --> INTENT
    INTENT --> SPREAD
    SPREAD --> FAISS
    SPREAD --> GRAPH
    LEARN --> SPREAD
    SKILLS --> BDG
    BDG --> LIFE
    BDG --> TENSION
    BDG --> STALE
    BDG --> GRAPH
    FAISS --> BRAIN
    GRAPH --> BRAIN

    style BRAIN fill:#e1f5e1
    style FAISS fill:#ffd700
    style SPREAD fill:#e6e6fa
    style BDG fill:#ffe0b2
```

---

## Version History

| Version | Changes |
|---------|---------|
| v10.26 | `/decide`, reasoning-checks, read roles (scope-mount), similarity calibration + `raw_similarity`, frontmatter-twin graph fix, source-authority template, skills ship with scripts, 60 skills |
| v07.26 | Reference scopes (CRM layer, 8 skills), incremental indexing, tension detection v2, animated architecture explainer, 57 skills |
| v06.26 | Seeded public knowledge base (1,031 decision-science notes + 11 MOCs), portable rebuilt index |
| v05.26 | Incubation loop, domain watch, insight interview, YouTube transcript, deep-research Phase 4, 45 skills |
| v04.26 | Brain Dependency Graph, staleness propagation, lifecycle scoring, tension detection, coherence sweeps, brain merge, explanatory images, LBS daemon, 36 skills |
| v03.26 | SYNAPSE memory, dialectic engine, autonomous research, insight graduation, 30 skills |
| v02.25 | Skills architecture, FAISS search, remove Smart Connections |
| v01.25 | Initial release with commands, Smart Connections, basic search |

---

## License

MIT - Use, modify, distribute freely. See [LICENSE](LICENSE).

---

## Contributing

Contributions welcome! Please read the existing code style and structure before submitting PRs.

---

**Questions?** Check the docs above or start with [QUICKSTART.md](QUICKSTART.md)
