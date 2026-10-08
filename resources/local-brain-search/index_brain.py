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
import json
import pickle
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import faiss
import networkx as nx
import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    BRAIN_PATH,
    BUILDER_VERSION,
    CORE_FOLDERS,
    DATA_DIR,
    EDGE_FORMULA,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    EXCLUDED_FOLDERS,
    FAISS_INDEX_PATH,
    GRAPH_PICKLE_PATH,
    INCLUDE_PATTERNS,
    MANIFEST_PATH,
    METADATA_PATH,
    MIN_CHUNK_LENGTH,
    SEMANTIC_EDGE_THRESHOLD,
    SEMANTIC_EDGE_TOP_K,
)


_FRONTMATTER_ONLY = re.compile(r'^---\s*\n.*?\n---\s*$', re.DOTALL)


def is_frontmatter_only(content: str) -> bool:
    """True when a chunk is a bare YAML frontmatter block and nothing else.

    Such chunks carry no meaning but DO carry byte-identical text across every
    note written by the same model on the same day, which makes them cosine-1.000
    twins of each other. See SIMILARITY-CALIBRATION.md -> Trap 3.
    """
    return bool(_FRONTMATTER_ONLY.match(content.strip()))


def is_meaningless_chunk(content: str) -> bool:
    """True when a chunk carries no meaning for edge building: a bare frontmatter
    block, OR an empty / sub-minimum body.

    The second class was found by the 2026-09-02 validation pass: 31 zero-byte stub
    notes (29 of them in 02-Permanent - Sleep, Autonomy, Polarization, ...) each had
    the empty string as their only chunk. Every empty string embeds to the same
    vector, so they formed a cosine-1.000 clique inside the core fingerprint and each
    stub spent its full SEMANTIC_EDGE_TOP_K quota on the other stubs. A further 25
    notes had only a bare title line ('# Vasopressin'). Neither is a meaning.
    """
    stripped = content.strip()
    if len(stripped) < MIN_CHUNK_LENGTH:
        return True
    return bool(_FRONTMATTER_ONLY.match(stripped))


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

    # Frontmatter-only chunks must never represent a note or terminate an edge.
    # CLAUDE.md mandates an identical metadata block on every note, so two notes
    # created the same day by the same model have BYTE-IDENTICAL frontmatter and
    # therefore identical embeddings. Using the first chunk as the representative
    # (the pre-2026-09-02 behaviour) made that a cosine-1.000 semantic edge between
    # unrelated notes: 9,208 of 26,065 edges (35%), with 28% of notes having a
    # semantic neighbourhood made ENTIRELY of same-date twins. Because 74% of notes
    # sit at the SEMANTIC_EDGE_TOP_K cap, those perfect scores are found first and
    # DISPLACE real neighbours - the failure is crowding-out, not added noise.
    # See SIMILARITY-CALIBRATION.md -> "Trap 3: the frontmatter collision".
    # Extended 2026-09-02 (validation pass): empty and sub-minimum chunks are excluded
    # for the same reason - see is_meaningless_chunk().
    boilerplate_rows = {
        i for i, meta in enumerate(metadata)
        if is_meaningless_chunk(meta.get('content', ''))
    }
    if boilerplate_rows:
        print(f"  excluding {len(boilerplate_rows)} frontmatter-only / empty chunks from edge building")

    # Create note_id to embedding index mapping. Prefer the first chunk with real
    # content; fall back to the first chunk only if a note has nothing else.
    note_embeddings = {}
    for i, meta in enumerate(metadata):
        note_id = meta['note_id']
        if i in boilerplate_rows:
            note_embeddings.setdefault(note_id, i)  # fallback only
            continue
        if note_id not in note_embeddings or note_embeddings[note_id] in boilerplate_rows:
            note_embeddings[note_id] = i

    total_notes = len(notes)
    for n_done, note in enumerate(notes, 1):
        if n_done % 500 == 0:  # heartbeat: keep the foreground call under the 300s watchdog
            print(f"  semantic edges: {n_done}/{total_notes} notes", flush=True)
        note_id = note['note_id']
        if note_id not in note_embeddings:
            continue

        idx = note_embeddings[note_id]
        if idx in boilerplate_rows:
            # The note has no meaningful chunk at all (empty stub / bare title):
            # nothing to search with, so it gets no semantic out-edges.
            continue
        query_embedding = embeddings[idx:idx+1]

        # Search for similar notes. The extra headroom absorbs both the
        # threshold filter and the frontmatter-only rows dropped below.
        k = SEMANTIC_EDGE_TOP_K * 4 + 10
        distances, indices = index.search(query_embedding, k)

        for dist, result_idx in zip(distances[0], indices[0]):
            if result_idx < 0 or result_idx >= len(metadata):
                continue

            # A frontmatter block is not a meaning - never let one END an edge either.
            if result_idx in boilerplate_rows:
                continue

            # The index is faiss.IndexFlatIP, so `dist` is the inner product,
            # which for normalized vectors IS the cosine similarity. Use it
            # directly. The old `1 - dist/2` assumed an L2 index and INVERTED
            # the edge ordering: it scored dissimilar pairs high (passing the
            # 0.65 threshold) and dropped truly-similar pairs. (EDGE_FORMULA /
            # BUILDER_VERSION in memory_config track this; bumped to cosine_ip/v2.)
            similarity = float(dist)

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


