---
title: Confidence Grounding in Internal Consistency - The Shared Human-AI Mechanism
type: theoretical-framework
acceptance: emerging
tags: #theoretical-framework #metacognition #confidence #calibration #internal-consistency #Koriat #LLM #human-AI #self-knowledge
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Confidence Grounding in Internal Consistency - The Shared Human-AI Mechanism

**Source**: Steyvers, M. & Peters, M.A.K. - "Metacognition and Uncertainty Communication in Humans and Large Language Models" - Current Directions in Psychological Science, 2025; Koriat (2012) "The Feeling of Knowing" framework
**Document Type**: Major Review + Theoretical Framework
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Metacognition Self-Monitoring

---

## Core Framework

Both humans and LLMs generate confidence ratings from the **internal consistency of candidate answers**, not from privileged access to ground truth. This explains, in a single principle, why both systems fail similarly in novel complex domains, why both show overconfidence in difficult tasks, and why the "feeling of certainty" can be deeply misleading.

---

## The Koriat (2012) Human Model

Asher Koriat identified that **subjective confidence tracks consistency of internally generated candidate responses**:
- When the brain generates multiple candidate answers and they converge → high confidence
- When candidates diverge → low confidence, uncertainty
- The actual correctness of the answers is irrelevant to confidence generation

**Result**: Confident but wrong is fully explained - you can have high internal consistency (many brain processes agreeing on the wrong answer) while being factually incorrect.

---

## The LLM Parallel

LLMs show the identical mechanism:
- Confidence proxied by **response consistency across regenerations** (if the model gives the same answer consistently, it signals higher confidence)
- Sampling consistency = LLM's internal consistency signal
- Both systems: confident when consistent, uncertain when inconsistent

**The 2025 insight**: This isn't a coincidence - it reflects that both systems are probability distributions over candidate responses, and confidence = concentration of that distribution. Different substrates, identical mathematical structure.

---

## Implications for the Vault's Existing Frameworks

**Connects to Dopamine/Confirmation Bias**:
Confirmation bias now has a deeper explanation: confirmation bias is selecting the information that increases internal consistency (more confirmatory evidence = converging candidates = higher confidence). The dopamine spike from confirmation is the reward signal for achieving internal consistency.

**Connects to the Uncertainty-Dopamine-Belief Loop**:
- Uncertainty = divergent internal candidates (low consistency)
- Belief formation = convergence of candidates (high consistency)
- Belief confirmation = additional convergence = more dopamine
- Challenge to beliefs = forced divergence = uncertainty/dopamine drop

This reframes the entire belief system framework in information-theoretic terms.

---

## The Practical Implication: No One Has Ground Truth Access

Neither humans nor AI have direct access to "how correct am I?" They both construct confidence from internal proxies. This has important implications:

1. **Confidence is not evidence of correctness** in any system
2. **External calibration** (feedback loops, prediction tracking, performance measurement) is the only route to accurate confidence
3. **High-consistency environments** (echo chambers, filter bubbles, organizational yes-men) produce high confidence in all participants regardless of correctness
4. **Metacognitive training** works by inserting external calibration feedback to correct the internal-consistency-only heuristic

---

## Field Acceptance Level

**Emerging**: The Koriat framework for humans is well-established (2012). The explicit parallel to LLMs is new (2025) and the formal equivalence is proposed but not exhaustively tested across architectures.
