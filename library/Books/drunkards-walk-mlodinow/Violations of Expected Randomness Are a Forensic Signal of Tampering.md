---
title: Violations of Expected Randomness Are a Forensic Signal of Tampering
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #randomness #forensic-statistics #fraud-detection #distributions #probability
---

# Violations of Expected Randomness Are a Forensic Signal of Tampering
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 8
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
Because genuinely random social and physical data follow predictable distributions, a deviation from the expected pattern is itself evidence of an intervening cause. The ABSENCE of the noise you should see is the tell. Where clustering-illusion errors come from expecting chance to be too smooth, this principle inverts it: when chance is suspiciously too smooth, too truncated, or too regular, something is manipulating the data.

## Mechanism / Why It Matters
Honest random data carry a characteristic fingerprint - a bell curve has both tails, a Poisson count has its expected spread, free choices distribute around a stable mean. A tamperer typically removes part of that fingerprint: shaving a tail, censoring values past a threshold, or compressing the spread. The missing or misshapen portion is detectable precisely because we know what undisturbed randomness should look like.

This makes statistical shape a forensic instrument. It is the logical complement of the clustering illusion: there, people wrongly cry "tampering" at expected clumps; here, the trained eye correctly infers tampering from MISSING expected variation. The skill is knowing the reference distribution well enough to notice what is absent, not just what is present.

It matters because it converts probability theory into a detector of fraud, evasion, and manipulation across domains - draft-dodging, short-weighting, and game-fixing all leave their signature as a dent in an otherwise predictable distribution.

## Evidence
- Quetelet inferred large-scale draft-dodging from roughly 2,200 conscripts "missing" from just above the French height cutoff - the bell curve's expected count there was depleted, implying men faking shortness to evade service.
- Poincare caught his baker shorting loaves: weighing his daily bread over a year, the weights lacked the bell curve's expected light (underweight) tail - the baker was saving the small loaves for others and giving Poincare only acceptable ones, which itself reshaped the distribution.
- Wolfers detected point-shaving across roughly 70,000 NCAA basketball games: heavy favorites won by just UNDER the point spread too often, a distortion of the expected margin distribution consistent with players manipulating the score but not the win.
