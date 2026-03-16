---
name: test-memory-system
description: Comprehensive testing playbook for Local Brain Search memory improvements (Phases 1, 3, 4)
automation: manual
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
user-invocable: true
metadata:
  version: "1.0"
  created: 2026-02-18
  author: Cornelius
  related-systems:
    - local-brain-search
    - SYNAPSE-memory-architecture
---

# Test Memory System

## Purpose

Comprehensively test the new memory improvements implemented in Local Brain Search:
- **Phase 1:** Intent Classification
- **Phase 3:** Spreading Activation
- **Phase 4:** Usage-Based Learning (Q-values)

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Memory Config | `resources/local-brain-search/memory_config.py` | ✓ | | Central configuration |
| Q-Values | `resources/local-brain-search/data/q_values.json` | ✓ | | Learned preferences |
| Usage History | `resources/local-brain-search/data/usage_history.jsonl` | ✓ | | Event tracking |
| FAISS Index | `resources/local-brain-search/data/brain.faiss` | ✓ | | Vector index |
| Graph | `resources/local-brain-search/data/brain_graph.pkl` | ✓ | | Note graph |
| Test Report | `resources/memory-test-reports/` | | ✓ | Output location |

## Prerequisites

- Virtual environment activated: `source resources/local-brain-search/venv/bin/activate`
- FAISS index built: `data/brain.faiss` exists
- Graph built: `data/brain_graph.pkl` exists
- Dependencies installed: `pip install -r requirements.txt`

## Inputs

- None (runs full test suite)

---

## Process

### Step 1: Environment Verification

Verify all components are installed and accessible.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search
source venv/bin/activate

# Check files exist
ls -la data/brain.faiss data/brain_metadata.pkl data/brain_graph.pkl

# Check Python dependencies
python -c "import faiss; import networkx; import sentence_transformers; print('All dependencies OK')"

# Check new modules exist
python -c "from intent import classify_intent; from spreading import spreading_activation; from learning import get_learning_stats; print('All new modules OK')"
```

**Expected:** All files exist, all imports succeed.

---

### Step 2: Test Intent Classification

Test that queries are correctly classified into four intent types.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search
source venv/bin/activate
python intent.py
```

**Test Cases:**

| Query | Expected Intent | Confidence |
|-------|-----------------|------------|
| "What is dopamine?" | factual | >70% |
| "How does motivation work?" | conceptual | >70% |
| "Connect dopamine and Buddhism" | synthesis | >70% |
| "Recent notes about AI agents" | temporal | >70% |
| "Dopamine" | factual | >50% |
| "relationship between identity and belief" | synthesis | >70% |
| "patterns across neuroscience and AI" | synthesis | >80% |

**Record Results:**
- Total queries tested: X
- Correctly classified: Y
- Accuracy: Y/X %

---

### Step 3: Test Static vs Spreading Search

Compare results between static (traditional) and spreading activation modes.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Test 1: Static search
./run_search.sh "dopamine and motivation" --mode static --limit 5 --json | python -m json.tool

# Test 2: Spreading search (same query)
./run_search.sh "dopamine and motivation" --mode spreading --limit 5 --json | python -m json.tool

# Test 3: Synthesis query (where spreading should excel)
./run_search.sh "connect Buddhism neuroscience consciousness" --mode static --limit 5 --json
./run_search.sh "connect Buddhism neuroscience consciousness" --mode spreading --limit 5 --json
```

**Expected Results:**
- Static and spreading should produce DIFFERENT result sets
- Spreading mode should find cross-domain connections
- Spreading should reduce "hub dominance" (e.g., Dopamine note appearing in everything)

**Record:**
- Result overlap: X out of 5 (should be 0-2 for synthesis queries)
- Spreading iterations: usually 3-5
- Did spreading find non-obvious connections? Y/N

---

### Step 4: Test Intent-Adaptive Spreading

Verify that different intents produce different spreading parameters.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Factual query (should use minimal spreading)
./run_search.sh "What is dopamine?" --mode spreading --json 2>&1 | grep -E "(iterations|Intent)"

# Synthesis query (should use maximum spreading)
./run_search.sh "connect dopamine Buddhism identity" --mode spreading --json 2>&1 | grep -E "(iterations|Intent)"
```

