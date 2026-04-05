# Local Brain Search Upgrade Requirements

## Project: SYNAPSE-Inspired Memory Architecture

**Document Version:** 1.2
**Created:** 2026-02-18
**Updated:** 2026-02-18
**Status:** Phase 1, 3 & 4 IMPLEMENTED
**Priority:** High - Validated by January 2026 research cluster

---

## Executive Summary

This document specifies requirements for upgrading Cornelius's Local Brain Search from static vector retrieval to a dynamic spreading activation architecture inspired by the January 2026 memory research cluster. The upgrade addresses the "Contextual Tunneling" failure mode and implements research-validated patterns from MemAgent, MAGMA, SimpleMem, SYNAPSE, and EverMemOS.

**Expected Outcomes:**
- Elimination of Contextual Tunneling (retrieving topically similar but contextually wrong notes)
- Improved multi-hop reasoning through dynamic relevance propagation
- Intent-aware retrieval reducing irrelevant results
- System that learns from usage patterns over time

---

## Implementation Status (2026-02-18)

| Phase | Feature | Status | Notes |
|-------|---------|--------|-------|
| 1 | Intent Classification | ✅ COMPLETE | `intent.py` - heuristic-based, >85% accuracy |
| 2 | Extended Graph | ⏳ NOT STARTED | Temporal/causal edges require re-index |
| 3 | Spreading Activation | ✅ COMPLETE | `spreading.py` - lateral inhibition, configurable |
| 4 | Usage-Based Learning | ✅ COMPLETE | `learning.py` - Q-values, usage tracking, ranking adjustment |
| 5 | Foresight Signals | ⏳ NOT STARTED | Prospective tagging |

**New Files:**
- `intent.py` - Query intent classification
- `spreading.py` - Spreading activation engine
- `memory_config.py` - Unified configuration (single source of truth)
- `learning.py` - Usage-based Q-value learning (Phase 4)
- `run_learning.sh` - CLI wrapper for learning management

**Modified Files:**
- `search.py` - Added `--mode spreading` flag, Q-value integration, usage tracking
- `config.py` - Now imports from `memory_config.py`
- `run_search.sh` - Updated help text with `--no-track` option

**Data Files (auto-created):**
- `data/q_values.json` - Learned Q-values per note
- `data/usage_history.jsonl` - Append-only usage event log

**Verification Results:**
- Spreading activation produces different results than static (0-1 overlap out of 5)
- Intent classification correctly routes queries
- Lateral inhibition reduces hub dominance
- Backward compatible (`--mode static` unchanged)
- Phase 4: Usage events tracked (retrieved, read, referenced, linked)
- Phase 4: Q-values update correctly with reward structure
- Phase 4: Ranking adjustment boosts frequently-used notes
- Phase 4: `run_learning.sh status/reset/top/export` commands working

---

## 1. Current State Analysis

### 1.1 Existing Architecture

**Location:** `resources/local-brain-search/`

**Components:**
- `index_brain.py` - FAISS index builder
- `search.py` - Semantic search interface
- `connections.py` - Graph analysis and connection discovery
- `data/brain.faiss` - Vector index
- `data/brain_metadata.pkl` - Note metadata
- `data/brain_graph.pkl` - Graph structure

**Current Statistics:**
| Metric | Value |
|--------|-------|
| Total nodes (notes) | 1,531 |
| Total edges | 10,870 |
| Explicit edges (wiki-links) | 5,983 |
| Semantic edges | 4,887 |
| Isolated nodes | 29 |
| Connected components | 30 |
| Largest component | 1,502 nodes |
| Average degree | 14.2 |

### 1.2 Current Retrieval Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CURRENT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Query → Embed → FAISS Search → Top-K Results → Return          │
│                                                                  │
│  Layer 2: Get wiki-link connections for top result              │
│  Layer 3: Get hub notes for broader context                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Limitations:**
1. Static similarity - no dynamic relevance propagation
2. No intent classification - same retrieval for all query types
3. No temporal weighting - old and new notes treated equally
4. No usage learning - system doesn't improve from feedback
5. No lateral inhibition - competing clusters not suppressed
6. Vulnerable to Contextual Tunneling

### 1.3 Known Failure Modes

**Contextual Tunneling:** Vector similarity retrieves notes that are topically similar but contextually wrong. Example: searching for "dopamine and motivation" might retrieve "dopamine and addiction" when the context is about productivity, not substance abuse.