def load_previous(force):
    """Per-note metadata + reconstructed embedding vectors from the persisted
    index, so an incremental run can REUSE the embedding of any note whose
    content is unchanged (matched by content_hash). Returns (meta_by_note,
    vecs_by_note, hash_by_note); all empty on --force, a missing/mismatched
    index, or any read error (=> a full rebuild). Vectors come straight out of
    the IndexFlatIP via reconstruct_n — no separate embedding cache needed."""
    if force or not (FAISS_INDEX_PATH.exists() and METADATA_PATH.exists()):
        return {}, {}, {}
    try:
        idx = faiss.read_index(str(FAISS_INDEX_PATH))
        with open(METADATA_PATH, 'rb') as f:
            meta = pickle.load(f)
        if idx.ntotal != len(meta):        # index/metadata drifted apart — distrust both
            return {}, {}, {}
        vecs = idx.reconstruct_n(0, idx.ntotal)
    except Exception as e:
        print(f"  (could not reuse previous index: {e}; full rebuild)", flush=True)
        return {}, {}, {}
    meta_by_note, vecs_by_note, hash_by_note = {}, {}, {}
    for i, m in enumerate(meta):
        nid = m['note_id']
        meta_by_note.setdefault(nid, []).append(m)
        vecs_by_note.setdefault(nid, []).append(vecs[i])
        hash_by_note.setdefault(nid, m.get('content_hash'))
    vecs_by_note = {k: np.vstack(v).astype('float32') for k, v in vecs_by_note.items()}
    return meta_by_note, vecs_by_note, hash_by_note


