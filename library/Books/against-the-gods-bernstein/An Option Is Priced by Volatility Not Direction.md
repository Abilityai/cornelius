---
title: An Option Is Priced by Volatility Not Direction
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #optionality #volatility #black-scholes #convexity #finance
---

# An Option Is Priced by Volatility Not Direction
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) — Ch. 18 (Black-Scholes; the AT&T vs Microsoft option comparison)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
The value of an option depends on HOW FAR the underlying might move, not WHICH WAY. Because the payoff is asymmetric — downside capped at the premium paid, upside open — the direction of the expected move is irrelevant to its price. The decisive input is volatility. This is the pricing corollary to optionality: it supplies the number that [[Optionality - The Engine of Antifragility]] describes qualitatively.

## Mechanism / Why It Matters
The asymmetry truncates the bad tail (you can lose only the premium) while leaving the good tail open. Under that truncation, a larger spread of possible outcomes is unambiguously more valuable regardless of where the distribution is centered — more dispersion means a fatter open upside without a fatter downside. So price decouples from directional forecast and attaches to dispersion. The transferable lens: wherever payoffs are convex, you are long volatility regardless of your view on direction, and you should value the position by its spread of outcomes, not your guess about the mean.

## Evidence
This decoupling is the conceptual heart of the Black-Scholes-Merton model (Black, Scholes, Merton, 1973): the formula prices an option without any term for the expected return or directional drift of the underlying, while volatility enters as the dominant input. Bernstein illustrates it by comparing options on a placid stock (AT&T) and a volatile one (Microsoft): the more volatile underlying commands the more valuable option even with no view on which way either will go.