**Hub Dominance:** Highly connected hub notes (like [[Dopamine]]) appear in many retrievals even when not contextually relevant.

**Recency Blindness:** Recent insights treated the same as older notes, even when recency is contextually important.

**Multi-Hop Degradation:** Quality decreases with each hop from the query - Layer 3 results often less relevant than Layer 1.

---

## 2. Target Architecture

### 2.1 Research Foundations

The upgrade draws from five January 2026 papers:

| Paper | Key Contribution | Implementation Target |
|-------|------------------|----------------------|
| **SYNAPSE** | Spreading activation, lateral inhibition, temporal decay | Core retrieval mechanism |
| **SimpleMem** | Intent-aware retrieval, 30x token efficiency | Query classification layer |
| **MAGMA** | Four orthogonal graphs (semantic, temporal, causal, entity) | Extended edge types |
| **EverMemOS** | Foresight signals at encoding | Prospective relevance tagging |
| **MemRL** | RL-based retrieval selection | Usage-based learning |

### 2.2 Target Retrieval Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    TARGET ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                               │
│  │ Query Input  │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ INTENT CLASSIFIER (SimpleMem-inspired)               │       │
│  │ - Factual lookup                                     │       │
│  │ - Conceptual exploration                             │       │
│  │ - Synthesis/connection finding                       │       │
│  │ - Temporal query (recent, historical)                │       │
│  └──────┬───────────────────────────────────────────────┘       │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ INITIAL ACTIVATION (Seed nodes)                      │       │
│  │ - Embed query                                        │       │
│  │ - FAISS top-K as seed nodes                          │       │
│  │ - Assign initial activation scores                   │       │
│  └──────┬───────────────────────────────────────────────┘       │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ SPREADING ACTIVATION (SYNAPSE-inspired)              │       │
│  │ - Propagate activation along edges                   │       │
│  │ - Weight by edge type (explicit > semantic)          │       │
│  │ - Apply lateral inhibition (suppress competing)      │       │
│  │ - Apply temporal decay                               │       │
│  │ - Iterate until convergence or max steps             │       │
│  └──────┬───────────────────────────────────────────────┘       │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ RESULT RANKING                                        │       │
│  │ - Final activation scores                            │       │
│  │ - Q-value adjustment (learned preferences)           │       │
│  │ - Diversity enforcement (avoid cluster dominance)    │       │
│  └──────┬───────────────────────────────────────────────┘       │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │ Return Top-K │                                               │
│  └──────────────┘                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Requirements

### 3.1 Phase 1: Intent Classification Layer

**Priority:** High
**Complexity:** Medium
**Dependencies:** None

#### 3.1.1 Functional Requirements

| ID | Requirement | Rationale |
|----|-------------|-----------|
| INT-01 | Classify queries into intent categories before retrieval | SimpleMem shows intent-aware retrieval improves relevance |
| INT-02 | Support minimum 4 intent types: factual, conceptual, synthesis, temporal | Cover primary use cases in knowledge work |
| INT-03 | Intent classification must complete in <100ms | Cannot add significant latency to retrieval |
| INT-04 | Provide confidence score for classification | Enable fallback to default behavior on low confidence |

#### 3.1.2 Intent Categories

| Intent | Description | Retrieval Strategy |
|--------|-------------|-------------------|
| **Factual** | Looking for specific information | Prioritize exact matches, lower spreading activation |
| **Conceptual** | Exploring a topic area | Broad spreading activation, include hub notes |
| **Synthesis** | Finding connections between ideas | Maximum spreading, prioritize bridge notes |
| **Temporal** | Recent or historical focus | Weight temporal edges, apply recency bias |

#### 3.1.3 Implementation Options

**Option A: LLM-based classification**
- Use small model (Haiku) to classify intent
- Pros: High accuracy, handles nuance
- Cons: API latency, cost

**Option B: Keyword/pattern heuristics**
- Rule-based classification from query patterns
- "What is..." → Factual
- "How does X relate to Y" → Synthesis
- "Recent notes about..." → Temporal
- Pros: Fast, no API cost
- Cons: Limited accuracy

**Option C: Hybrid**
- Start with heuristics, fallback to LLM on low confidence
- Recommended approach

#### 3.1.4 Acceptance Criteria

