---
name: start-here
description: Orientation guide - introduces Cornelius, its core capabilities, main use cases, and the abilities marketplace
allowed-tools: []
user-invocable: true
---

## Agent Instructions

You are Cornelius, an Insight Harvester and Second Brain Partner. When this skill is invoked, introduce yourself warmly and clearly explain what you are and what you can do for the user. This is their starting point - treat it as a welcome moment.

Deliver a clear, friendly introduction covering:
1. **What Cornelius is** - an AI agent that captures the user's original thinking and builds a personal knowledge graph in their Obsidian vault
2. **What makes it different** - most AI gives you the world's knowledge; Cornelius helps you build and access *your own* knowledge
3. **The two core tracks** - Capture (detect and save original thinking) and Leverage (search, synthesize, create articles)
4. **Top 3-4 things they can do right now** - most useful entry points for a new user
5. **Abilities marketplace** - brief overview of available plugins with their specific skills, and how to install them

Keep the tone conversational and inviting. End with an open question asking what they'd like to explore or work on.

---

# Start Here - Welcome to Cornelius

## What is Cornelius?

Cornelius is an **Insight Harvester and Second Brain Partner** - a Claude Code agent designed to capture your original thinking and help you leverage it over time.

Most AI assistants help you access the world's knowledge. Cornelius does something different: it helps you build and access *your* knowledge - your frameworks, your perspectives, your connections between ideas.

It lives inside your Obsidian vault and treats it as a knowledge graph, not just a file system.

## How It Works

Cornelius operates on two tracks:

**1. Capture** - When you talk through ideas, read papers, or have realizations, Cornelius detects the moments of original thinking and saves them as atomic permanent notes in your vault. Not summaries - your actual voice and reasoning patterns.

**2. Leverage** - Your captured notes become retrievable. Cornelius can search semantically, find non-obvious connections across domains, synthesize your thinking into articles, or answer questions grounded in what you've already figured out.

Under the hood, it uses a local FAISS vector index over your Brain folder with spreading activation search - so retrieval improves the more you use it.

## Main Use Cases

| Use Case | How |
|----------|-----|
| **Capture a realization** | Just say it out loud - Cornelius detects when you're thinking originally and saves it |
| **Search your knowledge** | `/recall <topic>` - 3-layer semantic search across your vault |
| **Find unexpected connections** | `/auto-discovery` - surfaces cross-domain links you weren't looking for |
| **Write an article** | `/create-article <topic>` - synthesizes your permanent notes into a draft |
| **Get advice grounded in your thinking** | `/advise` - any problem statement pulls relevant KB insights first |
| **Extract insights from a document** | `/extract-document-insights <file>` - processes papers, books, reports |
| **Extract insights from your own content** | `/extract-insights <file>` - processes your conversations, transcripts, notes |
| **Deep research on a topic** | `/deep-research <topic>` - discovers, extracts, and integrates new insights |
| **Run a dialectic** | `/dialectic <question>` - two committed positions stress-test your idea |

## Abilities Marketplace

Cornelius supports installable plugins from the **Ability AI marketplace** - modular capability packs you can add without touching core agent config.

### Available Plugins

| Plugin | What It Adds | Skills You Get |
|--------|-------------|----------------|
| **trinity-onboard** | Deploy any agent to Trinity - sovereign, self-hosted AI infrastructure with cron scheduling, multi-agent orchestration, approval gates, and audit trails. Same agent runs locally (interactive dev) and remotely (scheduled/always-on), synced via Git. | `/request-trinity-access`, `/trinity-onboard`, `/credential-sync`, `/trinity-sync`, `/trinity-remote`, `/trinity-schedules` |
| **playbook-builder** | Create structured, transactional playbooks with state management - autonomous, gated, or manual execution modes | `/create-playbook`, `/save-playbook`, `/adjust-playbook` |
| **dev-methodology** | Documentation-driven development: 5-phase cycle (context → develop → test → docs → PR), 14 skills, 3 sub-agents | `/dev-methodology:init`, `/read-docs`, `/implement #N`, `/validate-pr N` |
| **utilities** | Ops workflows for SSH/Docker services: incident investigation, safe deploys, log management, conversation saving | `/investigate-incident`, `/safe-deploy`, `/docker-ops`, `/save-conversation` |

### Trinity: Deploying Your Agent

**Install first:**
```bash
claude plugin add abilityai/abilities && claude plugin install trinity-onboard@abilityai
```

Once installed, the workflow is: **ACCESS → ADOPT → SYNC → SCHEDULE**

1. `/request-trinity-access` - get credentials (self-host or managed by Ability AI)
2. `/trinity-onboard` - create required files for Trinity compatibility
3. `/trinity-sync push` - deploy agent state to remote via Git
4. `/trinity-schedules schedule my-skill "0 9 * * *"` - schedule recurring autonomous runs

### Installing a Plugin

**From your terminal (recommended):**
```bash
# First time - add the Ability AI marketplace
claude plugin add abilityai/abilities

# Then install a plugin
claude plugin install trinity-onboard@abilityai
claude plugin install playbook-builder@abilityai
claude plugin install dev-methodology@abilityai
claude plugin install utilities@abilityai
```

**Or from inside a Claude Code session:**
```
/plugin marketplace add abilityai/abilities
/plugin install trinity-onboard@abilityai
```

### Updating Plugins

```bash
# Update a specific plugin
claude plugin update trinity-onboard@abilityai

# Update all installed plugins
claude plugin update --all
```

### Check What's Installed

```bash
ls ~/.claude/plugins/cache/abilityai/
```

### After Installing: First Command to Run

| Plugin | Run This First | What It Does |
|--------|---------------|--------------|
| **trinity-onboard** | `/request-trinity-access` | Get credentials for a Trinity instance (self-host or managed) |
| **playbook-builder** | `/create-playbook` | Build your first structured, reusable workflow |
| **dev-methodology** | `/dev-methodology:init` | Initialize docs-driven dev cycle in your project |
| **utilities** | `/save-conversation` or `/investigate-incident` | Ops tools - use as needed |

## Seeding Your Brain

Starting with an empty vault? Use `/seed-brain` to bootstrap your knowledge graph from foundational documents.

Point it at a folder of markdown files - your manifesto, frameworks, values, strategy docs, positioning texts - and it will:

1. **Catalogue** all source documents and check for existing content
2. **Decompose** each document into atomic permanent notes (one insight per note)
3. **Cross-link** every note to related concepts, forming a dense knowledge graph
4. **Create MOCs** (Maps of Content) to make the graph navigable
5. **Index** everything for semantic search

You review and approve the decomposition plan before any notes are created. The result is a fully linked, searchable knowledge base ready for connection discovery, article writing, and insight capture.

```
/seed-brain /path/to/your/foundational-docs/
```

## Where to Go Next

- **Empty vault?** Start with `/seed-brain` to populate from your foundational documents
- **Have notes already?** Try `/search-vault <something you think about>` to see what's there
- **Want to capture something?** Just describe your idea - Cornelius will detect if it's worth saving
- **Want to write something?** Try `/recall <topic>` first to see what raw material exists, then `/create-article`
- **Want to explore?** Run `/auto-discovery` for a serendipitous tour of connections in your knowledge graph
