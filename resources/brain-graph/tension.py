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


# Structural artifact filters (mirror the 2026-07-11 curation pass): pairs that
# match these are detector artifacts, not contradictions, and are never emitted.
_INDEX_PAT = re.compile(
    r"(CHANGELOG|Changelogs/|REGISTRY|ARTICLE-INDEX|_book\.md$|_metadata\.md$|"
    r"05-Meta/Thinking/|05-Meta/Reports/|05-Meta/AI Crystallizations/|"
    r"MOC - |00-Inbox/|Watch Log|watch-log|DASHBOARD|README)",
    re.IGNORECASE,
)
# Above this, "high divergence" is boilerplate variation on one text, not opposition.
_NEAR_DUP_SIMILARITY = 0.93

# A note's REPRESENTATIVE chunk must carry meaning. 83% of notes have a bare YAML
# frontmatter block as their first chunk (CLAUDE.md mandates an identical metadata
# block on every note), and some stubs have an empty body. Querying with such a
# vector finds mostly other boilerplate (>= 0.93, dropped as near-dup) and little in
# [0.75, 0.93) - measured 2026-09-02 on 293 such notes: 121 usable hits, 3 in 4 notes
# with none, vs 765 hits with the representative mapping. Before the fix this
# detector was mostly blind for those notes, and what it did see was matched on
# metadata-like text, not claims. Mirrors index_brain.is_meaningless_chunk() in local-brain-search
# (kept local to avoid a cross-package import; keep the two in step).
_FRONTMATTER_ONLY = re.compile(r"^---\s*\n.*?\n---\s*$", re.DOTALL)
_MIN_MEANINGFUL_CHARS = 50  # = local-brain-search memory_config indexing.min_chunk_length


def _is_boilerplate_chunk(content: str) -> bool:
    stripped = (content or "").strip()
    if len(stripped) < _MIN_MEANINGFUL_CHARS:
        return True
    return bool(_FRONTMATTER_ONLY.match(stripped))


def _representative_chunks(metadata: list[dict], wanted: set[str] | None = None) -> dict[str, int]:
    """note_id -> index of its first MEANINGFUL chunk. Notes with no meaningful chunk
    are omitted (they cannot be in a tension; they have no claim)."""
    rep: dict[str, int] = {}
    for i, m in enumerate(metadata):
        nid = m.get("note_id")
        if not nid or nid in rep or (wanted is not None and nid not in wanted):
            continue
        if _is_boilerplate_chunk(m.get("content", "")):
            continue
        rep[nid] = i
    return rep


def _pair_key(note_a: str, note_b: str) -> tuple[str, str]:
    """Path-independent pair identity: sorted basenames, so a note moving folders
    (e.g. graduating from Books/ to 02-Permanent/) keeps its dismissal."""
    base_a = note_a.rsplit("/", 1)[-1]
    base_b = note_b.rsplit("/", 1)[-1]
    return tuple(sorted([base_a, base_b]))


def _same_source_scope(note_a: str, note_b: str) -> bool:
    """Both notes from one DI session or one book scope: a source arguing with
    itself is the author's rhetoric, not a KB tension."""
    parts_a, parts_b = note_a.split("/"), note_b.split("/")
    if len(parts_a) < 2 or len(parts_b) < 2 or parts_a[0] != parts_b[0]:
        return False
    return parts_a[0] in ("Document Insights", "Books") and parts_a[1] == parts_b[1]


# Brand/vision notes are aspirational statements, not opposable propositions.
# They live in 02-Permanent alongside analytical insights but carry a distinct
# register the negation-keyword stance heuristic systematically misreads (a Vow
# reads as assertive; the note next to it reads as contradicting). They are
# identified by frontmatter tag, not by name (name lists rot).
_BRAND_TAGS = {"vows", "luminous-mind", "luminous", "seals", "canon",
               "voice", "brand", "thresholds"}
_TAGS_LINE = re.compile(r"^tags:\s*(.+)$", re.MULTILINE)


def _brand_excluded_notes() -> set[str]:
    """One-time scan: note_ids whose frontmatter tags mark them brand/vision."""
    excluded: set[str] = set()
    perm_dir = BRAIN_PATH / "02-Permanent"
    if not perm_dir.is_dir():
        return excluded
    for path in perm_dir.glob("*.md"):
        try:
            head = path.read_text(encoding="utf-8")[:800]
        except OSError:
            continue
        m = _TAGS_LINE.search(head)
        if not m:
            continue
        tags = {t.strip().strip("[]'\"").lower() for t in re.split(r"[,\[\]]", m.group(1))}
        if _BRAND_TAGS & tags:
            excluded.add(f"02-Permanent/{path.name}")
    return excluded


def _both_document_insights(note_a: str, note_b: str) -> bool:
    """Both notes are external research extractions. A tension here is 'the
    literature disagrees' - encountered-vs-encountered, not a synthesis gem for
    the owner's own thinking. The KB's valuable tensions always involve a core
    insight (a core note contradicting a DI/book finding stays in scope). This
    also removes the unbounded re-flood vector: DI is the largest, fastest-
    growing folder, and its cross-session near-duplicates dominate the raw
    detector output."""
    return note_a.startswith("Document Insights/") and note_b.startswith("Document Insights/")


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
    """Get the embedding of a note's first MEANINGFUL chunk (never bare frontmatter)."""
    rep = _representative_chunks(metadata, {note_id})
    if note_id not in rep:
        return None
    return index.reconstruct(int(rep[note_id]))


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
        _pair_key(t["note_a"], t["note_b"]) for t in enrichments.get("tensions", [])
    }
    # Pairs a curation pass judged non-tensions stay dismissed across re-scans -
    # without this, every scan re-floods the store with pruned artifacts.
    dismissed = {tuple(p) for p in enrichments.get("dismissed_tensions", [])}

    # Filter to target layers
    candidates = [
        nid for nid, ndata in nodes.items()
        if ndata.get("layer") in target_layers
    ]

    if not candidates:
        print("No candidate notes found for tension detection.")
        return []

    brand_excluded = _brand_excluded_notes()
    if brand_excluded:
        candidates = [c for c in candidates if c not in brand_excluded]

    print(f"Scanning {len(candidates)} notes for tensions...")

    index, metadata = _load_faiss_and_metadata()

    # Build note_id -> REPRESENTATIVE chunk index (first meaningful chunk, never the
    # frontmatter block). Fixed 2026-09-02: the index rebuild that removed the
    # frontmatter collision from the graph did NOT reach this detector, which picks
    # its own chunk straight from the FAISS metadata.
    note_chunk_idx = _representative_chunks(metadata, set(nodes))

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
            # A boilerplate chunk is not a claim - it can never be the other end of a tension.
            if _is_boilerplate_chunk(metadata[idx].get("content", "")):
                continue
            if other_id not in nodes or nodes[other_id].get("layer") not in target_layers:
                continue

            pair_key = _pair_key(note_id, other_id)
            if pair_key in checked or pair_key in existing_tensions or pair_key in dismissed:
                continue
            checked.add(pair_key)

            # Structural artifact filters
            if _INDEX_PAT.search(note_id) or _INDEX_PAT.search(other_id):
                continue
            if similarity >= _NEAR_DUP_SIMILARITY:
                continue
            if _same_source_scope(note_id, other_id):
                continue
            if _both_document_insights(note_id, other_id):
                continue
            if other_id in brand_excluded:
                continue

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