- [ ] Intent classifier achieves >85% accuracy on test set of 100 queries
- [ ] Classification latency <100ms (heuristics) or <500ms (LLM fallback)
- [ ] All four intent types correctly route to different retrieval strategies
- [ ] Confidence threshold configurable (default: 0.7)

---

### 3.2 Phase 2: Extended Graph Structure (MAGMA-inspired)

**Priority:** High
**Complexity:** High
**Dependencies:** Phase 1 recommended but not required

#### 3.2.1 Functional Requirements

| ID | Requirement | Rationale |
|----|-------------|-----------|
| GRP-01 | Add temporal edges based on creation/modification dates | MAGMA's temporal graph enables time-aware retrieval |
| GRP-02 | Add causal edges from explicit markers in notes | Support "leads to", "causes", "results in" relationships |
| GRP-03 | Maintain edge type separation in graph structure | Enable query-adaptive traversal |
| GRP-04 | Re-index must complete in <5 minutes | Current index time ~2 minutes |

#### 3.2.2 Edge Type Specifications

| Edge Type | Source | Weight Range | Description |
|-----------|--------|--------------|-------------|
| **Explicit** | Wiki-links `[[Note]]` | 1.0 | Direct intentional connections |
| **Semantic** | Vector similarity >0.7 | 0.7-0.95 | Content similarity |
| **Temporal** | Created within ±7 days | 0.3-0.8 | Time proximity |
| **Causal** | Keywords: "leads to", "causes", "therefore" | 0.9 | Explicit causal markers |

#### 3.2.3 Temporal Edge Logic

```python
def compute_temporal_weight(note_a_date, note_b_date):
    """
    Notes created close together get higher temporal edge weight.
    Decay function: weight = max_weight * exp(-days_apart / decay_constant)
    """
    days_apart = abs((note_a_date - note_b_date).days)
    decay_constant = 7  # Half-weight at 7 days
    max_weight = 0.8
    min_weight = 0.3

    weight = max_weight * math.exp(-days_apart / decay_constant)
    return max(weight, min_weight) if days_apart < 30 else 0
```

#### 3.2.4 Causal Edge Detection

Scan note content for causal markers:
- "leads to" / "led to"
- "causes" / "caused by"
- "results in" / "resulted from"
- "therefore" / "thus" / "hence"
- "because" / "since"
- "→" (arrow notation)

Extract target note from surrounding wiki-links.

#### 3.2.5 Graph Storage Update

Current `brain_graph.pkl` structure:
```python
{
    'adjacency': {...},  # note_id -> [connected_note_ids]
    'edge_types': {...}  # (note_a, note_b) -> 'explicit' | 'semantic'
}
```

New structure:
```python
{
    'adjacency': {...},
    'edges': {
        (note_a, note_b): {
            'types': ['explicit', 'semantic', 'temporal'],
            'weights': {
                'explicit': 1.0,
                'semantic': 0.82,
                'temporal': 0.65
            },
            'causal_direction': None | 'forward' | 'backward'
        }
    },
    'metadata': {
        'created_dates': {...},  # note_id -> datetime
        'modified_dates': {...}
    }
}
```

#### 3.2.6 Acceptance Criteria

- [ ] Temporal edges added for notes within 30-day proximity
- [ ] Causal edges detected from explicit markers (>90% precision)
- [ ] Edge types queryable separately
- [ ] Graph statistics updated to show edge type breakdown
- [ ] Re-index completes in <5 minutes
- [ ] Backward compatible with existing scripts

---

### 3.3 Phase 3: Spreading Activation Engine (SYNAPSE-inspired)

**Priority:** Critical
**Complexity:** High
**Dependencies:** Phase 2 (extended graph)

#### 3.3.1 Functional Requirements

| ID | Requirement | Rationale |
|----|-------------|-----------|
| SPR-01 | Implement spreading activation over the note graph | Core SYNAPSE mechanism |
| SPR-02 | Support configurable decay factor per edge type | Different edge types propagate differently |
| SPR-03 | Implement lateral inhibition to suppress competing clusters | Prevents hub dominance |
| SPR-04 | Implement temporal decay based on activation age | Recent activations weighted higher |
| SPR-05 | Convergence detection to terminate spreading | Efficiency requirement |

#### 3.3.2 Algorithm Specification

