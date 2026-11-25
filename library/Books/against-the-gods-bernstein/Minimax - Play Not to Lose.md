---
title: Minimax - Play Not to Lose
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #game-theory #minimax #loss-avoidance #survival-first #decision-theory
---

# Minimax - Play Not to Lose
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) — Ch. 15 (von Neumann, 1926/1928)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
Von Neumann's minimax theorem (1928): against an at-least-moderately-intelligent opponent, "certain defeat results from any strategy whose aim is to win rather than to avoid losing." The rational move is to minimize your maximum possible loss - and, where the game allows, to randomize your choices so the opponent cannot read and exploit your intentions.

## Mechanism / Why It Matters
The principle inverts the naive objective. Loss-*avoidance*, not gain-*maximization*, is the integral move under adversarial uncertainty. Reaching for the highest-payoff option telegraphs your aim and invites the strongest counter-move precisely where it hurts most; a rational adversary will punish your greed. So the disciplined actor settles for "the best of a bad bargain" - the strategy whose worst-case outcome is least bad. Randomization protects this by denying the opponent any pattern to attack. The posture generalizes well beyond two-player zero-sum games into a survival-first stance: in any environment where ruin is possible and adversaries adapt, protect the downside first and let the upside be a residual, because you only get to keep playing if you do not get knocked out.

## Evidence
Von Neumann's minimax theorem (proved 1928, presented 1926-1928): in any finite two-player zero-sum game there exists a value and optimal (possibly mixed) strategies guaranteeing each player no worse than that value. A proven theorem, not an empirical claim - hence established.
