---
title: AI-Human Forecasting Hybrids Show 23-41 Percent Accuracy Improvement
type: research-finding
evidence-level: high
tags: #research-finding #forecasting #human-AI #superforecasting #Brier-score #prediction-markets #collective-intelligence
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# AI-Human Forecasting Hybrids Show 23-41 Percent Accuracy Improvement

**Source**: Forecasting Research Institute / LEAP initiative (Philip Tetlock), 2024-2025. Sources: Forecasting Research Substack 2024-2025; Epoch AI, "How well did forecasters predict 2025 AI progress?" 2025
**Document Type**: Research Studies / Analysis Reports
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Collective Intelligence Group Cognition

---

## Core Insight

The human-AI forecasting combination produces dramatically better results than either alone, with specific empirical measurements that clarify the relationship:

1. **AI Brier scores** in real forecasting tournaments: **0.135-0.159** (essentially matching generic human crowd ~0.149)
2. **Elite superforecaster Brier scores**: ~**0.02** - still dramatically better than current best AI
3. **Human-LLM hybrids**: **23-41% improvement** over unaugmented less-expert humans
4. **Superforecasters underestimated AI progress**: Even elite forecasters carried systematic biases about AI trajectories

---

## Evidence

**Study Design**: Real-world forecasting tournaments; LEAP initiative; Epoch AI retrospective analysis
**Sample**: Multiple forecasting competitions; elite superforecasters vs. AI models vs. hybrid configurations
**Key Results**:
- State-of-the-art AI (GPT-4, o4-mini, Claude-3.5-Sonnet) achieves Brier scores of 0.135-0.159
- Human crowd average: ~0.149 - AI now roughly matches unstructured crowd
- Elite superforecasters: ~0.02 - significant gap remains
- LLM assistants acting as superforecasters using structured reasoning enhanced less-expert humans by 23-41%
- LLM ensembles benefit from same aggregation effects as human crowds ("wisdom of silicon crowd")
- Simple averaging of human + machine forecasts outperforms either alone
- **Persistent overconfidence at high-probability levels** remains AI calibration challenge

**From LEAP**: Domain experts and superforecasters systematically underestimated AI progress across MATH, MMLU, and QuaLITY benchmarks in 2025 - even the best human forecasters carry systematic biases about AI development trajectories.

---

## What This Tells Us About Human-AI Complementarity

AI and elite humans have **different error profiles**:
- AI: High throughput, broad base rate knowledge, consistent calibration in the middle range, overconfident at high probabilities
- Elite superforecasters: Lower throughput, deep domain intuition, superior calibration across the range, better at integrating novel contextual factors

The 23-41% improvement from LLM assistance to less-expert humans suggests LLMs are serving as **calibration scaffolding** - helping less-experienced forecasters apply base rates and structured reasoning that they know abstractly but fail to apply consistently.

The gap between AI Brier (~0.14) and elite superforecasters (~0.02) is enormous - a factor of 7. This is not being closed by making models larger; it may require fundamentally different approaches (richer world models, genuine uncertainty representation, or hybrid ensembles).

---

## The Superforecaster Blind Spot on AI

LEAP initiative data shows elite superforecasters underestimated AI progress on major benchmarks. This is a fascinating meta-finding: the people most trained to avoid bias and reason probabilistically still carry systematic underestimation of AI development speed. Possible mechanisms:
- AI progress is in a domain where outside-view base rates are hard to establish
- AI is subject to "outside my area" expertise effects even for sophisticated forecasters
- The narrative of "AI is overhyped" is so dominant it becomes a systematic anchor