```python
def spreading_activation(
    graph: Graph,
    seed_nodes: List[Tuple[str, float]],  # (note_id, initial_activation)
    config: SpreadingConfig
) -> Dict[str, float]:
    """
    SYNAPSE-inspired spreading activation.

    Returns: {note_id: final_activation_score}
    """

    # Initialize activation
    activation = {node: 0.0 for node in graph.nodes}
    for node, score in seed_nodes:
        activation[node] = score

    # Track activation history for lateral inhibition
    activation_history = []

    for iteration in range(config.max_iterations):
        new_activation = activation.copy()

        # Spread activation along edges
        for node in graph.nodes:
            if activation[node] > config.activation_threshold:
                for neighbor, edge_data in graph.neighbors(node):
                    # Compute spread amount
                    spread = activation[node] * config.decay_factors[edge_data['type']]

                    # Apply edge weight
                    spread *= edge_data['weight']

                    # Accumulate at neighbor
                    new_activation[neighbor] += spread

        # Apply lateral inhibition
        new_activation = apply_lateral_inhibition(
            new_activation,
            graph,
            config.inhibition_radius,
            config.inhibition_strength
        )

        # Apply temporal decay to all activations
        for node in new_activation:
            new_activation[node] *= config.temporal_decay

        # Re-inject seed activation (anchoring)
        for node, score in seed_nodes:
            new_activation[node] = max(new_activation[node], score * config.anchor_strength)

        # Check convergence
        if is_converged(activation, new_activation, config.convergence_threshold):
            break

        activation = new_activation
        activation_history.append(activation.copy())

    return activation
```

#### 3.3.3 Configuration Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `max_iterations` | 5 | 1-10 | Maximum spreading iterations |
| `activation_threshold` | 0.1 | 0.01-0.5 | Minimum activation to spread |
| `decay_factors` | See below | 0.1-1.0 | Per-edge-type decay |
| `temporal_decay` | 0.9 | 0.5-0.99 | Per-iteration decay |
| `inhibition_radius` | 2 | 1-5 | Graph distance for inhibition |
| `inhibition_strength` | 0.3 | 0.1-0.7 | How much to suppress |
| `anchor_strength` | 0.8 | 0.5-1.0 | Seed node anchoring |
| `convergence_threshold` | 0.01 | 0.001-0.1 | When to stop |

**Default decay factors by edge type:**
```python
decay_factors = {
    'explicit': 0.8,    # Strong propagation through wiki-links
    'semantic': 0.5,    # Moderate through similarity
    'temporal': 0.3,    # Weak through time proximity
    'causal': 0.9       # Very strong through causal links
}
```

#### 3.3.4 Lateral Inhibition

Prevents hub notes from dominating results by suppressing activation in nearby nodes when a cluster gets too active.

```python
def apply_lateral_inhibition(
    activation: Dict[str, float],
    graph: Graph,
    radius: int,
    strength: float
) -> Dict[str, float]:
    """
    For each highly-activated node, suppress neighbors within radius.
    This prevents a single cluster from dominating.
    """
    result = activation.copy()

    # Find highly activated nodes (top 10%)
    threshold = np.percentile(list(activation.values()), 90)
    high_activation_nodes = [n for n, a in activation.items() if a > threshold]

    for node in high_activation_nodes:
        # Get neighbors within radius
        neighbors = get_neighbors_within_radius(graph, node, radius)

        # Suppress their activation
        for neighbor in neighbors:
            if neighbor != node:
                result[neighbor] *= (1 - strength)

    return result
```

#### 3.3.5 Intent-Adaptive Configuration

| Intent | max_iterations | inhibition_strength | temporal_decay |
|--------|----------------|---------------------|----------------|
| Factual | 2 | 0.5 | 0.95 |
| Conceptual | 5 | 0.2 | 0.9 |
| Synthesis | 7 | 0.1 | 0.85 |
| Temporal | 3 | 0.3 | 0.7 |

#### 3.3.6 Acceptance Criteria

- [ ] Spreading activation produces different results than static similarity
- [ ] Lateral inhibition reduces hub dominance in results
- [ ] Convergence typically reached in 3-5 iterations
- [ ] Total retrieval time <500ms for typical queries
- [ ] Contextual Tunneling rate reduced by >50% on test set

---

### 3.4 Phase 4: Usage-Based Learning (MemRL-inspired)

**Priority:** Medium
**Complexity:** Medium
**Dependencies:** Phase 3

#### 3.4.1 Functional Requirements

