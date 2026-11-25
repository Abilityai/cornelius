---
title: Conditional Probability Inversion - P(A Given B) Generally Differs from P(B Given A)
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #conditional-probability #bayesian-reasoning #cognitive-bias #base-rate #reasoning-error
---

# Conditional Probability Inversion - P(A Given B) Generally Differs from P(B Given A)
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 6
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
The probability of A given B is generally not equal to the probability of B given A, yet intuition reflexively swaps the two. This single asymmetry is the engine that produces the medical false-positive trap and the legal prosecutor's fallacy as special cases. The two conditionals are related by base rates (Bayes' theorem), and ignoring those base rates is precisely what makes the swap feel valid.

## Mechanism / Why It Matters
P(A|B) and P(B|A) differ by the ratio of the unconditional probabilities P(A)/P(B). They coincide only when A and B are equally common. Whenever one is rare and the other common, the two conditionals can diverge by orders of magnitude - which is exactly the regime where intuition most confidently equates them. The mind appears to store conditional relationships as undirected associations and loses track of which way the conditioning runs.

Why it matters: this is a meta-principle that unifies an entire family of reasoning failures. Once you see that the medical case (positive test vs. disease) and the legal case (rare match vs. innocence) are the same structural error, the fix generalizes: name both directions explicitly, identify which one the decision actually requires, and supply the base rate that converts one into the other.

Everyday instances make the abstraction concrete. A suspicious partner conflates P(behaving secretively | having an affair), which is high, with P(having an affair | behaving secretively), which can be low if secretive behavior has many innocent causes. Conspiracy theories trade on conflating P(observed events | conspiracy is true) with P(conspiracy is true | observed events) - a coherent fit of events to a conspiracy says little about the conspiracy's probability if those events also arise readily by chance.

## Evidence
Structural rather than statistical: the principle is Bayes' theorem, P(A|B) = P(B|A) * P(A) / P(B), with the divergence governed by P(A)/P(B). Its instances are quantified in the linked notes - the HIV / mammography base-rate cases (off by roughly an order of magnitude when physicians swapped the directions) and the People v. Collins and Sally Clark courtroom cases.
