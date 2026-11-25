---
title: RLVR Training Reduces Spurious Correlations in LLM Reasoning - Evidence for Causal Structure
type: research-finding
evidence-level: moderate
tags: #research-finding #RLVR #LLM #reasoning-models #causal-structure #spurious-correlation #AI-training
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# RLVR Training Reduces Spurious Correlations in LLM Reasoning - Evidence for Causal Structure

**Source**: "Correlation or Causation: Analyzing the Causal Structures of LLM and LRM Reasoning Process" - arXiv 2509.17380 (2025) - https://arxiv.org/abs/2509.17380
**Document Type**: Empirical Analysis (arXiv, 2025)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Causal Reasoning Counterfactual Thinking

---

## Core Insight

Reinforcement Learning from Verifiable Rewards (RLVR) - the training method behind "reasoning models" like DeepSeek-R1 and similar systems - produces measurably stronger causal reasoning structures and fewer spurious correlations compared to standard supervised fine-tuning (SFT) or base LLM training. This is the first empirical evidence of a *training method* that improves genuine causal reasoning at the architectural level.

**The diagnostic method**: Adding causally irrelevant numbers to math problems (the "Math500-Noop" test) - models relying on spurious correlations get confused by irrelevant numbers; models with genuine causal reasoning structures do not.

---

## The Diagnostic Design

**Setup**: Standard math problems augmented with 1-2 causally irrelevant numerical conditions
- Example: "A train travels at 60 mph. The temperature is 72 degrees. How long to travel 120 miles?"
- A model relying on spurious correlations may try to incorporate the temperature into its calculation
- A model with genuine causal reasoning recognizes the temperature is causally irrelevant to the distance calculation

**Finding**: RLVR-trained models (reasoning models) show:
- Significantly less confusion from causally irrelevant numbers
- More robust performance when irrelevant conditions are added
- Stronger causal chain construction in solutions

**Standard SFT-trained models** show the inverse pattern: they are disrupted by irrelevant numbers because their training optimized for pattern matching over causal structure.

---

## Why RLVR Produces Stronger Causal Structure

RLVR trains models by:
1. Generating reasoning chains (chain-of-thought)
2. Evaluating the final answer against a verifiable ground truth (math, code, formal logic)
3. Backpropagating reward signals based on *correct outcomes*, not just plausible-sounding text

**The key mechanism**: Reward is only given for *correct answers* to verifiable problems. This creates selection pressure toward reasoning chains that actually track causal structure - chains that work because of genuine causal reasoning, not because they sound plausible.

In contrast, supervised fine-tuning on human-written text optimizes for text that *resembles* correct reasoning without requiring it to *produce* correct outcomes.

---

## The Partial Nature of the Finding

**Important caveat**: RLVR training improves causal structure on verifiable reasoning tasks (math, code, formal logic). It is not established whether this generalizes to:
- Open-ended causal inference in novel domains
- Pearl's Rung 2 (intervention) or Rung 3 (counterfactual) tasks
- Scientific or economic causal discovery benchmarks

The improvement is real and empirically confirmed, but it may be a narrow improvement at the edge of Rung 1/Rung 2 rather than a general solution to the causal hierarchy problem.

---

## Implications for AI Agent Design

This finding has direct practical implications for the existing AI agent architecture knowledge:

1. **Prefer reasoning models for planning tasks**: RLVR-trained models should be preferred over SFT models when causal reasoning quality matters (e.g., multi-step planning, debugging, causal attribution in agent workflows)

2. **The existing benchmark**: The vault already notes "ReAct + CoT = 34% improvement over standalone" - the RLVR finding suggests that the underlying model quality (RLVR vs. SFT) may interact significantly with prompting strategies

3. **Cost-performance tradeoff**: Reasoning models (RLVR-trained) typically have higher inference costs due to longer chains-of-thought; the causal improvement must be weighed against latency and cost in production
