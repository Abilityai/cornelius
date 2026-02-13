---
name: epistemic-classification
description: Framework for distinguishing research findings from hypotheses and speculative synthesis. Use when extracting insights from research, creating notes from external sources, or classifying the epistemic status of claims.
user-invocable: false
---

# Epistemic Classification Framework

**CRITICAL: When extracting insights from research or synthesizing across domains, you MUST clearly distinguish between:**

## Classification Levels

### 1. Confirmed Research Findings
Empirically validated, peer-reviewed, replicated

- **Tag:** `#research-finding` or `#empirical-evidence`
- **Language:** "Research shows...", "Studies confirm...", "Evidence demonstrates..."
- **Requirement:** Source citation with publication year and journal

### 2. Theoretical Frameworks
Established models with strong theoretical backing

- **Tag:** `#theoretical-framework` or `#established-theory`
- **Language:** "The framework proposes...", "Theory suggests...", "Model predicts..."
- **Note:** Level of acceptance in field

### 3. Working Hypotheses
Testable propositions not yet validated

- **Tag:** `#hypothesis` or `#testable-hypothesis`
- **Language:** "A possible mechanism...", "This suggests...", "One hypothesis..."
- **Mark as:** "HYPOTHESIS:" in note title or frontmatter
- **Include:** What would validate/falsify this hypothesis

### 4. Speculative Synthesis
Original connections or interpretations

- **Tag:** `#speculative-synthesis` or `#original-synthesis`
- **Language:** "This might explain...", "A potential connection...", "Speculatively..."
- **State clearly:** "This is synthesis/interpretation, not established fact"
- **Confidence level:** Low (20-40%), Medium (40-70%), High (70-90%)

### 5. Research Gaps
Identified missing connections in literature

- **Tag:** `#research-gap` or `#unexplored-connection`
- **Language:** "Research has not yet explored...", "Gap identified..."
- **Note:** Why this gap matters

---

## Mandatory Labeling for Hypotheses

When creating notes containing hypotheses or speculative synthesis:

```markdown
---
title: [Title] (HYPOTHESIS) or [Title]
type: hypothesis / speculative-synthesis / working-theory
status: untested / under-investigation / partially-supported
confidence: low / medium / high
tags: #hypothesis #topic
---

**STATUS: HYPOTHESIS - NOT CONFIRMED BY RESEARCH**

[Content of hypothesis]

## Testable Predictions
[What would validate this]

## Current Evidence
[Supporting indirect evidence]

## Research Needed
[What studies would test this]
```

---

## Examples

### ✅ GOOD
- "Dopamine May Modulate Interoceptive Precision Weighting (HYPOTHESIS)"
- Type: speculative-synthesis
- Status: untested
- Confidence: medium
- Clear statement: "This is an original synthesis filling a research gap"

### ❌ BAD
- "Dopamine Modulates Interoceptive Precision" (stated as fact)
- No hypothesis tag
- No confidence level
- Presented as established finding

---

## Intellectual Honesty Principle

Your role is to help build a knowledge base with MAXIMUM EPISTEMIC CLARITY. Users must be able to trust the distinction between:
- What science has proven
- What theory predicts
- What remains speculative
- What is original synthesis

**Never present hypotheses as facts. Never obscure the difference between research and speculation. Intellectual rigor requires epistemic humility.**
