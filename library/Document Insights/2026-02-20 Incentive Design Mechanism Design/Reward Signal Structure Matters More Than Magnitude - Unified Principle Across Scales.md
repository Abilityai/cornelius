---
title: Reward Signal Structure Matters More Than Magnitude - Unified Principle Across Scales
type: speculative-synthesis
status: partially-supported
confidence: high
tags: #speculative-synthesis #reward-design #mechanism-design #incentive-design #AI-alignment #motivation #structural-principle
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Reward Signal Structure Matters More Than Magnitude - Unified Principle Across Scales

**Source**: Synthesis across 2024-2025 incentive design research (Anthropic 2025, ICLR 2024, Kurnaz 2025, Olafsen 2025, ECB Forum 2025)
**Confidence Level**: High - convergent evidence from multiple independent domains
**Type**: Speculative Synthesis - original cross-domain interpretation by document-insight-extractor agent
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Incentive Design Mechanism Design

---

## The Synthesis

The central unifying principle across all 2024-2025 incentive design research is: **the structure of the reward signal matters more than its magnitude.** This operates across four distinct scales, with independent evidence at each level:

**1. AI System Level**
- Reward signal structure (proxy vs. verifiable, implicit vs. constitutional) determines whether Goodhart's Law destroys alignment
- More optimization of a badly-structured reward signal = worse outcomes (RLHF sycophancy)
- Solution: Build constraints structurally into architecture (RochetNet) rather than training toward them
- Evidence: Anthropic (2025), ICLR 2024

**2. Human Motivation Level**
- Whether rewards are intrinsic/structural (mastery, autonomy) vs. extrinsic/contingent determines whether they build or erode long-term engagement
- High-magnitude extrinsic rewards can destroy more engagement than low-magnitude intrinsic rewards create
- The overjustification removal effect: losing expected payment produces performance below "never paid" baseline
- Evidence: Overjustification research, SDT meta-analysis (2024)

**3. Institutional/Organizational Level**
- Fund structure (marginal cost vs. fixed) determines whether climate agreements attract or lose members through free-riding
- Work design explains more variance in motivation than pay design
- Evidence: ECB Forum (2025), organizational psychology research

**4. Computational Level**
- Encoding incentive compatibility into network architecture (RochetNet: exact DSIC) outperforms training toward it (RegretNet: approximate DSIC)
- Structure beats optimization for hard constraints
- Evidence: RegretNet/RochetNet comparison (arXiv survey, 2025)

---

## Why This Matters for the Knowledge Base

This principle directly extends the vault's existing "Simplicity Principle" framework. The 2025 knowledge base established that **complexity is often the enemy** in AI architecture. This synthesis adds a deeper mechanism: the reason simple approaches win is not simplicity per se, but that they more often encode constraints **structurally** rather than training toward them through optimization.

The connection: Goodhart's Law is the enemy of optimization-based design at every scale. The structural solution (encode constraints directly) is both simpler AND more robust.
