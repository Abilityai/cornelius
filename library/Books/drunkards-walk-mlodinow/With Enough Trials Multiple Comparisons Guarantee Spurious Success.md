---
title: With Enough Trials Multiple Comparisons Guarantee Spurious Success
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #multiple-comparisons #randomness #statistical-significance #survivorship-bias #probability
---

# With Enough Trials Multiple Comparisons Guarantee Spurious Success
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 9
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
A result significant at the 3% level still appears by chance in about 3 of every 100 null tests, so screening many candidates manufactures false positives almost guaranteed. A long streak by one actor among thousands is near-certain even when no single actor has any skill. The relevant probability is never "will this pre-named person succeed?" but "will SOMEONE, somewhere, over some window, succeed?"

## Mechanism / Why It Matters
The error is choosing the wrong denominator. When a remarkable success is observed and only THEN named, the mind computes the odds against that specific actor producing that specific run - an enormous number. But the actor was selected because they succeeded; the correct calculation runs over the full field of candidates and the full set of windows in which any of them could have produced an equally remarkable run.

This is the engine behind survivorship illusions in finance, sports, and forecasting: with thousands of mutual funds, pundits, or gamblers, an extraordinary winning streak somewhere is not surprising but expected. Attributing it to skill confuses the survivor with the strategy. The same arithmetic powers data dredging - test enough hypotheses and some will clear any significance threshold by chance alone.

The defense is to ask how many trials, actors, or comparisons were implicitly searched before this winner was singled out, and to inflate the bar accordingly. A 1-in-a-billion event becomes mundane once you multiply by a billion chances. This is distinct from the small-sample error: here the sample need not be small at all - the trap is the sheer number of independent tries.

## Evidence
- Bill Miller's 15-year streak of beating the S&P 500 was quoted in the press at odds up to 2.2-billion-to-1. Properly computed across 6,000+ active fund managers and many overlapping 15-year windows, the chance that SOMEONE achieved such a streak was roughly 75% - near-inevitable, not miraculous.
- The "Super Bowl indicator" (the conference of the winning team predicting the stock market's direction) hit 18 of 19 years - a pure coincidence surfaced by searching many candidate correlations.
- A test calibrated to 3% significance produces a false positive in about 3 of every 100 genuinely null comparisons by construction.
