---
name: insight-interview
description: KB-grounded Socratic interview. Searches existing notes on a topic, then runs a one-question-at-a-time dialogue to surface, sharpen, and extract your own thinking. Ends by running extract-insights on the full conversation transcript.
automation: manual
allowed-tools: [Bash, Read, Write, Glob, Grep, Task]
user-invocable: true
argument-hint: "<topic>"
---

# Insight Interview

A Socratic dialogue grounded in your own knowledge base. It finds what you already think, then probes the edges - gaps, underdeveloped claims, contradictions, missing connections - one question at a time. Your responses feed directly into the vault at the end.

## Purpose

Not to summarize a topic. Not to explain research. To find out what *you* actually think - and make that thinking precise enough to live in the knowledge base.

The KB is the context, not the content. Every question is anchored in a note you already wrote.

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Existing notes | `Brain/` via Local Brain Search | ✓ | |
| Permanent notes | `Brain/02-Permanent/` | ✓ | |
| Dialogue transcript | `resources/insight-interview-[slug]-[date].md` | | ✓ |
| Extracted insights | `Brain/AI Extracted Notes/` | | ✓ (via extract-insights) |

## Process

### Step 1: Search the KB

Run semantic search on the topic using Local Brain Search:

```bash
(cd resources/local-brain-search && python search.py "[topic]" --top_k 15 --mode spreading)
```

Also run a keyword grep across permanent notes:

```bash
grep -rl "[topic keywords]" Brain/02-Permanent/ Brain/AI\ Extracted\ Notes/ | head -20
```

Read the top 8-10 results. Understand:
- What the user already believes about this topic
- Which claims are well-developed vs. sketched
- Where tensions or contradictions exist between notes
- What connections are asserted but not fully argued
- What's notably absent (a gap where you'd expect a note)

### Step 2: Map the Frontier

Before asking anything, internally map 5-7 candidate question zones:

- **Existing claim to probe**: A strong assertion in a note that could be sharpened or challenged
- **Gap**: An angle you'd expect him to have thought about but haven't found
- **Contradiction**: Two notes that pull in opposite directions
- **Connection**: A note that seems related to another topic he knows well - does he see it?
- **So-what**: A well-documented insight with no clear practical implication
- **Origin**: A belief stated as fact - where did it come from?
- **Frontier**: The newest or most uncertain note - what's unresolved?

Prioritize. You'll likely cover 5-8 of these in a session.

### Step 3: Open the Dialogue

Introduce with one sentence of context showing what you found in the KB, then ask the first question. Keep it grounded - reference the specific note or claim:

> "You have a note [[X]] where you say '[direct quote or paraphrase]'. Given [new angle / related note / recent development], do you still hold that? Or has your view shifted?"

OR for a gap:

> "You have strong thinking on [A] and [B], but I didn't find anything on [C] - which sits right between them. What's your actual take?"

**One question only.** Wait for the response.

### Step 4: Dialogue Loop

After each response, decide:

- **Deepen this thread**: The answer opened something - follow it (ask for evidence, for the counterargument, for the implication)
- **Mark and move**: Useful answer, but another zone is more promising - transition to the next question
- **Capture and close**: The response crystallized something - reflect it back precisely, confirm it's right, then move on

Question types to cycle through (from `elicitation-techniques`):

| Type | When to use | Example |
|------|------------|---------|
| **Clarification** | Vague or assumed term | "What exactly do you mean by [X] here?" |
| **Assumption excavation** | Strong claim stated as fact | "What would have to be false for this not to hold?" |
| **Counterargument** | One-sided note | "What's the strongest case against this?" |
| **Connection probe** | Two related notes not linked | "Does this relate to your thinking on [Y]?" |
| **Implication** | Well-documented insight with no so-what | "If this is true, what changes?" |
| **Origin** | Belief with no cited source | "Where does this come from? Experience, reading, both?" |
| **Precision** | Fuzzy claim | "How strong is this? Always? Sometimes? Under what conditions?" |

Aim for 6-10 exchanges. Stop when:
- You've covered the main frontier zones
- The conversation is producing diminishing returns
- The user says "done", "enough", or similar

### Step 5: Close

Before ending, ask one final open question:

> "Is there anything on this topic that you think is important but we haven't touched?"

Give space for any loose threads.

### Step 6: Save Transcript

Create a transcript file combining the full dialogue:

```
resources/insight-interview-[topic-slug]-[YYYY-MM-DD].md
```

Format:
```markdown
# Insight Interview: [Topic]
**Date**: YYYY-MM-DD
**KB notes consulted**: [list of note titles]
**Questions asked**: [count]

---

**[Question 1]**
[Response]

**[Question 2]**
[Response]

...

---
*Raw transcript for extract-insights processing*
```

### Step 7: Run Extract-Insights

Invoke the extract-insights skill on the transcript:

```
/extract-insights resources/insight-interview-[topic-slug]-[YYYY-MM-DD].md
```

This will:
- Deduplicate against existing KB
- Extract new insights in your voice
- Create or update notes in `Brain/AI Extracted Notes/`
- Log changes in `Brain/05-Meta/Changelogs/`

Report what was created or updated.

## Dialogue Principles

- **One question at a time.** Always. No lists of questions.
- **Show your work.** Reference the specific note you're drawing from. This makes it feel like a conversation with someone who read your stuff, not a generic interview.
- **Don't summarize back every time.** Only reflect back when something crystallized - and then be precise.
- **Follow energy.** If a response is animated or detailed, stay in that thread.
- **Don't lead.** The question opens space; it doesn't suggest the answer.
- **Tolerate "I don't know".** That's a real answer. Ask what would need to be true to know.

## Outputs

- Dialogue transcript: `resources/insight-interview-[slug]-[date].md`
- Extracted insight notes: `Brain/AI Extracted Notes/`
- Changelog entry: `Brain/05-Meta/Changelogs/`

## Usage

```
/insight-interview self-improving agents
/insight-interview dopamine and motivation
/insight-interview the folder paradigm
```
