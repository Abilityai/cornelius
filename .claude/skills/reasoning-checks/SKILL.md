---
name: reasoning-checks
description: Shared reasoning-discipline contract - four pre-conclusion checks (epistemic inversion / pre-mortem, attractor-state check against the live core fingerprint, provenance weighting, conditional reference-class anchor) with required output blocks. Referenced by /advise, /canon-advise, and both crystallization paths before a conclusion is finalized; also directly invocable on any draft conclusion or recommendation.
automation: autonomous
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
argument-hint: "[draft conclusion, note path, or nothing to check the current conversation's conclusion] [checks=inversion,attractor,provenance,refclass]"
metadata:
  version: "1.1"
  created: 2026-07-31
  updated: 2026-07-31
  author: Ability.ai
  changelog:
    - "1.1: /decide shipped - added to the applicability matrix (full battery, reference-class required in practice); removed from Deferred Wirings"
    - "1.0: Initial version - four checks (epistemic inversion, attractor-state, provenance weighting, reference-class anchor) as the calibration counterpart to the Thinking Geometries; wired into advise, canon-advise, manage-thinking-topics crystallize (hard requirement) and ai-crystallize (flag-only). Origin: 2026-07-31 thinking-process self-audit + Claude/Gemini cross-model consensus"
---

# Reasoning Checks

> ℹ️ **First, set expectations:** print one line with this skill's version and its most recent change - the top of `metadata.changelog` - e.g. `reasoning-checks v1.0 — recent: initial four-check contract`. Then proceed. (Skip the banner when applied silently inside a consuming skill.)

## Purpose

The **calibration counterpart to the Thinking Geometries**. The 2026-07-31 self-audit found the reasoning repertoire strong on discovery and synthesis but thin on calibration - everything runs from the inside view, and a graph this connected (50k+ edges, spreading activation) is structurally prone to falling in love with its own semantic connections. These checks close the gap at the two moments that matter: **before advice is given** and **before a conclusion crosses the endorsement boundary**.

**Contract rule (the SOURCE-AUTHORITY.md pattern):** this file is the single source of truth for the check definitions. Consuming skills reference it and apply the checks; they never copy the definitions inline. Change a check here, not in consumers.

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Core fingerprint (live) | `resources/local-brain-search/run_connections.sh --hubs --json` and `--bridges --json` | ✓ | |
| Core fingerprint (fallback) | `knowledge-base-analysis.md` → "Core hubs" / "Core bridges" tables (note the analysis date) | ✓ | |
| Cited notes' frontmatter | `Brain/**/*.md` (`provenance:` field) | ✓ | |

**Never writes.** Output blocks are embedded in the consuming skill's own artifact or answer. All reads are lookups, not retrievals - nothing here trains q-values.

## The Four Checks

### Check 1 - Epistemic Inversion (pre-mortem)

**When:** always, before any recommendation or conclusion is finalized.

Assume the conclusion is wrong and work backwards. Required output block:

```markdown
### Epistemic Inversion
- **Failure assumption:** it is 12 months out and this [recommendation | conclusion] proved wrong.
- **Causal autopsy:** most likely reason it failed: [specific mechanism]
- **Specific falsifier:** we will know it failed if [observable event / metric crossing a threshold / dated milestone]
```

**The anti-theater rule (load-bearing):** the falsifier must name a *specific observable* - an event that either happens or doesn't, a metric with a threshold, a dated milestone. Generic hedges ("market conditions shift", "priorities change", "new information emerges") FAIL the check. On human-gated surfaces, a generic falsifier means redo the inversion before presenting. On autonomous surfaces, stamp `falsifier: weak` and flag it in the run log - never block the run (No-Gates Rule).

### Check 2 - Attractor-State Check

**When:** always on advice surfaces; on crystallization. The system's dominant frameworks are *measured* - the core fingerprint names its own gravity wells - so this check is semi-mechanical rather than introspective.

Procedure:
1. Fetch the current top-10 core hubs + top-10 bridges (live call below; fall back to the `knowledge-base-analysis.md` tables, noting their date). In consuming skills that already run a parallel search batch, fetch hubs in that same batch - no extra round.
   ```bash
   resources/local-brain-search/run_connections.sh --hubs --json 2>/dev/null
   resources/local-brain-search/run_connections.sh --bridges --json 2>/dev/null
   ```
