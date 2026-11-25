---
title: LLM Language and Framing Effects Are as Strong as Architecture in Cooperation
type: research-finding
evidence-level: moderate
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
tags: #research-finding #LLM #game-theory #framing-effects #cooperation #prompt-engineering #AI-governance #language-effects
---

# LLM Language and Framing Effects Are as Strong as Architecture in Cooperation

**Source**: "Understanding LLM Agent Behaviours via Game Theory: Strategy Recognition, Biases and Multi-Agent Dynamics", arXiv:2512.07462, December 2024/January 2025. URL: https://arxiv.org/html/2512.07462v1
**Document Type**: Research Paper
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Game Theory Cooperation Science

---

## Core Insight

LLMs exhibit systematic, model- and language-dependent cooperation biases in game-theoretic settings, and linguistic framing can have effects on cooperation behavior as strong as architectural differences between models. This means prompt wording is not merely stylistic - it shapes strategic behavior as fundamentally as the underlying model architecture. This has direct implications for AI governance and multi-agent system design.

---

## Evidence

**Study Design**: Game-theoretic experiments across multiple LLMs, multiple game types, multiple linguistic framings
**Key Finding**: Cooperation behavior is both model-dependent and framing-dependent
**Framing Effect Magnitude**: Language effects as strong as architectural differences between different LLMs
**Implication**: LLMs are not neutral strategic actors; they have cooperation biases built into their training that are modulated by linguistic context

---

## Why This Is Significant

This finding has a disturbing implication: if you deploy multiple LLM agents in a multi-agent system, the cooperation dynamics between them will depend on:
1. Which models you choose (architectural bias)
2. How you frame their instructions (linguistic bias)
3. How the models' biases interact

You cannot treat LLM agents as interchangeable rational actors. They have systematic personality-like biases in strategic settings, and these biases are language-dependent - meaning they can shift dramatically with small prompt changes.

**For AI governance**: If framing effects are as strong as architectural differences, then prompt engineering is governance. Organizations deploying AI agents need to treat prompt design as a strategic governance decision, not a technical implementation detail.

---

## The Dual Implication

1. **Vulnerability**: Adversarial prompt manipulation can alter AI cooperation behavior as easily as deploying a different model
2. **Opportunity**: Careful prompt engineering (like Social Chain-of-Thought) can dramatically improve cooperation without changing the underlying model