**Expected:**
- Factual: max_iterations=2, inhibition_strength=0.5
- Conceptual: max_iterations=5, inhibition_strength=0.2
- Synthesis: max_iterations=7, inhibition_strength=0.1
- Temporal: max_iterations=3, temporal_decay=0.7

---

### Step 5: Test Lateral Inhibition

Verify that hub notes don't dominate results.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Search for topic where Dopamine.md is a known hub
./run_search.sh "motivation reward behavior" --mode spreading --limit 10 --json

# Check if Dopamine.md dominates or if diverse results appear
```

**Expected:**
- Top 10 results should include notes beyond the immediate Dopamine cluster
- Lateral inhibition suppresses over-represented clusters
- Results should show diversity across topics

**Record:**
- Number of results from Dopamine cluster: X/10
- Number of distinct topic clusters represented: Y

---

### Step 6: Test Usage-Based Learning Status

Check current learning system state.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Check learning status
./run_learning.sh status

# View top notes by Q-value
./run_learning.sh top --limit 10

# Export full learning data
./run_learning.sh export --output /tmp/learning_export.json
```

**Expected:**
- Learning enabled: True
- Events tracked with proper structure
- Q-values in reasonable range (-1.0 to 2.0)

**Record:**
- Total events tracked: X
- Unique notes with Q-values: Y
- Average Q-value: Z

---

### Step 7: Test Usage Event Tracking

Verify that search operations are being tracked.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Count events before
BEFORE=$(wc -l < data/usage_history.jsonl)

# Run a search
./run_search.sh "test query for tracking" --mode spreading --limit 5

# Count events after
AFTER=$(wc -l < data/usage_history.jsonl)

echo "Events before: $BEFORE, after: $AFTER, new: $((AFTER - BEFORE))"

# Verify event structure
tail -5 data/usage_history.jsonl | python -m json.tool
```

**Expected:**
- New events should be logged (5 for limit=5)
- Events should have: timestamp, note_id, query, query_intent, event_type, position, session_id, mode

---

### Step 8: Test Q-Value Updates

Verify that different event types produce appropriate Q-value changes.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Get current Q-value for a test note
cat data/q_values.json | python -c "import json,sys; d=json.load(sys.stdin); print(d.get('02-Permanent/Dopamine.md', 'not found'))"

# Log a read event
./run_learning.sh log read "02-Permanent/Dopamine.md" --query "test"

# Check Q-value increased
cat data/q_values.json | python -c "import json,sys; d=json.load(sys.stdin); print(d.get('02-Permanent/Dopamine.md', 'not found'))"
```

**Expected Q-value changes:**
- retrieved: +0.0 (no change)
- read: +0.5 base reward
- referenced: +1.0 base reward
- linked: +1.5 base reward

**Note:** Actual changes are modulated by learning_rate (0.1) and position factor.

---

### Step 9: Test Q-Value Ranking Adjustment

Verify that Q-values influence search result ranking.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# First, artificially boost a note's Q-value
python -c "
import json
with open('data/q_values.json', 'r') as f:
    q = json.load(f)
q['02-Permanent/Identity.md'] = 1.5  # High Q-value
with open('data/q_values.json', 'w') as f:
    json.dump(q, f, indent=2)
print('Q-value set for Identity.md')
"

# Search for something where Identity.md is somewhat relevant
./run_search.sh "belief systems self" --mode spreading --limit 10 --json

# Check if Identity.md ranks higher due to Q-value boost
```

**Expected:**
- Notes with high Q-values should rank higher (30% weight by default)
- Q-value boost = 1.0 + (q_value * 0.3)

---

### Step 10: Test No-Track Mode

Verify that --no-track flag prevents usage logging.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Count events before
BEFORE=$(wc -l < data/usage_history.jsonl)

# Run search with --no-track
./run_search.sh "no track test" --mode static --no-track

# Count events after
AFTER=$(wc -l < data/usage_history.jsonl)

echo "Events should be same: before=$BEFORE, after=$AFTER"
```

**Expected:** No new events logged when --no-track is used.

---

### Step 11: Test Configuration Loading

Verify memory_config.py is the single source of truth.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Print current configuration
python memory_config.py

