---
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
tags: [research-finding, LLM, prompting, chain-of-thought, conceptual-metaphor, reasoning, AI, cognitive-architecture]
---

# CMT Prompting Paradigm - Conceptual Metaphor Theory Improves LLM Reasoning

**Source**: Kramer, O. (2025). "Conceptual Metaphor Theory as a Prompting Paradigm for Large Language Models." arXiv:2502.01901, February 4, 2025.
**Document Type**: Research Paper (arXiv preprint, February 2025)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Language Metaphor Conceptual Thought

---

## Core Insight

Using Conceptual Metaphor Theory (CMT) as a prompting paradigm for LLMs - guiding models to interpret abstract concepts (target domains) by explicitly mapping them onto familiar physical experiences (source domains) - consistently improves reasoning accuracy, creative insight generation, and metaphorical coherence across multiple model families (Llama3.2, Phi3, Gemma2, Mistral).

This works because human abstract reasoning is organized around source-to-target domain mappings. CMT prompting aligns LLM processing with human cognitive architecture.

---

## Evidence

**Study Design**: CMT-augmented Chain-of-Thought (CoT) prompting tested across four LLM families
**Models Tested**: Llama3.2, Phi3, Gemma2, Mistral
**Results**: Consistent outperformance of baselines across:
- Domain-specific reasoning tasks
- Creative insight generation
- Metaphor interpretation accuracy

**Particularly effective for**: Economic and physical burden metaphors, where source-target alignment is complex and multi-dimensional.

---

## The Method

**Standard CoT**: Guides model through reasoning steps sequentially.

**CMT-augmented CoT**: Guides model to:
1. Identify the abstract target domain (e.g., "economic debt")
2. Map it explicitly onto a familiar physical source domain (e.g., "physical burden/weight")
3. Reason through the problem using the source domain logic
4. Re-map conclusions back to the target domain

The explicit source-to-target mapping step is the key innovation. It forces the model to engage the conceptual structure that humans use implicitly.

---

## Why This Matters for AI Architecture

This finding suggests that **human cognitive architecture is a design template for AI reasoning**. CMT is not just a theory of human language - it is a description of how abstract reasoning works in general. Building these mappings explicitly into prompts improves AI reasoning because it aligns the computation with the structure that produces reliable reasoning in humans.

**Practical implication**: When using LLMs for complex reasoning tasks, prompting them to explicitly map abstract problems onto familiar physical source domains consistently improves performance. This is a transferable prompt engineering technique.

---

## Limitations

- Not all abstract concepts map cleanly to physical metaphors
- Additional computational overhead vs. standard CoT
- Potential for metaphorical mappings to introduce new errors if source domain has inappropriate properties
- Requires identifying the right source domain (some mappings are better than others)
