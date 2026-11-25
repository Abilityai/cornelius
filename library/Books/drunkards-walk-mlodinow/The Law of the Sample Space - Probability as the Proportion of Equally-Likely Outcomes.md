---
title: The Law of the Sample Space - Probability as the Proportion of Equally-Likely Outcomes
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #sample-space #probability #enumeration #equiprobability #randomness
---

# The Law of the Sample Space - Probability as the Proportion of Equally-Likely Outcomes
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 3
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
For a random process whose outcomes are EQUALLY LIKELY, the probability of a favorable result equals the proportion of total outcomes that are favorable. The decisive subtlety is the equiprobability precondition: you must enumerate the underlying equally-likely cases, not aggregated summaries, or you reproduce d'Alembert's classic misenumeration error.

## Mechanism / Why It Matters
The law looks trivial - count favorable outcomes, divide by total outcomes - but it only holds over a sample space whose elements are genuinely equally likely. The error mode is choosing the wrong unit of enumeration. For two coin tosses, the four ordered sequences HH, HT, TH, TT are equally likely, so P(one head) = 2/4 = 1/2. But the aggregated summary "0 heads, 1 head, 2 heads" has three categories that are NOT equally likely (the middle one occurs twice as often), and treating those three as the sample space gives a wrong 1/3.

This is exactly d'Alembert's mistake: he argued P(at least one head in two tosses) was 2/3 by counting collapsed outcomes (head on first toss / tail-then-head / tail-then-tail) as if equally likely. The correct enumeration over the four ordered sequences gives 3/4.

Why it matters: this is the foundational move underneath the entire conditional-probability cluster. The Monty Hall result, the two-children problem, and Bayesian updating all reduce to correctly listing the equally-likely branches and counting the favorable ones. Get the sample space right and the rest follows; aggregate too early and intuition betrays you.

## Evidence
Two-coin enumeration: four equally-likely ordered outcomes (HH, HT, TH, TT) give P(exactly one head) = 1/2 and P(at least one head) = 3/4, contradicting d'Alembert's aggregated 2/3. The structural point is that the equiprobability assumption must attach to the chosen sample space, not to an arbitrary summary partition of it.
