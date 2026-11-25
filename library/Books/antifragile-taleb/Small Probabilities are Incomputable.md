---
title: Small Probabilities are Incomputable
type: research-finding
evidence-level: moderate
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #tail-risk #probability #uncertainty #black-swan
---

# Small Probabilities are Incomputable

**Source**: Nassim Nicholas Taleb, *Antifragile: Things That Gain from Disorder* (Random House, 2012) — Appendix II ("Where Most Economic Models Fragilize and Blow People Up")
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/antifragile-taleb

## Core Insight
Tail probabilities are convex to parameter error, so the rarer the event the more precision its estimate needs — and since every estimate carries error (and errors have errors), tail probabilities are effectively incomputable even with the correct model. Compounding layers of uncertainty fatten the tails regardless of the base distribution, which dissolves clean "Knightian uncertainty."

## Mechanism / Why It Holds
A nonlinear (convex) map from parameter to probability means a small uncertainty in the standard deviation produces a large, asymmetric rise in tail probability. "Something estimated needs to have an estimation error... probability cannot be zero if it is estimated." Recursively percolating the error-of-error converges toward power-law / fat-tailed behavior even when starting from a Gaussian — so fat tails are partly *epistemic*, not just a property of the world.

## Evidence
For a "three-sigma" event (≈1 in 740 observations), the probability rises ~60% from a +5% move in sigma; a 5% average error implies ~20% underestimation. "Six sigma" amplifies fivefold; "ten sigma" differences exceed a billion-fold. Fukushima's "once per million years" becomes ~once per 30 years once layers of uncertainty are percolated. Mathematical derivation (Taleb, *Antifragile* Appendix II, 2012). Source-tier credible-interpreter: the formal result is relayed in the book, not the primary technical paper.
