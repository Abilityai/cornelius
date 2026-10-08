#!/usr/bin/env python3
"""Measure the live similarity-score distributions this system's thresholds are set against.

Why this exists
---------------
Every skill in the vault carries hard-coded similarity thresholds ("0.75+ = strong
connection", "semantic edge at 0.65", "unhooked below 0.70"). Those numbers were
written at different times against DIFFERENT measurement spaces, and the score scale
is population-dependent, not global. A threshold that is routine in one space is
unreachable in another. This script measures the three spaces on the CURRENT index so
the numbers in SIMILARITY-CALIBRATION.md are reproducible rather than remembered.

Re-run it after any embedding-model change, index-builder change, or large ingestion
wave, and update SIMILARITY-CALIBRATION.md with the output.

Usage
-----
    venv/bin/python calibrate_similarity.py                    # all three spaces
    venv/bin/python calibrate_similarity.py --sample 100       # bigger query sample
    venv/bin/python calibrate_similarity.py --session "2026-09-02 Lex"
        # also measure one ingestion session against core (space 3)

Spaces measured
---------------
  1. chunk <-> chunk cosine     - what the GRAPH's semantic edges are built from
  2. title-query -> vault       - what /recall, /search-vault, /find-connections see
  3. title-query -> core        - what an ingestion of NEW external material sees
"""
import argparse
import pickle
import random
import re
import sys
from pathlib import Path

import faiss
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from memory_config import (  # noqa: E402
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    METADATA_PATH,
    GRAPH_PICKLE_PATH,
    resolve_read_scope,
)
from scope import build_scope_selector  # noqa: E402


def describe(label, values, marks=(0.45, 0.65, 0.75)):
    a = np.asarray(values, dtype=float)
    if a.size == 0:
        print(f"{label}: no data")
        return
    print(
        f"{label} n={a.size:>5} | min {a.min():.3f}  p25 {np.percentile(a, 25):.3f}  "
        f"median {np.median(a):.3f}  p75 {np.percentile(a, 75):.3f}  "
        f"p95 {np.percentile(a, 95):.3f}  max {a.max():.3f}"
    )
    frac = "  ".join(f">={m}: {100 * np.mean(a >= m):.0f}%" for m in marks)
    print(f"{' ' * len(label)}   {frac}")


def space_1_graph_edges():
    """chunk<->chunk cosine, as persisted on the graph's semantic edges."""
    print("\n=== SPACE 1: chunk<->chunk cosine (graph semantic edges) ===")
    with open(GRAPH_PICKLE_PATH, "rb") as f:
        graph = pickle.load(f)
    weights = [
        d.get("weight") or d.get("semantic_similarity")
        for _, _, d in graph.edges(data=True)
        if d.get("type") == "semantic"
    ]
    weights = [w for w in weights if w]
    describe("semantic edge weight ", weights, marks=(0.65, 0.75, 0.90))
    print(
        "  NOTE: built by add_semantic_edges() from each note's REPRESENTATIVE chunk (its first\n"
        "        meaningful chunk - never bare frontmatter or an empty stub, since 2026-09-02) vs all\n"
        "        chunks, floored at SEMANTIC_EDGE_THRESHOLD (memory_config: graph.semantic_edge_threshold).\n"
        "        This is the HIGH-scoring space - do not carry these numbers into query space."
    )


def _load():
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
    from sentence_transformers import SentenceTransformer

    return index, metadata, SentenceTransformer(EMBEDDING_MODEL)


def _first_chunk_by_note(metadata):
    first = {}
    for i, m in enumerate(metadata):
        first.setdefault(m["note_id"], i)
    return first


