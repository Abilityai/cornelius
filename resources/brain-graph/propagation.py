"""
Brain Dependency Graph - Staleness Propagation Engine

Computes staleness scores by propagating change signals along typed,
directed edges with attenuation by edge type, distance, and hub dampening.
"""
from __future__ import annotations

from collections import defaultdict

import networkx as nx

from config import get_propagation_config
from models import StalenessResult


def compute_staleness(
    G: nx.DiGraph,
    enrichments: dict,
    changed_note: str,
    change_magnitude: float = 1.0,
) -> StalenessResult:
    """
    Propagate staleness from a changed note through the graph.

    Staleness flows DOWNSTREAM only (source -> target along authority direction).
    Attenuated by: edge_decay[type] x distance_decay[hop] x hub_dampening.

    Returns StalenessResult with all affected notes and their staleness scores.
    """
    config = get_propagation_config()
    edge_decay = config["edge_decay"]
    distance_decay = config["distance_decay"]
    hub_threshold = config["hub_threshold"]
    max_depth = config["max_propagation_depth"]

    nodes_data = enrichments.get("nodes", {})
    edges_data = enrichments.get("edges", {})

    affected: dict[str, float] = {}
    total_examined = 0

    # BFS with depth tracking
    # Queue items: (note_id, current_staleness, depth)
    queue = [(changed_note, change_magnitude, 0)]
    visited = {changed_note}

    while queue:
        current_id, current_signal, depth = queue.pop(0)

        if depth >= max_depth:
            continue

        hop = depth  # 0-indexed: first hop from source is hop 0
        if hop >= len(distance_decay):
            continue

        # Get outgoing edges (downstream propagation)
        if current_id not in G:
            continue

        for _, neighbor in G.out_edges(current_id):
            total_examined += 1

            # Get edge enrichment
            edge_key = f"{current_id}||{neighbor}"
            edge_data = edges_data.get(edge_key, {})
            edge_type = edge_data.get("edge_type", "references")
            authority = edge_data.get("authority", "none")

            # Only propagate along authority direction
            # If authority=source, the source drives the target -> propagate forward
            # If authority=target, the target is authoritative -> don't propagate
            if authority == "target":
                continue

            # Tension edges are immune
            if edge_type == "tension":
                continue

            # Compute staleness for this neighbor
            type_decay = edge_decay.get(edge_type, 0.2)
            dist_decay = distance_decay[hop] if hop < len(distance_decay) else 0.0

            # Hub dampening
            neighbor_degree = G.degree(neighbor)
            hub_dampen = 1.0
            if neighbor_degree > hub_threshold:
                hub_dampen = hub_threshold / neighbor_degree

            staleness = current_signal * type_decay * dist_decay * hub_dampen

            if staleness > 0.01:  # Skip negligible signals
                # Keep max staleness if visited from multiple paths
                if neighbor in affected:
                    affected[neighbor] = max(affected[neighbor], staleness)
                else:
                    affected[neighbor] = staleness

                # Continue propagation if not visited
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, staleness, depth + 1))

    # Remove the source note itself
    affected.pop(changed_note, None)

    return StalenessResult(
        changed_note=changed_note,
        change_magnitude=change_magnitude,
        affected_notes=dict(sorted(affected.items(), key=lambda x: -x[1])),
        propagation_depth=max_depth,
        total_examined=total_examined,
    )


def update_staleness_scores(enrichments: dict, result: StalenessResult, threshold: float = 0.3) -> int:
    """
    Update staleness_score in enrichments for affected notes.
    Returns count of notes updated above threshold.
    """
    nodes = enrichments.get("nodes", {})
    count = 0
    for note_id, score in result.affected_notes.items():
        if note_id in nodes:
            # Take max of existing and new staleness
            old = nodes[note_id].get("staleness_score", 0.0)
            nodes[note_id]["staleness_score"] = max(old, score)
            if score >= threshold:
                count += 1
    return count
