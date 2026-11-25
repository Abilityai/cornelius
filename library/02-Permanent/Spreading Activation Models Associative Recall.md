---
created: 2025-01-01
tags: [memory, graph-theory, search]
type: permanent
---

# Spreading Activation Models Associative Recall

Spreading activation is a model of memory in which activating one concept automatically energizes the concepts connected to it. Activation flows outward across a network of associations, with strength diminishing as it travels farther from the starting point.

The model originated in cognitive psychology to explain why recalling one idea makes related ideas easier to retrieve, and it has since informed how networked information systems rank results. When a starting node is activated, energy passes along its edges to neighboring nodes, then to their neighbors, weakening with distance so that closely related items receive the most activation. Applied to a note collection, beginning from one note and spreading activation across its links surfaces a ranked neighborhood of associated notes. This mirrors how human memory retrieves by association rather than by exact address.

**Why this matters**: It provides a principled way to retrieve not just a matching note but its most relevant associated notes.

**Related concepts**:
- [[Knowledge Graphs Make Connections Visible]] - the network across which activation spreads
- [[Semantic Search Versus Keyword Search]] - an alternative, similarity-based route to relevance
- [[Spaced Repetition Strengthens Retention]] - both concern how associative memory is accessed and reinforced
