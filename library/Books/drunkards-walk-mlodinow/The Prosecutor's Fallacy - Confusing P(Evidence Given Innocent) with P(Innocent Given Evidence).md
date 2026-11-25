---
title: The Prosecutor's Fallacy - Confusing P(Evidence Given Innocent) with P(Innocent Given Evidence)
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #prosecutors-fallacy #conditional-probability #legal-reasoning #base-rate #bayesian-reasoning
---

# The Prosecutor's Fallacy - Confusing P(Evidence Given Innocent) with P(Innocent Given Evidence)
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 2 + Ch. 6
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
The prosecutor's fallacy treats the probability that innocent circumstances would produce the evidence, P(evidence | innocent), as if it were the probability of innocence given the evidence, P(innocent | evidence). A small number for the first is presented as if it were a small number for the second. The rarity of an innocent explanation is not the same as its improbability once the evidence is in hand.

## Mechanism / Why It Matters
A match probability of 1-in-12-million does not mean a 1-in-12-million chance of innocence. The correct question is how many OTHER people or couples in the relevant population would also match - if there are several, the matching defendant is just one of them, and the match alone establishes little. The fallacy collapses the denominator, ignoring the size of the reference population over which the rare event has many chances to occur.

This is the courtroom face of [[Conditional Probability Inversion - P(A Given B) Generally Differs from P(B Given A)]]. Because P(A|B) and P(B|A) are routinely swapped by intuition, an impressive-sounding rarity statistic gets misread as a probability of guilt. The error is amplified when the statistic is also computed wrongly (multiplying non-independent factors), but even a correct rarity figure does not answer the guilt question.

Why it matters: this fallacy has produced wrongful convictions. The remedy is to always ask the inverted, decision-relevant conditional - given the evidence, how probable is innocence - and to compare the likelihood of the evidence under competing hypotheses rather than fixating on the raw rarity of one.

## Evidence
People v. Collins: a 1-in-12-million random-match figure for a couple's described features was presented as a 1-in-12-million chance of innocence; the relevant quantity is the expected number of OTHER matching couples in the population. Sally Clark: two cot deaths were quoted at 73-million-to-1, leading to a wrongful conviction; the correct question is the relative likelihood of two SIDS deaths versus two murders, with double-SIDS estimated roughly 9 times more likely than double-murder. Dershowitz / O.J. Simpson: the cited 1-in-2,500 rate of a wife-batterer going on to murder is irrelevant once the wife is already dead - among murdered battered women, roughly 90% were killed by their abuser.