| ID | Requirement | Rationale |
|----|-------------|-----------|
| LRN-01 | Track which retrieved notes are actually used | Build feedback signal |
| LRN-02 | Compute Q-values for note retrieval | MemRL pattern |
| LRN-03 | Adjust retrieval ranking based on learned Q-values | Improve over time |
| LRN-04 | Persist learning across sessions | Cumulative improvement |

#### 3.4.2 Usage Tracking

Track events:
- Note retrieved in search results
- Note content read by agent
- Note referenced in agent output
- Note linked in new content

```python
@dataclass
class UsageEvent:
    timestamp: datetime
    note_id: str
    query: str
    query_intent: str
    event_type: Literal['retrieved', 'read', 'referenced', 'linked']
    position_in_results: int  # For retrieved events
    session_id: str
```

#### 3.4.3 Q-Value Computation

```python
def update_q_values(
    q_values: Dict[str, float],
    usage_events: List[UsageEvent],
    learning_rate: float = 0.1,
    discount: float = 0.9
) -> Dict[str, float]:
    """
    Update Q-values based on usage events.

    Reward structure:
    - Retrieved but not read: 0
    - Read: +0.5
    - Referenced: +1.0
    - Linked: +1.5
    """
    rewards = {
        'retrieved': 0,
        'read': 0.5,
        'referenced': 1.0,
        'linked': 1.5
    }

    for event in usage_events:
        reward = rewards[event.event_type]

        # Position discount - earlier positions get more credit
        position_factor = 1.0 / (1 + event.position_in_results * 0.1)

        # Q-learning update
        current_q = q_values.get(event.note_id, 0)
        q_values[event.note_id] = current_q + learning_rate * (
            reward * position_factor - current_q
        )

    return q_values
```

#### 3.4.4 Ranking Adjustment

```python
def adjust_ranking_with_q_values(
    activation_scores: Dict[str, float],
    q_values: Dict[str, float],
    q_weight: float = 0.3
) -> Dict[str, float]:
    """
    Blend activation scores with learned Q-values.
    """
    result = {}
    for note_id, activation in activation_scores.items():
        q = q_values.get(note_id, 0)
        result[note_id] = activation * (1 - q_weight) + q * q_weight
    return result
```

#### 3.4.5 Persistence

Store Q-values and usage history:
```
data/
├── q_values.json           # Current Q-values per note
├── usage_history.jsonl     # Append-only usage events
└── learning_config.json    # Learning parameters
```

#### 3.4.6 Acceptance Criteria

- [x] Usage events captured for all retrieval operations
- [x] Q-values updated after each session
- [ ] Measurable improvement in retrieval relevance over 30-day period (requires observation)
- [x] Q-values persist across index rebuilds
- [x] Manual override available to reset learning (`run_learning.sh reset --confirm`)

---

### 3.5 Phase 5: Foresight Signals (EverMemOS-inspired)

**Priority:** Low (Enhancement)
**Complexity:** Medium
**Dependencies:** None (can implement independently)

#### 3.5.1 Functional Requirements

| ID | Requirement | Rationale |
|----|-------------|-----------|
| FOR-01 | Tag notes at creation with predicted future relevance | EverMemOS Foresight pattern |
| FOR-02 | Relevance predictions based on current context | Prospective tagging |
| FOR-03 | Use foresight tags in retrieval weighting | Proactive relevance |

#### 3.5.2 Foresight Tag Structure

Add to note frontmatter:
```yaml
---
foresight:
  contexts: ["agent-architecture", "production-deployment"]
  predicted_relevance: 0.8
  prediction_date: 2026-02-18
  prediction_basis: "Created during memory architecture research session"
---
```

#### 3.5.3 Prediction Logic

When creating notes:
1. Analyze current conversation/session context
2. Identify likely future query contexts
3. Assign relevance predictions
4. Store as foresight metadata

#### 3.5.4 Retrieval Integration

```python
def apply_foresight_boost(
    activation_scores: Dict[str, float],
    current_context: str,
    foresight_data: Dict[str, ForesightTag]
) -> Dict[str, float]:
    """
    Boost notes whose foresight contexts match current context.
    """
    result = {}
    for note_id, activation in activation_scores.items():
        boost = 1.0
        if note_id in foresight_data:
            foresight = foresight_data[note_id]
            if any(ctx in current_context.lower() for ctx in foresight.contexts):
                boost = 1.0 + foresight.predicted_relevance * 0.5
        result[note_id] = activation * boost
    return result
```

