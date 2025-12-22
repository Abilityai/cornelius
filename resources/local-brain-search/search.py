#!/usr/bin/env python3
"""
Semantic search across Brain notes using FAISS.

Usage:
    python search.py "your query"
    python search.py "your query" --limit 20
    python search.py "your query" --threshold 0.7
    python search.py "your query" --full  # Show full content
"""
import argparse
import pickle
import sys

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    DEFAULT_SEARCH_LIMIT,
    DEFAULT_SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    METADATA_PATH,
)


def format_result(result: dict, show_full: bool = False) -> str:
    """Format a search result for display."""
    lines = []

    # Header
    similarity = result['similarity']
    title = result['title']
    heading = result['heading']
    filepath = result['filepath']

    lines.append(f"\n{'='*60}")
    lines.append(f"[{similarity:.1%}] {title}")
    if heading != title:
        lines.append(f"  Section: {heading}")
    lines.append(f"  Path: {filepath}")

    # Content preview
    content = result['content']
    if show_full:
        lines.append(f"\n{content}")
    else:
        # Show first 300 chars
        preview = content[:300]
        if len(content) > 300:
            preview += "..."
        lines.append(f"\n{preview}")

    return '\n'.join(lines)


def search(
    query: str,
    limit: int = DEFAULT_SEARCH_LIMIT,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    show_full: bool = False,
) -> list[dict]:
    """Search for notes matching the query."""
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
    seen_notes = set()  # For optional deduplication

    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(metadata):
            continue

        meta = metadata[idx]

        # For IndexFlatIP with normalized vectors, distance IS cosine similarity
        similarity = float(dist)

        if similarity < threshold:
            continue

        # Optional: deduplicate by note (show only best chunk per note)
        # note_id = meta['note_id']
        # if note_id in seen_notes:
        #     continue
        # seen_notes.add(note_id)

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

    return formatted_results


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
    args = parser.parse_args()

    results = search(
        query=args.query,
        limit=args.limit,
        threshold=args.threshold,
        show_full=args.full,
    )

    if args.json:
        import json
        print(json.dumps(results, indent=2))
        return

    if not results:
        print(f"No results found for: {args.query}")
        print(f"(threshold: {args.threshold})")
        return

    print(f"\nFound {len(results)} results for: {args.query}")
    print(f"(threshold: {args.threshold})")

    for result in results:
        print(format_result(result, show_full=args.full))

    print(f"\n{'='*60}")


if __name__ == '__main__':
    main()
