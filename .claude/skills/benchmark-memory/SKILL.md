---
name: benchmark-memory
description: Systematic benchmarking framework for Local Brain Search memory system with LLM-as-judge scoring
automation: gated
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Task
user-invocable: true
---

# Benchmark Memory System

Systematic benchmarking framework to measure retrieval quality, compare configurations, and identify optimal parameters for the Local Brain Search memory system.

## Purpose

1. **Measure retrieval quality objectively** using LLM-as-judge scoring
2. **Compare different configuration settings** (spreading vs static, parameter sweeps)
3. **Identify optimal parameters** for different query types (factual, conceptual, synthesis)
4. **Generate reproducible results** against frozen test datasets

## Design Principles

- **Contained**: Skill + sub-agent + bundled scripts
- **Reproducible**: Test against frozen Brain snapshot
- **Automated**: LLM-as-judge for relevance scoring
- **Analyzable**: CSV output for analysis

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Brain snapshot | `.claude/skills/benchmark-memory/snapshots/` | Yes | Yes |
| Query sets | `.claude/skills/benchmark-memory/query-sets/` | Yes | Yes |
| Benchmark results | `.claude/skills/benchmark-memory/results/` | Yes | Yes |
| Analysis reports | `.claude/skills/benchmark-memory/analysis/` | No | Yes |
| Memory system | `resources/local-brain-search/` | Yes | No |

## Prerequisites

- Local Brain Search system indexed (`resources/local-brain-search/data/brain.faiss`)
- Python venv at `resources/local-brain-search/venv/` with search dependencies
- Claude Code CLI installed and authenticated (for LLM-as-judge scoring via headless mode)

### LLM-as-Judge Scoring

This skill uses **Claude Code headless mode** (`claude -p`) for LLM relevance scoring, not a separate API key. This means:

- No `ANTHROPIC_API_KEY` environment variable needed
- Uses your existing Claude Code authentication
- Default model: `sonnet` (good quality) - can also use `haiku` (faster/cheaper) or `opus`
- JSON output via prompt engineering for reliable scoring

To verify Claude Code is available:
```bash
claude --version
```

### Installing Dependencies

Dependencies are installed in the local-brain-search venv:

```bash
cd resources/local-brain-search
source venv/bin/activate
pip install pandas tqdm  # anthropic not required - uses Claude Code headless
```

## Sub-Commands

### `/benchmark-memory setup`

Create a frozen Brain snapshot and build its index.

```bash
cd .claude/skills/benchmark-memory/scripts
./run_benchmark.sh --list-snapshots  # Check existing
python3 create_snapshot.py           # Create new snapshot
```

**What it does:**
1. Creates snapshot directory with date stamp
2. Copies Brain folder (excluding .obsidian, .trash)
3. Builds FAISS index for the snapshot
4. Creates SNAPSHOT-INFO.md with metadata

### `/benchmark-memory create-queries [--count N]`

Generate or manage test query sets.

```bash
cd .claude/skills/benchmark-memory/scripts
python build_query_set.py --count 50 --output ../query-sets/core-50.json
```

**Query Categories (50 total):**
| Category | Count | Example |
|----------|-------|---------|
| Factual | 10 | "What is dopamine?" |
| Conceptual | 10 | "How does motivation work?" |
| Synthesis | 15 | "Connect Buddhism and neuroscience" |
| Temporal | 5 | "Recent notes about AI agents" |
| Needle | 5 | "Note about intermittent reinforcement" |
| Broad | 5 | "Identity" |

### `/benchmark-memory run [--config CONFIG] [--snapshot SNAPSHOT]`

Execute benchmark with specified configuration.

```bash
cd .claude/skills/benchmark-memory/scripts
./run_benchmark.sh --config focused --snapshot brain-snapshot-2026-02-18
./run_benchmark.sh --dry-run --config focused  # Preview without execution
./run_benchmark.sh --list-configs              # List available configs
```

**Configurations:**
- `focused`: 15 key configurations (recommended for initial benchmarking)
- `single:CONFIG_NAME`: Run single configuration
- `all`: Full parameter sweep (expensive)

**Estimated cost per run:**
- 50 queries x 10 results x 15 configs = 7,500 LLM scores
- Using Sonnet (default): ~$75
- Using Haiku: ~$7.50

### `/benchmark-memory analyze [--results FILE]`

Generate analysis summary from benchmark results.

```bash
cd .claude/skills/benchmark-memory/scripts
python analyze_results.py --results ../results/benchmark-*.csv
```

**Outputs:**
- Summary by configuration
- Summary by query category
- Best config per intent
- Recommendations

## Workflow

```
Step 1: Setup (one-time)
/benchmark-memory setup
    |
    v
Step 2: Create Queries (one-time)
/benchmark-memory create-queries --count 50
    |
    v
Step 3: Run Benchmark (per experiment)
/benchmark-memory run --config focused
    |
    v
Step 4: Analyze Results
/benchmark-memory analyze
```

