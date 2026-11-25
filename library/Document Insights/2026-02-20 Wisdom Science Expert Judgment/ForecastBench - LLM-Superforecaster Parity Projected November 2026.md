---
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
title: ForecastBench - LLM-Superforecaster Parity Projected November 2026
type: research-finding
evidence-level: high
tags: #research-finding #AI #forecasting #superforecasters #LLM #ForecastBench #ICLR
---

# ForecastBench - LLM-Superforecaster Parity Projected November 2026

**Source**: ForecastBench Team (2024/2025). "ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities." arXiv:2409.19839. Published as ICLR 2025 conference paper. https://www.forecastbench.org/
**Document Type**: Benchmark study / ICLR conference paper
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Wisdom Science Expert Judgment

---

## Core Insight

ForecastBench - a contamination-free dynamic benchmark - provides the most rigorous comparison of LLMs and superforecasters to date. LLMs have already surpassed average human forecasters and are on track to reach superforecaster-level performance by November 2026 (95% CI: December 2025 - January 2028). One specialized system (AIA Forecaster) has already achieved this threshold.

---

## Evidence

**Study Design**: Evaluated 17 top LLMs including GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro against crowd forecasts and superforecasters on 1,000 continuously updated questions about future events. Contamination-free by design (new questions added continuously).

**2024 Baseline Results** (Brier Score - lower is better):
- Superforecasters: 0.068
- General public: 0.083
- Best LLM (Claude 3.5): 0.119

**2025 Update**:
- Superforecasters: 0.081
- Best LLM (GPT-4.5): 0.101
- General public: No longer in top 22 - LLMs now outperform average human forecasters

**Rate of Improvement**: LLMs improve approximately 0.016 Brier points annually

**AIA Forecaster**: Specialized system combining agentic news search + supervisor reconciliation + statistical calibration - has already achieved superforecaster-level performance (2025)

**Good Judgment Project validation**: Superforecasters outperformed financial markets on Federal Reserve rate decisions for the third consecutive year (2024), beating the CME FedWatch tool.

**BIN Model finding**: Noise reduction (filtering out irrelevant variance) plays a MORE significant role than bias reduction in superforecaster accuracy. They filter noise better than they correct directional errors.

**Citation**: ForecastBench Team (2024/2025), arXiv:2409.19839, ICLR 2025

---

## What This Updates

The existing vault note Human + AI will make better forecasts than either of them separately was written from a 2022 perspective when AI was clearly inferior. This updates that picture significantly: the hybrid advantage still holds, but the asymmetry has shifted - AI is now the stronger forecaster on most questions, with humans providing contextual and moral grounding advantages.

The vault note about Brier Score is a way to measure the accuracy of a probability forecast is directly relevant - this benchmark uses Brier scores throughout.
