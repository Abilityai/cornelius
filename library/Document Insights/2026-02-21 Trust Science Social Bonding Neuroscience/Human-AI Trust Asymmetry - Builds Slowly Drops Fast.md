---
title: Human-AI Trust Asymmetry - Builds Slowly Drops Fast
type: research-finding
evidence-level: moderate
tags: #research-finding #AI-trust #human-AI #trust-calibration #overtrust #undertrust #asymmetry #design-implication
created: 2026-02-21
updated: 2026-02-21
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Human-AI Trust Asymmetry - Builds Slowly Drops Fast

**Source**: Multiple: (1) "Trust Formation, Error Impact, and Repair in Human-AI Financial Advisory: A Dynamic Behavioral Analysis" - *MDPI Behavioral Sciences* 2025 (https://www.mdpi.com/2076-328X/15/10/1370); (2) "Developing trustworthy artificial intelligence: insights from research on interpersonal, human-automation, and human-AI trust" - *Frontiers in Psychology* 2024 (https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1382693/full); (3) Interdisciplinary Human-AI Trust Research (I-HATR) Framework 2024
**Document Type**: Research Papers / Framework
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-21
**Session**: 2026-02-21 Trust Science Social Bonding Neuroscience

---

## Core Insight

Human trust in AI systems has fundamentally different temporal dynamics than trust in humans: trust builds more slowly via accuracy cues and familiarity but drops more rapidly after AI errors than after equivalent human errors. Simpler tasks show greater trust degradation following errors. This asymmetry has critical design implications - AI systems need explicit error recovery mechanisms to prevent irreversible trust collapse.

---

## Evidence

**Study Design**: Behavioral study in financial advisory contexts; longitudinal review of automation trust research (30 years)

**Key Results**:
- **Slower trust building**: AI trust builds more slowly than human trust - requires more repeated accuracy demonstrations
- **Faster trust loss**: Trust loss after AI errors occurs MORE rapidly than with human error
- **Task complexity effect**: Simpler tasks show *greater* trust degradation following AI errors (counterintuitive - when AI seems simpler, errors appear more inexplicable)
- **Trust formation phases** (financial advisory study): Formation via accuracy cues → single-error shock → post-error repair via explanations
- **Over-trust failure mode**: Systematic over-reliance even when AI contradicts available evidence - mere knowledge that advice originates from AI can cause over-reliance
- **Under-trust failure mode**: Trusting AI below its capability leads to underutilization and productivity loss

**I-HATR Framework - Three Core Dimensions**:
1. Trustor characteristics (user attributes)
2. Trustee attributes (AI system properties)
3. Interactive context (task, environment, relationship)

**Replication**: Based on 30-year longitudinal review of automation trust research and 2024-2025 papers

---

## The Over-Trust / Under-Trust Problem

| Failure Mode | Mechanism | Consequence |
|-------------|-----------|-------------|
| Over-trust | Trusting AI beyond actual capability | Misuse, safety failures, automation bias |
| Under-trust | Trusting AI below actual capability | Underutilization, productivity loss |
| Calibrated trust | Confidence aligned with actual capability | Optimal human-AI performance |

**Key insight**: Calibrated trust requires transparency, appropriate uncertainty communication, and task-aligned explanations. Neither too much transparency (undermines confidence) nor too little (creates misplaced trust) is optimal.

---

## Design Implications

1. **Error recovery mechanisms are not optional** - given the asymmetric temporal dynamics, a single error can permanently collapse accumulated trust
2. **Post-error explanations matter**: The 2025 study showed explanations after single errors help repair trust - they engage the mentalizing circuit (Circuit 2) to interpret the error as non-diagnostic of future behavior
3. **Uncertainty communication**: AI systems must communicate uncertainty authentically - not just confidence scores, but in context-appropriate ways
4. **Task-aligned explanations**: The type of explanation should match the task type and user mental model
