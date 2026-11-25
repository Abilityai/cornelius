---
created: 2026-02-20
updated: 2026-02-20
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
tags: [research-finding, AI, framing, cognitive-bias, LLM, confirmation-bias, decision-making, AI-safety]
---

# AI Systems Are Framing-Susceptible - Cognitive Mirroring or Statistical Property

**Source**: (1) "Cognitive Biases in Artificial Intelligence: Susceptibility of a Large Language Model to Framing Effect and Confirmation Bias." *Journal of Psychological Science*, 2025. (2) "Source framing triggers systematic bias in large language models." *Science Advances*, 2025.
**Document Type**: Research Findings (peer-reviewed, 2025)
**Extracted By**: AI (document-insight-extractor agent)
**Extraction Date**: 2026-02-20
**Session**: 2026-02-20 Language Metaphor Conceptual Thought

---

## Core Insight

LLMs (tested: Google's Gemini 1.5 Pro, DeepSeek) are systematically susceptible to framing effects and confirmation bias - the same cognitive distortions that affect human judgment. This means LLMs do not merely generate framed outputs; they are *recipients* of framing, meaning their "judgments" are as susceptible to linguistic manipulation as human judgments.

---

## Evidence

**Study 1 - Journal of Psychological Science, 2025**: Tested Gemini 1.5 Pro and DeepSeek for framing effects and confirmation bias. Results: both models exhibit these biases systematically.

**Study 2 - Science Advances, 2025**: "Source framing triggers systematic bias in large language models" - LLMs show significant variation in evaluative judgments depending on how the *source* of information is framed (not just the content).

---

## The Two Interpretations (Both Profound)

**Interpretation 1: Cognitive Mirroring**
LLMs have internalized human cognitive biases through training on human text. The framing susceptibility is a reflection of human psychology encoded in language patterns. LLMs are mirrors of human cognition - including its biases.

**Interpretation 2: Statistical Language Property**
Framing effects arise from general statistical properties of language rather than specifically human psychological vulnerabilities. If true, any sufficiently complex language model will be framing-susceptible regardless of training data - it is a property of language structure itself.

**Either interpretation has profound implications**: Interpretation 1 means LLMs reproduce human irrationality at scale. Interpretation 2 means framing susceptibility is even more fundamental - it is embedded in the architecture of language.

---

## Why This Is Counter-Intuitive

The default assumption is that AI would be immune to framing effects because:
- AI has no ego to defend
- AI has no emotional investment in outcomes
- AI processes all information as data

The finding shows this assumption is wrong. Framing susceptibility may not require human-like psychology - it may emerge from language processing itself.

---

## Implications for AI-Assisted Decision Making

Organizations deploying AI for consequential decisions (medical, legal, financial, hiring) need to account for:
1. **Prompt framing systematically biases outputs** - the same question asked differently generates different "judgments"
2. **Source framing biases AI evaluation** - how you describe the source of information affects how AI evaluates it
3. **Confirmation bias in AI** - AI may preferentially generate outputs that confirm implicit frames in the prompt

This is not about jailbreaking or adversarial attacks - it is about ordinary linguistic framing of the kind that occurs in every prompt.
