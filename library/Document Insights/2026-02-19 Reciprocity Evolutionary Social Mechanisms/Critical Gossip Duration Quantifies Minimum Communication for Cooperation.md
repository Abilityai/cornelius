---
created: 2026-02-19
updated: 2026-02-19
created_by: claude-sonnet-4-5-20250929
updated_by: claude-sonnet-4-5-20250929
agent_version: 01.25
type: research-finding
evidence-level: high
tags: #research-finding #empirical-evidence #gossip #reputation #cooperation #indirect-reciprocity #communication
---

# Critical Gossip Duration Quantifies Minimum Communication for Cooperation

**Source**: Kawakatsu, M., Kessinger, T.A., & Plotkin, J.B. (2024). A mechanistic model of gossip, reputations, and cooperation. Proceedings of the National Academy of Sciences, 121(20), e2400689121
**Document Type**: Research Paper
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-19
**Session**: 2026-02-19 Reciprocity Evolutionary Social Mechanisms

---

## Core Insight

Researchers derived the first **quantitative formula for the minimum gossip duration (τ*)** required to sustain cooperation through indirect reciprocity. Without sufficient gossip, populations converge to pure defection. The critical gossip duration decreases with benefit-to-cost ratio and increases with assessment and execution errors - providing the first mathematical answer to "How much communication is required for large-scale human cooperation?"

---

## Evidence

**Study Design**: Three-timescale evolutionary model + stochastic simulations (N=100 populations, Wright-Fisher dynamics)

**Key Formula**:
```
τ* = [log 2 - (b/c)/(b/c - 1)] / [2(1-u_a)(b/c)/(b/c - (b/c)*)]
```

Where:
- b/c = benefit-to-cost ratio of cooperation
- u_a = assessment error rate
- u_e = execution error rate

**Key Properties**:
- τ* decreases monotonically with benefit-to-cost ratio (less gossip needed when cooperation highly beneficial)
- τ* increases with both types of errors (noisy environments require more communication)
- Peer-to-peer and single-source gossip mathematically equivalent under parameter transformation

**Results**:
- **Without gossip**: Populations converge to pure defection
- **Sufficient gossip**: Stabilizes discriminator strategies supporting high cooperation
- **Unbiased gossip noise**: Destabilizes cooperation
- **Biased gossip**: Can facilitate or hinder cooperation depending on direction

**Sample Size**: Theoretical derivation validated with computational simulations across parameter space

**Citation**: Published May 14, 2024, PNAS
