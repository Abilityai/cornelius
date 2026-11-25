---
title: The Law of Large Numbers Is Not the Law of Averages
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #law-of-large-numbers #probability #gamblers-fallacy #uncertainty
---

# The Law of Large Numbers Is Not the Law of Averages
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) — Ch. 5 / Ch. 8 (Jacob Bernoulli, *Ars Conjectandi*)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
Jacob Bernoulli's Law of Large Numbers says only that a LARGER sample makes the observed average more likely to fall within a stated bound of the true average. It does NOT promise that a losing streak will be "balanced out," and independent trials never acquire memory. Conflating the two - the Law of Large Numbers with a folk "Law of Averages" - is the engine of the gambler's fallacy.

## Mechanism / Why It Matters
The LLN is a statement about a *probability*: as n grows, the probability that the gap between the observed average and the true average exceeds some fixed bound shrinks toward zero. Note what it does not say. It never promises the gap reaches zero, and it says nothing about any particular future trial.

The folk "Law of Averages" smuggles in a false corollary: that after a run of tails, heads is "due" to restore balance. But a fair coin has no memory; P(heads) stays 1/2 regardless of history. The streak is not cancelled by a compensating reverse streak - it is *diluted* by a growing mass of later independent trials, while the streak's own outcomes stand permanently. Convergence happens by swamping, not by correction.

Why it matters: this single distinction inoculates against the most common probabilistic error there is. It also reframes "the average will work out" - true only in the limit, in probability, and never a guarantee for the next bet or for a finite run. The bound matters more than the limit when stakes are real and trials are few.

## Evidence
Jacob Bernoulli's *Ars Conjectandi* (posthumous, 1713) proved the first version of the Law of Large Numbers as a theorem about the probability that the sample frequency stays within a chosen tolerance of the true frequency - explicitly a convergence-in-probability claim, not a balancing claim.
