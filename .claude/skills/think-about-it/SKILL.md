---
name: think-about-it
description: Free-form thinking mode - consider a topic through successive distinct knowledge-base perspectives (hub lenses, original frameworks, wildcard distant notes). One perspective pass per invocation, state persists across runs, emits [[DONE]] when the exploration weaves together. Loop-compatible by design.
automation: autonomous
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
user-invocable: true
argument-hint: "<topic> (free text; first run creates the thinking file, later runs continue it)"
---

# Think About It

Free-form counterpart to the incubation loop. No hypotheses, no confidence tracking, no fixed move rotation - just the same topic viewed through a different KB lens each pass, until the perspectives weave into something worth keeping.

## Purpose

Put Cornelius in open thinking mode on a topic. Where `/incubation-loop` converges on an answer to a question, `/think-about-it` circles a topic - each pass looks through one distinct perspective drawn from the knowledge base and writes down what that lens reveals, distorts, or contradicts. The exploration ends with a Weave: a synthesis of the threads and candidate permanent-note seeds.

## Loop Compatibility Contract

This skill is designed to be driven by a loop (`/loop`, `/trinity:loop`, or manual re-invocation):

- **One perspective pass per invocation** (single-task rule; each pass completes in well under 10 minutes)
- **All state lives in the topic file** - safe across separate context windows; no in-session memory assumed
- **Fixed reply format** (Step 7) so `{{previous_response}}` chaining and Until-mode sentinels work
- **`[[DONE]]` appears in the reply if and only if** the topic file's status is `woven` - tied to verifiable file state, not self-assessment
- **Idempotent on woven topics** - re-invoking a finished topic re-reports the Weave and `[[DONE]]` without writing anything

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Topic file | `Brain/05-Meta/Thinking/Freeform/[slug].md` | ✓ | ✓ | Perspective passes + frontmatter state |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Semantic search (`--no-track`) |
| Permanent notes | `Brain/02-Permanent/` | ✓ | | Evidence + wildcard lens source |
| MOCs | `Brain/03-MOCs/` | ✓ | | Hub lens grounding |

**Deliberately NOT in `THINKING-REGISTRY.md`** - freeform topics are invisible to the incubation loop. The two engines never touch each other's state. If a Weave concludes the topic deserves rigorous treatment, promote it manually via `/manage-thinking-topics`.

## Process

### Step 1: Resolve Topic and State

`$ARGUMENTS` = the topic, free text. Slugify to kebab-case.

```bash
date '+%Y-%m-%d'
ls "Brain/05-Meta/Thinking/Freeform/" 2>/dev/null
```

- File `Brain/05-Meta/Thinking/Freeform/[slug].md` missing → create it from the template below (`pass_count: 0`, `status: exploring`), then continue.
- No arguments given → list existing freeform topics with their status and pass counts, exit cleanly (no `[[DONE]]`).
- File exists with `status: woven` → reply with the Weave summary and end with `[[DONE]]`. Write nothing.

### Step 2: Pick the Next Lens

Read `lenses_used` from frontmatter. Choose exactly ONE unused lens from the deck:

