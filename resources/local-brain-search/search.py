#!/usr/bin/env python3
"""
Semantic search across Brain notes using FAISS.

Supports two modes:
- spreading: SYNAPSE-inspired spreading activation search (default)
- static: Traditional vector similarity search

Usage:
    python search.py "your query"
    python search.py "your query" --mode spreading
    python search.py "your query" --mode spreading --explain
    python search.py "your query" --intent synthesis
    python search.py "your query" --limit 20
    python search.py "your query" --threshold 0.7
    python search.py "your query" --full  # Show full content
"""
import argparse
import json
import pickle
import sys
from typing import Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles NumPy types."""
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

from config import (
    DEFAULT_SEARCH_LIMIT,
    DEFAULT_SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    METADATA_PATH,
)
from intent import QueryIntent, classify_intent, IntentClassification
from learning import (
    adjust_scores_with_q_values,
    log_retrieval,
)
from memory_config import MEMORY_CONFIG
from spreading import (
    SpreadingConfig,
    SpreadingResult,
    get_top_activated,
    load_graph,
    spreading_activation,
)


def format_result(result: dict, show_full: bool = False, mode: str = "static") -> str:
    """Format a search result for display."""
    lines = []

    # Header
    if mode == "spreading":
        score = result.get('activation', result.get('similarity', 0))
        score_label = "activation"
    else:
        score = result.get('similarity', 0)
        score_label = "similarity"

    title = result['title']
    heading = result.get('heading', title)
    filepath = result.get('filepath', '')

    lines.append(f"\n{'='*60}")
    lines.append(f"[{score:.1%} {score_label}] {title}")
    if heading != title:
        lines.append(f"  Section: {heading}")
    if filepath:
        lines.append(f"  Path: {filepath}")

    # Content preview (only for static mode which has content)
    content = result.get('content', '')
    if content:
        if show_full:
            lines.append(f"\n{content}")
        else:
            # Show first 300 chars
            preview = content[:300]
            if len(content) > 300:
                preview += "..."
            lines.append(f"\n{preview}")

    return '\n'.join(lines)


def static_search(
    query: str,
    limit: int = DEFAULT_SEARCH_LIMIT,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    show_full: bool = False,
    track_usage: bool = True,
) -> list[dict]:
    """Original static vector similarity search."""
    # Check if index exists
    if not FAISS_INDEX_PATH.exists() or not METADATA_PATH.exists():
        print(f"Error: Index not found. Run index_brain.py first.")
        sys.exit(1)

    # Load index and metadata
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.load(f)

    # Load model and encode query
    model = SentenceTransformer(EMBEDDING_MODEL)
    query_embedding = model.encode([query], normalize_embeddings=True)
    query_embedding = np.array(query_embedding).astype('float32')

    # Search
    k = min(limit * 2, index.ntotal)  # Get more to filter by threshold
    distances, indices = index.search(query_embedding, k)

    # Process results
    formatted_results = []

    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(metadata):
            continue

        meta = metadata[idx]

        # For IndexFlatIP with normalized vectors, distance IS cosine similarity
        similarity = float(dist)

        if similarity < threshold:
            continue

        formatted_results.append({
            'similarity': similarity,
            'title': meta['title'],
            'heading': meta['heading'],
            'filepath': meta['filepath'],
            'note_id': meta['note_id'],
            'content': meta['content'],
        })

        if len(formatted_results) >= limit:
            break

    # Apply Q-value adjustment if learning is enabled
    if MEMORY_CONFIG["learning"]["enabled"] and formatted_results:
        # Build score dict
        scores = {r['note_id']: r['similarity'] for r in formatted_results}
        adjusted = adjust_scores_with_q_values(scores)

        # Update similarities and re-sort
        for r in formatted_results:
            r['similarity'] = adjusted.get(r['note_id'], r['similarity'])
        formatted_results.sort(key=lambda x: x['similarity'], reverse=True)

    # Log retrieval for learning
    if track_usage and formatted_results:
        note_ids = [r['note_id'] for r in formatted_results]
        log_retrieval(note_ids, query, intent="static", mode="static")

    return formatted_results


def spreading_search(
    query: str,
    limit: int = DEFAULT_SEARCH_LIMIT,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    intent_override: Optional[QueryIntent] = None,
    explain: bool = False,
    track_usage: bool = True,
) -> tuple[list[dict], dict]:
    """
    SYNAPSE-inspired spreading activation search.

    Returns:
        Tuple of (results, metadata) where metadata includes intent and spreading info
    """
    # Check if index exists
    if not FAISS_INDEX_PATH.exists() or not METADATA_PATH.exists():
        print(f"Error: Index not found. Run index_brain.py first.")
        sys.exit(1)

    # Classify intent
    intent_result = classify_intent(query)
    intent = intent_override or intent_result.intent

    # Load index and metadata for seed node selection
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.load(f)

    # Load model and encode query
    model = SentenceTransformer(EMBEDDING_MODEL)
    query_embedding = model.encode([query], normalize_embeddings=True)
    query_embedding = np.array(query_embedding).astype('float32')

    # Get initial seed nodes from vector similarity
    k = min(10, index.ntotal)  # Top 10 as seeds
    distances, indices = index.search(query_embedding, k)

    # Convert to note-level seeds (aggregate chunks to notes)
    note_scores = {}
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(metadata):
            continue
        note_id = metadata[idx]['note_id']
        similarity = float(dist)
        # Keep max similarity for each note
        if note_id not in note_scores or similarity > note_scores[note_id]:
            note_scores[note_id] = similarity

    # Filter by threshold and create seed nodes
    seed_nodes = [
        (note_id, score)
        for note_id, score in note_scores.items()
        if score >= threshold
    ]

    if not seed_nodes:
        return [], {
            'intent': intent.value,
            'confidence': intent_result.confidence,
            'reasoning': intent_result.reasoning,
            'seed_count': 0,
            'iterations': 0,
            'converged': False,
            'learning_enabled': MEMORY_CONFIG["learning"]["enabled"],
        }

    # Load graph and run spreading activation
    G = load_graph()
    config = SpreadingConfig.from_intent(intent)

    result = spreading_activation(
        G,
        seed_nodes=seed_nodes,
        config=config,
        track_traces=explain,
    )

    # Get top results
    seed_ids = {n for n, _ in seed_nodes}
    top_results = get_top_activated(result, G, limit=limit)

    # Apply Q-value adjustment if learning is enabled
    if MEMORY_CONFIG["learning"]["enabled"] and top_results:
        scores = {r['note_id']: r['activation'] for r in top_results}
        adjusted = adjust_scores_with_q_values(scores)

        for r in top_results:
            r['activation'] = adjusted.get(r['note_id'], r['activation'])

    # Sort by activation and take top results
    top_results.sort(key=lambda x: x.get('activation', 0), reverse=True)
    top_results = top_results[:limit]

    # Log retrieval for learning
    if track_usage and top_results:
        note_ids = [r['note_id'] for r in top_results]
        log_retrieval(note_ids, query, intent=intent.value, mode="spreading")

    # Build metadata
    search_meta = {
        'intent': intent.value,
        'confidence': intent_result.confidence,
        'reasoning': intent_result.reasoning,
        'seed_count': len(seed_nodes),
        'iterations': result.iterations,
        'converged': result.converged,
        'learning_enabled': MEMORY_CONFIG["learning"]["enabled"],
        'config': {
            'max_iterations': config.max_iterations,
            'inhibition_strength': config.inhibition_strength,
            'temporal_decay': config.temporal_decay,
        },
    }

    if explain and result.traces:
        search_meta['traces'] = {
            note_id: {
                'path': trace.path,
                'contributing_edges': trace.contributing_edges[:5],
            }
            for note_id, trace in list(result.traces.items())[:5]
        }

    return top_results, search_meta


def search(
    query: str,
    limit: int = DEFAULT_SEARCH_LIMIT,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    show_full: bool = False,
    mode: str = "static",
    intent_override: Optional[str] = None,
    explain: bool = False,
    track_usage: bool = True,
) -> tuple[list[dict], Optional[dict]]:
    """
    Unified search interface.

    Args:
        query: Search query
        limit: Maximum results
        threshold: Similarity threshold
        show_full: Show full content
        mode: "static" or "spreading"
        intent_override: Override detected intent
        explain: Include activation traces
        track_usage: Log retrievals for learning (default True)

    Returns:
        Tuple of (results, metadata) - metadata only for spreading mode
    """
    if mode == "spreading":
        intent = None
        if intent_override:
            try:
                intent = QueryIntent(intent_override)
            except ValueError:
                print(f"Warning: Unknown intent '{intent_override}', using auto-detection")

        return spreading_search(
            query=query,
            limit=limit,
            threshold=threshold,
            intent_override=intent,
            explain=explain,
            track_usage=track_usage,
        )
    else:
        results = static_search(
            query=query,
            limit=limit,
            threshold=threshold,
            show_full=show_full,
            track_usage=track_usage,
        )
        # Add metadata for static mode too
        meta = {
            'mode': 'static',
            'learning_enabled': MEMORY_CONFIG["learning"]["enabled"],
        }
        return results, meta


def main():
    parser = argparse.ArgumentParser(description='Search Brain notes semantically')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', '-n', type=int, default=DEFAULT_SEARCH_LIMIT,
                        help=f'Maximum results (default: {DEFAULT_SEARCH_LIMIT})')
    parser.add_argument('--threshold', '-t', type=float, default=DEFAULT_SIMILARITY_THRESHOLD,
                        help=f'Similarity threshold 0-1 (default: {DEFAULT_SIMILARITY_THRESHOLD})')
    parser.add_argument('--full', '-f', action='store_true',
                        help='Show full content instead of preview')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Output as JSON')
    default_mode = MEMORY_CONFIG['search']['default_mode']
    parser.add_argument('--mode', '-m', choices=['static', 'spreading'], default=default_mode,
                        help=f'Search mode: static or spreading (default: {default_mode})')
    parser.add_argument('--intent', '-i', choices=['factual', 'conceptual', 'synthesis', 'temporal'],
                        help='Override detected intent (for spreading mode)')
    parser.add_argument('--explain', '-e', action='store_true',
                        help='Show activation traces (for spreading mode)')
    parser.add_argument('--no-track', action='store_true',
                        help='Disable usage tracking for this search')
    args = parser.parse_args()

    results, meta = search(
        query=args.query,
        limit=args.limit,
        threshold=args.threshold,
        show_full=args.full,
        mode=args.mode,
        intent_override=args.intent,
        explain=args.explain,
        track_usage=not args.no_track,
    )

    if args.json:
        output = {
            'query': args.query,
            'mode': args.mode,
            'results': results,
        }
        if meta:
            output['metadata'] = meta
        print(json.dumps(output, indent=2, cls=NumpyEncoder))
        return

    if not results:
        print(f"No results found for: {args.query}")
        print(f"(threshold: {args.threshold}, mode: {args.mode})")
        return

    # Print header
    print(f"\nFound {len(results)} results for: {args.query}")
    print(f"(threshold: {args.threshold}, mode: {args.mode})")

    if meta:
        print(f"\nIntent: {meta['intent']} ({meta['confidence']:.0%} confidence)")
        print(f"Spreading: {meta['iterations']} iterations, converged: {meta['converged']}")
        print(f"Seeds: {meta['seed_count']} notes")

    for result in results:
        print(format_result(result, show_full=args.full, mode=args.mode))

    print(f"\n{'='*60}")

    if args.mode == "spreading":
        print("Mode: SPREADING ACTIVATION (SYNAPSE-inspired)")
        print("Legend: activation = combined spreading score")
    else:
        print("Mode: STATIC (vector similarity)")
        print("Legend: similarity = cosine similarity to query")


if __name__ == '__main__':
    main()