def _probe(index, metadata, embeddings, note_ids, scope_folders, exclude_substr=None):
    """Return (self_max, best_other) raw cosine per query, honouring a read scope."""
    params = backing = None
    if scope_folders is not None:
        selector, backing = build_scope_selector(metadata, scope_folders)
        if selector is None:
            return [], []
        params = faiss.SearchParameters()
        params.sel = selector
    distances, indices = index.search(embeddings, 200, params=params)
    self_max, best_other = [], []
    for row, note_id in enumerate(note_ids):
        own = other = None
        for dist, idx in zip(distances[row], indices[row]):
            if idx < 0:
                continue
            meta = metadata[idx]
            if exclude_substr and exclude_substr in meta["filepath"]:
                continue
            if meta["note_id"] == note_id:
                own = own if own is not None else float(dist)
            elif other is None:
                other = float(dist)
            if own is not None and other is not None:
                break
        if own is not None:
            self_max.append(own)
        if other is not None:
            best_other.append(other)
    return self_max, best_other


def space_2_query_vault(index, metadata, model, sample, seed):
    print("\n=== SPACE 2: title-query -> whole vault (what search/recall sees) ===")
    first = _first_chunk_by_note(metadata)
    random.seed(seed)
    note_ids = random.sample(list(first.keys()), min(sample, len(first)))
    titles = [metadata[first[n]]["title"] for n in note_ids]
    emb = model.encode(titles, normalize_embeddings=True).astype("float32")
    self_max, best_other = _probe(index, metadata, emb, note_ids, None)
    describe("title -> OWN note   ", self_max)
    describe("title -> BEST OTHER ", best_other)
    print(
        "  NOTE: high values here are dominated by near-duplicate operational artifacts\n"
        "        (session changelogs, folder READMEs) - a high score is NOT evidence of insight."
    )


def space_2b_query_scoped(index, metadata, model, sample, seed):
    """Space 2 at the two everyday READ mounts (scope-mount contract, 2026-09-04).

    `core` is what a voice read sees; `core,Books,document-insights` (the reasoning
    mount) is what /advise, /recall, /decide and the other reasoning/lookup reads see
    since the scope mount policy. Titles are sampled from notes INSIDE each mount and
    probed against that mount only, so each row is its own population - a threshold
    tuned on one must not be carried to the other.
    """
    from memory_config import in_read_scope  # noqa: E402
    first = _first_chunk_by_note(metadata)
    for label, token in (("core (voice reads)", "core"),
                         ("reasoning mount core,Books,document-insights", "core,books,document-insights")):
        rs = resolve_read_scope(token)
        pool = [n for n in first if in_read_scope(n, rs)]
        random.seed(seed)
        note_ids = random.sample(pool, min(sample, len(pool)))
        titles = [metadata[first[n]]["title"] for n in note_ids]
        emb = model.encode(titles, normalize_embeddings=True).astype("float32")
        self_max, best_other = _probe(index, metadata, emb, note_ids, rs)
        print(f"\n=== SPACE 2 @ {label}: population {len(pool)} notes ===")
        describe("title -> OWN note   ", self_max)
        describe("title -> BEST OTHER ", best_other)


def space_3_session_vs_core(index, metadata, model, session):
    print(f"\n=== SPACE 3: new session '{session}' -> core (what ingestion sees) ===")
    first = _first_chunk_by_note(metadata)
    # Session-index artifacts (the changelog, README) are not "new material" - keep
    # them out of the query set or they inflate n and the best-in-vault tail.
    note_ids = [
        n for n, i in first.items()
        if session in metadata[i]["filepath"]
        and not re.search(r"CHANGELOG|README", metadata[i]["filepath"], re.IGNORECASE)
    ]
    if not note_ids:
        print("  no notes matched that session substring")
        return
    titles = [metadata[first[n]]["title"] for n in note_ids]
    emb = model.encode(titles, normalize_embeddings=True).astype("float32")
    # resolve_read_scope('core') -> the CORE_FOLDERS set. Passing the literal
    # string 'core' to build_scope_selector matches NOTHING and silently yields
    # an empty result - always resolve tokens first.
    _, best_core = _probe(
        index, metadata, emb, note_ids, resolve_read_scope("core"), exclude_substr=session
    )
    _, best_all = _probe(index, metadata, emb, note_ids, None, exclude_substr=session)
    describe("-> best in CORE     ", best_core)
    describe("-> best in VAULT    ", best_all)
    print(
        "  NOTE: this is the auto-linking population. A genuinely NEW external source\n"
        "        scores far lower against core than an incremental note does."
    )


