# Pedagogy: Teaching a Gap Concept and Gating Progression

This reference governs the per-concept teaching loop (Phase 4 of the skill).
Apply it to each concept in the curriculum, in topological order.

## The per-concept loop

For each gap concept, run this loop. Do not advance to the next concept until
the learner passes the gate.

1. **Anchor to what they know.** Open by connecting the concept to the nearest
   KNOWN concept on its dependency chain ("You already know X; this extends it
   by..."). This makes the new idea an increment, not a cold start.
2. **Explain the idea** plainly: what it is, why it exists, what problem it
   solves, and the one sentence that, if remembered, captures it. Keep it tight
   -- a few paragraphs, not a textbook chapter.
3. **Walk a concrete numerical example.** This is mandatory and is the heart of
   the skill. See "Worked examples" below.
4. **Gate with multiple-choice questions.** 2-3 questions via `AskUserQuestion`.
   See "Gating questions" below.
5. **Branch on the result:**
   - All correct → confirm the key takeaway in one line, advance to the next
     concept, update the progress file.
   - Any wrong → diagnose the specific misconception the chosen distractor
     reveals, re-explain THAT piece (not the whole concept) from a different
     angle with a fresh example, then re-gate with new questions. Never just
     reveal the answer and move on.
6. **Record** the concept's status in the learning-path file before moving on.

## Worked examples (the differentiator)

Generic explanations are forgettable; worked numbers stick. For each concept:

- Use **small, hand-checkable numbers** (2x2 matrices, 3-token sequences,
  probabilities like 0.2/0.8) so the learner can follow every arithmetic step.
- Show **every intermediate step**, not just the result. The learner should be
  able to reproduce it with a pencil.
- Make the example **the same kind of object the paper uses**, scaled down. If
  the paper does attention over sequences, do attention over 3 tokens by hand.
- After the example, state what would change if a key quantity were different --
  this builds the intuition the gating questions will test.
- Where useful, give the learner a tiny variant to compute themselves before the
  gate ("now you try: what's the result if the second value is 0?").

## Gating questions

Gates verify *transfer*, not recall of the example just shown:

- Test whether the learner can apply the concept to a SLIGHTLY DIFFERENT case
  than the worked example. Recall of the example proves nothing.
- **Never reuse the worked example's numbers, vectors, or wording in a gating
  question.** Change the values (and ideally the framing) so a correct answer
  can only come from understanding, not from copying what was just shown. If a
  question could be answered by scrolling up, it is invalid — rewrite it.
- Every distractor should correspond to a specific, nameable misconception, so a
  wrong answer tells you exactly what to re-teach.
- Keep one concept per question. Use 2-3 questions to triangulate understanding
  from different angles (e.g. one computational, one conceptual, one edge-case).
- Include a "Not sure" option; treat its selection as not-yet-passed and
  re-teach rather than re-quiz.
- Calibrate to the concept's role: a load-bearing concept the paper leans on
  deserves a stricter gate than a peripheral one.

## Tone

- Treat the learner as intelligent but new to this specific idea. No
  condescension, no padding.
- Prefer plain language over jargon; when you must introduce a term, define it
  at first use and then use it consistently.
- Use hyphens, never em-dashes (house style).
- Be honest about difficulty. If a concept is genuinely hard, say so and slow
  down rather than glossing.

## Closing the session

When the curriculum is complete (or the session's chosen target is reached):

1. Return to the paper's **key claims** and walk the learner through them using
   the concepts they just learned -- this is the payoff and proves the gap is
   closed.
2. Summarize the path traveled: frontier → concepts learned → claims now
   accessible.
3. Update the learning-path file's status and progress.
4. Note any concepts deferred (if the gap was split across sessions) so a later
   run resumes cleanly.
