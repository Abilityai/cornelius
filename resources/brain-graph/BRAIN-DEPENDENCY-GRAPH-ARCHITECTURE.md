# Brain Dependency Graph Architecture

**A directed, mode-aware knowledge graph where the agent maintains coherence by propagating changes along typed edges - not just storing and retrieving notes.**

---

## The Problem With Flat Knowledge Graphs

Current Zettelkasten and Obsidian-based knowledge systems treat links as undirected "related to" connections. This creates three failure modes:

1. **Silent staleness** - When your understanding of dopamine evolves, 362 linked notes continue reflecting the old model. No signal tells you which ones are now wrong.
2. **Ambiguous authority** - When a permanent note contradicts its source material, who wins? The system doesn't know.
3. **No propagation** - Changes are local. The agent can search the graph but cannot reason about what SHOULD change when something DOES change.

The Brain Dependency Graph solves this by giving every relationship **direction**, **mode**, and **type** - turning the knowledge base from a retrieval engine into a coherence engine.

---

## Core Concepts

### Three Properties of Every Edge

Every relationship between two notes has three independent properties:

#### 1. Direction (Source → Target)

**Source**: The authoritative note. When source and target disagree, the source is assumed correct.
**Target**: The derived note. When source and target disagree, the target is potentially stale.

Direction answers: **"When these two things conflict, which one should I trust?"**

**Critical design principle**: Authority is **edge-local, not node-global**. The same note can be authoritative over one connection and subordinate to another. Your interpretation of Kahneman is authoritative over your article about bias, but subordinate to Kahneman's actual text for empirical claims.

#### 2. Mode (Generative vs Reflective)

**Generative** (prescriptive): The note defines intent - what you believe SHOULD be true. Your original frameworks, hypotheses, predictions. These drive reality.

**Reflective** (descriptive): The note reflects reality - what currently IS true according to evidence or sources. Literature notes, summaries, empirical observations. These follow reality.

Mode answers: **"Does this note drive understanding or follow it?"**

**Agent behavior differs by mode:**
- Conflict in a **reflective** note? Source material wins. Auto-propagation is safe.
- Conflict in a **generative** note? This is a creative decision. The agent flags but never auto-resolves.

#### 3. Edge Type

Not all connections have the same semantics. Six fundamental edge types:

| Edge Type | Semantics | Staleness Propagation | Direction |
|-----------|-----------|----------------------|-----------|
| **derives-from** | B was synthesized from A | High (0.8) | A → B |
| **instantiates** | B is a specific case of framework A | High (0.7) | A → B |
| **references** | B mentions a concept from A | Low (0.2) | A → B |
| **associates** | B is thematically related to A | Near-zero (0.05) | Bidirectional |
| **tension** | A and B contradict productively | Zero (immune) | Bidirectional |
| **supersedes** | B replaces A (A is deprecated) | Full (1.0) | B → A |

---

## Artifact Types (Node Types)

### The Seven Layers

```
┌─────────────────────────────────────────────┐
│  LAYER 7: INDICES                           │
│  Meta-structural: analysis, dashboards      │
│  Mode: Always reflective                    │
│  Rebuilt, never "authored"                  │
├─────────────────────────────────────────────┤
│  LAYER 6: SYNTHESES                         │
│  Articles, essays, composed output          │
│  Mode: Reflective (of frameworks/insights)  │
│  Can flip to generative via reader feedback │
├─────────────────────────────────────────────┤
│  LAYER 5: LENSES                            │
│  MOCs, navigational indices, cluster views  │
│  Mode: Reflective (derived from members)    │
│  Never authoritative - always reconstructed │
├─────────────────────────────────────────────┤
│  LAYER 4: FRAMEWORKS                        │
│  Original mental models, theories           │
│  Mode: Generative (drives downstream)       │
│  Highest creative authority                 │
├─────────────────────────────────────────────┤
│  LAYER 3: INSIGHTS                          │
│  Atomic permanent notes                     │
│  Mode: Mixed (reflective OR generative)     │
│  Lifecycle determines current mode          │
├─────────────────────────────────────────────┤
│  LAYER 2: IMPRESSIONS                       │
│  Inbox captures, fleeting notes, highlights │
│  Mode: Reflective                           │
│  Temporary - processed into insights        │
├─────────────────────────────────────────────┤
│  LAYER 1: SIGNALS                           │
│  Raw inputs: books, papers, conversations   │
│  Mode: Reflective (empirical authority)     │
│  External truth, not your creation          │
└─────────────────────────────────────────────┘
```

