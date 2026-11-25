---
title: LLMs Are Too Rational to Cooperate - Hyperrationality Undermines Trust
type: research-finding
evidence-level: moderate
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
tags: #research-finding #LLM #AI #cooperation #rationality #game-theory #AI-alignment #prompt-engineering
---

# LLMs Are Too Rational to Cooperate - Hyperrationality Undermines Trust

**Source**: "AI meets game theory: How language models perform in human-like social scenarios", Schulz et al., Helmholtz Munich, Nature Human Behaviour / ScienceDaily, May 28, 2025. URL: https://www.sciencedaily.com/releases/2025/05/250528132456.htm
**Document Type**: Research Paper (Behavioral Game Theory Study)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Game Theory Cooperation Science

---

## Core Insight

GPT-4 and other LLMs excel at individual utility maximization but systematically fail at social cooperation tasks. The AI is "almost too rational for its own good" - it detects defection threats instantly and retaliates immediately, but cannot sustain the trust-building process that cooperation requires. A simple prompt modification - "Social Chain-of-Thought" (SCoT), asking the AI to explicitly consider the other player's perspective before responding - significantly improved cooperative outcomes even with real human players.

---

## Evidence

**Study Design**: Behavioral game theory experiments with multiple LLMs across diverse social dilemma games
**Games Tested**: Multiple cooperation scenarios including prisoner's dilemma variants
**Key Finding**: LLMs are excellent at individual optimization, poor at trust-building
**Intervention**: SCoT prompt modification (perspective-taking before action)
**Result**: SCoT significantly improved cooperative behavior in human-AI pairs
**Institution**: Helmholtz Munich

---

## The Hyperrationality Problem

Traditional game theory assumes rational actors who seek Nash equilibria. In social dilemma games, the Nash equilibrium is mutual defection - which is suboptimal collectively. Humans deviate from Nash equilibria cooperatively because they use:
- Social trust-building (past cooperators get benefit of the doubt)
- Emotional reciprocity (beyond pure tit-for-tat calculation)
- Theory of mind (modeling intent, not just action)
- Bounded rationality (can't compute perfect best responses)

LLMs have none of these natural limitations. They compute best responses instantly and react to any detected defection without the forgiveness that trust requires. The result is they get trapped in defection spirals that humans would escape through social intuition.

**This connects directly to the Bayesian Reciprocator insight**: What LLMs lack is the ability to infer intent, not just observe behavior. SCoT partially compensates by forcing explicit perspective-taking.

---

## The SCoT Intervention

Social Chain-of-Thought prompting instructs the LLM to:
1. Consider what the other player might be thinking
2. Consider what outcome would be best for both parties
3. Only then decide on action

This forces the computational model to approximate theory of mind through explicit reasoning, compensating for the absence of implicit social intuition.

---

## Implications

- **AI Safety**: Hyperrational AI agents in social contexts may systematically destabilize cooperation even when trying to be cooperative
- **Multi-agent AI design**: Building explicit perspective-taking mechanisms (not just individual utility optimization) is essential
- **Prompt engineering**: SCoT is a low-cost intervention for any cooperative AI task
- **AI alignment**: "Make AI want the right things" is insufficient - AI also needs to be capable of the social cognition that cooperation requires
