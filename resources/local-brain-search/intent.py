#!/usr/bin/env python3
"""
Intent classification for queries.

Classifies queries into four categories:
- factual: Looking for specific information
- conceptual: Exploring a topic area
- synthesis: Finding connections between ideas
- temporal: Recent or historical focus

Inspired by SimpleMem's intent-aware retrieval.
"""
import re
from dataclasses import dataclass
from enum import Enum


class QueryIntent(Enum):
    FACTUAL = "factual"
    CONCEPTUAL = "conceptual"
    SYNTHESIS = "synthesis"
    TEMPORAL = "temporal"


@dataclass
class IntentClassification:
    """Result of intent classification."""
    intent: QueryIntent
    confidence: float
    reasoning: str


# Pattern-based classification rules
FACTUAL_PATTERNS = [
    r"^what is\b",
    r"^what are\b",
    r"^who is\b",
    r"^who are\b",
    r"^define\b",
    r"^definition of\b",
    r"^explain\b",
    r"\bmeaning of\b",
    r"^find\b.*\bnote\b",
    r"^get\b.*\bnote\b",
    r"^show me\b",
    r"^look up\b",
    r"\bspecifically\b",
    r"\bexactly\b",
]

CONCEPTUAL_PATTERNS = [
    r"^how does\b",
    r"^how do\b",
    r"^why does\b",
    r"^why do\b",
    r"\babout\b",
    r"\bexplore\b",
    r"\bunderstand\b",
    r"\blearn\b",
    r"\bconcept\b",
    r"\bframework\b",
    r"\btheory\b",
    r"\bmodel\b",
    r"\bideas?\b.*\babout\b",
    r"\bthoughts?\b.*\bon\b",
]

SYNTHESIS_PATTERNS = [
    r"\bconnect\b",
    r"\brelate\b",
    r"\brelation\b",
    r"\blink\b",
    r"\bbridge\b",
    r"\bbetween\b",
    r"\bcompar[ei]",
    r"\bcontrast\b",
    r"\bsimilar\b",
    r"\bpattern\b",
    r"\btheme\b",
    r"\bacross\b",
    r"and.*and",  # Multiple topics
    r"\+",  # Explicit combination
    r"\bsynthes",
    r"\bintegrat",
    r"\bcombine\b",
]

TEMPORAL_PATTERNS = [
    r"^recent\b",  # "recent" at start gets high weight
    r"\brecent\b",
    r"\brecently\b",
    r"\blatest\b",
    r"\bnew\b",
    r"\btoday\b",
    r"\byesterday\b",
    r"\bthis week\b",
    r"\blast week\b",
    r"\bthis month\b",
    r"\blast month\b",
    r"\b202[4-9]\b",  # Year references
    r"\bjanuary\b|\bfebruary\b|\bmarch\b|\bapril\b|\bmay\b|\bjune\b",
    r"\bjuly\b|\baugust\b|\bseptember\b|\boctober\b|\bnovember\b|\bdecember\b",
    r"\bhistor",
    r"\bold\b",
    r"\boriginal\b",
    r"\bearlier\b",
    r"\bprevious\b",
]


def _score_patterns(query: str, patterns: list[str]) -> float:
    """Score how many patterns match the query."""
    query_lower = query.lower()
    score = 0.0
    for p in patterns:
        if re.search(p, query_lower):
            # Patterns starting with ^ (beginning of query) get extra weight
            if p.startswith('^'):
                score += 0.5
            else:
                score += 0.3
    # Normalize with diminishing returns
    return min(1.0, score + (0.1 if score > 0 else 0))


def classify_intent(query: str) -> IntentClassification:
    """
    Classify query intent using heuristic patterns.

    Returns the most likely intent with confidence score.
    """
    query = query.strip()

    # Score each intent type
    scores = {
        QueryIntent.FACTUAL: _score_patterns(query, FACTUAL_PATTERNS),
        QueryIntent.CONCEPTUAL: _score_patterns(query, CONCEPTUAL_PATTERNS),
        QueryIntent.SYNTHESIS: _score_patterns(query, SYNTHESIS_PATTERNS),
        QueryIntent.TEMPORAL: _score_patterns(query, TEMPORAL_PATTERNS),
    }

    # Additional heuristics

    # Short queries are often factual lookups
    if len(query.split()) <= 3 and scores[QueryIntent.SYNTHESIS] < 0.3:
        scores[QueryIntent.FACTUAL] += 0.2

    # Questions with multiple concepts suggest synthesis
    concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', query)
    if len(concepts) >= 2:
        scores[QueryIntent.SYNTHESIS] += 0.2

    # Queries with "my" or "I" suggest conceptual exploration
    if re.search(r'\bmy\b|\bI\b', query):
        scores[QueryIntent.CONCEPTUAL] += 0.15

    # Find highest scoring intent
    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    # If no clear winner, default to conceptual (safest for exploration)
    if best_score < 0.2:
        best_intent = QueryIntent.CONCEPTUAL
        best_score = 0.5
        reasoning = "No strong pattern match, defaulting to conceptual exploration"
    else:
        # Build reasoning
        matched_patterns = []
        if best_intent == QueryIntent.FACTUAL:
            for p in FACTUAL_PATTERNS:
                if re.search(p, query.lower()):
                    matched_patterns.append(p)
        elif best_intent == QueryIntent.CONCEPTUAL:
            for p in CONCEPTUAL_PATTERNS:
                if re.search(p, query.lower()):
                    matched_patterns.append(p)
        elif best_intent == QueryIntent.SYNTHESIS:
            for p in SYNTHESIS_PATTERNS:
                if re.search(p, query.lower()):
                    matched_patterns.append(p)
        elif best_intent == QueryIntent.TEMPORAL:
            for p in TEMPORAL_PATTERNS:
                if re.search(p, query.lower()):
                    matched_patterns.append(p)

        reasoning = f"Matched patterns: {matched_patterns[:3]}" if matched_patterns else "Heuristic scoring"

    return IntentClassification(
        intent=best_intent,
        confidence=min(1.0, best_score + 0.3),  # Boost confidence for matched patterns
        reasoning=reasoning,
    )


def get_spreading_config(intent: QueryIntent) -> dict:
    """Get spreading activation configuration for an intent type."""
    from memory_config import MEMORY_CONFIG
    intent_configs = MEMORY_CONFIG["spreading"]["intent_configs"]
    return intent_configs.get(intent.value, intent_configs["conceptual"])


if __name__ == "__main__":
    # Test cases
    test_queries = [
        "What is dopamine?",
        "How does motivation work?",
        "Connect dopamine and Buddhism",
        "Recent notes about AI agents",
        "Dopamine",
        "relationship between identity and belief",
        "my thoughts on consciousness",
        "latest insights on memory systems",
        "explain spreading activation theory",
        "patterns across neuroscience and AI",
    ]

    print("Intent Classification Tests")
    print("=" * 60)

    for query in test_queries:
        result = classify_intent(query)
        print(f"\nQuery: {query}")
        print(f"  Intent: {result.intent.value}")
        print(f"  Confidence: {result.confidence:.0%}")
        print(f"  Reasoning: {result.reasoning}")
