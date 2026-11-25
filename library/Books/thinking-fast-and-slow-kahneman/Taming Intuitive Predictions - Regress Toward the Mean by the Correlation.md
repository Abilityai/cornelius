---
title: Taming Intuitive Predictions - Regress Toward the Mean by the Correlation
type: theoretical-framework
acceptance: established
source-tier: primary
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #prediction #regression-to-the-mean #calibration
---

# Taming Intuitive Predictions - Regress Toward the Mean by the Correlation
**Source**: Daniel Kahneman, *Thinking, Fast and Slow* (Farrar, Straus and Giroux, 2011) - Part II, "Intuitive Predictions"
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/thinking-fast-and-slow-kahneman

## Core Insight
System 1 matches the extremeness of a prediction to the extremeness of the evidence - prediction equals evaluation - ignoring that weak evidence warrants regression toward the mean. Intuitive predictions are therefore systematically non-regressive and overconfident. The corrective: move from the baseline toward your intuition only by the FRACTION equal to the evidence-outcome correlation.

## Mechanism / Why It Matters
Because System 1 substitutes "how impressive is the evidence?" for "how predictive is it?", it assigns the same percentile to the predictor and the outcome. Calibrated prediction requires explicitly discounting for the imperfect correlation between them. This is the actionable counterpart to the fact that regression has no cause: you must build the regression in by hand.

## Evidence
- "Julie read fluently at age 4 -> her GPA?" yields ~3.7-3.8 because people assign the same percentile to reading precocity and GPA.
- IDF officer-school study: the distribution of PREDICTED grades was nearly identical to the distribution of EVALUATION grades - completely nonregressive.
- Four-step fix: (1) start at the average / base rate, (2) get the intuitive matching estimate, (3) estimate the evidence-outcome correlation, (4) move that fraction of the distance from average toward intuition.
- Honest cost: an unbiased prediction can never "call" a rare extreme.
