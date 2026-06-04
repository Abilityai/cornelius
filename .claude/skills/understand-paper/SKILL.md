---
name: understand-paper
description: Understand a research paper or deep technical concept by extracting its key concepts, finding the learner's prerequisite-knowledge frontier through multiple-choice probing, then teaching the gap concept-by-concept with worked numerical examples and gated quizzes. Use when the user wants to deeply understand a paper (arXiv link, PDF, or topic), asks to "learn" or "be tutored on" something technical, or hits a paper above their current level.
argument-hint: <arxiv-url | pdf-path | topic>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, WebFetch, mcp__qmd__deep_search, mcp__qmd__get
---

# Understand Paper — Adaptive Prerequisite Tutor

Turn a paper (or technical topic) the learner cannot yet follow into a
personalized curriculum, then teach it. The skill finds the gap between what the
learner already knows and what the paper demands, then closes that gap one
concept at a time with worked examples and comprehension gates.

**Input:** `$ARGUMENTS` — an arXiv id/URL, a local PDF path, a PDF URL, or a bare
topic name.

## Operating principle

Concepts form a **dependency DAG** (fundamental → advanced). The paper's key
concepts are the targets. The learner's knowledge is a downward-closed region of
that DAG; its boundary is the **frontier**. The distance from frontier to targets
is the **gap**, and the topologically-sorted gap is the **curriculum**. Read
`references/frontier-assessment.md` for the full model before Phase 2.

## Bundled resources

- `scripts/extract_paper.py` — full-text extraction from arXiv/PDF. Run with
  `uv run` (deps auto-install): `uv run .claude/skills/understand-paper/scripts/extract_paper.py "<input>" /tmp/paper.txt`
- `references/frontier-assessment.md` — the DAG-probing algorithm and gap computation. Load before Phase 2.
- `references/pedagogy.md` — the per-concept teaching loop, worked-example rules, and gating-question design. Load before Phase 4.
- `assets/learning-path-template.md` — the learning-path file structure (copy and fill).

## Workflow

### Phase 0 — Ingest

1. Detect input kind from `$ARGUMENTS`:
   - **arXiv / PDF URL / local PDF** → run `extract_paper.py` to dump full text
     to a temp file, then `Read` that file. (For a local PDF you may also Read it
     directly, but the script avoids truncation on long papers.)
   - **Bare topic** → skip extraction; treat the topic as the target. Optionally
     use `qmd deep_search` to find any source notes the user already has on it.
2. Create the learning-path file (see Phase 1).

### Phase 1 — Extract key concepts

1. Read the paper and identify its **key claims** (what it actually asserts) and
   the **key concepts** required to understand those claims. These concepts are
   the DAG's target sinks.
2. Build the **concept dependency DAG**: trace each key concept down through its
   prerequisites to fundamentals. Capture edges (`A -> B` = B needs A).
3. Copy `assets/learning-path-template.md` to:
   `hekate/01-Sources/Learning Paths/[slug]/[slug].md`
   (kebab-case slug from the paper/topic). Fill in source, key claims, and the
   DAG. Use the Cornelius frontmatter (set `created`/`updated` to today, the
   `*_by` fields to your model name, `agent_version: 02.25`, `status: assessing`).

### Phase 2 — Locate the frontier (probing)

Follow `references/frontier-assessment.md`. Summary:

1. Order concepts by DAG depth.
2. **Check the vault first** (cheap signal): `qmd deep_search` for each concept.
   If the user has substantive notes on a concept, treat that as provisional
   evidence of KNOWN and probe to confirm rather than from scratch.
3. Probe efficiently with `AskUserQuestion` multiple-choice questions, starting
   mid-chain and binary-searching the boundary. Batch 2-4 independent probes per
   call. One concept per question; always include a "Not sure" option and treat
   guessed-correct / low-confidence as UNKNOWN.
4. Aim for ~4-8 questions total, not an exhaustive sweep — downward closure does
   the rest.
5. Record statuses in the learning-path file's frontier table.

### Phase 3 — Build the curriculum

1. Compute the **gap**: UNKNOWN concepts on any path from the frontier to the key
   concepts.
2. **Topologically sort** the gap — this is the teaching sequence.
3. Write it into the learning-path file's "The Gap (Curriculum)" checklist.
4. Edge cases:
   - Empty gap → skip teaching; go straight to a guided walk of the key claims.
   - Very large gap → tell the learner, and offer to either teach the whole path
     or pick an intermediate `session_target` and resume later.
5. Show the learner the curriculum and confirm before teaching.

### Phase 4 — Teach the gap, concept by concept

Follow `references/pedagogy.md`. For each curriculum concept in order:

1. Anchor to the nearest KNOWN concept.
2. Explain the idea concisely (what, why, the one load-bearing sentence).
3. Walk a **concrete numerical example** with small hand-checkable numbers and
   every intermediate step — this is mandatory.
4. **Gate** with 2-3 `AskUserQuestion` questions testing transfer to a slightly
   different case. Do not advance until passed.
5. On a wrong answer, diagnose the misconception the chosen distractor reveals,
   re-teach that piece from a new angle with a fresh example, then re-gate.
6. Update the concept's checkbox and Progress Log entry in the learning-path file
   (set `updated`/`updated_by`) before moving on.

### Phase 5 — Close

1. Walk the learner through the paper's **key claims** using the concepts just
   learned — the payoff that proves the gap is closed.
2. Set `status: complete` (or note deferred concepts and the resume point if the
   session was split).
3. Tell the user the full output path and open the folder:
   `open "hekate/01-Sources/Learning Paths/[slug]/"`
4. Optionally suggest running `/refresh-index` so the new learning path is
   searchable.

## Resuming

If a learning-path file already exists for this input, read it, report the
current frontier and progress, and continue from the first unchecked curriculum
concept instead of re-assessing.

## Notes

- Use hyphens, never em-dashes (house style).
- All quizzes use the native `AskUserQuestion` picker, not plain-text A/B/C/D.
- The learning-path file is the single source of truth and the resume point —
  keep it current as you go, not only at the end.
