---
title: LLMs Are Causal Parrots - Stuck at Rung 1 of Pearl's Causal Hierarchy
type: research-finding
evidence-level: high
tags: #research-finding #LLM #causal-reasoning #Pearl #AI-limitations #empirical-evidence
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# LLMs Are Causal Parrots - Stuck at Rung 1 of Pearl's Causal Hierarchy

**Source**: Multiple 2024-2025 benchmarks: CausalProbe 2024 (NeurIPS 2024); "Benchmarking LLM Causal Reasoning with Scientifically Validated Relationships" (arXiv 2510.07231, 2025); CLadder (NeurIPS 2023/arXiv 2312.04350); CORR2CAUSE benchmark; Judea Pearl interview (causalai.causalens.com)
**Document Type**: Multiple Benchmark Studies + Expert Commentary
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Causal Reasoning Counterfactual Thinking

---

## Core Insight

Large language models consistently and empirically fail at causal reasoning beyond statistical association. Across five independent 2024-2025 benchmarks, the best-performing LLMs achieve only 57.6% accuracy on real-world causal benchmarks and 33.38% F1 on causal inference from correlation tasks. This is not a training gap - it reflects a fundamental architectural limitation: transformers trained on co-occurrence statistics are oriented toward Rung 1 (association) of Pearl's Causal Hierarchy and cannot natively access Rung 2 (intervention) or Rung 3 (counterfactual reasoning).

**Judea Pearl's verdict**: "These kinds of questions form the ladder of causation that deep learning cannot give you an answer to unless all answers are inserted explicitly."

---

## Pearl's Causal Hierarchy (The Three Rungs)

| Rung | Type | Query Form | Example |
|------|------|-----------|---------|
| Rung 1 - Association | Seeing | P(Y\|X) | What correlates with recovery? |
| Rung 2 - Intervention | Doing | P(Y\|do(X)) | What happens if I give this drug? |
| Rung 3 - Counterfactual | Imagining | P(Y_x\|X=x', Y=y') | Would this patient have recovered if treated? |

LLMs are empirically confirmed to operate primarily at Rung 1 and fail at Rungs 2 and 3.

---

## Evidence

**Benchmark Performance (2024-2025):**

| Benchmark | Venue | Key Result |
|-----------|-------|-----------|
| CausalProbe 2024 | NeurIPS 2024 | "Level-1 shallow causal reasoning" only; performance drops significantly vs. older benchmarks |
| Econ/Finance Causal Benchmark | arXiv 2025 | Best LLM: **57.6% accuracy** - model scale does NOT improve this |
| CORR2CAUSE | - | Best model **F1 = 33.38%** |
| CLadder | NeurIPS 2023 | "Highly challenging"; LLMs perform poorly across 10,112 questions |
| CauSciBench | NeurIPS 2025 | Systematic failures confirmed on scientific causal inference |

**Key diagnostic finding** (arXiv 2509.17380, 2025): Adding causally irrelevant numbers to math problems (Math500-Noop test) reveals which models reason causally vs. rely on spurious correlations. RLVR-trained "reasoning" models show stronger causal structures; standard LLMs get confused by irrelevant numbers.

**Two primary failure modes identified** (arXiv 2410.23884):
1. **Temporal bias**: Inferring causality from narrative event order rather than logical structure
2. **Memorized world knowledge without context**: Retrieving training facts instead of reasoning through the specific scenario

---

## Why This Is Architecturally Fundamental, Not a Data Problem

Benchmark contamination evidence: LLMs perform better on older benchmarks (familiar training data) than fresh 2024-2025 ones. This confirms the performance is from memorization, not reasoning. Scaling up model size does NOT improve performance on novel causal benchmarks - ruling out the "just needs more training" hypothesis.
