---
title: The Viniar Problem - In-Model Probability Is Not Real-World Probability
type: theoretical-framework
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #models #model-failure #probability #risk-models #finance
---

# The Viniar Problem - In-Model Probability Is Not Real-World Probability

**Source**: John Kay & Mervyn King, *Radical Uncertainty: Decision-Making Beyond the Numbers* (W. W. Norton, 2020) - Ch. 19
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/radical-uncertainty-kay-king

## Core Insight

A probability calculated inside a model is conditional on the model being true. To make a claim about probability in the real world, you must compound the in-model probability with the (usually unknowable) probability that the model itself is true. Kay & King name this the Viniar problem, after Goldman Sachs CFO David Viniar, who in August 2007 described markets experiencing "25-standard-deviation events, several days in a row." A 25-sigma event is so improbable that the universe has not existed long enough to expect a single one. So such a report is overwhelmingly more likely to be evidence of model failure than of genuine extreme bad luck.

## Mechanism / Why It Matters

The error is a category confusion between a conditional probability and an unconditional one. Inside the model, a 25-sigma move is near-impossible by construction. But that figure is P(event | model is true), and it tells you almost nothing about P(event) in the world. When you observe an outcome the model deems all but impossible, Bayesian reasoning says the rational update is overwhelmingly toward "the model is wrong," not toward "an astronomically rare thing just happened." Viniar inverted this: he treated the model's verdict as a window onto reality rather than as conditional on the model. The lesson generalises far beyond finance: any reported probability of an extreme event is really a joint statement about the event and the model, and the second term - model failure - usually dominates the first whenever the event is extreme. This is why catastrophic tail outcomes are almost always model failures rather than realised tail draws.

## Evidence

Kay & King: Viniar "confused a probability as calculated within a model with a probability in the world of which the model claimed to be a representation... To make a statement about probability in a real world it is necessary to compound the probability derived from the model itself with the probability that the model is itself true... We shall call this problem of model failure the Viniar problem." The arithmetic of 25 standard deviations supplies the quantitative force: the implied frequency is so low that the multi-billion-year age of the universe is too short to expect one occurrence, let alone several on consecutive days.