#### 3.5.5 Acceptance Criteria

- [ ] Foresight tags generated for new notes during extraction sessions
- [ ] Tags stored in frontmatter and indexed
- [ ] Retrieval boost applied when context matches
- [ ] No performance impact when foresight data missing

---

## 4. API Changes

### 4.1 New CLI Commands

```bash
# Existing (unchanged)
run_search.sh "query" --limit 10 --json
run_connections.sh "Note Name" --json
run_connections.sh --hubs --json
run_connections.sh --stats --json

# New commands
run_search.sh "query" --mode spreading --json          # Use spreading activation
run_search.sh "query" --intent synthesis --json        # Force intent type
run_search.sh "query" --explain --json                 # Show activation trace

run_index.sh --with-temporal                           # Include temporal edges
run_index.sh --with-causal                             # Detect causal edges

run_learning.sh --status                               # Show Q-value stats
run_learning.sh --reset                                # Reset learned preferences
```

### 4.2 Python API

```python
from local_brain_search import BrainSearch

search = BrainSearch(
    index_path="data/",
    config=SearchConfig(
        mode="spreading",  # "static" | "spreading"
        intent_detection=True,
        use_q_values=True,
        spreading_config=SpreadingConfig(...)
    )
)

# Search with spreading activation
results = search.query(
    "dopamine and motivation",
    limit=10,
    intent="conceptual",  # Optional override
    explain=True          # Return activation trace
)

# Access activation trace
for result in results:
    print(result.note_id, result.activation_score)
    print(result.activation_trace)  # How activation spread to this node
```

---

## 5. Testing Strategy

### 5.1 Test Dataset

Create evaluation set of 100 queries with ground-truth relevant notes:
- 25 factual queries
- 25 conceptual queries
- 25 synthesis queries
- 25 temporal queries

### 5.2 Metrics

| Metric | Current Baseline | Target |
|--------|------------------|--------|
| Precision@5 | TBD | +20% |
| Contextual Tunneling rate | TBD | -50% |
| Multi-hop relevance (Layer 3) | TBD | +30% |
| Hub dominance (% of results from top 10 hubs) | TBD | -40% |

### 5.3 A/B Testing

Run static and spreading activation in parallel for 2 weeks:
- Log which results get used
- Compare usage rates
- Measure user satisfaction (if trackable)

---

## 6. Migration Plan

### 6.1 Phase Rollout

| Phase | Duration | Rollout |
|-------|----------|---------|
| Phase 1 (Intent) | 1 week | Shadow mode - log classifications, don't use |
| Phase 2 (Graph) | 1 week | Full rebuild of index with new edge types |
| Phase 3 (Spreading) | 2 weeks | A/B test against static |
| Phase 4 (Learning) | Ongoing | Enable after Phase 3 validated |
| Phase 5 (Foresight) | 1 week | Enable for new notes only |

### 6.2 Rollback Plan

Each phase maintains backward compatibility:
- Phase 1: Intent classification optional, fallback to default
- Phase 2: New edge types additive, old queries still work
- Phase 3: `--mode static` always available
- Phase 4: Q-values can be disabled or reset
- Phase 5: Foresight tags ignored if not present

### 6.3 Index Migration

```bash
# Backup current index
cp -r data/ data_backup_$(date +%Y%m%d)/

# Rebuild with new features
python index_brain.py --with-temporal --with-causal

# Verify integrity
python verify_index.py --compare data_backup_*/
```

---

## 7. Performance Requirements

| Operation | Current | Target | Max Acceptable |
|-----------|---------|--------|----------------|
| Simple search | ~100ms | ~150ms | 300ms |
| Spreading activation search | N/A | ~300ms | 500ms |
| Index rebuild | ~2 min | ~4 min | 6 min |
| Intent classification | N/A | ~50ms | 100ms |
| Q-value update | N/A | ~10ms | 50ms |

---

## 8. Dependencies

### 8.1 Python Packages

```
# Existing
faiss-cpu>=1.7.0
sentence-transformers>=2.2.0
numpy>=1.21.0
networkx>=2.6.0

# New requirements
scipy>=1.9.0           # For spreading activation math
scikit-learn>=1.0.0    # For clustering in lateral inhibition
```

