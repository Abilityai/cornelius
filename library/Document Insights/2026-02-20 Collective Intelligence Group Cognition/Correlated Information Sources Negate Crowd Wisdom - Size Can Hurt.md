---
title: Correlated Information Sources Negate Crowd Wisdom - Size Can Hurt
type: research-finding
evidence-level: moderate
tags: #research-finding #wisdom-of-crowds #information-correlation #collective-intelligence #forecasting #failure-mode
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Correlated Information Sources Negate Crowd Wisdom - Size Can Hurt

**Source**: Orzechowski et al. (2025), "Limits of the wisdom of crowds" - synthetic population models and ML ensembles examining correlated information degradation
**Document Type**: Research Paper (2025)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Collective Intelligence Group Cognition

---

## Core Insight

When diverse-seeming individuals share correlated information sources, **larger groups actively hurt accuracy** rather than helping it. The wisdom-of-crowds benefit depends entirely on the independence of errors - when information sources are correlated, adding more people to the group amplifies the shared error rather than canceling individual errors.

This is a counter-intuitive finding: more people, less wisdom, when information is correlated.

---

## Evidence

**Study Design**: Synthetic population models; ML ensemble analysis with controlled information correlation
**Evidence Level**: Moderate - synthetic models need real-world validation
**Key Results**:
- Group size helps when individual information is genuinely independent
- Group size hurts when individual information sources are correlated
- The more correlated the information sources, the more damaging additional members become
- This pattern holds in both human crowd simulations and ML ensemble experiments

**The Synthetic Population Method**: Computational models allow controlling information correlation precisely - something impossible in natural experiments where you can't know exactly how correlated information sources are.

---

## Why This Is Particularly Relevant Now

Modern information environments massively increase information correlation:
1. **Social media filter bubbles**: People within communities see very similar content
2. **Large language models**: AI systems trained on similar data provide highly correlated "views"
3. **News media consolidation**: Fewer independent information sources means correlated inputs to diverse-seeming people
4. **Cross-posting and viral content**: The same information reaches many people simultaneously through shared channels

The apparent diversity of voices in modern discourse may mask deep information correlation - which means adding more voices to a debate may be decreasing collective wisdom, not increasing it.

---

## The Dangerous Implication for AI Ensembles

AI model ensembles trained on similar data (all LLMs trained on the same internet corpus) may exhibit exactly this failure mode: **they look diverse but share highly correlated information representations**. LLM ensemble averaging may not provide the diversity benefit it appears to, because the models share too many underlying correlations.

True AI ensemble diversity requires training on fundamentally different data sources, with different architectures, and different inductive biases - not just running the same model type multiple times with different random seeds.