### Default Relationship Directions Between Layers

```
Signals ──derives-from──→ Impressions ──derives-from──→ Insights
                                                           │
                                              ┌────────────┼────────────┐
                                              ▼            ▼            ▼
                                          Frameworks    Lenses     Syntheses
                                              │                       ▲
                                              └───instantiates────────┘
                                              └───drives──→ Insights (new)
```

But the interesting edges are the ones that DON'T follow the default flow:

- **Frameworks → Insights** (generative direction): A framework predicts something, generating a new insight to investigate
- **Syntheses → Frameworks** (feedback loop): Publishing reveals gaps that refine the model
- **Insights ↔ Insights** (tension edges): Productive contradictions between domains
- **Experience → Frameworks** (invalidation): Lived experience can override theoretical models

---

## The Lifecycle System

### Three Phases of a Note

Notes are not born with fixed properties. They transition through lifecycle phases, and the agent should **detect** transitions rather than require manual declaration.

```
┌──────────────┐      ┌───────────────┐      ┌──────────────┐
│  REFLECTIVE  │ ───→ │ CRYSTALLIZING │ ───→ │  GENERATIVE  │
│              │      │               │      │              │
│ Tracks       │      │ Beginning to  │      │ Actively     │
│ sources      │      │ generate own  │      │ drives new   │
│              │      │ connections   │      │ notes        │
│ Authority:   │      │ Authority:    │      │ Authority:   │
│ sources win  │      │ contested     │      │ this note    │
│              │      │               │      │ wins         │
└──────────────┘      └───────────────┘      └──────────────┘
```

### Detection Signals (Not Manual Tags)

The agent detects lifecycle phase through behavioral signals:

| Signal | Measurement | Threshold |
|--------|-------------|-----------|
| **Citation frequency** | How often is this note referenced in NEW notes? | >5 citations in 30 days → crystallizing |
| **Generative ratio** | Outbound "generated-from-this" edges / inbound "derives-from" edges | Ratio > 1.0 → crystallizing; > 2.0 → generative |
| **Cross-domain reach** | Number of distinct thematic clusters citing this note | 3+ clusters → generative |
| **Temporal acceleration** | Is citation rate increasing over time? | Positive derivative → crystallizing |
| **Prediction generation** | Does this note produce testable claims? | Any prediction → generative candidate |

**Example from existing vault:**
- "Uncertainty-Dopamine-Belief Loop" has in-degree 149, drives notes across neuroscience, Buddhism, behavioral economics, and AI adoption. Generative ratio >>2.0. This is a generative framework even though it started as a pattern noticed across reflective notes.

### Lifecycle Transitions Are Gradual, Not Discrete

The system maintains a **generativity score** (0.0 to 1.0) rather than hard categories:

- 0.0-0.3: Reflective - sources are authoritative
- 0.3-0.6: Crystallizing - authority is contested, flag conflicts for human review
- 0.6-1.0: Generative - this note is authoritative over its downstream

The agent surfaces transitions: *"This note appears to have crossed from reflective to crystallizing - it's now driving connections across 3 domains that its sources don't cover. Consider promoting to framework status."*

---

## The Tension Edge: Contradictions as Features

This is the most important departure from the code-world artifact dependency graph. In software, contradictions are bugs. In a brain, contradictions are often the most productive zones in the entire graph.

### What Makes a Tension Edge

A tension edge connects two notes that:
- Are in genuine intellectual contradiction
- The contradiction is INTENTIONAL and PRODUCTIVE
- Neither side "wins" - the tension IS the value
- Resolution would destroy insight, not create it

### Properties

| Property | Value |
|----------|-------|
| Direction | Bidirectional (neither side is authoritative) |
| Staleness propagation | Zero (immune to propagation) |
| Mode | N/A - tension transcends generative/reflective |
| Conflict resolution | NEVER automatic - always surfaces to human |
| Synthesis signal | HIGH - tension zones are where articles and new frameworks emerge |

### Example From Existing Vault

