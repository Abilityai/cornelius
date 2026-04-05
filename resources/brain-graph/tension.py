"""
Brain Dependency Graph - Tension Detection

Detects productive contradictions: notes with high semantic similarity
but opposing conclusions. Tension edges are immune to staleness propagation
and represent the most valuable synthesis opportunities.
"""
from __future__ import annotations

import pickle
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

from config import LBS_FAISS_PATH, LBS_METADATA_PATH, BRAIN_PATH
from models import TensionRecord


# Opposing stance indicators
_NEGATION_PATTERNS = [
    r"\bnot\b", r"\bnever\b", r"\bno\b", r"\bcannot\b", r"\bimpossible\b",
    r"\bcontradicts?\b", r"\boppos(?:es?|ite|ing)\b", r"\bfalse\b",
    r"\brather than\b", r"\binstead\b", r"\bhowever\b", r"\bbut\b",
    r"\bdespite\b", r"\balthough\b",
]

_POSITIVE_STANCE = [
    r"\bis\b", r"\bare\b", r"\benables?\b", r"\bcreates?\b", r"\bdrives?\b",
    r"\brequires?\b", r"\bmust\b", r"\bshould\b", r"\balways\b",
]


def _extract_conclusion_sentences(content: str) -> list[str]:
    """Extract sentences that look like conclusions (last sentences of paragraphs)."""
    paragraphs = content.split("\n\n")
    conclusions = []
    for para in paragraphs:
        para = para.strip()
        if not para or para.startswith("#") or para.startswith("---"):
            continue
        sentences = re.split(r'(?<=[.!?])\s+', para)
        if sentences:
            # Take the last sentence of each paragraph
            conclusions.append(sentences[-1].strip())
    return conclusions[:5]  # Max 5 conclusion sentences


def _compute_stance_divergence(content_a: str, content_b: str) -> float:
    """
    Estimate how much two texts diverge in stance.
    Returns 0.0 (aligned) to 1.0 (strongly opposing).
    Simple heuristic: count negation/opposition patterns relative to positive patterns.
    """
    conclusions_a = _extract_conclusion_sentences(content_a)
    conclusions_b = _extract_conclusion_sentences(content_b)

    if not conclusions_a or not conclusions_b:
        return 0.0

    text_a = " ".join(conclusions_a).lower()
    text_b = " ".join(conclusions_b).lower()

    # Count opposing patterns in each
    neg_a = sum(1 for p in _NEGATION_PATTERNS if re.search(p, text_a))
    neg_b = sum(1 for p in _NEGATION_PATTERNS if re.search(p, text_b))
    pos_a = sum(1 for p in _POSITIVE_STANCE if re.search(p, text_a))
    pos_b = sum(1 for p in _POSITIVE_STANCE if re.search(p, text_b))

    # Stance polarity: positive = assertive, negative = contradicting
    polarity_a = (pos_a - neg_a) / max(pos_a + neg_a, 1)
    polarity_b = (pos_b - neg_b) / max(pos_b + neg_b, 1)

    # Divergence: difference in polarity
    divergence = abs(polarity_a - polarity_b) / 2.0  # Normalize to 0-1
    return min(divergence, 1.0)


def _load_faiss_and_metadata():
    """Load FAISS index and metadata for similarity search."""
    try:
        import faiss
    except ImportError:
        print("Error: faiss not available. Install with: pip install faiss-cpu", file=sys.stderr)
        sys.exit(1)

    if not LBS_FAISS_PATH.exists() or not LBS_METADATA_PATH.exists():
        print("Error: FAISS index not found. Run local-brain-search indexing first.", file=sys.stderr)
        sys.exit(1)

    index = faiss.read_index(str(LBS_FAISS_PATH))
    with open(LBS_METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def _get_note_content(note_id: str, metadata: list[dict]) -> str:
    """Get concatenated content for a note from metadata chunks."""
    chunks = [m["content"] for m in metadata if m.get("note_id") == note_id]
    return "\n\n".join(chunks)


def _get_note_embedding(note_id: str, metadata: list[dict], index) -> np.ndarray | None:
    """Get the first chunk's embedding for a note."""
    for i, m in enumerate(metadata):
        if m.get("note_id") == note_id:
            return index.reconstruct(i)
    return None


def detect_tensions(
    enrichments: dict,
    similarity_threshold: float = 0.75,
    divergence_threshold: float = 0.3,
    max_per_note: int = 3,
    target_layers: set[str] | None = None,
) -> list[TensionRecord]:
    """
    Detect potential productive tensions across the knowledge base.

    Looks for note pairs with:
    1. High semantic similarity (>similarity_threshold)
    2. Opposing conclusions (stance divergence > divergence_threshold)

    Only considers insight and framework notes by default.
    """
    if target_layers is None:
        target_layers = {"insight", "framework"}

    nodes = enrichments.get("nodes", {})
    existing_tensions = {
        (t["note_a"], t["note_b"]) for t in enrichments.get("tensions", [])
    }
    # Also check reverse
    existing_tensions.update(
        (t["note_b"], t["note_a"]) for t in enrichments.get("tensions", [])
    )

    # Filter to target layers
    candidates = [
        nid for nid, ndata in nodes.items()
        if ndata.get("layer") in target_layers
    ]

    if not candidates:
        print("No candidate notes found for tension detection.")
        return []

    print(f"Scanning {len(candidates)} notes for tensions...")

    index, metadata = _load_faiss_and_metadata()

    # Build note_id -> first chunk index mapping
    note_chunk_idx = {}
    for i, m in enumerate(metadata):
        nid = m.get("note_id")
        if nid and nid not in note_chunk_idx and nid in nodes:
            note_chunk_idx[nid] = i

    new_tensions = []
    checked = set()

    for note_id in candidates:
        if note_id not in note_chunk_idx:
            continue

        chunk_idx = note_chunk_idx[note_id]
        embedding = index.reconstruct(int(chunk_idx)).reshape(1, -1)

        # Search for similar notes
        k = min(20, index.ntotal)
        distances, indices = index.search(embedding, k)

        found_for_note = 0
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(metadata):
                continue

            similarity = float(dist)  # IndexFlatIP: inner product = cosine for normalized vectors
            if similarity < similarity_threshold:
                continue

            other_id = metadata[idx]["note_id"]

            # Skip self, non-candidates, already checked pairs
            if other_id == note_id:
                continue
            if other_id not in nodes or nodes[other_id].get("layer") not in target_layers:
                continue

            pair_key = tuple(sorted([note_id, other_id]))
            if pair_key in checked or pair_key in existing_tensions:
                continue
            checked.add(pair_key)

            # Check stance divergence
            content_a = _get_note_content(note_id, metadata)
            content_b = _get_note_content(other_id, metadata)
            divergence = _compute_stance_divergence(content_a, content_b)

            if divergence >= divergence_threshold:
                tension = TensionRecord(
                    note_a=note_id,
                    note_b=other_id,
                    similarity=round(similarity, 3),
                    description=f"Similarity {similarity:.2f}, stance divergence {divergence:.2f}",
                    synthesis_artifacts=[],
                    detected=datetime.now().strftime("%Y-%m-%d"),
                )
                new_tensions.append(tension)
                found_for_note += 1
                if found_for_note >= max_per_note:
                    break

    print(f"  New tensions found: {len(new_tensions)}")
    return new_tensions