**Hub lenses** (the KB's thematic centers of gravity):
Dopamine & Motivation · Flow & Peak Performance · Buddhism & Consciousness · AI Agents & Architecture · Decision-Making & Biases · Identity & Belief Systems · Attention Economics

**Framework lenses** (the user's original frameworks - view the topic from inside one):
Uncertainty-Dopamine-Belief Loop · The Folder Paradigm · Cross-Domain Consilience · External Anchor Principle · Self-Construction Stack · Three Gaps Framework · Four Pillars of Deep Agency · Safety as Velocity

**Wildcard lens** (auto-discovery style - a random permanent note from an unrelated cluster):
```bash
python3 -c "import random,glob; print(random.choice(glob.glob('Brain/02-Permanent/*.md')))"
```
Re-roll once if the sampled note is obviously about the topic itself; otherwise the friction is the point.

Selection rules:
- Never reuse a lens within a topic.
- Prefer the unused lens with the most *generative friction* - not the most obviously related one. Obvious relevance produces summary; friction produces thought.
- By pass 4 at least one wildcard must have been used; if not, this pass is a wildcard.

### Step 3: Gather KB Material Through That Lens

```bash
# --no-track: autonomous reads must not train q-values (learning hygiene, same as incubation-loop)
# read role: reasoning (contract: scope-mount) - the reasoning mount, so a lens can land on what the user has READ, not only what he wrote
BRAIN_READ_SCOPE=core,Books,document-insights python3 resources/local-brain-search/search.py "[topic] [lens core terms]" --limit 6 --mode spreading --no-track 2>/dev/null
BRAIN_READ_SCOPE=core,Books,document-insights python3 resources/local-brain-search/search.py "[lens core concept]" --limit 4 --mode spreading --no-track 2>/dev/null
```

Read the 3-4 most promising notes in full. These ground the pass - every pass must cite real notes, and a `Books/` or `Document Insights/` note is cited as encountered material, never as the user's view.

### Step 4: Think

Write 2-4 paragraphs of actual free-form thinking: What does the topic look like from inside this lens? What does this lens make visible that previous passes missed? What does it distort or refuse to see? Capture analogies, tensions, reframings, open questions.

- No hypotheses, no confidence percentages - that is the incubation loop's job.
- If a thread contradicts an earlier pass, name the contradiction explicitly and leave it standing. Premature resolution kills the weave.
- Preserve the user's framing vocabulary where the notes supply it.

### Step 5: Append the Pass

Append to the topic file:

```markdown
### Pass [N]: Through the lens of [Lens Name] - YYYY-MM-DD

**Notes consulted:** [[Note A]], [[Note B]], [[Note C]]

**What this lens reveals:**
[2-4 paragraphs from Step 4]

**Threads pulled:**
- [tension / analogy / question worth keeping - 1 line each]

**Novelty:** high | medium | low
```

Rate novelty honestly: `high` = a genuinely new thread appeared; `medium` = deepened an existing thread; `low` = mostly re-derived prior passes. The honest `low` is what lets the loop terminate.

Update frontmatter: `pass_count`, `lenses_used`, `last_two_novelty`, `updated`, `updated_by`.

### Step 6: Weave Check

Weave when EITHER:
- `pass_count >= 7`, OR
- the last two passes are both `novelty: low` (the lenses have stopped paying)

If weaving, append:

```markdown
---

## The Weave

[3-6 paragraphs braiding the threads: the strongest cross-lens pattern, the contradiction
that stayed productive, what the topic turned out to actually be about]

**Candidate permanent-note seeds:**
- [2-3 one-line seeds that could become atomic notes]

**Promote to incubation?** [yes + suggested central question | no + why not]
```

Set `status: woven` in frontmatter.

### Step 7: Reply (Fixed Contract)

- **Not woven:** `Pass N - lens: [lens]. [The single most interesting thread, 1-2 sentences.] Continuing.`
- **Woven:** 2-3 sentence Weave summary + the candidate note seeds + final line `[[DONE]]`

The reply ends with `[[DONE]]` if and only if status is `woven`.

## Looping Recipes

**Remote (Trinity), Until mode - the demo shape:**
```
/trinity:loop git pull --rebase, then run /think-about-it "<topic>", then commit and push;
relay the skill's reply verbatim — until done, max 10, every 30s
```
(`stop_signal: [[DONE]]`, `max_runs: 10`, `delay_seconds: 30`, `timeout_per_run: 1200`)

**Local dynamic loop:** `/loop run /think-about-it "<topic>"; stop when the reply contains [[DONE]]`

**Manual:** just invoke `/think-about-it "<topic>"` repeatedly; each call advances one pass.

## Topic File Template

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: [model-name]
updated_by: [model-name]
agent_version: 01.25
topic: "[topic as given]"
pass_count: 0
lenses_used: []
last_two_novelty: []
status: exploring
---

# Thinking Freely: [Topic Title]

## Topic
[The topic as given, one sentence of framing if needed]

---
*[Perspective passes appended below by /think-about-it]*
```

## Error Handling

| Error | Recovery |
|-------|----------|
| `Freeform/` directory missing | Create it, continue |
| KB search returns empty | Retry with alternate terms from the lens; if still empty, ground the pass in the wildcard note alone and say so in the pass |
| All lenses in the deck used before weave | Force weave this pass regardless of novelty |
| Topic file corrupt / unparseable frontmatter | Rename to `[slug]-corrupt-YYYY-MM-DD.md`, recreate fresh, note the reset in the new file |

## Completion Checklist

- [ ] Topic file resolved (created or loaded)
- [ ] One unused lens selected per the rules
- [ ] KB searched through the lens; 3-4 notes read in full
- [ ] Pass appended with notes cited and honest novelty rating
- [ ] Frontmatter state updated
- [ ] Weave check performed; Weave written if triggered
- [ ] Reply follows the fixed contract ([[DONE]] iff woven)
