---
title: LLMs Fail at Motor Concepts - Empirical Proof of Embodiment Gap
type: research-finding
evidence-level: high
tags: #research-finding #LLM #embodiment-gap #motor-concepts #grounding-problem #AI #nature-human-behaviour
created: 2026-02-18
updated: 2026-02-18
created_by: claude-sonnet-4-5-20250929
updated_by: claude-sonnet-4-5-20250929
agent_version: 01.25
---

# LLMs Fail at Motor Concepts - Empirical Proof of Embodiment Gap

**Source**: Xu, Q. et al. (The Ohio State University) - "Large language models without grounding recover non-sensorimotor but not sensorimotor features of human concepts" - Nature Human Behaviour, September 2025, Volume 9, pp. 1871-1886 - PMID: 40468013 - https://www.nature.com/articles/s41562-025-02203-8
**Document Type**: Empirical Research Paper (Nature Human Behaviour - top-tier peer reviewed)
**Evidence Level**: High - systematic empirical measurement in top-tier journal
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-18
**Session**: 2026-02-18 Embodied Cognition Interoception

---

## Core Insight

The symbol grounding problem for AI is real, severe, and cannot be solved by more data or more modalities. A Nature Human Behaviour study empirically demonstrated that similarity between human and LLM concept representations **decreases systematically** from non-sensorimotor domains to sensory domains to motor domains. In motor domains, alignment is **minimal** even with visual training added. "An AI tool like ChatGPT can't represent the concept of a flower the way a human does" - because the human concept includes tactile, olfactory, and motor dimensions that no text or image training can provide.

---

## Evidence

**Study Design**: Comparative analysis of concept representations
**Sample**: ~4,442 lexical concepts
**Models Tested**: State-of-the-art LLMs with and without visual training
**Measurement**: Multidimensional concept representation similarity between humans and models

**Results by Domain**:
| Domain | Human-Model Alignment |
|--------|----------------------|
| Non-sensorimotor (abstract) | Moderate to good |
| Sensory | Poor |
| Motor | Minimal even with visual training |

**Key Finding**: Adding visual training improved sensory alignment somewhat but **did not solve the motor domain gap**. The failure is not about insufficient data or modalities - it is about the absence of embodied interaction.

---

## What the Flower Represents

The concrete example from the paper: ChatGPT cannot represent "flower" the way a human does, because the human concept includes:
- Tactile: the texture of petals, resistance of stems when picked
- Olfactory: specific scent profiles, seasonal associations
- Motor: the gesture of bending to smell, picking, arranging
- Proprioceptive: the weight in the hand, the muscle memory of weeding
- Interoceptive: the bodily state changes associated with these activities

These are not peripheral details. They are **constitutive** of what "flower" means to a human. LLMs have access only to the statistical relationships between text tokens - a shadow of the concept, accurate for non-sensorimotor dimensions, increasingly hollow for sensory and motor dimensions.
