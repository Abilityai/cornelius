---
title: Combinations and the Full Sample Space
type: concept
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #probability #sample-space #combinatorics #cognitive-bias #cardano
---

# Combinations and the Full Sample Space
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) - Ch. 4 (Cardano, *Liber de Ludo Aleae*, c.1525)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
Cardano (c.1525, *Liber de Ludo Aleae*) first defined probability as favorable outcomes divided by total outcomes, and crucially recognized that the relevant total is the set of *combinations*, not faces. Two dice yield 36 combinations, not 12 - which is why a 7 is six times likelier than snake-eyes. Naive intuition systematically undercounts the number of ways an event can occur.

## Mechanism / Why It Matters
Correctly enumerating the entire opportunity set is the foundation of all probability. Every probability is a ratio, and the denominator is the full sample space of distinguishable ways the world could turn out. Intuition collapses combinations that are actually distinct - it sees "a 7" as one thing rather than six ordered pairs - and so misprices likelihoods. The durable cognitive lesson: when a probability feels wrong, the error is usually a miscounted sample space, not bad arithmetic.

## Evidence
Bernstein attributes the first systematic favorable-over-total definition to Cardano's gambling manual (Ch. 4). The two-dice example is the canonical demonstration: 6 of the 36 combinations sum to 7, versus 1 of 36 for double-ones - a 6:1 ratio that vanishes if one counts only the 11 possible totals.
