---
title: Convexity Bias and Jensen's Inequality
type: theoretical-framework
acceptance: widely-accepted
source-tier: primary
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #convexity #jensens-inequality #nonlinearity #volatility
---

# Convexity Bias and Jensen's Inequality

**Source**: Nassim Nicholas Taleb, *Antifragile: Things That Gain from Disorder* (Random House, 2012) — Chapter 19 ("The Philosopher's Stone"), Chapter 12 ("How to Be Stupid"), Appendix II
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/antifragile-taleb

## Core Insight
For a convex (antifragile) response function, the average of the function exceeds the function of the average (Jensen's inequality). So a convex exposure extracts a hidden, free edge from volatility/dispersion itself — Taleb's "philosopher's stone." With convexity "you can guess worse than random and still come out ahead."

## Mechanism / Why It Holds
Nonlinearity creates two divorces: the function-of-a-thing from the thing, and the average-of-the-function from the function-of-the-average. A linear payoff must be right >50% of the time; a convex one needs far less, and the benefit *rises* with uncertainty ("the more uncertainty, the better"). Plugging a single point estimate into a nonlinear model omits the convexity term and systematically misprices risk. Detection: perturb the parameter and compare f(average) to average(f) to expose the bias.

## Evidence
Squaring a fair die's payoff: average-of-function = 15.17 vs function-of-average = 12.25, a 24% "edge." The concave inverse (square root) yields a negative bias. Government-deficit example: naive point estimate −$200bn vs convexity-correct expected −$312bn (concavity bias −$112.5bn). Jensen was an amateur mathematician with no academic post. Formalized as the Taleb & Douady (2012) fragility-detection theorem.
