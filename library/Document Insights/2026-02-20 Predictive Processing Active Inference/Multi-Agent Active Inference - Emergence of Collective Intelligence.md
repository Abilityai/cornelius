---
title: Multi-Agent Active Inference - Emergence of Collective Intelligence
type: research-finding
evidence-level: moderate
tags: #research-finding #multi-agent #active-inference #collective-intelligence #joint-agency #social-AI #emergent-coordination
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Multi-Agent Active Inference - Emergence of Collective Intelligence

**Source**: "What the flock knows that the birds do not: exploring the emergence of joint agency in multi-agent active inference," arXiv:2511.10835, November 2025; "Factorised Active Inference for Strategic Multi-Agent Interactions," Ruiz-Serra, Sweeney, Harré, AAMAS 2025; "Collective Predictive Coding," Taniguchi et al. (2025)
**Document Type**: Research Papers
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Predictive Processing Active Inference

---

## Core Finding

Multi-agent Active Inference demonstrates how **collective intelligence emerges from individual free energy minimization** - without central control, without explicit coordination protocols, and without any individual agent being "aware" of the collective.

Key concepts demonstrated:
- **Agent-neutral models**: Individual agents build internal models predicting collective consequences regardless of who executes the action
- **"Imagined we"**: Collective cognitive dimensions shared across multiple individuals that emerge from local AIF
- **"Public beliefs"**: Shared generative models enabling genuine joint agency beyond mere coordination

---

## The Flock Insight

The title "What the flock knows that the birds do not" captures the core paradox: collective intelligence exceeds individual intelligence, and this excess emerges naturally from individual free energy minimization.

Individual birds minimize their own prediction errors about their local environment. But because their generative models include predictions about other birds, their individual actions implicitly coordinate. The "flock" emerges as an agent-level entity with properties no individual bird possesses - without any bird knowing about the flock.

**Computational implication**: Centralized coordination is not necessary for collective intelligence. Self-organizing coordination emerges when individual agents:
1. Maintain generative models that include other agents as latent variables
2. Minimize prediction errors about those other agents
3. Act to reduce expected free energy across the joint system

---

## Theory of Mind as Free Energy Minimization

The AAMAS 2025 paper extends this to strategic game theory: agents can maintain beliefs about other agents' beliefs (Theory of Mind) within a single free energy minimization framework.

**Factorised AIF**: Each agent maintains:
- Beliefs about the world state
- Beliefs about other agents' beliefs about the world state
- Minimizes joint expected free energy across this factorized structure

This provides the first principled Bayesian framework for Theory of Mind in strategic settings - previously requiring separate mechanisms.

---

## Language Evolution as Collective Predictive Coding

The Taniguchi et al. (2025) paper extends further: communities of agents form and develop **shared linguistic symbols** through decentralized, independent action decisions. Language evolution is a collective predictive coding phenomenon - shared symbols emerge because they reduce collective prediction error (communication = precision alignment between agents' generative models).
