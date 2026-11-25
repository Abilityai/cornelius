---
title: The Probability of an Event Scales with the Number of Pathways That Produce It
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #probability #combinatorics #coincidence #sample-space #counting #randomness
---

# The Probability of an Event Scales with the Number of Pathways That Produce It
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 4
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
An outcome's probability is proportional to the number of distinct ways (ordered realizations) it can occur, not to its surface description. Symmetric-looking outcomes are therefore not equiprobable: when order-of-occurrence multiplies the pathways, an outcome with many orderings dominates one with few. This counting effect is the hidden engine behind apparent coincidence - we underestimate the explosive growth in the number of opportunities for a match.

## Mechanism / Why It Matters
The trap is treating an event by its label rather than by the realizations underneath it. Three dice showing a "triple" feels as special as any other total, but the count tells a different story: (3,3,3) has exactly 1 ordering while (6,3,1) has 6 distinct orderings (3! permutations). Aggregate the orderings under each total and a sum of 10 becomes slightly more probable than a sum of 9 - a difference that defeated even Galileo's contemporaries until the sample space was counted properly.

The same mechanism makes coincidences feel paranormal when they are routine. The birthday problem needs only 23 people for even odds of a shared birthday because the relevant count is the number of PAIRS (253 pairs among 23 people), which grows quadratically while naive intuition tracks the linear count of people. Whenever the pathways to an outcome multiply faster than we feel, we mislabel the expected as the miraculous - and reach for a special cause where mere counting suffices.

## Evidence
- Three dice: total of 10 arises via 27 ordered combinations vs 25 for a total of 9, a measurable asymmetry resolved only by enumerating the full ordered sample space.
- Birthday problem: 23 people yield 253 pairs and a >50% chance of a shared birthday; the count of pairs (n(n-1)/2) outpaces intuition that tracks n.
- (6,3,1) is 6x more likely than (3,3,3) as a dice triple because it has 3! = 6 ordered realizations versus 1.
