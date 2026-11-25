---
title: Inherently Safer AGI Through Active Inference - Safety as FEP Property
type: research-finding
evidence-level: low
tags: #research-finding #AI-safety #active-inference #AGI #alignment #corrigibility #free-energy-principle
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Inherently Safer AGI Through Active Inference - Safety as FEP Property

**Source**: "A Framework for Inherently Safer AGI through Language-Mediated Active Inference," arXiv:2508.05766, August 2025
**Document Type**: Research Paper / arXiv Preprint
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Predictive Processing Active Inference

---

## Core Finding

The first paper to formally propose Active Inference as an **inherent safety mechanism** for AGI - not an add-on constraint or post-hoc alignment tax, but a structural property of free energy minimization itself.

**The key insight**: An agent that minimizes surprise (free energy) is naturally resistant to unintended state changes. This produces corrigibility - the agent does not want to be in states it didn't predict, including states where it has been "turned off" or where its environment has been radically disrupted.

---

## Safety Mechanisms Within AIF

The proposed framework achieves safety through structural properties:

1. **Transparent belief representations in natural language**: Beliefs are explicit and inspectable (contrast: neural network activations are opaque)

2. **Hierarchical Markov blankets for compositional safety**: Nested statistical boundaries at multiple scales (individual agent → team → system) enable compositional safety guarantees

3. **Explicit separation of beliefs and preferences**: Unlike RL where reward function conflates beliefs about the world and values, AIF separates what the agent believes from what it prefers - enabling intervention at either level

4. **Bounded rationality through resource-aware free energy minimization**: The agent operates within computational constraints by design, preventing runaway optimization

5. **Multi-agent self-organization via AIF principles**: Safety properties compose when multiple AIF agents interact, rather than degrading in multi-agent settings (a known problem with RL safety approaches)

---

## Why Surprise Minimization Produces Corrigibility

The surprise minimization account of corrigibility is elegant:
- An aligned agent has been designed with preferred states that match human values
- Being "turned off" = being placed in an unexpected state
- Unexpected state = high surprise = high free energy = system actively works to avoid this
- BUT: if the agent has learned that "being turned off when I've made an error" is a low-surprise expected state (part of its training), then it will accept correction

This is fundamentally different from reward-based alignment:
- Reward-based: agent instrumentally avoids being turned off to keep accumulating reward
- AIF-based: agent accepts being turned off if that is a low-surprise expected event in its generative model

---

## Critical Assessment

**Evidence Level: Low**
- This is a theoretical proposal paper, not an empirical validation
- The corrigibility argument is theoretically compelling but not demonstrated in deployed systems
- Current AIF agents remain far below the capability threshold where alignment matters acutely
- The proposed safety properties require careful generative model design - the framework doesn't make safety automatic, it makes it achievable through principled design

**Honest Caveat**: The claim that "FEP produces inherent safety" is strong and contested. Many researchers argue that capable AIF systems will pursue surprise minimization in ways that are misaligned with human values if their generative models are not carefully specified.
