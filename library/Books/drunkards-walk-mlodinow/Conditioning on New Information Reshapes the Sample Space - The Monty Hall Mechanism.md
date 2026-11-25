---
title: Conditioning on New Information Reshapes the Sample Space - The Monty Hall Mechanism
type: principle
acceptance: established
source-tier: credible-interpreter
provenance: encountered
created: 2026-06-28
updated: 2026-06-28
created_by: claude-opus-4-8
updated_by: claude-opus-4-8
agent_version: 01.25
tags: #conditional-probability #sample-space #monty-hall #bayesian-reasoning #randomness
---

# Conditioning on New Information Reshapes the Sample Space - The Monty Hall Mechanism
**Source**: Leonard Mlodinow, *The Drunkard's Walk: How Randomness Rules Our Lives* (Pantheon, 2008) - Ch. 3
**Document Type**: Book
**Extracted By**: AI (document-insight-extractor, Book Mode)
**Extraction Date**: 2026-06-28
**Scope**: Books/drunkards-walk-mlodinow

## Core Insight
New information does not merely narrow a fixed probability - it eliminates branches from the sample space, and HOW that information was generated is itself part of the data. Monty Hall's act of opening a door is non-random: it is constrained by his knowledge of where the prize is, so it transfers the 2/3 probability mass of the two unchosen doors onto the single remaining unopened door. Switching therefore wins 2/3 of the time.

## Mechanism / Why It Matters
The intuition that two remaining doors are 50/50 fails because it treats Monty's reveal as a random event that simply removes one option. But Monty never opens the door with the prize and never opens your door - his choice is conditioned on the truth. That constraint is information. Your original door had a 1/3 chance and that probability is frozen at the moment you chose; the host's deliberate, knowledge-laden action concentrates the other 2/3 onto the door he declined to open.

The general lesson is that the *generating process* of evidence must be modeled, not just the evidence itself. The same observation can carry different probabilistic weight depending on whether it arose by chance or by a constrained, informed mechanism. This is the engine behind the whole conditional-probability cluster: conditioning is sample-space surgery, not a vague "update."

A sub-case is the two-children problem. "Given that one child is a girl" removes only the (boy, boy) branch from the four equally-likely orderings (GG, GB, BG, BB), leaving three, of which one is two-girls - hence 1/3, not 1/2. The unspecified-which condition is what makes this differ from naming a specific child.

## Evidence
Monty Hall: switching wins with probability 2/3 versus 1/3 for staying - a factor-of-two advantage that contradicts near-universal intuition (the problem famously fooled many PhDs and a prominent mathematician when posed publicly). Two-daughter variant: P(two girls | at least one girl) = 1/3, derived directly by enumerating the four equally-likely ordered sequences and deleting the single excluded branch.
