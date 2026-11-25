---
title: The St. Petersburg Paradox
type: concept
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #paradox #expected-utility #probability #risk
---

# The St. Petersburg Paradox
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) — Ch. 6-7 (Nicolaus & Daniel Bernoulli, 1738)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
A coin-doubling game - pay 2^(n-1) ducats if the first heads appears on toss n - has an INFINITE mathematical expectation, yet no rational person will pay more than a small finite sum to play it. The chasm between infinite expected value and finite willingness-to-pay is the canonical demonstration that expected-value maximization fails as a decision rule.

## Mechanism / Why It Matters
The expected value is the sum over all tosses of (probability of stopping there) x (payoff), which equals (1/2)(1) + (1/4)(2) + (1/8)(4) + ... = 1/2 + 1/2 + 1/2 + ... = infinity. By the expected-value rule you should stake your entire fortune to enter. Nobody does. The rule is broken.

Daniel Bernoulli's resolution: value the payoffs by **utility**, not money. Because utility is concave (diminishing marginal utility), the astronomically large late-game prizes - which occur with vanishingly small probability - add almost nothing in utility terms. The infinite money sum collapses to a finite, modest utility sum, matching what people actually pay. The paradox is thus the historical motor that *produced* expected-utility theory.

**TENSION (wire, do not merge):** Bernstein resolves the paradox through utility *curvature* - the problem is the shape of the value function. Taleb's frame is different: the issue is **fat tails and non-ergodicity** - the rare gigantic payoff is precisely the tail event that dominates, and a single player's time-average diverges from the ensemble expectation. Same paradox, two distinct diagnoses; keep both edges live.

## Evidence
Posed by Nicolaus Bernoulli (1713) and resolved by Daniel Bernoulli in his 1738 St. Petersburg memoir, which introduced utility and its diminishing marginal increments as the analytic device.
