"""
Brain Dependency Graph - Lifecycle Detection Engine

Computes lifecycle scores (0.0 reflective -> 1.0 generative) from
behavioral signals: citation frequency, generative ratio, cross-domain
reach, and temporal acceleration.
"""
from __future__ import annotations

import os
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import networkx as nx

from config import get_lifecycle_config, BRAIN_PATH
from models import LifecycleTransition


def _get_note_mtime(note_id: str, G: nx.DiGraph) -> float | None:
    """Get file modification time for a note (used as proxy for creation/edit date)."""
    node_data = G.nodes.get(note_id, {})
    filepath = node_data.get("filepath")
    if filepath and os.path.exists(filepath):
        return os.path.getmtime(filepath)
    return None


def _count_recent_citations(
    note_id: str,
    G: nx.DiGraph,
    window_seconds: float,
    now: float,
) -> int:
    """Count inbound edges from notes modified within the time window."""
    count = 0
    for src, _ in G.in_edges(note_id):
        mtime = _get_note_mtime(src, G)
        if mtime and (now - mtime) <= window_seconds:
            count += 1
    return count


def _compute_generative_ratio(
    note_id: str,
    enrichments: dict,
    G: nx.DiGraph,
) -> float:
    """
    Compute ratio of generative outbound edges to reflective inbound edges.
    Generative edges: instantiates, derives-from (outbound where this note is authority)
    Reflective edges: derives-from (inbound where source is authority)
    """
    edges_data = enrichments.get("edges", {})
    generative_out = 0
    reflective_in = 0

    # Outbound edges where this note is the authority (source)
    for _, dst in G.out_edges(note_id):
        edge_key = f"{note_id}||{dst}"
        edge_data = edges_data.get(edge_key, {})
        edge_type = edge_data.get("edge_type", "references")
        authority = edge_data.get("authority", "none")
        if edge_type in ("instantiates", "derives-from") and authority == "source":
            generative_out += 1

    # Inbound edges where source is authority over this note
    for src, _ in G.in_edges(note_id):
        edge_key = f"{src}||{note_id}"
        edge_data = edges_data.get(edge_key, {})
        edge_type = edge_data.get("edge_type", "references")
        authority = edge_data.get("authority", "none")
        if edge_type in ("derives-from",) and authority == "source":
            reflective_in += 1

    if reflective_in == 0:
        return generative_out * 1.5  # No inbound authority = more generative
    return generative_out / reflective_in


def _compute_cross_domain_reach(note_id: str, G: nx.DiGraph) -> int:
    """Count distinct vault subdirectories (clusters) that cite this note."""
    clusters = set()
    for src, _ in G.in_edges(note_id):
        # Use first path component as cluster proxy
        parts = src.split("/")
        if len(parts) >= 1:
            clusters.add(parts[0])
    return len(clusters)


def _compute_temporal_acceleration(
    note_id: str,
    G: nx.DiGraph,
    window_seconds: float,
    now: float,
) -> float:
    """
    Compare citation rate in recent half vs prior half of the window.
    Positive = accelerating, negative = decelerating.
    """
    half_window = window_seconds / 2
    midpoint = now - half_window

    recent_count = 0
    prior_count = 0

    for src, _ in G.in_edges(note_id):
        mtime = _get_note_mtime(src, G)
        if mtime is None:
            continue
        age = now - mtime
        if age <= half_window:
            recent_count += 1
        elif age <= window_seconds:
            prior_count += 1

    # Normalize to a -1 to 1 scale
    total = recent_count + prior_count
    if total == 0:
        return 0.0
    return (recent_count - prior_count) / total


def compute_lifecycle_score(
    note_id: str,
    G: nx.DiGraph,
    enrichments: dict,
) -> tuple[float, dict[str, float]]:
    """
    Compute lifecycle score for a single note.
    Returns (score, signal_values) tuple.
    """
    config = get_lifecycle_config()
    signals_config = config["signals"]
    window_days = config["detection_window_days"]
    window_seconds = window_days * 86400
    now = time.time()

    # Compute raw signals
    citation_freq = _count_recent_citations(note_id, G, window_seconds, now)
    gen_ratio = _compute_generative_ratio(note_id, enrichments, G)
    cross_domain = _compute_cross_domain_reach(note_id, G)
    temporal_accel = _compute_temporal_acceleration(note_id, G, window_seconds, now)

    # Normalize signals to 0-1 range
    cf_config = signals_config["citation_frequency"]
    gr_config = signals_config["generative_ratio"]
    cd_config = signals_config["cross_domain_reach"]
    ta_config = signals_config["temporal_acceleration"]

    cf_norm = min(citation_freq / max(cf_config["crystallizing_min"] * 3, 1), 1.0)
    gr_norm = min(gen_ratio / max(gr_config["generative_min"] * 1.5, 1), 1.0)
    cd_norm = min(cross_domain / max(cd_config["generative_min"] * 2, 1), 1.0)
    ta_norm = max(0.0, min((temporal_accel + 1) / 2, 1.0))  # Map [-1,1] to [0,1]

    # Weighted sum
    score = (
        cf_config["weight"] * cf_norm +
        gr_config["weight"] * gr_norm +
        cd_config["weight"] * cd_norm +
        ta_config["weight"] * ta_norm
    )
    score = round(min(max(score, 0.0), 1.0), 3)

    signal_values = {
        "citation_frequency": citation_freq,
        "generative_ratio": round(gen_ratio, 2),
        "cross_domain_reach": cross_domain,
        "temporal_acceleration": round(temporal_accel, 3),
        "cf_normalized": round(cf_norm, 3),
        "gr_normalized": round(gr_norm, 3),
        "cd_normalized": round(cd_norm, 3),
        "ta_normalized": round(ta_norm, 3),
    }

    return score, signal_values


def compute_all_lifecycles(
    G: nx.DiGraph,
    enrichments: dict,
) -> list[LifecycleTransition]:
    """
    Compute lifecycle scores for all insight and framework notes.
    Updates enrichments in-place. Returns list of transitions.
    """
    config = get_lifecycle_config()
    nodes = enrichments.get("nodes", {})
    transitions = []

    target_layers = {"insight", "framework"}
    candidates = [
        nid for nid, ndata in nodes.items()
        if ndata.get("layer") in target_layers
    ]

    print(f"Computing lifecycle for {len(candidates)} notes...")

    for note_id in candidates:
        if note_id not in G:
            continue

        old_score = nodes[note_id].get("lifecycle", 0.0)
        old_phase = LifecycleTransition.phase_name(old_score)

        new_score, signals = compute_lifecycle_score(note_id, G, enrichments)
        new_phase = LifecycleTransition.phase_name(new_score)

        # Update enrichment
        nodes[note_id]["lifecycle"] = new_score

        # Detect transition
        if old_phase != new_phase:
            transitions.append(LifecycleTransition(
                note_id=note_id,
                old_score=old_score,
                new_score=new_score,
                old_phase=old_phase,
                new_phase=new_phase,
                signals=signals,
            ))

    print(f"  Transitions detected: {len(transitions)}")
    return transitions
