---
title: Curiosity-Driven RL for AI - CD-RLHF and CDE as Applied Neuroscience
type: research-finding
evidence-level: moderate
tags: #research-finding #AI #reinforcement-learning #curiosity #RLHF #LLM #intrinsic-motivation #agent-design
created: 2026-02-21
updated: 2026-02-21
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Curiosity-Driven RL for AI - CD-RLHF and CDE as Applied Neuroscience

**Source**: (1) "Curiosity-Driven Reinforcement Learning from Human Feedback" (CD-RLHF), ACL 2025 / arXiv 2501.11463; (2) "CDE: Curiosity-Driven Exploration for Efficient Reinforcement Learning in Large Language Models," arXiv 2509.09675 (September 2025); (3) "Incentivizing Exploration With Causal Curiosity as Intrinsic Motivation," NeurIPS 2024 Workshop
**Document Type**: Research Papers (AI/ML)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-21
**Session**: 2026-02-21 Curiosity Epistemic Motivation Neuroscience

---

## Core Insight

The AI reinforcement learning field is directly operationalizing human curiosity neuroscience findings from 2024-2025. Three major papers demonstrate that injecting curiosity-inspired mechanisms into AI training resolves persistent problems (output diversity collapse, entropy collapse in RLVR, alignment-diversity tradeoff) - validating that human curiosity neuroscience discovered universal principles for intelligent systems, not just human quirks.

---

## Three Curiosity AI Mechanisms

### 1. CD-RLHF - Curiosity-Driven RLHF (ACL 2025)

**Problem Solved**: Standard RLHF optimizes for human preferences but loses output diversity ("diversity-alignment tradeoff")

**Mechanism**: Intrinsic Curiosity Module (ICM) estimates curiosity as a novelty metric (prediction error about environment state), producing intrinsic rewards during training

**Human Parallel**: ICM = dopaminergic information prediction error (IPE) signal. The AI is given artificial dopamine spikes for novelty, exactly as human brains are.

**Result**: Enhanced output diversity WITHOUT compromising alignment quality. Mitigates diversity-alignment tradeoff.

---

### 2. CDE - Curiosity-Driven Exploration for LLMs (arXiv 2025)

**Problem Solved**: Entropy collapse in RLVR training - LLMs becoming overconfident and repetitive during reinforcement training

**Two-Signal Mechanism**:
- **Actor-level**: Perplexity over generated responses (epistemic uncertainty about own output = curiosity about own predictions)
- **Critic-level**: Variance of value estimates from multi-head architecture (uncertainty about value estimates)
- Both serve as exploration bonuses; actor-wise bonus inherently penalizes overconfident errors

**Human Parallel**: Entropy collapse = satiation/boredom; CDE signals = the brain's curiosity triggers that prevent habitual exploitation

---

### 3. Causal Curiosity (NeurIPS 2024)

**Mechanism**: Agent integrates causal inference with model-based RL; curiosity = changes in the agent's internal causal model (not just prediction error, but causal structure discovery)

**Human Parallel**: Epistemic curiosity about mechanisms - "I want to know WHY, not just WHAT" - is the highest form of human curiosity. This paper operationalizes it for AI.

**Separate value functions**: Extrinsic rewards (task completion) AND intrinsic causal discovery (separate curiosity budget)

**Result**: Improved learning efficiency vs. standard RL on structural causal model environments

---

## The Human-AI Curiosity Parallel Table

| AI Problem | AI Solution | Human Neural Equivalent |
|-----------|------------|------------------------|
| Low output diversity | ICM intrinsic reward (CD-RLHF) | Dopaminergic IPE signal for novelty |
| Entropy collapse | Perplexity/variance bonuses (CDE) | Curiosity system preventing boredom/satiation |
| Poor causal learning | Causal curiosity module | Epistemic curiosity about mechanisms |
| Noisy TV problem | Targeted prediction error (not random) | Maladaptive curiosity / compulsive novelty-seeking |

**The "Noisy TV" problem** is particularly instructive: AI curiosity agents can become trapped seeking maximally unpredictable stimuli rather than genuinely informative ones - a direct parallel to human information addiction, compulsive scrolling, and cyberchondria. The solution in both human and AI cases is the same: curiosity must be calibrated to information VALUE, not just information NOVELTY.

---

## Implications for Agent Architecture Design

These findings suggest agent design principles directly derived from human curiosity neuroscience:
1. **Intrinsic motivation modules** should be included in advanced agents (not just extrinsic reward optimization)
2. **Exploration bonuses** should use prediction error, not random noise (mirrors dopaminergic teaching signal)
3. **Diversity mechanisms** prevent exploitation collapse (mirror biological boredom/satiation prevention)
4. **Separate value functions** for extrinsic tasks vs. intrinsic discovery (mirrors dual-system curiosity architecture)
