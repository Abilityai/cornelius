---
title: Trust Mediates Cognitive Offloading Decisions
type: research-finding
evidence-level: moderate
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
tags: #research-finding #trust #cognitive-offloading #HCI #tool-design #calibration
---

# Trust Mediates Cognitive Offloading Decisions

**Source**: [Authors]. (2025). "Cognitive Offloading in Short-Term Memory Tasks: Trust Toward Tools as a Moderator." Human-Computer Interaction (Tandfonline). DOI: 10.1080/10447318.2025.2474449.
**Document Type**: Research Paper
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Extended Mind Cognitive Augmentation

---

## Core Finding

The decision to offload cognitive tasks to external tools is not determined solely by task difficulty or memory load - users' **subjective trust in external tools** mediates whether and how much they offload.

- **High trust**: Users offload more, even when this is suboptimal
- **Low trust** (even in accurate tools): Users maintain unnecessary internal cognitive load, leading to suboptimal strategy use
- **Miscalibrated trust** (trusting inaccurate tools): Produces the worst outcomes - unnecessary offloading to unreliable systems

---

## Implication: Trust Calibration as Design Priority

For AI tool design, this finding establishes trust calibration as a first-order design concern - not trust maximization.

**What AI tool design typically optimizes for**: User trust (smooth experience, confident outputs, high satisfaction)

**What this research shows is needed**: Accurately calibrated trust - users should trust tools precisely to the degree those tools deserve trust

**Problem with current AI tool design**:
1. AI tools present confident outputs regardless of uncertainty
2. Sycophancy (per System 0 research) makes AI seem more aligned with user beliefs than it is
3. The result is systematic over-trust - users offload more than is rational
4. This produces cognitive debt (unnecessary offloading of integrative reasoning) while feeling appropriate

---

## The Black-Box Trust Problem

AI tools that are perceived as reliable but not clearly understood (black boxes) produce miscalibrated trust:
- Over-reliance: Users trust AI beyond its actual reliability
- Under-reliance: Users distrust AI that would actually be helpful (when they've experienced prior failures)

Neither produces optimal human-AI cognitive division. The solution is not more trust or less trust but better-calibrated trust - which requires AI to communicate its uncertainty and limitations clearly.
