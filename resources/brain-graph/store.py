"""
Brain Dependency Graph - Persistence Layer

Loads/saves graph_enrichments.json and overlays enrichments onto the NetworkX graph.
Never modifies the original brain_graph.pkl from Local Brain Search.
"""
from __future__ import annotations

import json
import pickle
import sys
from datetime import datetime
from pathlib import Path

import networkx as nx
import numpy as np

from config import ENRICHMENTS_PATH, LBS_GRAPH_PATH, DATA_DIR
from models import NodeEnrichment, EdgeEnrichment, TensionRecord


class NumpyEncoder(json.JSONEncoder):
    """Handle NumPy types in JSON serialization."""
    def default(self, obj):
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# =============================================================================
# ENRICHMENTS PERSISTENCE
# =============================================================================

def _empty_enrichments() -> dict:
    """Create an empty enrichments structure."""
    return {
        "version": "1.0",
        "last_bootstrap": None,
        "last_coherence_sweep": None,
        "nodes": {},
        "edges": {},
        "tensions": [],
    }


def load_enrichments() -> dict:
    """Load enrichments from JSON. Returns empty structure if not found."""
    if not ENRICHMENTS_PATH.exists():
        return _empty_enrichments()
    with open(ENRICHMENTS_PATH) as f:
        return json.load(f)


def save_enrichments(data: dict) -> None:
    """Save enrichments to JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ENRICHMENTS_PATH, "w") as f:
        json.dump(data, f, indent=2, cls=NumpyEncoder)


def get_node_enrichment(enrichments: dict, note_id: str) -> NodeEnrichment | None:
    """Get enrichment for a specific node."""
    node_data = enrichments.get("nodes", {}).get(note_id)
    if node_data is None:
        return None
    return NodeEnrichment.from_dict(node_data)


def get_edge_enrichment(enrichments: dict, src: str, dst: str) -> EdgeEnrichment | None:
    """Get enrichment for a specific edge."""
    key = f"{src}||{dst}"
    edge_data = enrichments.get("edges", {}).get(key)
    if edge_data is None:
        return None
    return EdgeEnrichment.from_dict(edge_data)


def set_node_enrichment(enrichments: dict, note_id: str, node: NodeEnrichment) -> None:
    """Set enrichment for a specific node."""
    enrichments.setdefault("nodes", {})[note_id] = node.to_dict()


def set_edge_enrichment(enrichments: dict, src: str, dst: str, edge: EdgeEnrichment) -> None:
    """Set enrichment for a specific edge."""
    key = f"{src}||{dst}"
    enrichments.setdefault("edges", {})[key] = edge.to_dict()


# =============================================================================
# GRAPH LOADING
# =============================================================================

def load_lbs_graph() -> nx.DiGraph:
    """Load the Local Brain Search NetworkX graph (read-only reference)."""
    if not LBS_GRAPH_PATH.exists():
        print(f"Error: LBS graph not found at {LBS_GRAPH_PATH}", file=sys.stderr)
        print("Run local-brain-search/run_index.sh first.", file=sys.stderr)
        sys.exit(1)
    with open(LBS_GRAPH_PATH, "rb") as f:
        return pickle.load(f)


def load_enriched_graph() -> tuple[nx.DiGraph, dict]:
    """
    Load the LBS graph and overlay enrichments as node/edge attributes.
    Returns (graph, enrichments) tuple.
    The graph is a copy - never modifies the pkl.
    """
    G = load_lbs_graph()
    enrichments = load_enrichments()

    # Overlay node enrichments
    for note_id, node_data in enrichments.get("nodes", {}).items():
        if note_id in G.nodes:
            G.nodes[note_id].update({
                "bdg_layer": node_data.get("layer"),
                "bdg_lifecycle": node_data.get("lifecycle", 0.0),
                "bdg_staleness": node_data.get("staleness_score", 0.0),
            })

    # Overlay edge enrichments
    for edge_key, edge_data in enrichments.get("edges", {}).items():
        parts = edge_key.split("||", 1)
        if len(parts) == 2:
            src, dst = parts
            if G.has_edge(src, dst):
                G.edges[src, dst].update({
                    "bdg_edge_type": edge_data.get("edge_type"),
                    "bdg_authority": edge_data.get("authority", "none"),
                })

    return G, enrichments


def find_note_id(G: nx.DiGraph, query: str) -> str | None:
    """Find note ID by name, title, or partial match."""
    query_lower = query.lower()

    # Exact match
    if query in G.nodes:
        return query

    # Search by title or filename
    for node_id in G.nodes:
        node_data = G.nodes[node_id]
        title = node_data.get("title", "").lower()
        stem = Path(node_id).stem.lower()
        if query_lower == title or query_lower == stem:
            return node_id

    # Partial match
    for node_id in G.nodes:
        node_data = G.nodes[node_id]
        title = node_data.get("title", "").lower()
        stem = Path(node_id).stem.lower()
        if query_lower in title or query_lower in stem:
            return node_id

    return None
