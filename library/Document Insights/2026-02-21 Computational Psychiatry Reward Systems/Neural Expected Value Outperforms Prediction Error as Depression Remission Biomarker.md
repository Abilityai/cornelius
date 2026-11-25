---
title: Neural Expected Value Outperforms Prediction Error as Depression Remission Biomarker
type: research-finding
evidence-level: moderate
tags: #research-finding #depression #biomarker #reinforcement-learning #remission #precision-psychiatry
created: 2026-02-21
updated: 2026-02-21
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Neural Expected Value Outperforms Prediction Error as Depression Remission Biomarker

**Source**: "Reinforcement Learning Processes as Forecasters of Depression Remission" (*Journal of Affective Disorders*, September 2024; PubMed 39271064; DOI via ScienceDirect)
**Document Type**: Research Paper
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-21
**Session**: 2026-02-21 Computational Psychiatry Reward Systems

---

## Core Insight

Both neural prediction error (nPE) and neural expected value (nEV) signals measured during an fMRI reward learning task can forecast whether depressed patients will remit. **Neural Expected Value (nEV) outperformed neural Prediction Error (nPE)** as a remission predictor.

This is a theoretically important finding: it suggests that the brain's current **value representations** (how much it expects future outcomes to be worth) matter more for recovery than its **capacity to update from errors** (RPE). A patient whose brain still assigns significant expected value to future positive outcomes is more likely to recover than a patient who can learn from errors but sees nothing worth pursuing.

---

## Evidence

**Study Design**: Support vector machine classifiers applied to fMRI data during probabilistic learning task
**Sample Size**: N=55 participants with depression (36 completing CBT, 19 followed naturalistically)
**Key Results**:
- Both nPE and nEV classifiers forecasted remission significantly better than null
- nEV outperformed nPE as predictor
- Prediction accuracy was **treatment-agnostic** - worked for CBT completers AND naturalistic course
- Combining reward and loss learning signals improved accuracy further

---

## Why nEV > nPE as a Biomarker

**Prediction Error (nPE)**: Measures the brain's capacity to update beliefs when outcomes differ from expectations - the learning rate

**Expected Value (nEV)**: Measures the brain's current value representations - how much it expects future rewards to be worth

The nEV advantage means: **it's not about learning speed, it's about retained hope**. A brain that still generates significant expected value for future positive outcomes has the motivational foundation for recovery. A brain that sees nothing worth pursuing cannot benefit from learning more efficiently.

This is consistent with the anhedonia research: the brain with retained RPE capacity (higher ventral striatal prediction errors) shows reduced anhedonia 6 months later. Both findings point to the same underlying construct - the residual reward representation capacity predicts recovery.

---

## Clinical Application

These neural biomarkers are ready for clinical evaluation as treatment selection tools:
- High nEV + CBT candidate: The patient's value system is intact; therapy can provide new evidence
- Low nEV: Dopaminergic augmentation may be needed first to restore value representations before therapy can work

This is the precision psychiatry vision becoming concrete: use baseline computational parameters to select treatment before starting it.