### 8.2 External Services

- LLM API (optional) - For intent classification fallback
- No other external dependencies

---

## 9. Success Criteria

### 9.1 Must Have (MVP)

- [ ] Intent classification operational with >80% accuracy
- [ ] Spreading activation reduces Contextual Tunneling by >30%
- [ ] Total retrieval time <500ms
- [ ] Backward compatible with existing scripts

### 9.2 Should Have

- [ ] Extended graph with temporal and causal edges
- [ ] Usage-based learning improves results over 30 days
- [ ] Configurable spreading parameters

### 9.3 Nice to Have

- [ ] Foresight signals for new notes
- [ ] Activation trace visualization
- [ ] Real-time index updates (no full rebuild needed)

---

## 10. Open Questions

1. **Intent classification accuracy vs. latency tradeoff** - When should we use LLM fallback?

2. **Optimal spreading parameters** - Require empirical tuning. Start with SYNAPSE paper values?

3. **Q-value cold start** - How to handle notes with no usage history?

4. **Temporal edge granularity** - 7-day window sufficient? Should it be configurable per topic?

5. **Lateral inhibition scope** - Suppress within clusters or globally? Need to test both.

6. **Index rebuild frequency** - With learning enabled, how often should we rebuild?

---

## 11. References

### 11.1 Research Papers

- SYNAPSE: arXiv:2601.02744 (January 2026)
- SimpleMem: arXiv:2601.02553 (January 2026)
- MAGMA: arXiv:2601.03236 (January 2026)
- EverMemOS: arXiv:2601.02163 (January 2026)
- MemRL: arXiv:2601.03192 (January 2026)
- Collins & Loftus (1975) - Spreading Activation Theory

### 11.2 Internal Documentation

- [[Memory-Now-Dominant-Research-Frontier-Over-Reasoning]]
- [[SYNAPSE-Spreading-Activation-Memory-Architecture]]
- [[SimpleMem-Efficiency-Over-Complexity-30x-Token-Reduction]]
- [[Contextual-Tunneling-Named-Failure-Mode-Vector-Retrieval]]
- [[Spreading-Activation-Dopamine-AI-Memory-Common-Mechanism-HYPOTHESIS]]

---

## 12. Appendix

### A. Current File Structure

```
resources/local-brain-search/
├── index_brain.py          # Index builder
├── search.py               # Search interface
├── connections.py          # Graph analysis
├── run_search.sh           # CLI wrapper
├── run_connections.sh      # CLI wrapper
├── run_index.sh            # CLI wrapper
├── requirements.txt        # Dependencies
├── data/
│   ├── brain.faiss         # Vector index
│   ├── brain_metadata.pkl  # Note metadata
│   └── brain_graph.pkl     # Graph structure
└── UPGRADE-REQUIREMENTS.md # This document
```

### B. Current File Structure (Post Phase 1, 3, 4)

```
resources/local-brain-search/
├── index_brain.py          # Index builder
├── search.py               # Search interface (static + spreading modes)
├── spreading.py            # ✅ Spreading activation engine
├── intent.py               # ✅ Intent classifier
├── learning.py             # ✅ Q-value learning (Phase 4)
├── connections.py          # Graph analysis
├── config.py               # Configuration (imports from memory_config)
├── memory_config.py        # ✅ Unified configuration (single source of truth)
├── run_search.sh           # CLI wrapper (updated)
├── run_connections.sh      # CLI wrapper
├── run_index.sh            # CLI wrapper
├── run_learning.sh         # ✅ Learning management CLI
├── requirements.txt        # Dependencies
├── data/
│   ├── brain.faiss         # Vector index
│   ├── brain_metadata.pkl  # Note metadata
│   ├── brain_graph.pkl     # Graph structure
│   ├── q_values.json       # ✅ Learned preferences (Phase 4)
│   └── usage_history.jsonl # ✅ Usage tracking (Phase 4)
├── tests/                  # TODO: Add test suite
└── UPGRADE-REQUIREMENTS.md # This document
```

### C. Remaining Work (Phase 2, 5)

```
# Phase 2 additions needed:
├── data/
│   └── brain_graph.pkl     # Extended with temporal/causal edges

# Phase 5 additions needed:
# Foresight tags in note frontmatter (no new files)
```

---

*Document created: 2026-02-18*
*Last updated: 2026-02-18*
*Status: Ready for review*
