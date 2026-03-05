#!/usr/bin/env python3
"""
Spreading activation engine for semantic memory retrieval.

Implements SYNAPSE-inspired spreading activation with:
- Configurable decay factors per edge type
- Lateral inhibition to prevent hub dominance
- Temporal decay for activation age
- Convergence detection

Based on Collins & Loftus (1975) spreading activation theory
and the SYNAPSE paper (arXiv:2601.02744, January 2026).
"""
import pickle
from dataclasses import dataclass, field
from typing import Optional

import networkx as nx
import numpy as np

from config import GRAPH_PICKLE_PATH
from intent import QueryIntent, get_spreading_config


@dataclass
class SpreadingConfig:
    """Configuration for spreading activation."""

    # Iteration control
    max_iterations: int = 5
    convergence_threshold: float = 0.01

    # Activation thresholds
    activation_threshold: float = 0.1  # Minimum to spread
    anchor_strength: float = 0.8  # How much to re-inject seed activation

    # Decay factors by edge type
    decay_factors: dict = field(default_factory=lambda: {
        'explicit': 0.8,  # Strong propagation through wiki-links
        'semantic': 0.5,  # Moderate through similarity
        'temporal': 0.3,  # Weak through time proximity
        'causal': 0.9,    # Very strong through causal links
    })

    # Temporal decay (per iteration)
    temporal_decay: float = 0.9

    # Lateral inhibition
    inhibition_strength: float = 0.3
    inhibition_percentile: float = 90  # Top N% are "high activation"

    @classmethod
    def from_memory_config(cls) -> "SpreadingConfig":
        """Create config from memory_config.py settings."""
        from memory_config import MEMORY_CONFIG
        cfg = MEMORY_CONFIG["spreading"]
        return cls(
            max_iterations=cfg["max_iterations"],
            convergence_threshold=cfg["convergence_threshold"],
            activation_threshold=cfg["activation_threshold"],
            anchor_strength=cfg["anchor_strength"],
            decay_factors=cfg["decay_factors"].copy(),
            temporal_decay=cfg["temporal_decay"],
            inhibition_strength=cfg["inhibition_strength"],
            inhibition_percentile=cfg["inhibition_percentile"],
        )

    @classmethod
    def from_intent(cls, intent: QueryIntent) -> "SpreadingConfig":
        """Create config from query intent."""
        from memory_config import MEMORY_CONFIG
        base_cfg = MEMORY_CONFIG["spreading"]
        intent_config = get_spreading_config(intent)

        return cls(
            max_iterations=intent_config.get("max_iterations", base_cfg["max_iterations"]),
            convergence_threshold=base_cfg["convergence_threshold"],
            activation_threshold=base_cfg["activation_threshold"],
            anchor_strength=base_cfg["anchor_strength"],
            decay_factors=base_cfg["decay_factors"].copy(),
            temporal_decay=intent_config.get("temporal_decay", base_cfg["temporal_decay"]),
            inhibition_strength=intent_config.get("inhibition_strength", base_cfg["inhibition_strength"]),
            inhibition_percentile=base_cfg["inhibition_percentile"],
        )


@dataclass
class ActivationTrace:
    """Trace of how activation reached a node."""
    path: list[str]
    activation_history: list[float]
    contributing_edges: list[tuple[str, str, str]]  # (source, target, edge_type)


@dataclass
class SpreadingResult:
    """Result of spreading activation."""
    activations: dict[str, float]
    iterations: int
    converged: bool
    traces: Optional[dict[str, ActivationTrace]] = None


def load_graph() -> nx.DiGraph:
    """Load the brain graph."""
    with open(GRAPH_PICKLE_PATH, 'rb') as f:
        return pickle.load(f)


def get_neighbors_within_radius(
    G: nx.DiGraph,
    node: str,
    radius: int,
) -> set[str]:
    """Get all nodes within graph distance of radius."""
    neighbors = set()
    current = {node}

    for _ in range(radius):
        next_level = set()
        for n in current:
            for neighbor in G.neighbors(n):
                if neighbor not in neighbors and neighbor != node:
                    next_level.add(neighbor)
                    neighbors.add(neighbor)
            for neighbor in G.predecessors(n):
                if neighbor not in neighbors and neighbor != node:
                    next_level.add(neighbor)
                    neighbors.add(neighbor)
        current = next_level

    return neighbors


def apply_lateral_inhibition(
    activation: dict[str, float],
    G: nx.DiGraph,
    config: SpreadingConfig,
) -> dict[str, float]:
    """
    Apply lateral inhibition to prevent hub dominance.

    For highly activated nodes, suppress neighbors within radius.
    This prevents a single cluster from dominating results.
    """
    if not activation:
        return activation

    result = activation.copy()

    # Find highly activated nodes (top percentile)
    values = list(activation.values())
    if not values:
        return result

    threshold = np.percentile(values, config.inhibition_percentile)
    high_activation_nodes = [n for n, a in activation.items() if a >= threshold]

    # For each highly activated node, suppress its neighbors
    for node in high_activation_nodes:
        neighbors = get_neighbors_within_radius(G, node, radius=2)
        for neighbor in neighbors:
            if neighbor in result and neighbor not in high_activation_nodes:
                result[neighbor] *= (1 - config.inhibition_strength)

    return result


def is_converged(
    old_activation: dict[str, float],
    new_activation: dict[str, float],
    threshold: float,
) -> bool:
    """Check if activation has converged."""
    if not old_activation:
        return False

    total_change = 0.0
    for node in new_activation:
        old_val = old_activation.get(node, 0.0)
        new_val = new_activation[node]
        total_change += abs(new_val - old_val)

    return total_change < threshold


