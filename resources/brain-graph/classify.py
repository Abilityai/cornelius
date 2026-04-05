"""
Brain Dependency Graph - Classification Engine

Classifies notes into layers and types edges based on heuristics.
This is the bootstrap engine that converts the flat LBS graph into a
directed, mode-aware dependency graph.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

import networkx as nx

from config import (
    BRAIN_PATH, get_artifact_types, get_default_edges,
    get_framework_detection, load_config,
)
from models import (
    Layer, EdgeType, Authority, NodeEnrichment, EdgeEnrichment,
)
from store import (
    load_lbs_graph, load_enrichments, save_enrichments,
    set_node_enrichment, set_edge_enrichment,
)


# =============================================================================
# LAYER CLASSIFICATION
# =============================================================================

def _build_path_layer_map(artifact_types: dict) -> list[tuple[str, str]]:
    """
    Build ordered list of (path_prefix, layer_name) from config.
    More specific paths first to avoid false matches.
    """
    pairs = []
    for layer_name, layer_config in artifact_types.items():
        for vpath in layer_config.get("vault_paths", []):
            pairs.append((vpath, layer_name))
    # Sort by path length descending (more specific first)
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    return pairs


def _parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return {}

    if not content.startswith("---"):
        return {}

    end = content.find("---", 3)
    if end == -1:
        return {}

    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Handle YAML lists inline [a, b, c]
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
            result[key] = value
    return result


def _is_framework_by_frontmatter(frontmatter: dict, detection_config: dict) -> bool:
    """Check if frontmatter indicates a framework note."""
    note_type = frontmatter.get("type", "")
    if isinstance(note_type, str):
        note_type_lower = note_type.lower()
        for indicator in detection_config.get("type_indicators", []):
            if indicator in note_type_lower:
                return True
    return False


def _is_framework_by_title(title: str, detection_config: dict) -> bool:
    """Check if note title matches framework patterns."""
    for pattern in detection_config.get("title_patterns", []):
        if re.search(pattern, title, re.IGNORECASE):
            return True
    return False


def _is_framework_by_graph(
    note_id: str, G: nx.DiGraph, detection_config: dict
) -> bool:
    """Check if graph metrics indicate a framework note."""
    thresholds = detection_config.get("graph_thresholds", {})
    in_deg = G.in_degree(note_id)
    out_deg = G.out_degree(note_id)
    if in_deg < thresholds.get("min_in_degree", 20):
        return False
    if out_deg < thresholds.get("min_out_degree", 10):
        return False
    # Betweenness is expensive for full graph; skip if no pre-computed value
    return True


def classify_node(
    note_id: str,
    G: nx.DiGraph,
    path_layer_map: list[tuple[str, str]],
    framework_detection: dict,
) -> NodeEnrichment:
    """Classify a single note into a layer."""
    # Step 1: Path-based classification
    for path_prefix, layer_name in path_layer_map:
        if note_id.startswith(path_prefix):
            # Special case: 02-Permanent/ could be framework
            if layer_name == "insight" and path_prefix == "02-Permanent/":
                node_data = G.nodes.get(note_id, {})
                filepath = node_data.get("filepath")
                title = node_data.get("title", Path(note_id).stem)

                # Check frontmatter
                if filepath:
                    fm = _parse_frontmatter(Path(filepath))
                    if _is_framework_by_frontmatter(fm, framework_detection):
                        return NodeEnrichment(
                            layer=Layer.FRAMEWORK.value,
                            classification_confidence=0.85,
                        )

                # Check title patterns
                if _is_framework_by_title(title, framework_detection):
                    return NodeEnrichment(
                        layer=Layer.FRAMEWORK.value,
                        classification_confidence=0.70,
                    )

                # Check graph metrics
                if _is_framework_by_graph(note_id, G, framework_detection):
                    return NodeEnrichment(
                        layer=Layer.FRAMEWORK.value,
                        classification_confidence=0.60,
                    )

            confidence = 0.95 if layer_name in ("signal", "impression", "lens") else 0.85
            return NodeEnrichment(
                layer=layer_name,
                classification_confidence=confidence,
            )

    # Fallback: unclassified notes default to insight
    return NodeEnrichment(layer=Layer.INSIGHT.value, classification_confidence=0.3)


# =============================================================================
# EDGE CLASSIFICATION
# =============================================================================

def _build_edge_type_lookup(default_edges: list) -> dict[tuple[str, str], dict]:
    """Build lookup from (src_layer, dst_layer) -> edge config."""
    lookup = {}
    for edge_def in default_edges:
        key = (edge_def["from_type"], edge_def["to_type"])
        lookup[key] = {
            "edge_type": edge_def["edge_type"],
            "authority": edge_def.get("authority", "none"),
        }
    return lookup


def classify_edge(
    src_id: str,
    dst_id: str,
    src_layer: str,
    dst_layer: str,
    original_type: str,
    edge_lookup: dict[tuple[str, str], dict],
    same_layer_defaults: dict,
) -> EdgeEnrichment:
    """Classify a single edge based on source/target layers."""
    # Semantic edges always become associates
    if original_type == "semantic":
        return EdgeEnrichment(
            edge_type=EdgeType.ASSOCIATES.value,
            authority=Authority.NONE.value,
            confidence=0.90,
            original_type=original_type,
        )

    # Look up cross-layer default
    key = (src_layer, dst_layer)
    if key in edge_lookup:
        match = edge_lookup[key]
        return EdgeEnrichment(
            edge_type=match["edge_type"],
            authority=match["authority"],
            confidence=0.75,
            original_type=original_type,
        )

    # Same-layer edges
    if src_layer == dst_layer:
        defaults = same_layer_defaults.get(src_layer, {})
        return EdgeEnrichment(
            edge_type=defaults.get("edge_type", EdgeType.REFERENCES.value),
            authority=defaults.get("authority") or Authority.NONE.value,
            confidence=0.60,
            original_type=original_type,
        )

    # Fallback: references
    return EdgeEnrichment(
        edge_type=EdgeType.REFERENCES.value,
        authority=Authority.NONE.value,
        confidence=0.40,
        original_type=original_type,
    )


# =============================================================================
# INITIAL LIFECYCLE FROM GRAPH METRICS
# =============================================================================

def compute_initial_lifecycle(note_id: str, G: nx.DiGraph) -> float:
    """
    Compute an initial lifecycle score from graph structure.
    This is a rough estimate; the full lifecycle engine (lifecycle.py)
    does temporal analysis.
    """
    in_deg = G.in_degree(note_id)
    out_deg = G.out_degree(note_id)

    if in_deg == 0 and out_deg == 0:
        return 0.0

    # Generative ratio proxy
    gen_ratio = out_deg / max(in_deg, 1)

    # Normalize: many inbound citations + high gen_ratio = generative
    citation_signal = min(in_deg / 50.0, 1.0)  # saturates at 50
    ratio_signal = min(gen_ratio / 3.0, 1.0)   # saturates at 3.0

    # Weighted combination
    score = 0.5 * citation_signal + 0.5 * ratio_signal
    return round(min(score, 1.0), 3)


# =============================================================================
# FULL BOOTSTRAP
# =============================================================================

def bootstrap(force: bool = False) -> dict:
    """
    Bootstrap the entire graph: classify all nodes and edges.
    Returns the enrichments dict.
    """
    enrichments = load_enrichments()

    if enrichments.get("last_bootstrap") and not force:
        print("Graph already bootstrapped. Use --force to re-bootstrap.")
        print(f"  Last bootstrap: {enrichments['last_bootstrap']}")
        print(f"  Nodes: {len(enrichments.get('nodes', {}))}")
        print(f"  Edges: {len(enrichments.get('edges', {}))}")
        return enrichments

    print("Loading LBS graph...")
    G = load_lbs_graph()
    config = load_config()

    artifact_types = config["artifact_types"]
    default_edges = config["default_edges"]
    same_layer_defaults = config.get("same_layer_defaults", {})
    framework_detection = config.get("framework_detection", {})

    path_layer_map = _build_path_layer_map(artifact_types)
    edge_lookup = _build_edge_type_lookup(default_edges)

    # Reset enrichments
    enrichments = {
        "version": "1.0",
        "last_bootstrap": datetime.now().isoformat(),
        "last_coherence_sweep": None,
        "nodes": {},
        "edges": {},
        "tensions": [],
    }

    # Classify nodes
    print(f"Classifying {G.number_of_nodes()} nodes...")
    layer_counts = {}
    framework_count = 0

    for note_id in G.nodes:
        node_enrichment = classify_node(
            note_id, G, path_layer_map, framework_detection,
        )
        # Compute initial lifecycle for insights and frameworks
        if node_enrichment.layer in ("insight", "framework"):
            node_enrichment.lifecycle = compute_initial_lifecycle(note_id, G)

        set_node_enrichment(enrichments, note_id, node_enrichment)
        layer_counts[node_enrichment.layer] = layer_counts.get(node_enrichment.layer, 0) + 1
        if node_enrichment.layer == "framework":
            framework_count += 1

    print("  Layer distribution:")
    for layer in ("signal", "impression", "insight", "framework", "lens", "synthesis", "index"):
        count = layer_counts.get(layer, 0)
        print(f"    {layer:12s}: {count:5d}")

    # Classify edges
    print(f"Typing {G.number_of_edges()} edges...")
    edge_type_counts = {}

    for src, dst, edge_data in G.edges(data=True):
        src_node = enrichments["nodes"].get(src)
        dst_node = enrichments["nodes"].get(dst)
        if not src_node or not dst_node:
            continue

        original_type = edge_data.get("type", "explicit")
        edge_enrichment = classify_edge(
            src, dst,
            src_node["layer"], dst_node["layer"],
            original_type,
            edge_lookup, same_layer_defaults,
        )
        set_edge_enrichment(enrichments, src, dst, edge_enrichment)
        et = edge_enrichment.edge_type
        edge_type_counts[et] = edge_type_counts.get(et, 0) + 1

    print("  Edge type distribution:")
    for et in ("derives-from", "instantiates", "references", "associates", "tension", "supersedes"):
        count = edge_type_counts.get(et, 0)
        print(f"    {et:15s}: {count:6d}")

    # Save
    save_enrichments(enrichments)
    print(f"\nBootstrap complete. Saved to {ENRICHMENTS_PATH}")
    print(f"  Nodes classified: {len(enrichments['nodes'])}")
    print(f"  Edges typed: {len(enrichments['edges'])}")
    print(f"  Frameworks detected: {framework_count}")

    return enrichments


# Import at bottom to avoid circular
from config import ENRICHMENTS_PATH
