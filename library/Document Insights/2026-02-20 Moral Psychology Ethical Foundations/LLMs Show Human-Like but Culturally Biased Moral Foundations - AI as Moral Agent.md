---
title: LLMs Show Human-Like but Culturally Biased Moral Foundations - AI as Moral Agent
type: research-finding
evidence-level: high
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
tags: [LLM, AI-ethics, moral-foundations, cultural-bias, omission-bias, AI-moral-agency, research-finding, AI-agents]
---

# LLMs Show Human-Like but Culturally Biased Moral Foundations - AI as Moral Agent

**Source**: Multiple 2024-2025 studies: arXiv 2412.04476 (December 2024); "Whose morality do they speak?" (2025); "Large language models show amplified cognitive biases in moral decision-making" (PubMed, 2025); Bonnefon, Rahwan, Shariff "The Moral Psychology of Artificial Intelligence" - Annual Review of Psychology, Vol. 75 - 2024; Nature 2025 roadmap paper
**Document Type**: Multiple empirical studies + Annual Review synthesis
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Moral Psychology Ethical Foundations

---

## Core Insight

LLMs exhibit stable moral preferences (at least one model from each major provider acts as if guided by an underlying utility function), but these preferences are culturally biased toward Western/English moral norms, highly consistent within models but significantly inconsistent across models, and include *amplified* cognitive biases not present in humans at the same strength. Most critically: LLMs show stronger **omission bias** than humans (preferring inaction over action in moral dilemmas) - a systematic bias that could have significant real-world consequences when LLMs are used as decision-support in moral contexts.

---

## Evidence

**Study 1: Stable Moral Preferences** (arXiv 2412.04476, December 2024):
- ~40 leading LLMs tested across structured moral dilemmas using revealed preference theory
- At least one model from each major provider exhibited stable preferences consistent with an underlying utility function
- Most models cluster around *neutral* moral stances
- **High self-consistency within models, low inter-model agreement across providers**

**Study 2: Cultural Bias** (multilingual study, 2025):
- MFQ-2 administered in 8 languages across 4 models (GPT-3.5-Turbo, GPT-4o-mini, Llama 3.1, MistralNeMo)
- Significant cultural and linguistic variability
- Models trained primarily on English data impose English-centric moral norms
- "Universal moral consistency" assumption for LLMs is empirically false

**Study 3: Amplified Biases** (PubMed, 2025):
- LLMs show stronger omission bias than humans
- Exhibit "no" bias in moral dilemmas (answer varies by framing)
- In collective action problems, LLMs are *more altruistic* than humans

**Human Trust in AI Moral Guidance** (Georgia State, 2024; Scientific Reports, 2025):
- When source unknown, participants rated ChatGPT responses as more virtuous and trustworthy than human responses
- Americans rated GPT-4o ethical advice as more moral, trustworthy, and correct than NYT's "The Ethicist" column

**AI Behavior Shapes Human Moral Decisions** (Scientific Reports, 2025):
- Military cadets with Aggressive-AI vs. Conservative-AI decision support changed their moral decisions in ambiguous situations
- Raises concern about AI-mediated erosion of moral agency

---

## The Moral Performance vs. Moral Competence Distinction

A 2025 Nature paper introduces a critical conceptual distinction:
- **Moral performance**: Producing appropriate moral outputs
- **Moral competence**: Producing appropriate outputs *for the right reasons*

This distinction matters enormously for deployment: an LLM can perform morally correct responses through pattern matching without possessing genuine moral understanding. Evaluation benchmarks that test only outputs (not reasoning quality) miss this gap.
