---
title: The Central Limit Theorem - Aggregation Creates Order
type: theoretical-framework
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #central-limit-theorem #probability #laplace #aggregation
---

# The Central Limit Theorem - Aggregation Creates Order
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) - Ch. 9 (Pierre-Simon Laplace, 1809)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
Averages of repeated samples converge to a normal distribution and progressively shrink the dispersion around the grand average, regardless of the shape of the underlying distribution. A single die produces a flat (uniform) distribution, yet averaging repeated samples drawn from it produces a bell curve whose standard deviation collapses as sample size grows. Aggregation manufactures order out of disorder.

## Mechanism / Why It Matters
The theorem (Laplace, 1809) decouples the behavior of the *average* from the behavior of the *individual*. The parent distribution can be uniform, skewed, or lumpy; the distribution of sample means is still asymptotically normal and increasingly concentrated. This is the deep reason large samples yield reliable estimates: the noise of individual draws cancels in aggregate, and the precision of the estimate improves predictably with N. It is the load-bearing principle behind insurance (pooling many independent risks produces a stable, estimable aggregate loss), polling (a sample mean approximates the population mean within a shrinking band), and quality control. The transferable lesson: predictability does not require predictable individuals - it can emerge purely from aggregation of independent units.

## Evidence
Bernstein's worked illustration: the outcomes of a single die are uniformly distributed (each face equally likely, a flat histogram), but the *averages* of repeated rolls trace a bell-shaped curve, and that curve's spread narrows as the number of rolls per average increases. The result is a confirmed cornerstone of statistical theory.
