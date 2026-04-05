# Memory System Benchmark Requirements

**Version:** 1.0
**Created:** 2026-02-18
**Status:** Draft - Ready for Implementation

---

## 1. Overview

### 1.1 Objective

Create a systematic benchmarking framework to:
1. Measure retrieval quality objectively using LLM-as-judge scoring
2. Compare different configuration settings
3. Identify optimal parameters for different query types
4. Generate reproducible results against a frozen test dataset

### 1.2 Design Principles

- **Contained**: One skill + one sub-agent + bundled scripts
- **Reproducible**: Test against frozen Brain snapshot
- **Automated**: LLM-as-judge for relevance scoring
- **Analyzable**: CSV output for Python analysis

### 1.3 Research Foundation

Based on current best practices from:
- [RAGAS evaluation framework](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [LLM-as-Judge guide by Evidently AI](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
- [RAG Evaluation best practices 2025](https://www.getmaxim.ai/articles/complete-guide-to-rag-evaluation-metrics-methods-and-best-practices-for-2025/)

---

## 2. Test Brain Snapshot

### 2.1 Purpose

The knowledge base is actively developed. To ensure reproducible benchmarks:
- Create a frozen snapshot of the Brain at a point in time
- Run all benchmarks against this snapshot
- Relevance scores remain valid across config changes
- Can re-run experiments without re-scoring

### 2.2 Snapshot Structure

```
resources/local-brain-search/benchmarks/
├── snapshots/
│   └── brain-snapshot-2026-02-18/
│       ├── Brain/                    # Frozen copy of Brain folder
│       ├── data/
│       │   ├── brain.faiss          # Index built from snapshot
│       │   ├── brain_metadata.pkl
│       │   └── brain_graph.pkl
│       └── SNAPSHOT-INFO.md         # Metadata about snapshot
├── query-sets/
│   └── core-50.json                 # Test queries with ground truth
├── results/
│   └── benchmark-2026-02-18-*.csv   # Benchmark results
└── analysis/
    └── *.ipynb                      # Analysis notebooks
```

### 2.3 Snapshot Creation Process

```bash
# 1. Create snapshot directory
SNAPSHOT_DATE=$(date +%Y-%m-%d)
SNAPSHOT_DIR="benchmarks/snapshots/brain-snapshot-$SNAPSHOT_DATE"
mkdir -p "$SNAPSHOT_DIR"

# 2. Copy Brain folder (excluding .obsidian, .trash)
rsync -av --exclude='.obsidian' --exclude='.trash' \
  ../../Brain/ "$SNAPSHOT_DIR/Brain/"

# 3. Build index for snapshot
BRAIN_PATH="$SNAPSHOT_DIR/Brain" python index_brain.py \
  --output "$SNAPSHOT_DIR/data/"

# 4. Create snapshot info
echo "Snapshot Date: $SNAPSHOT_DATE" > "$SNAPSHOT_DIR/SNAPSHOT-INFO.md"
echo "Notes Count: $(find $SNAPSHOT_DIR/Brain -name '*.md' | wc -l)" >> "$SNAPSHOT_DIR/SNAPSHOT-INFO.md"
```

---

## 3. Query Test Set

### 3.1 Query Categories

| Category | Count | Purpose | Example |
|----------|-------|---------|---------|
| **Factual** | 10 | Single concept lookup | "What is dopamine?" |
| **Conceptual** | 10 | Topic exploration | "How does motivation work?" |
| **Synthesis** | 15 | Cross-domain connections | "Connect Buddhism and neuroscience" |
| **Temporal** | 5 | Recent/historical focus | "Recent notes about AI agents" |
| **Needle** | 5 | Specific note retrieval | "Note about intermittent reinforcement" |
| **Broad** | 5 | High-level topic | "Identity" |
| **Total** | 50 | | |

### 3.2 Query Set Schema

```json
{
  "version": "1.0",
  "created": "2026-02-18",
  "snapshot": "brain-snapshot-2026-02-18",
  "queries": [
    {
      "id": "q001",
      "query": "What is dopamine?",
      "category": "factual",
      "expected_intent": "factual",
      "notes": "Should retrieve Dopamine.md as top result",
      "ground_truth_notes": [
        "02-Permanent/Dopamine.md",
        "03-MOCs/MOC - Dopamine and Reward Systems.md"
      ]
    },
    {
      "id": "q002",
      "query": "Connect Buddhism and neuroscience consciousness",
      "category": "synthesis",
      "expected_intent": "synthesis",
      "notes": "Should find cross-domain bridges",
      "ground_truth_notes": [
        "02-Permanent/In Buddhism - Self is an Illusion.md",
        "02-Permanent/Flow is a selfless state.md",
        "02-Permanent/Duhkha and Dopamine - Buddhist Suffering Meets Neuroscience Craving.md"
      ]
    }
  ]
}
```

### 3.3 Ground Truth Options

For each query, ground truth can be:
1. **Manual**: Human-labeled relevant notes (most accurate)
2. **Wiki-link derived**: Notes linked from expected results
3. **LLM-generated**: Initial relevance assessment (to be validated)

**Recommendation**: Start with LLM-generated ground truth, manually validate top 20 queries.

---

## 4. Metrics

### 4.1 Performance Metrics (Automatic)

| Metric | Description | Collection |
|--------|-------------|------------|
| `latency_ms` | Query execution time | `time.time()` |
| `iterations` | Spreading iterations used | From metadata |
| `converged` | Whether spreading converged | From metadata |
| `seed_count` | Initial FAISS results | From metadata |

### 4.2 Retrieval Quality Metrics

| Metric | Formula | Range | Description |
|--------|---------|-------|-------------|
| **Precision@K** | `relevant_in_top_k / k` | 0-1 | Fraction of results that are relevant |
| **Recall@K** | `relevant_in_top_k / total_relevant` | 0-1 | Fraction of relevant notes found |
| **MRR** | `1 / rank_of_first_relevant` | 0-1 | Mean Reciprocal Rank |
| **NDCG@K** | Normalized DCG | 0-1 | Ranking quality with position discount |
| **Avg Score** | `mean(relevance_scores)` | 0-3 | Average LLM relevance score |
| **Diversity** | `unique_clusters / k` | 0-1 | Topic spread in results |

### 4.3 Metric Computation

```python
def compute_metrics(results: list, relevance_scores: list, ground_truth: list) -> dict:
    """
    results: list of note_ids returned by search
    relevance_scores: LLM scores (0-3) for each result
    ground_truth: list of known relevant note_ids
    """
    k = len(results)

    # Binary relevance (score >= 2 is relevant)
    relevant = [1 if s >= 2 else 0 for s in relevance_scores]

    # Precision@K
    precision = sum(relevant) / k if k > 0 else 0

    # Recall@K (if ground truth available)
    if ground_truth:
        found = sum(1 for r in results if r in ground_truth)
        recall = found / len(ground_truth)
    else:
        recall = None

    # MRR
    mrr = 0
    for i, rel in enumerate(relevant):
        if rel:
            mrr = 1 / (i + 1)
            break

    # NDCG@K
    dcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(relevance_scores))
    ideal = sorted(relevance_scores, reverse=True)
    idcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(ideal))
    ndcg = dcg / idcg if idcg > 0 else 0

    # Average score
    avg_score = np.mean(relevance_scores)

    return {
        'precision_at_k': precision,
        'recall_at_k': recall,
        'mrr': mrr,
        'ndcg_at_k': ndcg,
        'avg_score': avg_score,
    }
```

---

## 5. LLM-as-Judge Scoring

### 5.1 Scoring Scale

Based on best practices, use a **4-point scale** (0-3):

| Score | Label | Definition |
|-------|-------|------------|
| **0** | Irrelevant | No connection to query; wrong topic entirely |
| **1** | Tangential | Loosely related; mentions similar concepts but doesn't address query |
| **2** | Relevant | Addresses the query; contains useful information |
| **3** | Highly Relevant | Directly answers or is essential for answering the query |

### 5.2 Judge Prompt Template

```
You are evaluating the relevance of a retrieved note for a knowledge base search query.

## Query
{query}

## Query Intent
{intent} (factual/conceptual/synthesis/temporal)

## Retrieved Note
Title: {note_title}
Content (excerpt):
{note_content_excerpt}

## Scoring Instructions

Rate the relevance of this note to the query on a 0-3 scale:

0 = IRRELEVANT: No connection to query; wrong topic entirely
1 = TANGENTIAL: Loosely related; mentions similar concepts but doesn't address query
2 = RELEVANT: Addresses the query; contains useful information
3 = HIGHLY RELEVANT: Directly answers or is essential for answering the query

Consider:
- Does the note contain information that helps answer/explore the query?
- For synthesis queries: Does it bridge the concepts mentioned?
- For factual queries: Does it provide the specific information requested?
- For conceptual queries: Does it explain or explore the topic?

## Response Format

Return JSON only:
{
  "reasoning": "Brief explanation of your scoring (1-2 sentences)",
  "score": <0-3>
}
```

### 5.3 Judge Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Model | `claude-sonnet-4-20250514` | Good balance of quality/cost |
| Temperature | 0.0 | Consistent scoring |
| Max tokens | 150 | Short, structured response |
| Format | JSON | Easy parsing |

### 5.4 Bias Mitigation

1. **No position information**: Don't tell judge the result's rank
2. **Consistent excerpts**: Always use same content length (500 chars)
3. **Batch scoring**: Score all results for a query in random order
4. **Calibration set**: Manually validate 20% of scores

### 5.5 Cost Estimation

| Component | Per Query | For 50 Queries × 10 Results |
|-----------|-----------|----------------------------|
| Input tokens | ~400 | ~200,000 |
| Output tokens | ~50 | ~25,000 |
| **Est. Cost** | ~$0.01 | **~$5.00 per benchmark run** |

---

## 6. Configuration Space

### 6.1 Parameters to Test

| Parameter | Values | Default | Impact |
|-----------|--------|---------|--------|
| `mode` | static, spreading | spreading | Core algorithm |
| `seed_count` | 5, 10, 15 | 10 | Initial retrieval breadth |
| `max_iterations` | 2, 5, 7 | 5 | Spreading depth |
| `inhibition_strength` | 0.1, 0.3, 0.5 | 0.3 | Hub suppression |
| `temporal_decay` | 0.8, 0.9, 0.95 | 0.9 | Activation persistence |
| `q_weight` | 0.0, 0.3, 0.5 | 0.3 | Learning influence |
| `edge_decay_explicit` | 0.7, 0.8, 0.9 | 0.8 | Wiki-link propagation |
| `edge_decay_semantic` | 0.4, 0.5, 0.6 | 0.5 | Similarity propagation |

### 6.2 Focused Test Configurations

For initial benchmarking, test these 15 configurations:

```python
FOCUSED_CONFIGS = [
    # Baseline
    {"name": "static_baseline", "mode": "static"},
    {"name": "spreading_default", "mode": "spreading"},

    # Iteration sweep
    {"name": "spreading_iter2", "mode": "spreading", "max_iterations": 2},
    {"name": "spreading_iter7", "mode": "spreading", "max_iterations": 7},

    # Inhibition sweep
    {"name": "spreading_inhib_low", "mode": "spreading", "inhibition_strength": 0.1},
    {"name": "spreading_inhib_high", "mode": "spreading", "inhibition_strength": 0.5},

    # Decay sweep
    {"name": "spreading_decay_low", "mode": "spreading", "temporal_decay": 0.8},
    {"name": "spreading_decay_high", "mode": "spreading", "temporal_decay": 0.95},

    # Q-value sweep
    {"name": "spreading_no_learning", "mode": "spreading", "q_weight": 0.0},
    {"name": "spreading_high_learning", "mode": "spreading", "q_weight": 0.5},

    # Edge decay sweep
    {"name": "spreading_strong_explicit", "mode": "spreading", "edge_decay_explicit": 0.9},
    {"name": "spreading_weak_semantic", "mode": "spreading", "edge_decay_semantic": 0.4},

    # Combined optimizations (hypotheses)
    {"name": "synthesis_optimized", "mode": "spreading", "max_iterations": 7, "inhibition_strength": 0.1},
    {"name": "factual_optimized", "mode": "spreading", "max_iterations": 2, "inhibition_strength": 0.5},
    {"name": "balanced_optimized", "mode": "spreading", "max_iterations": 5, "inhibition_strength": 0.2, "temporal_decay": 0.85},
]
```

### 6.3 Per-Intent Configurations

After baseline, test intent-specific optimizations:

| Intent | Hypothesis | Test Config |
|--------|-----------|-------------|
| Factual | Low iterations, high inhibition | iter=2, inhib=0.5 |
| Conceptual | Medium spread, include hubs | iter=5, inhib=0.2 |
| Synthesis | Max spread, low inhibition | iter=7, inhib=0.1 |
| Temporal | Needs temporal edges (Phase 2) | baseline for now |

---

## 7. Implementation Architecture

### 7.1 Component Structure

```
.claude/skills/benchmark-memory/
├── SKILL.md                    # Skill definition and usage
├── scripts/
│   ├── create_snapshot.py      # Create frozen Brain snapshot
│   ├── build_query_set.py      # Generate/manage query test set
│   ├── run_benchmark.py        # Execute benchmark with config
│   ├── score_results.py        # LLM-as-judge scoring
│   ├── compute_metrics.py      # Calculate evaluation metrics
│   └── analyze_results.py      # Generate analysis summary
├── configs/
│   ├── focused_configs.json    # Test configurations
│   └── judge_prompt.txt        # LLM judge prompt template
└── README.md                   # Detailed documentation
```

### 7.2 Sub-Agent: benchmark-runner

```yaml
name: benchmark-runner
description: Execute memory benchmarks with LLM-as-judge scoring
tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
```

**Responsibilities:**
1. Load query set and configuration
2. Run searches against snapshot
3. Score results using LLM-as-judge
4. Compute metrics
5. Save results to CSV

### 7.3 Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  /benchmark-memory setup                                     │
│  - Create Brain snapshot                                     │
│  - Build index for snapshot                                  │
│  - Initialize query set (or load existing)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  /benchmark-memory run --config focused                      │
│  For each config in focused_configs:                         │
│    For each query in query_set:                              │
│      1. Execute search with config                           │
│      2. Score each result (LLM-as-judge)                     │
│      3. Compute metrics                                      │
│      4. Append to results CSV                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  /benchmark-memory analyze                                   │
│  - Load results CSV                                          │
│  - Compute aggregates by config, by query category           │
│  - Identify best configs per intent                          │
│  - Generate summary report                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Output Format

### 8.1 Results CSV Schema

```csv
timestamp,config_name,query_id,query_category,query_intent,mode,max_iterations,inhibition_strength,temporal_decay,q_weight,latency_ms,iterations_used,converged,result_1_note,result_1_score,result_2_note,result_2_score,...,result_10_note,result_10_score,precision_at_5,precision_at_10,mrr,ndcg_at_10,avg_score
```

### 8.2 Example Row

```csv
2026-02-18T15:30:00,spreading_default,q001,factual,factual,spreading,5,0.3,0.9,0.3,342,3,true,02-Permanent/Dopamine.md,3,03-MOCs/MOC - Dopamine.md,3,...,0.8,0.7,1.0,0.92,2.4
```

### 8.3 Summary CSV

Aggregated results for analysis:

```csv
config_name,query_category,n_queries,avg_precision_5,avg_precision_10,avg_mrr,avg_ndcg,avg_score,avg_latency_ms
spreading_default,factual,10,0.82,0.74,0.95,0.88,2.5,320
spreading_default,synthesis,15,0.71,0.65,0.78,0.76,2.1,450
...
```

---

## 9. Usage

### 9.1 Initial Setup

```bash
# Create snapshot and build index
/benchmark-memory setup

# Or manually:
cd resources/local-brain-search
python scripts/create_snapshot.py --date 2026-02-18
```

### 9.2 Create Query Set

```bash
# Generate initial query set (LLM-assisted)
/benchmark-memory create-queries --count 50

# Or load existing
/benchmark-memory load-queries --file query-sets/core-50.json
```

### 9.3 Run Benchmark

```bash
# Run focused configs (15 configurations × 50 queries)
/benchmark-memory run --config focused --snapshot brain-snapshot-2026-02-18

# Run single config
/benchmark-memory run --config spreading_default --snapshot brain-snapshot-2026-02-18
```

### 9.4 Analyze Results

```bash
# Generate analysis
/benchmark-memory analyze --results results/benchmark-2026-02-18-*.csv

# Open in Python
python -c "import pandas as pd; df = pd.read_csv('results/benchmark-*.csv'); print(df.groupby('config_name').mean())"
```

---

## 10. Success Criteria

### 10.1 Benchmark System

- [ ] Snapshot creation works and produces valid index
- [ ] Query set covers all categories (50+ queries)
- [ ] LLM judge produces consistent scores (>80% agreement on re-run)
- [ ] All 15 focused configs can be benchmarked
- [ ] Results CSV is valid and analyzable
- [ ] Total benchmark time < 2 hours for full run

### 10.2 Expected Insights

After running benchmarks, we should be able to answer:

1. **Does spreading beat static?** For which query types?
2. **Optimal iterations**: Is 5 better than 7 for synthesis?
3. **Inhibition impact**: Does high inhibition help factual queries?
4. **Learning value**: Does q_weight > 0 improve results over time?
5. **Best per-intent configs**: What settings work best for each query type?

---

## 11. Future Extensions

### 11.1 Phase 2 Additions

Once temporal/causal edges are implemented:
- Add temporal edge weight parameter
- Add causal edge weight parameter
- Test temporal queries properly

### 11.2 Advanced Metrics

- **Faithfulness**: Do results support the eventual answer?
- **Diversity score**: Using embedding clustering
- **Novelty**: Results not in ground truth but still valuable

### 11.3 Continuous Benchmarking

- Run weekly against latest snapshot
- Track metric trends over time
- Alert on significant regressions

---

## 12. Dependencies

### 12.1 Python Packages

```
# Already in requirements.txt
faiss-cpu
sentence-transformers
networkx
numpy

# Additional for benchmarking
pandas>=2.0.0
anthropic>=0.40.0  # For LLM judge
tqdm>=4.65.0       # Progress bars
```

### 12.2 API Keys

- `ANTHROPIC_API_KEY` - For LLM-as-judge scoring

---

## 13. Cost & Time Estimates

### 13.1 Per Benchmark Run

| Component | Count | Time | Cost |
|-----------|-------|------|------|
| Queries | 50 | - | - |
| Configs | 15 | - | - |
| Results per query | 10 | - | - |
| **Total searches** | 750 | ~60 min | $0 |
| **Total LLM scores** | 7,500 | ~30 min | ~$75 |
| **Total** | - | **~90 min** | **~$75** |

### 13.2 Reduced Cost Options

1. **Score top 5 only**: 3,750 scores → ~$37
2. **Use Haiku for judge**: ~$7.50 (10x cheaper, slightly less accurate)
3. **Cache scores**: Re-use scores when config doesn't change retrieval

**Recommendation**: Start with Haiku judge, validate sample against Sonnet.

---

---

## 14. Learnings from Supermemory Project

Your previous project `<your-supermemory-path>/` contains valuable research and implementation patterns relevant to this benchmark:

### 14.1 Key Research Insights (from `research_smart_mem.md`)

**Testing and Evaluation Best Practices (Section VIII.D):**
- "Rigorously test the system with a diverse set of queries and scenarios, targeting different parts and complexities of the JSON data"
- "Evaluate the relevance of retrieved information, the coherence of the generated subsets, and compliance with context window limitations"
- Implement feedback loops for continuous improvement

**The "Contextual Tunneling" Problem:**
- Vector similarity can retrieve "topically similar but contextually wrong" results
- This is exactly what spreading activation aims to solve
- Benchmark should specifically test for this failure mode

**Hybrid Retrieval Strategies:**
- Combine path-based, semantic (vector), and graph-based retrieval
- Different query types benefit from different strategies
- Our intent classification + spreading activation is a form of this

### 14.2 Relevant Implementation Patterns

**From `memory_service.py`:**
```python
# Token counting for response management
def count_tokens(text: str, model_name: str) -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

# Size management with iterative truncation
for _attempt in range(3):
    token_count = count_tokens(json_output)
    if token_count <= max_tokens:
        break
    # Truncate and retry
```

**From PRD (`prd.md`):**
- Schema endpoint: Understand structure before querying
- Natural language querying with LlamaIndex
- Response size management with `max_tokens` parameter

### 14.3 Benchmark Additions Based on Supermemory Research

| New Test | Rationale |
|----------|-----------|
| **Contextual Tunneling Detection** | Identify queries where static retrieves topically similar but contextually wrong notes |
| **Context Coherence** | Score whether results form a coherent context (not just individually relevant) |
| **Response Size Management** | Test that results fit within token budgets |
| **Schema Awareness** | Test if spreading follows graph structure appropriately |

### 14.4 Recommended Query Categories (Extended)

Based on supermemory research, add these query types:

| Category | Purpose | Example |
|----------|---------|---------|
| **Multi-hop** | Requires traversing connections | "What connects dopamine to Buddhism?" |
| **Aggregative** | Count or summarize | "How many notes about AI agents?" |
| **Structural** | Navigate by structure | "What's in the MOCs folder?" |
| **Ambiguous** | Tests disambiguation | "Flow" (could be psychology or programming) |

---

*Document created: 2026-02-18*
*Updated: 2026-02-18 (added supermemory insights)*
*Ready for implementation*