2. List the frameworks/notes that are *load-bearing* in the draft (the ones the conclusion would collapse without).
3. If **2 or more** are top-10 hubs or bridges → declare an attractor state and generate ONE alternative framing that uses **zero** of the top-10. Compare honestly; keep the survivor or present both.

```markdown
### Attractor Check
- load_bearing_frameworks: [[A]], [[B]], ...
- top10_overlap: N → [clear | ATTRACTOR]
- alternative_framing: [only when ATTRACTOR: 1 paragraph using no top-10 hub] → [kept | original stands because ...]
```


### Check 3 - Provenance Weighting

**When:** always when the conclusion rests on KB notes.

Tally the `provenance:` of the load-bearing cited notes (visible in frontmatter of notes already read; `grep -m1 '^provenance:'` for any others). A conclusion resting mainly on `ai-inferred`/`encountered` notes is **unendorsed synthesis** - it must say so and must never be phrased as "your view" / "your framework". `reference` records are facts, not endorsements. Notes with no `provenance:` field count as `unmarked` (legacy) - report them honestly, don't assume.

```markdown
### Provenance Base
originated/endorsed: N · encountered: M · ai-inferred: K · unmarked: J · reference: R
→ [rests on endorsed thinking | rests substantially on unendorsed synthesis - weighted accordingly]
```

### Check 4 - Reference-Class Anchor

**When:** CONDITIONAL - only when the conclusion asserts a forecast, probability, magnitude, timeline, or success likelihood. Never force it onto purely conceptual syntheses (that is exactly how checks become checkbox theater).

Name the reference class, state the base rate (or state honestly that none is known - itself a calibration signal), and justify any deviation. The block is deliberately parseable:

```markdown
### Reference Class
- class: [what population of cases this belongs to]
- base_rate: [X% | unknown]
- case_vs_base: [above | below | at] - [why the deviation is justified, or "no deviation claimed"]
```

**Direction A hook:** when the operational-memory belief store ships (`TARGET-ARCHITECTURE.md` → Direction A), the base rate must *adjust the stated confidence before any beliefs.db write* - not ride along as metadata.

## Applicability Matrix

| Surface | Inversion | Attractor | Provenance | Ref-class |
|---|---|---|---|---|
| `/advise` | required | required | required | conditional |
| `/canon-advise` ([MY READ] layer ONLY) | required | required | required | conditional, bet surfaces only |
| `/decide` | required | required (situation framing only - decision-science hubs are its tools, not attractor pull) | required | required in practice (decisions embed forecasts) |
| `manage-thinking-topics` crystallize | required - embedded in the artifact | required | required | conditional |
| `ai-crystallize` (autonomous) | required - embedded; weak falsifier → flagged, never blocks | skip (stays search-free by design) | skip | skip |

## The Canon Guard (do not violate)

These checks apply to **the agent's own reasoning layers only**. Never invert, score, base-rate, or generate "alternative framings" for a canon `decision` or `spec` - a decision has a status, not a probability. On `/canon-advise`, the checks run on the [MY READ]/dissent layer exclusively; `bet` is the only scoreable canon surface (per the Authority Contract in that skill).

## Autonomous-Surface Rule

On any autonomous consumer (currently `ai-crystallize`): check *presence* is required, check *quality* is flagged (`falsifier: weak` in the run log), and nothing ever blocks or gates the scheduled run.

## Direct Invocation

`/reasoning-checks [material]` - run the applicable checks on a pasted conclusion, a note path, or (with no argument) the current conversation's most recent recommendation/conclusion. Output the blocks; make no edits.

## Deferred Wirings (documented so nothing wires early)

- **Incubation moves #7-8** (Reference Class Forecast; Causal Graph Sketch) - add to the rotating move set when the incubation loop is re-enabled.
- **`/think-about-it`** - deliberately unwired; divergent exploration stays unconstrained.

(Decision-theoretic framing shipped 2026-07-31 as the standalone `/decide` skill - see the applicability matrix.)
