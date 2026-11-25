---
title: LLMs Are Heuristic Priors for Causal Discovery - Not Causal Oracles
type: research-finding
evidence-level: high
tags: #research-finding #LLM #causal-discovery #AI-architecture #hybrid-AI #causal-reasoning
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# LLMs Are Heuristic Priors for Causal Discovery - Not Causal Oracles

**Source**: "Large Language Models for Causal Discovery: Current Landscape and Future Directions" - IJCAI 2025 - https://www.ijcai.org/proceedings/2025/1186.pdf; "Causal Discovery through Synergizing Large Language Model" (LLM-CD) - KDD 2025 - https://www.cs.emory.edu/~jyang71/files/llmcd.pdf; "LLM Cannot Discover Causality" - arXiv 2506.00844 (2025) - https://arxiv.org/html/2506.00844v1
**Document Type**: Research Papers (IJCAI 2025, KDD 2025) + Critique Paper (arXiv 2025)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Causal Reasoning Counterfactual Thinking

---

## Core Insight

Three paradigms for using LLMs in causal discovery have been empirically compared (IJCAI 2025), and the results reveal a clear hierarchy: using LLMs as standalone causal reasoners performs worst; using them as **priors and critics to constrain traditional causal discovery algorithms** performs best.

Critically, a 2025 arXiv paper argues this is the only appropriate role: LLMs' autoregressive, correlation-driven modeling lacks theoretical grounding for causal reasoning. Injecting ground-truth knowledge via prompts can inflate reported performance - making evaluation misleading. The conclusion: **LLMs should not determine causal relationship existence or direction; they should only assist heuristic search.**

---

## The Three Paradigms Compared

| Paradigm | Approach | Empirical Performance |
|----------|----------|----------------------|
| 1. LLM as standalone causal reasoner | LLM alone, no observational data | Weakest - no theoretical grounding |
| 2. LLM post-refinement of statistical results | PC algorithm first, then LLM validates/refines | Moderate - reduces error but LLM errors still propagate |
| 3. LLM as prior/critic for statistical methods | LLM constrains traditional causal discovery algorithms | **Strongest** - combines world knowledge with statistical grounding |

---

## Evidence for the Best Approach

**LLM-CD (KDD 2025)**: A unified framework integrating LLMs with traditional causal discovery algorithms (specifically the PC algorithm) at multiple stages:
- LLM provides causal knowledge priors at initialization
- LLM acts as critic to validate intermediate graph structures
- Statistical algorithm provides rigorous causal structure search

**Results**: Up to **403.93% improvement in Recall** and **25.77% improvement in Ratio** across four datasets compared to traditional statistical methods alone.

**ASoT framework (Information Processing and Management, 2025)**: Uses multiple smaller open-source models (not one large model) with hierarchical query decomposition and dual-stream thought processing (parallel evaluation of competing hypotheses). Matches or exceeds state-of-the-art while enabling local deployment - important for privacy-sensitive enterprise use.

---

## The Critical Caution

The 2025 arXiv critique ("LLM Cannot Discover Causality") identifies a methodological trap in the field: **prompt engineering with injected ground-truth knowledge can inflate LLM causal performance to look impressive in benchmarks, while providing no evidence that the LLM can perform causal discovery on novel problems**.

This is analogous to the benchmark contamination problem: telling an LLM the answer structure in the prompt, then measuring how well it follows the hint, doesn't measure causal reasoning ability.

**Practical implication for AI practitioners**: When evaluating LLM causal capabilities, require performance on genuinely novel domains not present in training data, with no ground-truth hints in prompts.

---

## The Complexity of Causal Discovery

The fundamental challenge causal AI faces:
- The number of possible directed acyclic graphs (DAGs) grows **super-exponentially** with variables
- Traditional PC/score-based algorithms face computational explosion in high dimensions
- LLMs can prune the search space dramatically using world knowledge but cannot guarantee causal validity

BFS-based causal graph discovery achieves state-of-the-art results with only **linear** (not quadratic) query complexity when structured properly - showing that the computational challenge is solvable with right architecture.

---

## Implications for Existing AI Agent Architecture

This finding maps directly onto the existing knowledge base's work on AI agent design:
- Four Pillars of Deep Agency - The "planning" pillar needs causal models, not just correlational patterns; Paradigm 3 (LLM as prior + statistical algorithm) is the implementation path
- MOC - AI and Agents - Hybrid causal-linguistic architectures should be tracked as a production pattern
- The vault's existing "complexity skepticism" insight applies here: simpler hybrid approaches (Paradigm 3) outperform more complex pure-LLM approaches
