---
created: 2026-02-21
updated: 2026-02-21
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
title: LLMs Exhibit Human-Like Mental Accounting Biases Through Textual Learning Alone
type: research-finding
evidence-level: moderate
tags: [research-finding, AI, LLM, behavioral-economics, mental-accounting, cognitive-bias, AI-agents, house-money-effect]
---

# LLMs Exhibit Human-Like Mental Accounting Biases Through Textual Learning Alone

**Source**: "Folk Economics in the Machine: LLMs and the Emergence of Mental Accounting" - SSRN - 2024; "The Role of Mental Accounting in Risk-Taking and Spending: A Meta-Analysis of the House-Money Effect" - Frontiers in Psychology - 2025
**Document Type**: Empirical AI Research; Meta-Analysis
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-21
**Session**: 2026-02-21 Behavioral Economics Intertemporal Choice

---

## Core Insight

Large language models display key elements of human-like mental accounting (including aspects of the house-money effect) through textual learning alone - with no explicit reinforcement, incentive exposure, or experiential economic learning. LLMs diverge from humans in one notable direction: they maintain more cautiously conservative stances in house-money gambles. This has direct implications for AI-based financial tools, which may unintentionally reinforce or mitigate human mental accounting heuristics depending on context.

---

## Evidence

**Primary Study (SSRN, 2024)**:
**Study Design**: Experimental comparison of LLM responses to financial scenarios with known human mental accounting benchmarks
**Key Results**:
- LLMs display key elements of mental accounting: labeling effects, house-money sensitivity, context-dependent risk attitudes
- LLMs are more conservative than humans in house-money gambles (taking less risk with windfall income than humans typically do)
- Mental accounting patterns emerge from text training, not from embodied economic experience
**Citation**: "Folk Economics in the Machine: LLMs and the Emergence of Mental Accounting." SSRN. 2024. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4705130

**Meta-Analysis Context (Frontiers in Psychology, 2025)**:
- House-money effect is more prominent in student samples and weaker in field experiments
- A "reverse house-money effect" has been observed in some real-world settings
- Labeling salary as "bonus" promotes savings; calling it "regular salary" encourages consumption

---

## Why This Matters for AI Systems

**Implicit bias amplification**: An LLM used in financial advisory contexts will nudge users away from risky decisions with windfall income - not because it was designed to, but because it absorbed human mental accounting from training text. Whether this is a feature or bug depends on context.

**Emergent from language, not incentives**: This demonstrates that behavioral biases can be transmitted through textual cultural encoding, not just through direct reward learning. The implication: every LLM is trained on human-generated text saturated with human cognitive biases, and these biases are reproduced in AI behavior.

**Audit gap**: Most AI financial tools are not evaluated for mental accounting biases. The SSRN finding suggests this evaluation should be standard.
