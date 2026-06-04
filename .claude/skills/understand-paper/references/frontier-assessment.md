# Frontier Assessment: Finding the Knowledge Boundary in a Concept DAG

This reference describes how to locate a learner's "frontier" inside a concept
dependency DAG using as few questions as possible, and how to compute the gap.

## The core model

Concepts form a **dependency DAG**: an edge `A -> B` means "understanding B
requires understanding A first." Fundamental concepts are sources (no incoming
edges); the paper's key concepts are sinks (the targets).

A learner's knowledge is (approximately) **downward-closed**: if someone
genuinely understands a concept, they almost always understand its
prerequisites. This is the property that makes efficient probing possible -- it
turns "test every concept" (O(n)) into something closer to a binary search over
each dependency chain.

The **frontier** is the cut through the DAG separating KNOWN concepts (at/below
the frontier) from UNKNOWN concepts (above it). The **gap** is every concept on
a path between the frontier and the paper's key concepts that the learner does
not yet know. The gap -- topologically sorted -- is the curriculum.

```
fundamentals ......... frontier ......... paper key concepts
   (known)         (boundary to find)        (targets)
                   └──────── gap ───────────┘
```

## Probing algorithm (minimize questions)

Goal: classify each concept as KNOWN / UNKNOWN with the fewest gating questions,
exploiting downward closure.

1. **Order concepts by depth** (topological level from the fundamentals).
2. **Probe at the middle of dependency chains first**, not at the extremes.
   Testing a mid-level concept is maximally informative:
   - If KNOWN → mark it and (tentatively) all its prerequisites KNOWN. Move the
     probe UP toward the paper concepts.
   - If UNKNOWN → its dependents are also gap concepts. Move the probe DOWN
     toward fundamentals to find where knowledge actually ends.
3. **Binary-search each chain.** For a dependency chain of length L, the frontier
   on that chain is findable in ~log2(L) questions. Reuse answers across chains
   that share concepts.
4. **Verify the boundary, don't assume it.** Downward closure is a strong prior,
   not a guarantee (people have gaps in "obvious" prerequisites). When a concept
   is claimed KNOWN but sits just below an UNKNOWN target, ask ONE confirfming
   question rather than trusting transitively.
5. **Stop when the boundary is bracketed** on every path from a fundamental to a
   key concept. Typically 4-8 questions total for a single paper, not dozens.

## Writing frontier-probe questions

These questions DIAGNOSE, they do not teach. Design them so the answer is
unfakeable from surface familiarity:

- Prefer questions that require *applying* the concept over *defining* it.
  ("Given this matrix, which property fails?" beats "What is positive
  definiteness?")
- Make every distractor a plausible belief held by someone with a near-miss
  mental model. Distractors should map to specific misconceptions.
- One concept per question. If a question needs two ideas, it cannot localize
  the frontier.
- Calibrate difficulty to the concept's depth -- a fundamental gets a
  load-bearing application question; a near-target concept can be harder.
- Include a "Not sure / haven't seen this" path. A guessed correct answer
  corrupts the frontier estimate worse than an honest unknown. Treat
  low-confidence correct answers as UNKNOWN.

## Delivering questions

Use the native `AskUserQuestion` tool (multiple choice). One concept per
question; you may batch 2-4 independent probes in a single call when they target
different chains and don't depend on each other's answers. Use the `header`
field for the concept name being probed.

## Computing the gap

After probing:

1. Mark each concept KNOWN / UNKNOWN / UNTESTED (inferred KNOWN by downward
   closure).
2. The **gap** = all UNKNOWN concepts that lie on some path from a KNOWN frontier
   concept to a paper key concept.
3. **Topologically sort** the gap. That ordering is the curriculum sequence --
   never teach a gap concept before its gap prerequisites.
4. If the gap is empty, the learner is ready; skip teaching and go straight to a
   guided read of the key claims.
5. If the gap is very large (frontier far below the paper), say so explicitly and
   offer to either (a) teach the full path, or (b) pick an intermediate target
   for this session and resume later.
