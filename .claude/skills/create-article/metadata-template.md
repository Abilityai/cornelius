# Article Metadata Template

Use this template for the `_metadata.md` file in each article folder.

---

## Template

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: [model-name]
updated_by: [model-name]
agent_version: 01.25
---

# Article Metadata: [Article Title]

## Creation Record

**Title:** [Full article title]
**Created:** YYYY-MM-DD
**Author:** Eugene Kurogo (via Cornelius agent)
**Status:** Draft | Review | Ready | Published
**Platform:** Substack | Medium | LinkedIn | Blog | -

## Source Insights

This article synthesizes the following permanent notes and documents:

### Primary Sources
1. **[[Note Name]]** - [Brief description of how it's used]
2. **[[Note Name]]** - [Brief description]
3. **[[Note Name]]** - [Brief description]

### Supporting Knowledge Base Notes
4. **[[Note Name]]** - [Brief description]
5. **[[Note Name]]** - [Brief description]

### Document Insights Referenced
- [Document insight session/note if applicable]

## Thinking Process

[2-3 sentences max describing the synthesis approach or key insight that drove the article]

## Key Original Contributions

1. **[Contribution 1]** - [One sentence description]
2. **[Contribution 2]** - [One sentence description]

## Publication Record

| Date | Platform | URL |
|------|----------|-----|
| - | - | - |
```

---

## Example

```yaml
---
created: 2026-01-25
updated: 2026-01-25
created_by: claude-opus-4-5-20251101
updated_by: claude-opus-4-5-20251101
agent_version: 01.25
---

# Article Metadata: Cognitive-Aware AI Systems

## Creation Record

**Title:** Designing AI Agents for Human Depth: A Research Exploration
**Created:** 2026-01-25
**Author:** Eugene Kurogo (via Cornelius agent)
**Status:** Draft
**Platform:** -

## Source Insights

### Primary Sources
1. **[[Human-Cognitive-Aware Agent Design Principle]]** - Core framework for article
2. **[[AI agents create forced multitasking through wait-time arbitrage]]** - Central observation

### Supporting Knowledge Base Notes
3. **[[Attention as Universal Selection Pressure]]** - Theoretical grounding
4. **[[Flow is a selfless state]]** - Connection to flow states research
5. **[[Dopamine]]** - Reward fragmentation hypothesis

## Thinking Process

Article emerged from recognizing the conflict between AI parallelism optimization and human cognitive constraints. Synthesized neuroscience research with production AI patterns.

## Key Original Contributions

1. **Forced Multitasking Mechanism** - 6-step cycle explaining latency-induced context switching
2. **Dopamine Fragmentation Hypothesis** - Interrupted task completion disrupts reward cycles

## Publication Record

| Date | Platform | URL |
|------|----------|-----|
| - | - | - |
```

---

## Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| created | Yes | Date article was first created (YYYY-MM-DD) |
| updated | Yes | Date of last modification |
| created_by | Yes | Model that created the article |
| updated_by | Yes | Model that last modified |
| agent_version | Yes | Cornelius version (currently 01.25) |
| Title | Yes | Full article title |
| Status | Yes | Draft, Review, Ready, or Published |
| Platform | No | Target publication platform |
| Primary Sources | Yes | Main permanent notes used (3-5) |
| Supporting Notes | No | Additional notes referenced |
| Thinking Process | Yes | Brief synthesis description (2-3 sentences max) |
| Key Contributions | No | Original frameworks or insights |
| Publication Record | No | Fill in when published |

---

## Notes

- Keep this file SHORT - it's a record, not documentation
- Primary sources should link to actual permanent notes
- Update the Publication Record when article is published
- The thinking process helps future reference - why was this article written this way?
