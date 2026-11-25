---
title: Compulsivity as Hierarchical Control Failure - Transdiagnostic Dimension
type: research-finding
evidence-level: moderate
tags: #research-finding #compulsivity #OCD #addiction #hierarchical-RL #transdiagnostic #attentional-set
created: 2026-02-21
updated: 2026-02-21
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Compulsivity as Hierarchical Control Failure - Transdiagnostic Dimension

**Source**: "A Hierarchical Reinforcement Learning Model Explains Individual Differences in Attentional Set Shifting" (Talwar, Huys, Cormack, Roiser; Applied Computational Psychiatry Lab, CANTAB IED task analysis; September 26, 2024)
**Document Type**: Research Paper
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-21
**Session**: 2026-02-21 Computational Psychiatry Reward Systems

---

## Core Insight

Using CANTAB IED (Intra-Extra Dimensional Set Shifting) cognitive task data from two large independent population samples, hierarchical RL modeling provides a precise computational definition of compulsivity:

**Compulsivity = the inability to redirect attentional resources away from a learned feature dimension, even when contingencies change.**

This is mechanically defined as two separable deficits:
1. **Reduced learning velocity**: Slower updating of action values when contingencies change
2. **Increased attentional bias**: Excessive persistence of attention toward the initially relevant stimulus dimension

This computational phenotype appears transdiagnostically across OCD, addiction, and eating disorders - supporting the concept of a "compulsivity dimension" independent of diagnostic category.

---

## Evidence

**Study Design**: Hierarchical RL modeling applied to CANTAB IED task
**Samples**: Two large independent population samples
**Key Results**:
- Compulsive symptoms correlate with reduced learning velocity AND increased attentional bias toward initially relevant dimension
- Both components are independently measurable and separable
- Same computational phenotype appears across OCD, addiction, and eating disorders

---

## Why This Is More Precise Than "Habit"

The traditional description of compulsivity as "excessive habit" captures the surface phenomenon but misses the mechanism. This research identifies the specific RL failure:

- In healthy control: when contingencies change (the previously rewarded feature dimension stops being rewarded), attentional resources shift to the new relevant dimension
- In compulsivity: attentional resources remain locked to the old dimension even with explicit knowledge that contingencies have changed

This is NOT simply "habits overriding goals" - it is a failure of hierarchical attention allocation. The person knows the situation has changed; the brain's attentional machinery cannot follow.

---

## Clinical Implications

Different treatment targets for the two separable components:
- **Reduced learning velocity**: May respond to dopaminergic agents that accelerate reward learning
- **Attentional bias persistence**: May respond to cognitive training specifically targeting attentional set shifting
- Separating these computationally enables precision treatment selection
