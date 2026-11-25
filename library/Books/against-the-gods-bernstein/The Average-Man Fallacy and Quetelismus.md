---
title: The Average-Man Fallacy and Quetelismus
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #averages #data-mining #overfitting #statistics
---

# The Average-Man Fallacy and Quetelismus
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) - Ch. 10 (Adolphe Quetelet's *l'homme moyen*; Antoine Cournot; Francis Edgeworth)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
Two linked statistical cautions. (a) An average computed over a class need not correspond to any realizable member of that class. (b) Finding a normal distribution in data does not prove the data are genuinely homogeneous - the pattern may be an artifact of how hard you looked. Together they guard against reifying averages and against mistaking a fitted curve for a discovered law.

## Mechanism / Why It Matters
On the first caution, Cournot's rebuttal of Quetelet's *l'homme moyen* (the "average man") is decisive: "an average of all the sides of a bunch of right triangles would not be a right triangle, and a totally average man would be a monstrosity." Averaging across a heterogeneous class destroys the structural constraints that define its members, so the average can be a member of no real category. On the second caution, Edgeworth coined "Quetelismus" for the error of discovering normal distributions where they do not actually exist - what modern statisticians call data mining or overfitting: "torture the data long enough and the numbers will prove anything." Both are direct ammunition against reification of averages, spurious-pattern reasoning, and confusing a model fitted to noise with a real regularity. The transferable rule: an average is a summary, not an entity; and a found pattern must survive out-of-sample before it counts as a law.

## Evidence
Quetelet (mid-19th c.) introduced *l'homme moyen* as a real type; Cournot's right-triangle counterexample exposed the category error. Edgeworth's coinage of "Quetelismus" named the inverse error of over-discovering normality. These are established cautions (Cournot's logic) blended with interpretation (Edgeworth's critique of method).