**Neuroscience of belief rigidity** ↔ **Buddhist release of attachment**

- Neuroscience says: belief rigidity is neurological reality, changing minds is physically painful
- Buddhism says: attachment to all views creates suffering, release them
- These directly contradict. But the tension generated at least three original frameworks and multiple articles
- If a coherence engine had "resolved" this by flagging one side as stale, it would have destroyed the most valuable intellectual territory in the vault

### The Agent's Role With Tensions

1. **Detect** potential tensions (notes with high semantic similarity but opposing conclusions)
2. **Surface** them as synthesis opportunities, not problems
3. **Track** what has emerged from the tension zone (which frameworks, articles, insights were born here?)
4. **Never resolve** automatically - the human decides if a contradiction is productive or a genuine error

---

## Staleness Propagation

### The Cascade Problem

A hub note like "Flow is a selfless state" (365 connections) cannot flag 365 notes as stale when it changes. The system needs **attenuated propagation**.

### Propagation Rules

```
staleness_signal(target) = change_magnitude(source) × edge_decay(type) × distance_decay(hops)
```

**Edge decay by type:**
```
derives-from:    0.8   (tight coupling - high propagation)
instantiates:    0.7   (structural coupling)
references:      0.2   (loose coupling - low propagation)
associates:      0.05  (thematic only - near-zero)
tension:         0.0   (immune)
supersedes:      1.0   (full propagation - old version is dead)
```

**Distance decay:**
```
1 hop:  1.0
2 hops: 0.5
3 hops: 0.1
4+ hops: 0.0 (propagation stops)
```

**Lateral inhibition for hubs:**
When a note has >50 connections, apply a dampening factor:
```
hub_dampening = 50 / connection_count
```
This prevents high-degree hubs from generating noise cascades.

### Staleness Threshold

A note is flagged for review only when:
```
staleness_signal > 0.3
```

With this threshold and attenuation:
- A change to a hub note (365 connections) would flag ~15-30 notes for review
- A change to a framework note (20 tight derivations) would flag ~15 notes
- A change to a leaf note would flag 0-2 notes

### Direction Matters

Staleness propagates **only along the generative direction**:
- Framework changes → downstream insights are potentially stale (YES)
- Source material changes → framework that already transcended the source (NO - framework may have other supporting evidence)
- Insight changes → MOC needs rebuilding (YES - MOC is reflective)

---

## The Graph Schema

### Per-Note Metadata (Sidecar JSON)

All BDG metadata is stored in a single sidecar file (`data/graph_enrichments.json`), NOT in note frontmatter. This design decision keeps vault notes untouched - the BDG layer is fully additive and can be removed without affecting any notes.

```json
{
  "nodes": {
    "02-Permanent/Uncertainty-Dopamine-Belief Loop.md": {
      "layer": "framework",
      "lifecycle": 0.72,
      "staleness_score": 0.0,
      "last_coherence_check": "2026-04-01",
      "classification_confidence": 0.85
    }
  }
}
```

**Why not frontmatter?**
- Vault notes are the user's creative space - BDG metadata is system state, not content
- Frontmatter changes would create noisy git diffs across hundreds of files
- Lifecycle scores change frequently (weekly recomputation) - writing to 2,500+ files is wasteful
- The sidecar survives note edits and can be rebuilt from scratch via `bootstrap --force`

### Per-Edge Metadata (Sidecar JSON)

Edge types are also stored in the sidecar, keyed by `source||target`:

```json
{
  "edges": {
    "02-Permanent/Uncertainty-Dopamine-Belief Loop.md||02-Permanent/Dopamine.md": {
      "edge_type": "derives-from",
      "authority": "target",
      "confidence": 0.75,
      "original_type": "explicit"
    },
    "02-Permanent/Uncertainty-Dopamine-Belief Loop.md||02-Permanent/Buddhist Release of Attachment.md": {
      "edge_type": "tension",
      "authority": "none",
      "confidence": 0.80,
      "original_type": "explicit"
    }
  }
}
```

Note content and wiki-links remain unchanged. The BDG classifies existing `[[wiki-links]]` into typed edges using layer-based heuristics - it does not modify the links themselves.

### Central Graph Definition

A top-level `brain-graph.yaml` declares the structural rules:

```yaml
# brain-graph.yaml
# Declares artifact types, default relationships, and propagation rules

artifact_types:
  signal:
    layer: 1
    default_mode: reflective
    vault_paths: [01-Sources/]
    description: "Raw inputs - books, papers, conversations"
    
  impression:
    layer: 2
    default_mode: reflective
    vault_paths: [00-Inbox/]
    description: "First-pass captures, fleeting notes"
    
  insight:
    layer: 3
    default_mode: mixed  # determined by lifecycle score
    vault_paths: [02-Permanent/, AI Extracted Notes/]
    description: "Atomic permanent notes"
    
  framework:
    layer: 4
    default_mode: generative
    vault_paths: [02-Permanent/]  # subset, tagged
    description: "Original mental models and theories"
    
  lens:
    layer: 5
    default_mode: reflective
    vault_paths: [03-MOCs/]
    description: "Maps of content, navigational indices"
    
  synthesis:
    layer: 6
    default_mode: reflective
    vault_paths: [04-Output/]
    description: "Articles, essays, composed output"
    
  index:
    layer: 7
    default_mode: reflective
    vault_paths: [05-Meta/]
    description: "Structural meta - analysis, changelogs"

default_edges:
  # Layer 1 → 2
  - from_type: signal
    to_type: impression
    edge_type: derives-from
    authority: source  # signal is authoritative for empirical claims
    
  # Layer 2 → 3
  - from_type: impression
    to_type: insight
    edge_type: derives-from
    authority: target  # insight is YOUR interpretation
    
  # Layer 3 → 4 (emergence)
  - from_type: insight
    to_type: framework
    edge_type: derives-from
    authority: target  # framework transcends individual insights
    
  # Layer 4 → 3 (generation)
  - from_type: framework
    to_type: insight
    edge_type: instantiates
    authority: source  # framework drives new insights
    
  # Layer 3 → 5
  - from_type: insight
    to_type: lens
    edge_type: derives-from
    authority: source  # MOC reflects its member notes
    
  # Layer 4 → 6
  - from_type: framework
    to_type: synthesis
    edge_type: instantiates
    authority: source  # framework drives article
    
  # Layer 3 → 6
  - from_type: insight
    to_type: synthesis
    edge_type: derives-from
    authority: source  # insights drive article content

propagation:
  edge_decay:
    derives-from: 0.8
    instantiates: 0.7
    references: 0.2
    associates: 0.05
    tension: 0.0
    supersedes: 1.0
  distance_decay: [1.0, 0.5, 0.1, 0.0]
  hub_threshold: 50
  staleness_threshold: 0.3
  max_propagation_depth: 3

lifecycle:
  detection_window_days: 30
  crystallizing_threshold: 0.3
  generative_threshold: 0.6
  signals:
    citation_frequency:
      weight: 0.3
      crystallizing_min: 5  # citations in window
    generative_ratio:
      weight: 0.3
      crystallizing_min: 1.0
      generative_min: 2.0
    cross_domain_reach:
      weight: 0.25
      crystallizing_min: 2  # distinct clusters
      generative_min: 3
    temporal_acceleration:
      weight: 0.15
      crystallizing_min: 0.0  # positive derivative
```

---

## Agent Behavior: The Coherence Engine

### Event-Driven Responses

| Event | Agent Reasoning | Action |
|-------|----------------|--------|
| **Note created** | Classify layer and mode. Find upstream sources. Create edges. | Add to graph, compute initial lifecycle score |
| **Note substantially edited** | Walk downstream edges. Compute staleness for targets. | Flag targets above threshold for review |
| **Framework revised** | High-impact change. Walk all `instantiates` and `derives-from` edges downstream. | Generate staleness report, prioritized by propagation strength |
| **New source ingested** | Walk forward to impressions and insights that cite this source. | Flag reflective notes that may need updating |
| **Tension detected** | Two notes with high similarity but opposing conclusions. | Surface as synthesis opportunity, suggest article topic |
| **Lifecycle transition** | Behavioral signals cross threshold. | Notify: "This note appears to be crystallizing/generative" |
| **Periodic coherence sweep** | Walk entire graph computing staleness scores. | Produce coherence report: stale notes, orphaned nodes, emerging hubs |

### The Coherence Report

Generated periodically (weekly) or on-demand:

```markdown
# Brain Coherence Report - 2026-04-04

## Staleness Alerts (12 notes above threshold)
1. **"Dopamine drives exploration behavior"** (staleness: 0.67)
   - Upstream change: "Dopamine" framework revised 2026-03-28
   - Edge: derives-from (decay: 0.8)
   - Action needed: Review if the exploration claim still holds under revised model

2. **"AI agents need curiosity mechanisms"** (staleness: 0.54)
   - Upstream change: Same dopamine revision, 2 hops away
   - Edge: instantiates → derives-from (decay: 0.7 × 0.5 = 0.35)
   - Action needed: Light review

## Lifecycle Transitions (3 notes)
1. **"Context = Perspective + Information"** 
   - Score: 0.31 → 0.58 (crossed crystallizing threshold)
   - Cited by 8 new notes in 30 days across 3 clusters
   - Recommendation: Consider promoting to framework

## Productive Tensions (2 new)
1. **"Free will is compatible with determinism"** ↔ **"Buddhist dependent origination eliminates agency"**
   - Similarity: 0.82, Conclusion alignment: -0.7
   - Synthesis potential: HIGH
   - No existing article covers this intersection

## Structural Health
- Orphaned notes: 4 (no edges)
- Hub overload: "Flow is a selfless state" (387 edges, +22 since last check)
- Cluster gaps: AI Safety cluster still has no MOC
```

---

## Propagation Skills

Skills bound to specific edge types, triggered by changes:

### /propagate-framework-change
```yaml
trigger: framework note substantially edited
source_type: framework
edge_types: [instantiates, derives-from]
action: |
  1. Walk downstream edges (max depth 3)
  2. Compute staleness score per target
  3. Filter by threshold (>0.3)
  4. Generate prioritized review list
  5. For each flagged note, show:
     - What changed upstream
     - What claim in this note might be affected
     - Suggested action (review / update / OK)
```

### /propagate-source-update
```yaml
trigger: source material re-read or updated
source_type: signal
edge_types: [derives-from]
target_filter: lifecycle < 0.3  # only reflective notes
action: |
  1. Find all impressions and insights derived from this source
  2. Filter to reflective notes only (generative notes have transcended the source)
  3. Diff the source change against each target's claims
  4. Flag factual discrepancies
```

### /detect-tensions
```yaml
trigger: periodic (weekly) or on new note creation
action: |
  1. For each new/recently modified note:
     - Find notes with high semantic similarity (>0.75)
     - Check conclusion alignment (sentiment/stance analysis)
     - If high similarity + opposing conclusions → potential tension
  2. Check if tension edge already exists
  3. If new tension: surface as synthesis opportunity
  4. Track what has emerged from existing tension zones
```

### /rebuild-lens
```yaml
trigger: member insights change
source_type: insight
target_type: lens
action: |
  1. Identify which MOC contains the changed insight
  2. Rebuild MOC by re-scanning all member notes
  3. Update section headings, link lists, and summaries
  4. Flag any new notes that should be members but aren't
```

### /compute-lifecycle
```yaml
trigger: periodic (weekly)
action: |
  1. For each insight and framework note:
     - Count citations in last 30 days
     - Compute generative ratio (outbound/inbound)
     - Measure cross-domain reach
     - Calculate temporal acceleration
  2. Update lifecycle score
  3. Flag transitions that cross thresholds
  4. Surface promotion candidates
```

### /coherence-sweep
```yaml
trigger: periodic (weekly) or on-demand
action: |
  1. Walk entire graph computing staleness
  2. Detect orphaned nodes
  3. Identify hub overload
  4. Find cluster gaps (groups of notes with no lens)
  5. Detect new tensions
  6. Generate coherence report
```

---

## Mapping to Existing Vault

### Current Structure → Graph Layers

| Current Path | Graph Layer | Default Mode |
|---|---|---|
| `00-Inbox/` | Impression | Reflective |
| `01-Sources/` | Signal | Reflective |
| `02-Permanent/` | Insight (most), Framework (tagged subset) | Mixed |
| `03-MOCs/` | Lens | Reflective |
| `04-Output/Articles/` | Synthesis | Reflective |
| `05-Meta/` | Index | Reflective |
| `AI Extracted Notes/` | Insight | Reflective (initially) |
| `Document Insights/` | Insight (external) | Reflective |