def main():
    parser = argparse.ArgumentParser(description='Index Brain folder for local vector search')
    parser.add_argument('--force', action='store_true',
                        help='Ignore the existing index and re-embed every note in one '
                             'unbounded pass (for attended manual rebuilds).')
    parser.add_argument('--max-embed-notes', type=int, default=500,
                        help='Cap how many notes are (re)embedded per run so a big rebuild '
                             'splits into short, Trinity-safe calls (0 = unbounded). Notes past '
                             'the cap are deferred; the next run reuses whatever is already '
                             'indexed, so repeated runs converge. Prints "remaining=N" — the '
                             'caller re-runs while N>0.')
    args = parser.parse_args()

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading embedding model: {EMBEDDING_MODEL}...", flush=True)
    start_time = time.time()
    model = SentenceTransformer(EMBEDDING_MODEL)
    print(f"  Model loaded in {time.time() - start_time:.1f}s", flush=True)

    print(f"\nCollecting notes from {BRAIN_PATH}...", flush=True)
    notes = collect_notes()
    print(f"  Found {len(notes)} notes", flush=True)

    # ---- incremental reuse -------------------------------------------------
    # Reuse the embedding of every note whose content is unchanged since the last
    # build; only NEW or CHANGED notes are re-embedded, turning a ~15-20 min full
    # embed into seconds on a normal day. --max-embed-notes additionally bounds a
    # cold/forced rebuild into several SHORT runs (the "many short calls" the
    # Trinity stall watchdog requires): notes past the cap are deferred, reusing
    # their old vector if they have one, and the persisted partial index lets the
    # next run pick up where this one stopped. See .claude/skills/refresh-index.
    old_meta, old_vecs, old_hash = load_previous(args.force)
    cap = None if (args.force or args.max_embed_notes <= 0) else args.max_embed_notes

    all_metadata, all_vectors = [], []   # aligned; each vector is a 1-D float32 array
    embed_texts, embed_slots = [], []    # chunk texts to embed now + their slots in all_vectors
    reused = embedded = deferred = 0

    for note in notes:
        nid = note['note_id']
        if nid in old_vecs and old_hash.get(nid) == note['content_hash']:
            for m, v in zip(old_meta[nid], old_vecs[nid]):     # unchanged — reuse verbatim
                all_metadata.append(m)
                all_vectors.append(v)
            reused += 1
            continue
        if cap is not None and embedded >= cap:                # over this run's budget — defer
            if nid in old_vecs:                                # keep old vector so the index stays complete
                for m, v in zip(old_meta[nid], old_vecs[nid]):
                    all_metadata.append(m)
                    all_vectors.append(v)
            deferred += 1
            continue
        for j, chunk in enumerate(chunk_by_headings(note['content'], note['filepath'])):
            all_metadata.append({
                'note_id': nid,
                'title': note['title'],
                'heading': chunk['heading'],
                'filepath': str(note['filepath']),
                'content_hash': note['content_hash'],
                'chunk_index': j,
                'content': chunk['content'],
            })
            all_vectors.append(None)                           # placeholder, filled after embed
            embed_texts.append(chunk['content'])
            embed_slots.append(len(all_vectors) - 1)
        embedded += 1

    print(f"  reuse={reused} notes | embed={embedded} notes "
          f"({len(embed_texts)} chunks) | defer={deferred} notes", flush=True)

    # ---- embed only the delta (batched, flushed heartbeat) -----------------
    # Batched so a foreground call never goes silent >300s (the stall watchdog).
    # show_progress_bar stays OFF (its in-place tqdm bar emits nothing parseable
    # until EOF when piped). Batched encoding is numerically identical to one call
    # (normalize is per-vector).
    if embed_texts:
        t0 = time.time()
        HEARTBEAT_BATCH = 512
        for i in range(0, len(embed_texts), HEARTBEAT_BATCH):
            part = np.asarray(
                model.encode(embed_texts[i:i + HEARTBEAT_BATCH],
                             show_progress_bar=False, normalize_embeddings=True),
                dtype='float32')
            for k in range(len(part)):
                all_vectors[embed_slots[i + k]] = part[k]
            done = min(i + HEARTBEAT_BATCH, len(embed_texts))
            print(f"  embedded {done}/{len(embed_texts)} new chunks "
                  f"in {time.time() - t0:.0f}s", flush=True)

    embeddings = (np.vstack(all_vectors).astype('float32') if all_vectors
                  else np.zeros((0, EMBEDDING_DIM), dtype='float32'))

    print("\nBuilding FAISS index...", flush=True)
    index = faiss.IndexFlatIP(EMBEDDING_DIM)   # inner product == cosine (vectors are normalized)
    index.add(embeddings)
    print(f"  Index has {index.ntotal} vectors "
          f"({len(notes) - deferred} notes indexed, {deferred} deferred)", flush=True)

    print(f"Saving index to {FAISS_INDEX_PATH}...", flush=True)
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    print(f"Saving metadata to {METADATA_PATH}...", flush=True)
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(all_metadata, f)

    # Resumable stop: the graph + manifest tail runs ONLY on the final pass, so
    # every intermediate call stays short. deferred>0 means more notes await
    # embedding — the caller re-runs, which reuses this just-persisted partial
    # index and continues where we left off.
    if deferred:
        print(f"\nPARTIAL run: {deferred} notes not yet embedded; re-run to continue.", flush=True)
        print(f"RESULT reused={reused} embedded={embedded} remaining={deferred}", flush=True)
        return

    print("\nBuilding connection graph...", flush=True)
    G = build_explicit_graph(notes)
    print(f"  Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} explicit edges", flush=True)

    # Add semantic edges
    add_semantic_edges(G, index, all_metadata, notes, embeddings)
    semantic_edges = sum(1 for _, _, d in G.edges(data=True) if d.get('type') == 'semantic')
    print(f"  Added {semantic_edges} semantic edges", flush=True)

    print(f"\nSaving graph to {GRAPH_PICKLE_PATH}...", flush=True)
    with open(GRAPH_PICKLE_PATH, 'wb') as f:
        pickle.dump(G, f)

    # Print summary
    print("\n" + "=" * 50)
    print("INDEXING COMPLETE")
    print("=" * 50)
    print(f"Notes indexed: {len(notes)}")
    print(f"Total chunks: {len(all_metadata)}")
    print(f"Graph nodes: {G.number_of_nodes()}")
    print(f"Graph edges: {G.number_of_edges()}")
    print(f"  - Explicit (wiki-links): {G.number_of_edges() - semantic_edges}")
    print(f"  - Semantic (similarity): {semantic_edges}")
    print(f"This run: reused {reused} notes, embedded {embedded} notes")
    print(f"\nData stored in: {DATA_DIR}")

    # Build provenance stamp. Read by the daemon build-id guard (Phase 4) and by
    # health checks to verify the persisted graph was built with the corrected
    # cosine edge formula (cosine_ip / v2) rather than the inverted v1.
    manifest = {
        "edge_formula": EDGE_FORMULA,
        "builder_version": BUILDER_VERSION,
        "model": EMBEDDING_MODEL,
        "embedding_dim": EMBEDDING_DIM,
        "semantic_edge_threshold": SEMANTIC_EDGE_THRESHOLD,
        "semantic_edge_top_k": SEMANTIC_EDGE_TOP_K,
        "notes": len(notes),
        "chunks": len(all_metadata),
        "graph_nodes": G.number_of_nodes(),
        "graph_edges": G.number_of_edges(),
        "explicit_edges": G.number_of_edges() - semantic_edges,
        "semantic_edges": semantic_edges,
        "core_folders": sorted(CORE_FOLDERS),
        "built_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote build manifest to {MANIFEST_PATH} "
          f"(edge_formula={EDGE_FORMULA}, builder_version={BUILDER_VERSION})")
    print(f"RESULT reused={reused} embedded={embedded} remaining=0", flush=True)


if __name__ == '__main__':
    main()
