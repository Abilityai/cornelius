---
created: 2026-02-21
updated: 2026-02-21
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
title: Nudge Voltage Drop - Effects Collapse at Scale Due to Baseline Motivation Heterogeneity
type: research-finding
evidence-level: high
tags: [research-finding, behavioral-economics, nudge-theory, scalability, publication-bias, voltage-drop, meta-analysis]
---

# Nudge Voltage Drop - Effects Collapse at Scale Due to Baseline Motivation Heterogeneity

**Source**: BFI/University of Chicago - "Scaling Nudges: The Roles of Baseline Motivation and Substitution Effects" - February 2025; Hu et al. (2025) - "Assessing Nudge Impact: A Comprehensive Second-Order Meta-Analysis" - Journal of Behavioral Decision Making
**Document Type**: Large-Scale RCT Analysis; Second-Order Meta-Analysis
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-21
**Session**: 2026-02-21 Behavioral Economics Intertemporal Choice

---

## Core Insight

The "voltage drop" problem in nudge theory is now empirically documented at national scale: nudge effects that appear strong in pilot studies and website-user samples collapse when applied to general or administrative populations. The primary mechanism is baseline motivation heterogeneity - nudge effects depend critically on the population having sufficient pre-existing motivation to be nudged, and most real-world deployment fails this condition. After correcting for publication bias, the aggregated nudge effect size drops from d = 0.27 to d = 0.004.

---

## Evidence

**BFI/University of Chicago Study (2025)**:
**Study Design**: Analysis of 123 RCTs covering 20+ million people
**Key Results**:
- Intervention efficacy is significantly smaller among individuals with low baseline motivation
- Study populations with high baseline motivation (website users) show strong effects
- Administrative/population-wide samples show weak effects
- Substitution effects inflate apparent impact when outcome measures are narrow in scope or time horizon

**Hu et al. Second-Order Meta-Analysis (2025, JBDM)**:
- 13 meta-analyses, 1,638 primary studies, ~30 million participants
- Raw aggregated effect size: d = 0.27 (95% CI [0.16, 0.38])
- After publication bias correction: d = 0.004 - effectively zero
- Most component meta-analyses rated low or critically low methodological quality

**NEW mechanistic framework (ScienceDirect, 2025)**:
A nudge will work only if it is aligned with the underlying economic incentives of the decision-maker. Behavioral nudges fail when the economically optimal choice for the individual differs from the nudged choice.

---

## Why This Differs from the Existing Vault Note

The vault already contains [[Nudges Show Near-Zero Effects After Publication Bias Correction]] from the December 2025 session covering the Hu et al. meta-analysis. This note adds the NEW mechanistic explanation from the BFI scaling study (published February 2025, after that session):

1. **The "why" of the failure**: Baseline motivation heterogeneity is the primary driver, not just publication bias
2. **The screening test**: Before scaling any nudge, assess whether the target population has the motivational baseline required
3. **The mechanistic rule**: Nudges fail when economically optimal choice ≠ nudged choice
4. **The substitution problem**: Narrow outcome measurement inflates apparent impact by missing substitution effects

This is operationally different from just knowing "nudges don't work at scale" - it specifies the condition under which they can work.

---

## What Still Works (Evidence-Supported)

Despite the general skepticism, some nudge types retain empirical support:
- **Decision structure interventions** (defaults) consistently outperform description-based interventions
- **Food choice architecture** shows effect sizes up to 2.5x larger than other domains
- **Soft commitment devices** (appointments) outperform hard financial commitments in real-world health settings
- **Planning prompts** (implementation intentions): robust effectiveness in multiple domains
- **Temptation bundling**: pairing desired and undesired activities effectively counters delay

---

## The Implication for Behavioral Intervention Design

The proper framework is now:

1. **Before designing**: Does the target population have baseline motivation for the desired behavior?
2. **If high motivation**: Traditional nudge approaches can work
3. **If low motivation**: Nudges will fail; need to address motivation root cause first
4. **Alignment check**: Is the nudged choice actually the economically optimal choice for this population?
5. **Outcome scope**: Are you measuring narrow outcomes that may show substitution effects?
