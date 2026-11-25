---
title: In-Group Bias Emerges in Tabula Rasa AI Without Intrinsic Social Motivation
type: research-finding
evidence-level: high
tags: #research-finding #AI-bias #in-group-bias #emergence #multi-agent #algorithmic-fairness #tabula-rasa
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# In-Group Bias Emerges in Tabula Rasa AI Without Intrinsic Social Motivation

**Source**: Duenez-Guzman et al. and Koster et al., within Sehwag, U.M., McAvoy, A., Plotkin, J.B. (eds.), "Collective artificial intelligence and evolutionary dynamics" - PNAS Special Feature, Vol. 122, No. 25, June 2025. DOI: 10.1073/pnas.2505860122
**Document Type**: Research Papers within PNAS Special Feature
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Collective Intelligence Group Cognition

---

## Core Insight

Even "tabula rasa" AI agents - with no intrinsic social biases programmed in - **develop preferences for visually similar agents through exposure and familiarity alone**. These biases arise as a "byproduct of general cognitive processes without requiring intrinsic motivational mechanisms." Removing explicit bias mechanisms is insufficient for preventing in-group bias in AI systems; the bias is an **emergent property of general learning processes**.

---

## Evidence

**Study Design**: MARL (Multi-Agent Reinforcement Learning) experiments in "boat race" environments (stag hunt matrix game); agents learning from scratch with no bias-producing mechanisms
**Key Results**:
1. **Partner choice and statistical discrimination**: Increasing the salience of outcome-relevant features helps agents rely less on spurious correlations, producing fairer partner choices
2. **Emergent in-group bias**: Tabula rasa agents develop preferences for visually similar agents through exposure - pure familiarity effect
3. **Mitigation path**: Sufficient intergroup interaction can reduce emergent in-group bias

**What This Rules Out**: The assumption that unbiased training = unbiased AI. Even with no bias-inducing code, training environments with heterogeneous agents produce in-group preferences as an emergent learning outcome.

---

## Why This Is a Critical AI Safety Finding

Current algorithmic fairness approaches focus on:
1. Removing biased training data
2. Removing discriminatory features
3. Post-hoc debiasing of model outputs

This finding shows a **fourth problem** these approaches don't address: **bias-as-emergent-learning**. An agent that learns to interact effectively in a heterogeneous environment will learn to distinguish types, and learning to distinguish types + interacting repeatedly with similar types = in-group preference. This is a mathematical consequence of general learning, not a programming flaw.

**Implication**: AI fairness requires not just unbiased training data but **designed intergroup interaction** - the agent must have sufficient experience with diverse counterparts to prevent familiarity-driven preferences from hardening into discrimination.
