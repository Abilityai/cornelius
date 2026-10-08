---
name: decide
description: Structure a decision, not just advise on it. Switches modes when the question is "what should we do" - expands the real option set (status quo, defer, pilot, hybrids), classifies the decision type (reversibility, one-shot vs repeated, ruin exposure, risk vs radical uncertainty), applies the MATCHING decision rule (ergodic filter, expected-value decomposition, robustness / minimax regret, value-of-information), and delivers a recommendation with tripwires. KB-grounded in the user's own decision-science frameworks; runs the full reasoning-checks battery. Use when options or stakes are on the table ("X or Y?", "is it worth", go/no-go) - not for open exploration (/advise, /think-about-it) and never to relitigate a decision canon has already made (/canon-advise).
automation: autonomous
allowed-tools: [Bash, Read, Grep, Glob]
user-invocable: true
argument-hint: "<the decision - options, stakes, constraints in natural language>"
when_to_use: The question presents a choice between courses of action with real stakes - "should we do X or Y", "go/no-go on Z", "is it worth doing W now". Prefer /advise when the ask is understanding or framing; prefer /canon-advise when a company's canon already covers the direction.
metadata:
  version: "1.0"
  created: 2026-07-31
  updated: 2026-07-31
  author: Ability.ai
  changelog:
    - "1.0: Initial version - standalone decision-theoretic sibling of /advise (per the 2026-07-31 self-audit + cross-model consensus: a separate skill, never an /advise mode-switch). Option-set expansion, decision-type classification, rule-matched recommendation (ergodic filter / EV / robustness / VoI), tripwires, full reasoning-checks battery"
---

# Decide

> ℹ️ **First, set expectations:** print one line with this skill's version and its most recent change - the top of `metadata.changelog` - e.g. `decide v1.0 — recent: initial decision-structuring skill`. Then proceed.

## Purpose

`/advise` produces a better **map**; `/decide` produces a **choice**. When the question is "what should we do", frameworks alone under-deliver - the output must be a recommendation produced by an explicit decision rule, with the losing options accounted for and tripwires attached. The KB skeleton is decision science (Kahneman / Gilbert / Tetlock / Thaler / Kay-King, bound by Ergodicity); this skill is where that skeleton actually decides instead of only describing.

## Problem

$ARGUMENTS

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| LBS search | `resources/local-brain-search/run_search.sh` | ✓ | |
| Core hubs (attractor check) | `resources/local-brain-search/run_connections.sh --hubs --json` | ✓ | |
| KB notes | `Brain/**/*.md` | ✓ | |
| Reasoning-checks contract | `.claude/skills/reasoning-checks/SKILL.md` | ✓ | |
| Canon (conditional) | `Brain/Canon/**/*.md` via canon-mounted search | ✓ | |

Never writes. A decision brief may be saved to `Brain/05-Meta/Reports/` **only on explicit request** (Step 8).

## Composes

- `reasoning-checks` - the shared discipline contract (applied per its applicability matrix, this skill runs the full battery)

## Process

### Step 1: Decision Guard (route before structuring)

Confirm this is actually a decision: **two or more real courses of action, stakes, and someone who must choose**. If it is understanding-seeking ("help me think about X") → `/advise` or `/think-about-it`. If it is a company-direction question canon already covers → `/canon-advise` governs; **never relitigate a decided direction** - `/decide` may still structure a *new* decision that canon leaves open (run one canon-mounted search `BRAIN_READ_SCOPE=core,Canon` when the subject smells like company direction; if a `decision`/`spec` note decides it, say so and stop).

### Step 2: Frame the Decision

One block, before any retrieval:
- **Decision statement** - the choice in one sentence
- **Decider + deadline** - who chooses, by when, and what forces the timing (a decision with no deadline may be a defer candidate by default)
- **Irreversibility horizon** - what becomes hard to undo, and when

### Step 3: Parallel Retrieval (one batch)

Same fast-path discipline as `/advise` - no subagents, static search, one parallel batch. **Read role: reasoning** (contract: `scope-mount`): two passes per term, `core` as the spine and the reasoning mount as the evidence layer; run the `scope-mount` trigger check first and append `,company` / `,thinkers` / `,Books/<slug>` to the wide pass on a hit.

```bash
BRAIN_READ_SCOPE=core                          resources/local-brain-search/run_search.sh "[domain term 1]" --limit 3 --json
BRAIN_READ_SCOPE=core,Books,document-insights  resources/local-brain-search/run_search.sh "[domain term 1]" --limit 5 --json
BRAIN_READ_SCOPE=core                          resources/local-brain-search/run_search.sh "[domain term 2]" --limit 3 --json
BRAIN_READ_SCOPE=core,Books,document-insights  resources/local-brain-search/run_search.sh "[domain term 2]" --limit 5 --json
BRAIN_READ_SCOPE=core                          resources/local-brain-search/run_search.sh "[decision-structure term: ergodicity / optionality / reversibility / regret / explore exploit - match to the decision's shape]" --limit 3 --json
BRAIN_READ_SCOPE=core,Books,document-insights  resources/local-brain-search/run_search.sh "[the same decision-structure term]" --limit 5 --json
resources/local-brain-search/run_connections.sh --hubs --json   # fingerprint - always core; for the attractor check
```

