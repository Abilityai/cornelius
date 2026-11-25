---
title: Partial Proofs Multiply Never Sum - No Finite Number Reaches Certainty
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #probability #independence #and-rule #evidence-combination #reasoning-error
---

# Partial Proofs Multiply Never Sum - No Finite Number Reaches Certainty
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 2
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
Independent partial proofs combine by multiplication of their failure-complements, not by addition. Two independent "half proofs" therefore yield three-fourths of a proof, not a whole one, and no finite stack of partial proofs ever reaches certainty. Roman law's maxim that "two half proofs make a whole proof" is the canonical error of adding where one must multiply.

## Mechanism / Why It Matters
If each of two independent pieces of evidence leaves a 1/2 chance the claim is false, then both being satisfied leaves (1/2) * (1/2) = 1/4 chance of falsehood - that is, 3/4 of a proof, not a full one. The probability of certainty is approached only asymptotically: n independent half-proofs give 1 - (1/2)^n, which climbs toward 1 but never touches it for any finite n. Adding probabilities, by contrast, would falsely cross 1 after just two pieces.

The underlying rule is the AND-rule for independent events: P(A and B) = P(A) * P(B). The load-bearing caveat is genuine independence - if the partial proofs share a common cause or one depends on the other, the multiplication is invalid and the combination must be computed conditionally. Treating correlated evidence as independent overstates confidence; treating it as additive is simply wrong.

Why it matters: it formalizes why accumulating imperfect evidence yields strong-but-never-absolute belief, and it warns against the intuitive bookkeeping of "summing" supportive facts. It also sets up the related but distinct error case where two error sources of very different size must be combined by the OR/sum rule rather than multiplied.

## Evidence
Roman legal doctrine codified "two half proofs make a whole proof," an additive rule that the multiplication law refutes: two independent half-proofs leave (1/2)^2 = 1/4 probability of falsehood, i.e. 3/4 proof. Generalizing, n independent half-proofs yield 1 - (1/2)^n, which is bounded strictly below 1 for all finite n - certainty is unreachable by any finite accumulation.
