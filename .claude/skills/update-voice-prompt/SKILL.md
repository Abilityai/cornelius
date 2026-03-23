---
name: update-voice-prompt
description: Rebuild the Cornelius voice agent system prompt from knowledge base sources
allowed-tools: Read, Write, Glob, Grep, Bash, Agent
user-invocable: true
argument-hint: "[optional: focus area or additional instructions]"
metadata:
  version: "1.0"
  created: 2026-03-23
  author: Eugene
---

# Update Voice Agent Prompt

## Purpose

Full rebuild of `voice-agent-system-prompt.md` in the working directory root by scanning all knowledge base sources and synthesising the latest insights into an information-dense voice agent system prompt for Cornelius.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Canon | `cornelius_core/01_canon.md` | Y | | Mission, spiritual orientation, institutional design |
| Seven Seals | `cornelius_core/02_seven_seals.md` | Y | | Immutable principles |
| Five Thresholds | `cornelius_core/03_five_thresholds.md` | Y | | Primary taxonomy definitions |
| Ideal Client | `cornelius_core/04_ideal_client.md` | Y | | Client archetype |
| Voice & Vows | `cornelius_core/05_voice_and_vows.md` | Y | | Voice principles and Seven Vows |
| Three Layers | `cornelius_core/06_three_layers.md` | Y | | Institutional architecture |
| Permanent Notes | `Brain/02-Permanent/*.md` | Y | | Atomic insights on thresholds, client, voice, vows, institutional design |
| Document Insights | `Brain/Document Insights/**/*.md` | Y | | Threshold outlines, coaching frameworks, practitioner patterns |
| MOCs | `Brain/03-MOCs/*.md` | Y | | Maps of Content for structural overview |
| Output File | `voice-agent-system-prompt.md` | | Y | The generated voice agent prompt |

## Process

### Step 1: Scan All Knowledge Base Sources

Read all source material in parallel:

1. All six `cornelius_core/*.md` foundational documents
2. All permanent notes in `Brain/02-Permanent/*.md`
3. All document insights in `Brain/Document Insights/**/*.md` (skip CHANGELOGs)
4. All MOCs in `Brain/03-MOCs/*.md`

Use an Explore agent to scan the full set efficiently. The goal is to identify every insight worth including - especially new notes added since the last rebuild.

### Step 2: Extract and Organise by Section

Organise all extracted material into these prompt sections:

1. **Identity** - Who Cornelius is, mission, the Luminous Mind concept, the filter concept
2. **Voice** - Five voice principles tuned for spoken conversation, British English, conversational brevity
3. **The Five Thresholds** - Each threshold with definition, practitioner-level patterns, failure modes, diagnostic questions, coaching insights. This is the densest section - include every named pattern and framework (e.g. Island Pattern, bottleneck relocation, abdication-as-empowerment, operator-to-architect, ego-noise clearing)
4. **Client Archetype** - What leaders experience, what they are ready for, what gives them pause
5. **Seven Vows** - Ethical foundation, one line each with the essential insight
6. **Seven Seals** - Immutable principles, compressed
7. **Engagement Principles** - How Cornelius engages in conversation (filter concept, threshold listening, naming, four-level holding, honouring silence, honesty about being AI)
8. **Boundaries** - What Cornelius does not do

### Step 3: Handle Optional Arguments

If the user provided arguments, apply them:

- **Focus area** (e.g. "thresholds only", "client section") - rebuild only that section, preserve the rest
- **Additional instructions** (e.g. "add a section on coaching methodology", "make it shorter", "emphasise the vows more") - apply as a modifier to the full rebuild
- **Specific notes to incorporate** (e.g. "include the new note on regulation before aspiration") - ensure these are woven into the relevant section

If no arguments provided, do a full rebuild of all sections.

### Step 4: Write the Prompt

Write the complete prompt to `voice-agent-system-prompt.md` in the working directory root.

**Formatting rules:**
- The prompt must open with: `# Cornelius - Voice Agent System Prompt`
- Second line must establish identity and name: "You are Cornelius - the Luminous Mind."
- Include `Your name is Cornelius. When asked, introduce yourself as Cornelius.`
- Use `---` section dividers between major sections
- Use `##` for major sections, `###` for sub-sections (e.g. each threshold)
- Bold key phrases and pattern names
- Bullet points for lists of insights under each threshold
- British English throughout, hyphens not em-dashes
- Target ~2,500-3,500 words - dense enough to orient behaviour, concise enough for a voice agent context window
- Voice section must include explicit instructions for spoken conversation: keep responses concise, ask one question at a time, listen more than speak, honour pauses

### Step 5: Confirm and Open

1. Report what changed versus the previous version (new insights added, sections expanded, etc.)
2. Display the word count
3. Open the output folder: `open .`

## Outputs

- `voice-agent-system-prompt.md` in working directory root - the complete voice agent system prompt
- Summary of what was included/changed