### Bootstrapping the Graph

The graph doesn't need to be built from scratch. It can be bootstrapped from existing signals:

1. **Wiki-links** → Convert to typed edges using heuristics:
   - Link from Source → Permanent Note = `derives-from`
   - Link from Permanent Note → MOC = `derives-from` (note drives MOC)
   - Link between Permanent Notes in different clusters = `references` or `tension` (analyze content)
   - Link from Framework → Permanent Note = `instantiates`

2. **Semantic similarity** (already computed by Local Brain Search) → `associates` edges

3. **Lifecycle scores** → Compute from existing graph metrics (in-degree, out-degree, betweenness centrality)

4. **Tension detection** → Run once across all note pairs with high similarity + opposing conclusions

---

## Design Principles

### 1. The Agent is a Gardener, Not an Engineer

The brain is a collaborative space. The agent prunes, suggests, and surfaces patterns - but never decides that a living branch is dead wood just because it doesn't fit the trellis. All resolution of generative conflicts requires human judgment.

### 2. Detect, Don't Declare

Lifecycle transitions, tension edges, and authority relationships should be detected from behavioral signals wherever possible. Manual tagging is a fallback, not the primary mechanism. The system learns from how the human uses the knowledge base.

### 3. Authority is Contextual

The same note can be authoritative in one relationship and subordinate in another. Authority lives on edges, not nodes. This prevents the false hierarchy that kills creative knowledge bases.

### 4. Contradictions are Assets

The system must distinguish between:
- **Errors** (a reflective note that contradicts its source → fix it)
- **Evolution** (a generative note that contradicts its earlier version → update downstream)
- **Productive tensions** (two notes that contradict across domains → celebrate it, surface synthesis opportunities)

### 5. Staleness Propagates With Attenuation

Hub notes cannot create noise cascades. Decay by edge type, distance, and hub dampening ensure that only genuinely affected notes are flagged.

### 6. The Graph is the Agent's Operating Context

Like `CLAUDE.md` for code agents, `brain-graph.yaml` becomes part of the agent's loaded context. The agent doesn't rely on ad-hoc rules ("update MOCs when permanent notes change") - it derives behavior from the graph structure.

---

## What This Architecture Enables

1. **Coherence at scale** - 2,740+ notes stay internally consistent without manual tracking
2. **Intellectual honesty** - The system knows which claims are empirically grounded vs. original speculation
3. **Creative protection** - Productive contradictions are preserved and surfaced, not resolved
4. **Emergent structure** - Frameworks are detected as they form, not forced into existence
5. **Directed maintenance** - When something changes, the agent knows exactly what else needs attention
6. **Provenance tracking** - Every claim can be traced to its authority source through directed edges
7. **Synthesis intelligence** - Tension zones, lifecycle transitions, and cross-domain reach become explicit signals for article generation

---

## Implementation Phases

### Phase 1: Schema & Bootstrap
- Define `brain-graph.yaml` with artifact types and default edges
- Classify all notes into layers via sidecar JSON (no frontmatter changes)
- Bootstrap edge types from existing wiki-links using heuristics
- Compute initial lifecycle scores from graph metrics

### Phase 2: Propagation Engine
- Build staleness computation (edge decay × distance decay × hub dampening)
- Implement `/propagate-framework-change` skill
- Implement `/coherence-sweep` skill
- Generate first coherence report

### Phase 3: Lifecycle Detection
- Implement behavioral signal tracking (citation frequency, generative ratio, cross-domain reach)
- Build `/compute-lifecycle` skill
- Surface lifecycle transitions in coherence reports

### Phase 4: Tension System
- Build tension detection (high similarity + opposing conclusions)
- Implement tension edge type with immunity properties
- Track synthesis artifacts emerging from tension zones
- Surface synthesis opportunities

### Phase 5: Full Integration
- Graph loaded as agent operating context alongside CLAUDE.md
- All note CRUD operations automatically update the graph
- Propagation runs on every substantial edit
- Weekly coherence reports generated automatically
- Lifecycle transitions trigger agent notifications

---

*Architecture designed 2026-04-04. Inspired by the Artifact Dependency Graph pattern applied to knowledge management rather than software development.*
