---
title: Toddlers Outperform GPT-o1 on Abstract Causal Relational Reasoning
type: research-finding
evidence-level: high
tags: #research-finding #developmental-psychology #causal-reasoning #LLM-limitations #toddler-cognition #abstract-reasoning
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Toddlers Outperform GPT-o1 on Abstract Causal Relational Reasoning

**Source**: Goddu & Gopnik - "The development of human causal learning and reasoning" - *Nature Reviews Psychology*, Vol. 3, No. 5, pp. 319-339 (2024) - https://www.nature.com/s44159-024-00300-5; Goddu, Yiu & Gopnik - "Causal relational problem solving in toddlers" - *Cognition* (2025) - https://www.sciencedirect.com/science/article/pii/S0010027724002452
**Document Type**: Review Paper (Nature Reviews Psychology) + Experimental Study (Cognition)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Causal Reasoning Counterfactual Thinking

---

## Core Insight

Children as young as 24-30 months can infer abstract causal transformation rules - such as relative size relationships - and apply them to novel objects they have never seen before. On visual relational reasoning tasks requiring this kind of analogical causal generalization, 3-year-olds **outperform state-of-the-art multimodal AI models including GPT-o1**. AI systems can recognize objects but fail to perform the relational mapping required to generalize causal patterns abstractly.

Human causal understanding is rooted in **early-developing, general-purpose mechanisms for abstracting causal structure** - not domain-specific modules or accumulated factual knowledge. This architecture is fundamentally different from LLM training.

---

## Evidence

**Study Design**: Two experiments with 24-30 month toddlers (Goddu, Yiu & Gopnik, Cognition 2025)
**Task**: Toddlers observe a "blicket machine" that activates based on causal properties. They must infer the abstract relational rule (e.g., "the smaller object activates it") and apply this rule to entirely novel objects.
**Key Result**: Toddlers successfully inferred abstract relational rules (e.g., relative size transformation) and applied them to novel objects, **even when the solution required applying the rule in an unprecedented way**.

**AI Comparison** (Goddu & Gopnik, Nature Reviews Psychology 2024):
- Three-year-olds outperform GPT-o1 and other state-of-the-art multimodal AI on visual relational reasoning
- AI systems could recognize objects but failed to perform relational mapping
- The gap is specifically in **abstract causal generalization**, not object recognition

**Developmental timeline of human causal capacities**:
- 24-30 months: Abstract causal relational reasoning
- 3 years: Distinguishing high vs. low probability causes
- 4-5 years: Explicit counterfactual reasoning

---

## What Makes Human Causal Reasoning Distinctive

The 2024 Goddu & Gopnik review identifies two defining features of human causal understanding across cultures:

1. **Depersonalized**: Understanding causes that are NOT outcomes of one's own actions (unlike most animal causal learning)
2. **Decontextualized**: Understanding causes that generalize across different contexts (abstract causal schemas)

Both properties appear by age 2-3 years, before formal education, and before language is fully developed. This strongly suggests these capacities are core features of human cognition rather than learned cultural competencies.

---

## The Deep Paradox for AI Development

LLMs are trained on vast human-generated text - including every paper, book, and article about causal reasoning. They can discuss Pearl's causal hierarchy fluently, explain interventions and counterfactuals accurately, and solve some causal problems through pattern matching. Yet they fail on novel abstract relational tasks that a 3-year-old handles intuitively.

This creates a striking asymmetry:
- **LLMs**: Can verbalize causal concepts but cannot instantiate them in novel relational structures
- **Toddlers**: Cannot yet verbalize much but can apply abstract causal schemas to entirely new situations

The gap is in *causal abstraction capacity* - the ability to extract a relational rule and apply it structure-preservingly to new domains. This is the core of what Pearl calls Rung 2 (intervention/do-calculus reasoning).
