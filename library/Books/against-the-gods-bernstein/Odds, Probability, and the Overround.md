---
title: Odds, Probability, and the Overround
type: concept
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #odds #probability #overround #prediction-markets #cardano
---

# Odds, Probability, and the Overround
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) - Ch. 4 (Cardano)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
Cardano distinguished probability (favorable / total) from odds (favorable / unfavorable) - and odds are what matter at the betting table. The corollary is practical: convert every horse's offered odds back into implied probabilities and sum them. The total exceeds 100%, and that excess - the "overround" - is exactly what the house skims.

## Mechanism / Why It Matters
The gap between fair probability and offered odds is where any intermediary extracts value. Because the bookmaker shades each price slightly against the bettor, the implied probabilities sum to more than one; the surplus is the rake, baked invisibly into the quoted odds. Summing implied probabilities is therefore a general audit tool: it reveals the spread any market-maker is taking. This applies directly to prediction markets and to forecasting calibration, where a forecaster's stated probabilities should sum coherently rather than carrying a hidden overround.

## Evidence
Bernstein credits Cardano with separating odds from probability as two different ratios over the same outcomes (Ch. 4). The overround follows arithmetically: if a bookmaker offers prices implying, say, 55% and 55% on a two-horse race, the implied total is 110%, and the 10% excess is the margin no honest probability distribution would contain.
