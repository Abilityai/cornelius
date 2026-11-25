---
title: LLMs Systematically Encode Western Cultural Values at Global Scale - 107-Country Audit
type: research-finding
evidence-level: high
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
tags: [research-finding, LLM, AI-bias, cultural-bias, WEIRD, GPT, world-values-survey, global-scale, epistemic-infrastructure, cultural-epistemics]
---

# LLMs Systematically Encode Western Cultural Values at Global Scale - 107-Country Audit

**Source**: Tao, Y., et al. "Cultural bias and cultural alignment of large language models." *PNAS Nexus*, Vol. 3, Issue 9, pgae346, September 2024. https://academic.oup.com/pnasnexus/article/3/9/pgae346/7756548
**Supporting**: Messner, W., Greene, T., & Matalone, J. "From Bytes to Biases: Investigating the Cultural Self-Perception of Large Language Models." *SAGE Journals*, 2025. https://journals.sagepub.com/doi/10.1177/07439156251319788
**Supporting**: "How Well Do LLMs Represent Values Across Cultures? Empirical Analysis Based on Hofstede Cultural Dimensions." arXiv, 2024. https://arxiv.org/html/2406.14805v2
**Supporting**: Cultural Biases in LLM Recommendations. Emergent Mind, 2024-2025. https://www.emergentmind.com/topics/cultural-biases-in-llm-recommendations
**Document Type**: Multiple empirical audits and cross-cultural studies
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Cultural Cognition Social Epistemics

---

## Core Insight

Five generations of GPT models (GPT-3 through GPT-4o) all exhibit a **consistent and persistent bias toward self-expression values** - including environmental protection, tolerance of diversity, and gender equality - characteristic of English-speaking Protestant European nations. This bias holds across 107 countries and territories, five model versions, and multiple independent research teams. The bias appears structural (driven by training data composition and development team values), not correctable through simple optimization. When generating recommendations under baseline conditions, 80% of named entities come from WEIRD countries, rising to 92.2% for person recommendations and 100% for product recommendations.

---

## Evidence

**Primary Study (PNAS Nexus, September 2024)**:
- 107 countries and territories evaluated
- 5 GPT model versions (GPT-3 through GPT-4o) tested
- Comparison benchmark: World Values Survey (WVS) - largest global measure of cultural values
- Bias type: Toward "self-expression values" (Protestant European, English-speaking nations)
- Bias consistency: "Remarkably consistent" across all model versions
- **Critical finding**: Persistence across model generations suggests structural origin, not iterative error

**GLOBE Project Study (SAGE Journals, 2025)**:
- ChatGPT and Bard cultural self-perception both aligned most closely with English-speaking countries
- Used GLOBE project value questions (designed for cross-cultural organizational research)

**Hofstede Analysis (arXiv, 2024)**:
- GPT-4, GPT-4o, Llama 3, Command R+, Gemma tested against Hofstede's cultural dimensions
- Finding: "Cultural insensitivity and preference for dominant values" across all models

**Recommendation Audit (Emergent Mind, 2024-2025)**:
- Baseline conditions: 80% of named entities from WEIRD countries
- Product recommendations: 100% from WEIRD countries
- Person recommendations: 92.2% from WEIRD countries

**AI-to-Human Bias Feedback Loop (ScienceDaily, December 2024)**:
- Biased AI systems "can alter people's own beliefs" - not just reflect them
- "Polarization started to increase" when biased AI systems influence users over time
- Creates bidirectional amplification: biased humans create biased AI; biased AI makes humans more biased

---

## Why This Is Structurally Different from Previous Bias Problems

Prior cultural bias in knowledge systems (textbooks, academic journals, mainstream media) operated through:
- Selection effects (who gets published, cited)
- Distribution limits (language barriers, economic access)
- Institutional gatekeeping (universities, publishers)

LLM cultural bias operates through:
- **Universal access** - anyone with internet can query an LLM
- **Conversational framing** - bias appears as neutral facts or balanced perspectives
- **Scale** - billions of queries per day vs. millions of textbook readers
- **Feedback loops** - user behavior shapes future training data
- **Opacity** - users cannot identify what cultural priors are embedded in responses

The result: the most consequential epistemic infrastructure in human history is built on the cultural priors of approximately 12% of the world's population.

---

## Distinction from LLMs Show Human-Like but Culturally Biased Moral Foundations

The existing vault note [[LLMs Show Human-Like but Culturally Biased Moral Foundations - AI as Moral Agent]] covers LLM moral bias specifically (omission bias, moral foundations framework). This note covers a broader scope: LLM **cultural values** bias (World Values Survey, Hofstede dimensions, GLOBE project) across all domains, not just moral judgment. These are complementary but distinct problems:
- Moral foundations bias: *How* LLMs reason about right and wrong
- Cultural values bias: *What* LLMs treat as normal, recommended, desirable across all topics
