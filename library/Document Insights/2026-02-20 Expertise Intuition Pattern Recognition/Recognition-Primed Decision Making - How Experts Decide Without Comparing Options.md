---
title: Recognition-Primed Decision Making - How Experts Decide Without Comparing Options
type: theoretical-framework
acceptance: widely-accepted
tags: #theoretical-framework #decision-making #expertise #naturalistic-decision-making #RPD #Klein #intuition
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Recognition-Primed Decision Making - How Experts Decide Without Comparing Options

**Source**: Klein, G. Recognition-Primed Decision Model (multiple works). Probabilistic memory-enhanced RPD model (2024): *ScienceDirect*. https://www.sciencedirect.com/science/article/abs/pii/S095741742402774X. Applications validated in aviation (Wu et al., 2023; Zhu et al., 2024), medicine (*AJEM*, 2023), cybersecurity, firefighting.
**Document Type**: Theoretical Framework / Research Application
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Expertise Intuition Pattern Recognition

---

## Core Framework

Expert decision-makers in high-stakes naturalistic settings (firefighting, emergency medicine, aviation) do not compare options from a generated list - they recognize a situation as belonging to a type, generate a single workable course of action from their pattern library, and mentally simulate it to test adequacy. If it passes the simulation, they act. They only generate alternatives when the simulation fails.

This is the mechanism of expert intuition in action: not a mysterious sixth sense, but systematic pattern-to-action mapping built through experience in high-stakes environments.

---

## Context & Acceptance

**Field Acceptance**: Widely accepted - foundational to naturalistic decision making (NDM) research program
**Supporting Evidence**: Validated across aviation, medicine, cybersecurity, firefighting, military command
**2024 Extensions**: Probabilistic memory model improves predictive accuracy; ShadowBox training shows promise

---

## Three RPD Variations

1. **Variation 1 (most common)**: Situation recognized immediately - action follows directly. No deliberation.
2. **Variation 2**: Situation is unclear - expert diagnoses from known action inventory to identify situation type, then acts.
3. **Variation 3**: Action is unclear - expert runs mental simulation of the plausible action to test if it will work; if not, generates next alternative.

The critical difference from rational choice models: **options are generated and tested sequentially, not compared simultaneously**. Experts find the first satisficing option and use it.

---

## 2024-2025 Research Updates

**Probabilistic memory-enhanced RPD model (2024)**: Addresses uncertainty in memory retrieval, showing improved predictive accuracy in aviation simulations vs. baseline RPD. Adds realistic constraint: experts don't have perfect pattern access - they retrieve with varying confidence.

**ShadowBox Training (2025)**: Scenario-based exercises that immerse novices in expert mental models - showing promise for accelerating RPD development. Learners practice not just the decision but the expert's situational framing that precedes it.

**Firefighter study (331 firefighters)**: Six factors positively impacted safety through RPD: understanding the situation, risk perception, hazard identification, risk analysis, anticipation, and communication. However, **traditional risk assessment and risk treatment models showed no effect** - suggesting standard analytical frameworks miss how RPD actually works in emergencies.

---

## Why This Matters for AI-Era Decision Design

RPD has profound implications for how human-AI interfaces should be designed:
- AI should present situation classifications, not option lists, to support expert RPD
- For novices, AI-assisted option comparison is appropriate (they haven't built pattern libraries)
- Forcing option comparison on experts can disrupt RPD and degrade performance (similar to choking)
- The "human in the loop" design question must specify whether the human is an expert (RPD mode) or novice (analytical mode)
