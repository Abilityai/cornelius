---
created: 2025-01-01
tags: [search, information-retrieval, methodology]
type: permanent
---

# Semantic Search Versus Keyword Search

Keyword search matches the exact words in a query against the words in documents, while semantic search compares meaning by representing text as numerical vectors. Semantic search can find relevant material even when it shares no words with the query.

Keyword search is fast, transparent, and precise when the right term is known, but it fails when the same idea is expressed in different words or when a query uses synonyms. Semantic search encodes text as embeddings, points in a high-dimensional space where similar meanings sit close together, so a query can retrieve conceptually related passages regardless of exact wording. The trade-off is that semantic results can be less predictable and may surface loosely related material. In practice the two approaches complement each other, with keyword matching providing precision and semantic matching providing recall across paraphrase.

**Why this matters**: It explains why meaning-based retrieval can surface relevant notes that exact-word search would miss entirely.

**Related concepts**:
- [[Knowledge Graphs Make Connections Visible]] - graphs add link-based retrieval alongside both search styles
- [[Spreading Activation Models Associative Recall]] - a graph-based retrieval idea related to semantic similarity