def spreading_activation(
    G: nx.DiGraph,
    seed_nodes: list[tuple[str, float]],  # (note_id, initial_activation)
    config: Optional[SpreadingConfig] = None,
    track_traces: bool = False,
) -> SpreadingResult:
    """
    SYNAPSE-inspired spreading activation.

    Args:
        G: The note graph
        seed_nodes: Initial seed nodes with activation scores
        config: Spreading configuration
        track_traces: Whether to track activation paths (slower)

    Returns:
        SpreadingResult with final activation scores
    """
    if config is None:
        config = SpreadingConfig()

    # Initialize activation
    activation = {node: 0.0 for node in G.nodes}
    for node, score in seed_nodes:
        if node in activation:
            activation[node] = score

    # Track traces if requested
    traces = {} if track_traces else None
    if track_traces:
        for node, score in seed_nodes:
            if node in G.nodes:
                traces[node] = ActivationTrace(
                    path=[node],
                    activation_history=[score],
                    contributing_edges=[],
                )

    converged = False
    iteration = 0

    for iteration in range(config.max_iterations):
        new_activation = {n: 0.0 for n in G.nodes}

        # Spread activation along edges
        for node in G.nodes:
            current_activation = activation[node]
            if current_activation < config.activation_threshold:
                continue

            # Spread to neighbors (outgoing edges)
            for _, neighbor, edge_data in G.out_edges(node, data=True):
                edge_type = edge_data.get('type', 'explicit')
                decay = config.decay_factors.get(edge_type, 0.5)

                # Get edge weight (for semantic edges, this is similarity)
                edge_weight = edge_data.get('weight', 1.0)

                # Compute spread amount
                spread = current_activation * decay * edge_weight

                # Accumulate at neighbor
                new_activation[neighbor] += spread

                # Track trace
                if track_traces and spread > 0.01:
                    if neighbor not in traces:
                        traces[neighbor] = ActivationTrace(
                            path=[node, neighbor],
                            activation_history=[spread],
                            contributing_edges=[(node, neighbor, edge_type)],
                        )
                    else:
                        traces[neighbor].contributing_edges.append((node, neighbor, edge_type))

            # Also spread through incoming edges (bidirectional spreading)
            for source, _, edge_data in G.in_edges(node, data=True):
                edge_type = edge_data.get('type', 'explicit')
                decay = config.decay_factors.get(edge_type, 0.5) * 0.5  # Lower for reverse

                edge_weight = edge_data.get('weight', 1.0)
                spread = current_activation * decay * edge_weight

                new_activation[source] += spread

        # Apply lateral inhibition
        new_activation = apply_lateral_inhibition(new_activation, G, config)

        # Apply temporal decay to all activations
        for node in new_activation:
            new_activation[node] *= config.temporal_decay

        # Re-inject seed activation (anchoring)
        for node, score in seed_nodes:
            if node in new_activation:
                new_activation[node] = max(
                    new_activation[node],
                    score * config.anchor_strength
                )

        # Check convergence
        if is_converged(activation, new_activation, config.convergence_threshold):
            converged = True
            activation = new_activation
            break

        activation = new_activation

    return SpreadingResult(
        activations=activation,
        iterations=iteration + 1,
        converged=converged,
        traces=traces,
    )


def get_top_activated(
    result: SpreadingResult,
    G: nx.DiGraph,
    limit: int = 10,
    exclude_seeds: Optional[set[str]] = None,
    normalize: bool = True,
) -> list[dict]:
    """Get top activated notes with metadata."""
    exclude = exclude_seeds or set()

    # Sort by activation
    sorted_nodes = sorted(
        [(n, a) for n, a in result.activations.items() if n not in exclude and a > 0],
        key=lambda x: x[1],
        reverse=True,
    )

    # Normalize scores to 0-1 range
    if normalize and sorted_nodes:
        max_activation = sorted_nodes[0][1]
        if max_activation > 0:
            sorted_nodes = [(n, a / max_activation) for n, a in sorted_nodes]

    results = []
    for node_id, activation in sorted_nodes[:limit]:
        node_data = G.nodes.get(node_id, {})
        results.append({
            'note_id': node_id,
            'title': node_data.get('title', node_id),
            'activation': activation,
            'filepath': node_data.get('filepath', ''),
        })

    return results


if __name__ == "__main__":
    # Test spreading activation
    print("Loading graph...")
    G = load_graph()
    print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    # Test with a known hub node
    test_queries = [
        ("Dopamine", QueryIntent.CONCEPTUAL),
        ("Flow is a selfless state", QueryIntent.SYNTHESIS),
    ]

    for test_note, intent in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing spreading from: {test_note}")
        print(f"Intent: {intent.value}")

        # Find the note
        note_id = None
        for node in G.nodes:
            if test_note.lower() in G.nodes[node].get('title', '').lower():
                note_id = node
                break

        if not note_id:
            print(f"Note not found: {test_note}")
            continue

        print(f"Found: {note_id}")

        # Run spreading activation
        config = SpreadingConfig.from_intent(intent)
        result = spreading_activation(
            G,
            seed_nodes=[(note_id, 1.0)],
            config=config,
        )

        print(f"\nIterations: {result.iterations}, Converged: {result.converged}")
        print("\nTop activated notes:")

        top = get_top_activated(result, G, limit=10, exclude_seeds={note_id})
        for i, note in enumerate(top, 1):
            print(f"  {i}. [{note['activation']:.3f}] {note['title']}")