## Metrics Collected

### Performance Metrics
| Metric | Description |
|--------|-------------|
| `latency_ms` | Query execution time |
| `iterations` | Spreading iterations used |
| `converged` | Whether spreading converged |

### Quality Metrics
| Metric | Range | Description |
|--------|-------|-------------|
| **Precision@K** | 0-1 | Fraction of results that are relevant |
| **Recall@K** | 0-1 | Fraction of relevant notes found |
| **MRR** | 0-1 | Mean Reciprocal Rank |
| **NDCG@K** | 0-1 | Ranking quality with position discount |
| **Avg Score** | 0-3 | Average LLM relevance score |

### LLM-as-Judge Scoring Scale
| Score | Label | Definition |
|-------|-------|------------|
| 0 | Irrelevant | No connection to query |
| 1 | Tangential | Loosely related |
| 2 | Relevant | Addresses the query |
| 3 | Highly Relevant | Directly answers the query |

## Configurations to Test

### Baseline
- `static_baseline`: Traditional vector search
- `spreading_default`: Spreading activation with defaults

### Parameter Sweeps
- Iteration count: 2, 5, 7
- Inhibition strength: 0.1, 0.3, 0.5
- Temporal decay: 0.8, 0.9, 0.95
- Q-weight: 0.0, 0.3, 0.5

### Optimized Combinations
- `synthesis_optimized`: max_iterations=7, inhibition=0.1
- `factual_optimized`: max_iterations=2, inhibition=0.5
- `balanced_optimized`: max_iterations=5, inhibition=0.2, decay=0.85

## Output Files

### Results CSV
```
results/benchmark-YYYY-MM-DD-HHMMSS.csv
```

Schema:
```
timestamp,config_name,query_id,query_category,mode,max_iterations,
inhibition_strength,latency_ms,result_1_note,result_1_score,...,
precision_at_5,precision_at_10,mrr,ndcg_at_10,avg_score
```

### Analysis Report
```
analysis/report-YYYY-MM-DD.md
```

## Error Recovery

### Partial benchmark run
Results are appended incrementally. Resume by running with `--resume`:
```bash
python run_benchmark.py --config focused --resume
```

### API rate limits
Built-in retry with exponential backoff. Adjust `--delay` if needed:
```bash
python run_benchmark.py --config focused --delay 1.0
```

### Invalid snapshot
Re-create snapshot:
```bash
python create_snapshot.py --force
```

## Success Criteria

- [ ] Snapshot creation produces valid index
- [ ] Query set covers all 6 categories (50+ queries)
- [ ] LLM judge produces consistent scores (>80% agreement on re-run)
- [ ] All 15 focused configs can be benchmarked
- [ ] Results CSV is valid and analyzable
- [ ] Analysis identifies best config per query type

## Expected Insights

After running benchmarks, answer these questions:
1. Does spreading beat static? For which query types?
2. What's the optimal iteration count for synthesis queries?
3. Does high inhibition help factual queries?
4. Does q_weight > 0 improve results over time?
5. What settings work best for each query type?

## Cost Management

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Score top 5 only | 50% | Less data on long-tail |
| Use Haiku judge | 90% | Slightly less accurate |
| Cache scores | Variable | Only for unchanged retrieval |

**Recommendation**: Start with Haiku judge, validate sample against Sonnet.

## Directory Structure

```
.claude/skills/benchmark-memory/
├── SKILL.md                    # This file
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── run_benchmark.sh        # Wrapper script (uses venv Python)
│   ├── create_snapshot.py      # Create frozen Brain snapshot
│   ├── build_query_set.py      # Generate/manage query test set
│   ├── run_benchmark.py        # Execute benchmark with config
│   ├── score_results.py        # LLM-as-judge scoring
│   ├── compute_metrics.py      # Calculate evaluation metrics
│   └── analyze_results.py      # Generate analysis summary
├── configs/
│   ├── focused_configs.json    # Test configurations (15 configs)
│   └── judge_prompt.txt        # LLM judge prompt template
├── snapshots/                  # Frozen Brain copies
├── query-sets/                 # Test queries (core-50.json included)
├── results/                    # Benchmark CSVs
└── analysis/                   # Analysis reports
```

## Tested Components

| Component | Status | Notes |
|-----------|--------|-------|
| Snapshot creation | ✅ Works | Creates snapshot with FAISS index + graph |
| Query set | ✅ Works | 50 queries across 6 categories |
| Static search | ✅ Works | Traditional vector similarity |
| Spreading search | ✅ Works | Multi-iteration activation |
| 15 configs | ✅ Works | Focused parameter sweep |
| LLM-as-judge | ✅ Works | Uses Claude Code headless mode (`claude -p`) |
| Results CSV | Ready | Incremental writes, resume support |
