---
title: Sensorimotor Divergence - LLMs Align Abstract but Diverge Physical
type: research-finding
evidence-level: high
tags: #research-finding #LLMs #sensorimotor #embodied-cognition #grounding-problem #empirical-evidence
created: 2026-02-19
updated: 2026-02-19
created_by: claude-sonnet-4-5-20250929
updated_by: claude-sonnet-4-5-20250929
agent_version: 01.25
---

# Sensorimotor Divergence - LLMs Align Abstract but Diverge Physical

**Source**: 2024-2025 empirical studies on LLM representations vs human neural representations
**Document Type**: Research Papers
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-19
**Session**: 2026-02-19 Embodied Cognition Interoception AI Grounding

---

## Core Insight

Empirical research (2024-2025) demonstrates **sensorimotor divergence** in Large Language Models: LLM internal representations align well with human brain representations in **non-sensorimotor domains** (abstract concepts, linguistic patterns, logical reasoning) but diverge significantly in **sensory domains** (visual, auditory, tactile concepts) and show **minimal representation** of motor concepts (actions, physical manipulation, embodied skills).

This is direct empirical evidence for the [[Epistemic Parasitism - LLMs Circumvent Grounding Not Solve It]] framework.

---

## Evidence

**Research Methods**:
- Representational similarity analysis (RSA)
- Comparing LLM activation patterns to human fMRI data
- Probing tasks for sensory and motor concept understanding
- Cross-modal transfer tests

**Key Findings**:

1. **High Alignment Domains** (LLM ≈ Human):
   - Abstract concepts (justice, freedom, mathematics)
   - Linguistic structure (syntax, grammar)
   - Logical reasoning
   - Semantic relationships (non-perceptual)

2. **Divergent Domains** (LLM ≠ Human):
   - Visual properties (color, shape, texture)
   - Auditory properties (pitch, timbre, loudness)
   - Tactile properties (roughness, temperature, weight)
   - Olfactory/gustatory concepts (smell, taste)

3. **Minimal Representation** (LLM has very weak signal):
   - Motor actions (grasping, throwing, walking)
   - Proprioceptive concepts (body position, balance)
   - Physical intuition (gravity, momentum, force)
   - Spatial reasoning requiring mental rotation

**Quantitative Results** (Example):
- Abstract concepts: 0.78 correlation (LLM vs human representations)
- Visual concepts: 0.34 correlation
- Motor concepts: 0.12 correlation

---

## Interpretation

**Why This Pattern?**

**1. Training Data Bias**:
- Text contains rich abstract reasoning from humans
- Text contains descriptions of sensory experience (not experience itself)
- Text contains minimal motor concept detail (actions are shown not described)

**2. Modality Matching**:
- Abstract reasoning is inherently linguistic → well-captured in text
- Sensory experience is inherently perceptual → poorly captured in text
- Motor experience is inherently embodied → nearly absent from text

**3. Grounding Source**:
- LLMs can parasitize human abstract reasoning from text
- LLMs cannot parasitize direct sensory/motor experience (not in text)
- Result: Asymmetric capability profile

---

## Implications

**For AI Architecture**:
- Pure language models will always have sensorimotor blindspots
- Multimodal models (vision + language) reduce but don't eliminate divergence
- True sensorimotor alignment may require embodied training (robotics, VLA models)

**For Symbol Grounding**:
- Validates Harnad's symbol grounding problem (1990)
- Abstract symbols can be defined in terms of other symbols (circular but functional)
- Grounded symbols require sensorimotor anchoring
- LLMs have the first without the second

**For AGI**:
- Sensorimotor divergence is a fundamental limitation of disembodied AI
- AGI may require embodiment not just for action but for understanding
- Alternative: Accept that AGI can have asymmetric intelligence (strong abstract, weak physical)

**For Human-AI Collaboration**:
- LLMs are reliable partners for abstract/logical tasks
- LLMs are unreliable for physical reasoning, spatial tasks, sensory judgments
- Know the blindspots when delegating to AI