# Verify spreading uses config
python -c "
from memory_config import MEMORY_CONFIG
print('Spreading max_iterations:', MEMORY_CONFIG['spreading']['max_iterations'])
print('Learning enabled:', MEMORY_CONFIG['learning']['enabled'])
print('Q-weight:', MEMORY_CONFIG['learning']['q_weight'])
"
```

**Expected:**
- All configuration centralized in memory_config.py
- No hardcoded values in search.py, spreading.py, learning.py

---

### Step 12: Performance Benchmarks

Measure search latency for both modes.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Benchmark static search
time (for i in {1..5}; do ./run_search.sh "dopamine" --mode static --limit 10 --no-track > /dev/null; done)

# Benchmark spreading search
time (for i in {1..5}; do ./run_search.sh "dopamine" --mode spreading --limit 10 --no-track > /dev/null; done)
```

**Expected:**
- Static search: ~100-200ms per query
- Spreading search: ~300-500ms per query
- Spreading should be <2x slower than static

---

### Step 13: Edge Case Testing

Test boundary conditions.

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search

# Empty query
./run_search.sh "" --mode spreading --limit 5 2>&1

# Very long query
./run_search.sh "$(python -c 'print("dopamine " * 100)')" --mode spreading --limit 5 2>&1

# Non-existent topic
./run_search.sh "xyznonexistenttopicxyz" --mode spreading --limit 5 --json

# Unicode query
./run_search.sh "意識 consciousness" --mode spreading --limit 5 --json
```

**Expected:**
- Empty query: Graceful error or default behavior
- Long query: Should truncate or handle gracefully
- Non-existent: Return empty or low-confidence results
- Unicode: Should not crash

---

## Generate Test Report

After running all tests, generate a comprehensive report.

```bash
REPORT_DIR="/Users/eugene/Dropbox/Agents/Cornelius/resources/memory-test-reports"
REPORT_FILE="$REPORT_DIR/test-report-$(date +%Y-%m-%d-%H%M).md"
mkdir -p "$REPORT_DIR"
```

### Report Template

```markdown
# Memory System Test Report

**Date:** YYYY-MM-DD HH:MM
**Tester:** [name]
**System Version:** Cornelius v01.25

## Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Intent Classification | ✓/✗ | |
| Spreading Activation | ✓/✗ | |
| Lateral Inhibition | ✓/✗ | |
| Usage Tracking | ✓/✗ | |
| Q-Value Learning | ✓/✗ | |
| Configuration Loading | ✓/✗ | |
| Performance | ✓/✗ | |

## Detailed Results

### Intent Classification
- Accuracy: X%
- Failures: [list]

### Spreading vs Static
- Result overlap: X/5
- Spreading found cross-domain connections: Y/N
- Example good result: [describe]

### Lateral Inhibition
- Hub dominance reduced: Y/N
- Diversity improved: Y/N

### Learning System
- Events tracked: X
- Q-values updated correctly: Y/N
- Ranking adjustment working: Y/N

### Performance
- Static search avg: Xms
- Spreading search avg: Xms
- Acceptable: Y/N

## Issues Found

1. [Issue description]
   - Severity: High/Medium/Low
   - Steps to reproduce: [steps]
   - Suggested fix: [suggestion]

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Next Steps

- [ ] Address issues found
- [ ] Move to Phase 2 (Extended Graph) if all passes
- [ ] Enable spreading as default mode if stable
```

---

## Completion Checklist

- [ ] Step 1: Environment verified
- [ ] Step 2: Intent classification tested (>85% accuracy)
- [ ] Step 3: Static vs spreading compared
- [ ] Step 4: Intent-adaptive spreading verified
- [ ] Step 5: Lateral inhibition working
- [ ] Step 6: Learning status checked
- [ ] Step 7: Usage tracking verified
- [ ] Step 8: Q-value updates working
- [ ] Step 9: Ranking adjustment confirmed
- [ ] Step 10: No-track mode verified
- [ ] Step 11: Configuration centralized
- [ ] Step 12: Performance acceptable
- [ ] Step 13: Edge cases handled
- [ ] Test report generated and saved

## Error Recovery

If tests fail:

1. **Import errors:** Check `requirements.txt` installed in venv
2. **File not found:** Run `python index_brain.py` to rebuild index
3. **Learning errors:** Run `./run_learning.sh reset --confirm` to reset
4. **Config errors:** Check `memory_config.py` syntax

## Related Skills

- [/refresh-index](../refresh-index/) - Rebuild FAISS index
- [/search-vault](../search-vault/) - Production search interface
- [/recall](../recall/) - 3-layer semantic retrieval
