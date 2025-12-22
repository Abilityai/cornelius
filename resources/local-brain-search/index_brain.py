#!/usr/bin/env python3
"""
Index the Brain folder for local vector search using FAISS.

Usage:
    python index_brain.py [--force]

Options:
    --force    Re-index everything, ignoring existing index
"""
import argparse
import hashlib
import pickle
import re
import sys
import time
from pathlib import Path

import faiss
import networkx as nx
import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    BRAIN_PATH,
    DATA_DIR,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    EXCLUDED_FOLDERS,
    FAISS_INDEX_PATH,
    GRAPH_PICKLE_PATH,
    INCLUDE_PATTERNS,
    METADATA_PATH,
    MIN_CHUNK_LENGTH,
    SEMANTIC_EDGE_THRESHOLD,
    SEMANTIC_EDGE_TOP_K,
)


def extract_wikilinks(content: str) -> list[str]:
    """Extract wiki-links from markdown content."""
    # Match [[link]] or [[link|alias]]
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    matches = re.findall(pattern, content)
    return list(set(matches))


def extract_title_from_content(content: str, filepath: Path) -> str:
    """Extract title from first H1 or filename."""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return filepath.stem


def chunk_by_headings(content: str, filepath: Path) -> list[dict]:
    """Split content by headings into chunks."""
    chunks = []
    lines = content.split('\n')

    current_chunk = []
    current_heading = extract_title_from_content(content, filepath)

    for line in lines:
        # Check if this is a heading
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            # Save previous chunk if it has content
            chunk_text = '\n'.join(current_chunk).strip()
            if len(chunk_text) >= MIN_CHUNK_LENGTH:
                chunks.append({
                    'heading': current_heading,
                    'content': chunk_text,
                })
            # Start new chunk
            current_heading = heading_match.group(2).strip()
            current_chunk = [line]
        else:
            current_chunk.append(line)

    # Don't forget the last chunk
    chunk_text = '\n'.join(current_chunk).strip()
    if len(chunk_text) >= MIN_CHUNK_LENGTH:
        chunks.append({
            'heading': current_heading,
            'content': chunk_text,
        })

    # If no chunks created, use whole content
    if not chunks:
        chunks.append({
            'heading': extract_title_from_content(content, filepath),
            'content': content.strip(),
        })

    return chunks


def get_note_id(filepath: Path) -> str:
    """Generate consistent ID for a note."""
    relative = filepath.relative_to(BRAIN_PATH)
    return str(relative)


def content_hash(content: str) -> str:
    """Generate hash of content for change detection."""
    return hashlib.md5(content.encode()).hexdigest()


def collect_notes() -> list[dict]:
    """Collect all markdown notes from Brain folder."""
    notes = []

    for pattern in INCLUDE_PATTERNS:
        for filepath in BRAIN_PATH.rglob(pattern):
            # Skip excluded folders
            relative = filepath.relative_to(BRAIN_PATH)
            if any(part in EXCLUDED_FOLDERS for part in relative.parts):
                continue

            try:
                content = filepath.read_text(encoding='utf-8')
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}")
                continue

            wikilinks = extract_wikilinks(content)
            title = extract_title_from_content(content, filepath)

            notes.append({
                'filepath': filepath,
                'note_id': get_note_id(filepath),
                'title': title,
                'content': content,
                'wikilinks': wikilinks,
                'content_hash': content_hash(content),
            })

    return notes


def build_explicit_graph(notes: list[dict]) -> nx.DiGraph:
    """Build graph from explicit wiki-links."""
    G = nx.DiGraph()

    # Create mapping from title/filename to note_id
    title_to_id = {}
    stem_to_id = {}
    for note in notes:
        title_to_id[note['title'].lower()] = note['note_id']
        stem = Path(note['note_id']).stem.lower()
        stem_to_id[stem] = note['note_id']

    # Add nodes
    for note in notes:
        G.add_node(
            note['note_id'],
            title=note['title'],
            filepath=str(note['filepath']),
        )

    # Add edges from wiki-links
    for note in notes:
        for link in note['wikilinks']:
            link_lower = link.lower()
            target_id = title_to_id.get(link_lower) or stem_to_id.get(link_lower)
            if target_id and target_id != note['note_id']:
                G.add_edge(note['note_id'], target_id, type='explicit')

    return G