def space_4_duplicate_probe(index, metadata, model, sample, seed):
    """What a NEAR-DUPLICATE of an existing core note scores - the dedup population.

    Space 3 (new material -> core) measures NON-duplicates by construction, so it says
    nothing about what a duplicate scores; that mistake set the extractor's read-gate
    to 0.45 on 2026-09-02. A duplicate is approximated here by querying a core note
    with its own title and with its own first sentence, vault-wide, and asking (a) what
    raw cosine the note itself scores and (b) at what rank (among distinct notes) it
    appears. Added by the 2026-09-02 validation pass.
    """
    print("\n=== SPACE 4: near-duplicate probe (core note queried by its own title / first sentence) ===")
    from index_brain import is_frontmatter_only  # noqa: E402

    core = resolve_read_scope("core")
    first_content = {}
    for i, m in enumerate(metadata):
        if (any(f in m["filepath"] for f in core) and not is_frontmatter_only(m["content"])
                and m["content"].strip() and m["note_id"] not in first_content):
            first_content[m["note_id"]] = i
    random.seed(seed)
    ids = random.sample(list(first_content), min(sample, len(first_content)))

    def first_sentence(txt):
        body = re.sub(r"^#.*$", "", txt, flags=re.M)
        body = re.sub(r"^(Date|Source|Type|Title|Tags|Status):.*$", "", body, flags=re.M)
        body = re.sub(r"\[\[([^\]|]+)(\|[^\]]+)?\]\]", r"\1", body)
        body = re.sub(r"[*_`>]", "", body).strip()
        return re.split(r"(?<=[.!?])\s", body, 1)[0][:220]

    probes = (
        ("own title", [metadata[first_content[n]]["title"] for n in ids]),
        ("own first sentence", [first_sentence(metadata[first_content[n]]["content"]) for n in ids]),
    )
    for label, queries in probes:
        emb = model.encode(queries, normalize_embeddings=True).astype("float32")
        distances, indices = index.search(emb, 100)
        ranks, own_scores = [], []
        for row, note_id in enumerate(ids):
            seen, rank = [], None
            for dist, idx in zip(distances[row], indices[row]):
                if idx < 0:
                    continue
                nid = metadata[idx]["note_id"]
                if nid not in seen:
                    seen.append(nid)
                if nid == note_id:
                    rank = len(seen)
                    own_scores.append(float(dist))
                    break
            ranks.append(rank if rank else 999)
        r = np.asarray(ranks)
        describe(f"{label:18s} -> own ", own_scores, marks=(0.45, 0.60, 0.70))
        print(
            f"{' ' * 18}    own note at rank<=1: {100 * np.mean(r <= 1):.0f}%  <=3: {100 * np.mean(r <= 3):.0f}%"
            f"  <=5: {100 * np.mean(r <= 5):.0f}%  <=10: {100 * np.mean(r <= 10):.0f}%"
        )
    print(
        "  NOTE: this is the DEDUP population. A read-gate that only fires on score cannot\n"
        "        separate a duplicate from the best unrelated neighbour (their score ranges\n"
        "        overlap) - gate on RANK (read the top few) plus a raw-cosine tail."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=60)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--session", default=None, help="session-folder substring for space 3")
    args = ap.parse_args()

    space_1_graph_edges()
    index, metadata, model = _load()
    space_2_query_vault(index, metadata, model, args.sample, args.seed)
    space_2b_query_scoped(index, metadata, model, args.sample, args.seed)
    space_4_duplicate_probe(index, metadata, model, args.sample, args.seed)
    if args.session:
        space_3_session_vs_core(index, metadata, model, args.session)
    print("\nUpdate SIMILARITY-CALIBRATION.md with these figures and today's date.")


if __name__ == "__main__":
    main()
