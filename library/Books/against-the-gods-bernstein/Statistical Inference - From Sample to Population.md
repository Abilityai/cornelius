---
title: Statistical Inference - From Sample to Population
type: theoretical-framework
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #statistical-inference #sampling #probability #uncertainty
---

# Statistical Inference - From Sample to Population
**Source**: Peter L. Bernstein, *Against the Gods: The Remarkable Story of Risk* (Wiley, 1996) — Ch. 5 (Jacob Bernoulli, *Ars Conjectandi*; John Graunt)
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/against-the-gods-bernstein

## Core Insight
One can infer an estimate about an unknown whole from a limited sample, AND the reliability of that inference - the *probable error* - can itself be quantified. Most consequential decisions are impossible without this move: we almost never observe the full population, only a slice of it. The breakthrough was not just guessing the whole from a part, but attaching a measurable confidence to the guess.

## Mechanism / Why It Matters
This is the **inductive leap** from observed data to a general estimate. John Graunt estimated London's total population from incomplete mortality bills - reasoning from a partial record to the unseen whole. This direction is the *inverse* of the Law of Large Numbers. The LLN runs forward: given a known population frequency, a large sample's average converges toward it. Inference runs backward: given only the observed sample, infer the unknown population frequency. That inverse problem is harder, it is Jacob Bernoulli's central concern, and it is the road that leads toward Bayes.

Why it matters: insurance, actuarial science, polling, and quality control all rest on this inversion. And the "probable error" idea - a quantified bound on how wrong the estimate is likely to be - is the conceptual seed of the modern confidence interval. Crucially, inference is never certainty; it is a calibrated bet on the unobserved.

## Evidence
John Graunt's *Natural and Political Observations* (1662) built population and life-table estimates from fragmentary London death records. Jacob Bernoulli's *Ars Conjectandi* (posthumous, 1713) framed the harder inverse problem - how many observations are needed to know a true frequency within a given bound - and quantified the reliability of such estimates.