def add_semantic_edges(
    G: nx.DiGraph,
    index: faiss.Index,
    metadata: list[dict],
    notes: list[dict],
    embeddings: np.ndarray,
) -> None:
    """Add weak edges based on semantic similarity."""
    print("Adding semantic edges...")

    # Create note_id to embedding index mapping
    note_embeddings = {}
    for i, meta in enumerate(metadata):
        note_id = meta['note_id']
        if note_id not in note_embeddings:
            note_embeddings[note_id] = i  # Use first chunk as representative

    for note in notes:
        note_id = note['note_id']
        if note_id not in note_embeddings:
            continue

        idx = note_embeddings[note_id]
        query_embedding = embeddings[idx:idx+1]

        # Search for similar notes
        k = SEMANTIC_EDGE_TOP_K + 10  # Get extra to filter
        distances, indices = index.search(query_embedding, k)

        for dist, result_idx in zip(distances[0], indices[0]):
            if result_idx < 0 or result_idx >= len(metadata):
                continue

            # Convert L2 distance to cosine similarity (for normalized vectors)
            # L2^2 = 2 - 2*cos_sim, so cos_sim = 1 - L2^2/2
            similarity = 1 - dist / 2

            target_note_id = metadata[result_idx]['note_id']

            # Skip self-links and below threshold
            if target_note_id == note_id:
                continue
            if similarity < SEMANTIC_EDGE_THRESHOLD:
                continue

            # Check if we already have enough semantic edges for this note
            semantic_edges_count = sum(
                1 for _, t, d in G.out_edges(note_id, data=True)
                if d.get('type') == 'semantic'
            )
            if semantic_edges_count >= SEMANTIC_EDGE_TOP_K:
                break

            # Add or update edge
            if G.has_edge(note_id, target_note_id):
                # Already has explicit edge, add semantic weight
                G.edges[note_id, target_note_id]['semantic_similarity'] = similarity
            else:
                G.add_edge(
                    note_id,
                    target_note_id,
                    type='semantic',
                    weight=similarity,
                )


def main():
    parser = argparse.ArgumentParser(description='Index Brain folder for local vector search')
    parser.add_argument('--force', action='store_true', help='Force re-index everything')
    args = parser.parse_args()

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    start_time = time.time()
    model = SentenceTransformer(EMBEDDING_MODEL)
    print(f"  Model loaded in {time.time() - start_time:.1f}s")

    print(f"\nCollecting notes from {BRAIN_PATH}...")
    notes = collect_notes()
    print(f"  Found {len(notes)} notes")

    # Check for existing index
    if FAISS_INDEX_PATH.exists() and METADATA_PATH.exists() and not args.force:
        print("\nLoading existing index...")
        index = faiss.read_index(str(FAISS_INDEX_PATH))
        with open(METADATA_PATH, 'rb') as f:
            existing_metadata = pickle.load(f)
        print(f"  Existing index has {index.ntotal} vectors")

        # Check for changes
        existing_hashes = {m['note_id']: m.get('content_hash') for m in existing_metadata}
        notes_to_index = []
        for note in notes:
            if note['note_id'] not in existing_hashes or existing_hashes[note['note_id']] != note['content_hash']:
                notes_to_index.append(note)

        if not notes_to_index:
            print("  No changes detected, skipping re-indexing")
            # Still need to rebuild graph potentially
        else:
            print(f"  {len(notes_to_index)} notes have changed, will re-index all (FAISS doesn't support incremental)")
            args.force = True  # Force full re-index since FAISS doesn't support incremental well

    print("\nChunking notes...")
    all_chunks = []
    all_metadata = []

    for note in notes:
        chunks = chunk_by_headings(note['content'], note['filepath'])
        for j, chunk in enumerate(chunks):
            all_chunks.append(chunk['content'])
            all_metadata.append({
                'note_id': note['note_id'],
                'title': note['title'],
                'heading': chunk['heading'],
                'filepath': str(note['filepath']),
                'content_hash': note['content_hash'],
                'chunk_index': j,
                'content': chunk['content'],
            })

    print(f"  Created {len(all_chunks)} chunks from {len(notes)} notes")

    print("\nGenerating embeddings...")
    start_time = time.time()
    embeddings = model.encode(all_chunks, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype('float32')
    print(f"  Generated {len(embeddings)} embeddings in {time.time() - start_time:.1f}s")

    print("\nBuilding FAISS index...")
    # Use IndexFlatIP for cosine similarity (since embeddings are normalized)
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(embeddings)
    print(f"  Index has {index.ntotal} vectors")

    print(f"\nSaving index to {FAISS_INDEX_PATH}...")
    faiss.write_index(index, str(FAISS_INDEX_PATH))

    print(f"Saving metadata to {METADATA_PATH}...")
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(all_metadata, f)

    print("\nBuilding connection graph...")
    G = build_explicit_graph(notes)
    print(f"  Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} explicit edges")

    # Add semantic edges
    add_semantic_edges(G, index, all_metadata, notes, embeddings)
    semantic_edges = sum(1 for _, _, d in G.edges(data=True) if d.get('type') == 'semantic')
    print(f"  Added {semantic_edges} semantic edges")

    print(f"\nSaving graph to {GRAPH_PICKLE_PATH}...")
    with open(GRAPH_PICKLE_PATH, 'wb') as f:
        pickle.dump(G, f)

    # Print summary
    print("\n" + "=" * 50)
    print("INDEXING COMPLETE")
    print("=" * 50)
    print(f"Notes indexed: {len(notes)}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Graph nodes: {G.number_of_nodes()}")
    print(f"Graph edges: {G.number_of_edges()}")
    print(f"  - Explicit (wiki-links): {G.number_of_edges() - semantic_edges}")
    print(f"  - Semantic (similarity): {semantic_edges}")
    print(f"\nData stored in: {DATA_DIR}")


if __name__ == '__main__':
    main()