Then read the 2-4 most relevant notes in parallel (frontmatter `provenance:` rides along for the checks).

### Step 4: Expand the Option Set

The stated options are almost never the full set. Always add and assess:
- **Status quo** - explicitly, with its own costs (doing nothing is a choice)
- **Defer** - wait for information; a real option with a price (cost of delay) and a payoff (uncertainty resolved)
- **Pilot / staged commitment** - buy information while moving
- **Hybrids** - combinations the framing hid

Mark which options **preserve optionality** and which foreclose it.

### Step 5: Classify the Decision (this selects the machinery)

| Axis | Question | Consequence |
|------|----------|-------------|
| **Reversibility** | Two-way or one-way door? | One-way → more analysis, prefer option-preserving moves |
| **Frequency** | One-shot or repeated? | Repeated → play expected value; one-shot → tails dominate |
| **Ruin exposure** | Does any option carry an absorbing barrier (can't come back from the bad tail)? | Ergodic filter applies BEFORE any EV math |
| **Uncertainty regime** | Are probabilities honestly estimable (risk), or is this radical uncertainty? | Radical uncertainty → robustness/regret, NOT invented probabilities |

### Step 6: Consequence Table + the Matching Rule

Build a compact table: options × the 2-4 uncertainties that actually drive the outcome. Probabilities **only where estimable** and reference-class anchored (Check 4); payoffs in natural units, not scores.

Then apply the rule the classification selected - in this order:

1. **Ergodic filter first** - eliminate any option with ruin exposure regardless of its EV ("EV-positive but you can't survive the bad branch" is a losing bet by the user's own core framework). Name what it eliminated.
2. **Risk + repeated/reversible** → **expected-value decomposition** - show the components, not just the total.
3. **Radical uncertainty** → **robustness + minimax regret** - which option is acceptable across all live scenarios; which minimizes the worst regret. Do NOT fake point probabilities to force an EV number - saying "this is not probabilizable" is the Kay-King discipline, not a cop-out.
4. **Value of information** - if defer/pilot resolves a driving uncertainty and the delay cost is tolerable, the real option can beat both stated options.
5. **Regret cross-check** - long-lens (would the 10-year view flip this?). A cross-check, never the primary rule.

### Step 7: Reasoning Checks (required - full battery)

Apply `.claude/skills/reasoning-checks/SKILL.md`:
- **Epistemic Inversion** on the recommendation - the pre-mortem is *made* for decisions; specific falsifier required
- **Reference Class** - required in practice (a decision embeds forecasts; anchor every estimated probability/magnitude)
- **Attractor Check** - against the hubs fetched in Step 3. **Scope nuance:** the check applies to the *situation framing/diagnosis*, not to the decision machinery itself - decision-science hubs (Decision Making, Ergodicity, Superforecasting) are this skill's tools by construction and do not count as attractor pull. What counts: the *diagnosis* leaning on 2+ top hubs.
- **Provenance Base** - from the notes read in Step 3

### Step 8: Decision Brief (output)

```markdown
## Decision: [one-line statement]

**Type:** [reversible? one-shot/repeated? ruin exposure? risk/radical uncertainty] → **Rule applied:** [ergodic filter → EV | robustness/minimax regret | value-of-information]

**Option set considered:** [stated + added options; which were eliminated and by what]

**Consequence table:** [options × driving uncertainties]

**Recommendation:** [the choice, produced by the named rule - and why the losing options lose]

**Tripwires (revisit if):**
- [observable condition → what it changes]
- [date-based checkpoint if the decision was defer/pilot]

**KB grounding:** [[Note 1]], [[Note 2]] - [how each shaped the structure]

[reasoning-checks blocks: Epistemic Inversion · Reference Class · Attractor Check · Provenance Base]
```

**On explicit request only:** save the brief to `Brain/05-Meta/Reports/decision-[slug]-YYYY-MM-DD.md` (`provenance: ai-inferred`, standard frontmatter) - decision briefs are terminal deliverables, exactly what `Reports/` is for. Never auto-save.

## Rules

- **NO subagent spawning** - fast path, all inline
- **Parallel batches** - searches + hubs in one round, reads in one round; checks reuse those results
- **The recommendation must name its rule** - "this is an EV call" vs "this is a robustness call" is the whole point of the mode-switch; a recommendation with no named rule is `/advise` output wearing a costume
- **Never fake probabilities under radical uncertainty** - the regime classification is honest or the machinery is theater
- **Ruin trumps EV** - the ergodic filter is not optional when an absorbing barrier is live
- **Tripwires always** - a decision brief without revisit conditions is a prediction, not a decision
- If the KB lacks relevant frameworks, say so and structure the decision from general principles, labelled as such
