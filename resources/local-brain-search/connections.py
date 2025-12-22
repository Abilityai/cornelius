#!/usr/bin/env python3
"""
Find connections for a note in the Brain.

Usage:
    python connections.py "note name or path"
    python connections.py "Dopamine" --depth 2
    python connections.py "Dopamine" --semantic-only
    python connections.py --stats  # Show graph statistics
    python connections.py --hubs   # Find hub notes
    python connections.py --bridges # Find bridge notes
"""
import argparse
import json
import pickle
import sys
from collections import defaultdict
from pathlib import Path

import networkx as nx
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy types."""
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

from config import BRAIN_PATH, GRAPH_PICKLE_PATH


def load_graph() -> nx.DiGraph:
    """Load the connection graph."""
    if not GRAPH_PICKLE_PATH.exists():
        print(f"Error: Graph not found at {GRAPH_PICKLE_PATH}")
        print("Run index_brain.py first.")
        sys.exit(1)

    with open(GRAPH_PICKLE_PATH, 'rb') as f:
        return pickle.load(f)


def find_note_id(G: nx.DiGraph, query: str) -> str | None:
    """Find note ID by name, title, or partial match."""
    query_lower = query.lower()

    # Exact match on note_id
    if query in G.nodes:
        return query

    # Search by title or filename
    for node_id in G.nodes:
        node_data = G.nodes[node_id]
        title = node_data.get('title', '').lower()
        stem = Path(node_id).stem.lower()

        if query_lower == title or query_lower == stem:
            return node_id
        if query_lower in title or query_lower in stem:
            return node_id

    return None


def get_connections(
    G: nx.DiGraph,
    note_id: str,
    depth: int = 1,
    include_semantic: bool = True,
    include_explicit: bool = True,
) -> dict:
    """Get connections for a note up to specified depth."""
    result = {
        'note_id': note_id,
        'title': G.nodes[note_id].get('title', note_id),
        'outgoing': [],  # Notes this note links to
        'incoming': [],  # Notes linking to this note
        'semantic': [],  # Semantically similar notes
        'paths': {},     # Shortest paths to related notes
    }

    # Direct outgoing connections
    for _, target, data in G.out_edges(note_id, data=True):
        edge_type = data.get('type', 'explicit')
        if edge_type == 'semantic' and not include_semantic:
            continue
        if edge_type == 'explicit' and not include_explicit:
            continue

        target_data = G.nodes[target]
        result['outgoing'].append({
            'note_id': target,
            'title': target_data.get('title', target),
            'type': edge_type,
            'weight': data.get('weight', 1.0),
        })

    # Direct incoming connections
    for source, _, data in G.in_edges(note_id, data=True):
        edge_type = data.get('type', 'explicit')
        if edge_type == 'semantic' and not include_semantic:
            continue
        if edge_type == 'explicit' and not include_explicit:
            continue

        source_data = G.nodes[source]
        result['incoming'].append({
            'note_id': source,
            'title': source_data.get('title', source),
            'type': edge_type,
            'weight': data.get('weight', 1.0),
        })

    # Semantic connections (from edges marked as semantic)
    for _, target, data in G.out_edges(note_id, data=True):
        if data.get('type') == 'semantic':
            target_data = G.nodes[target]
            result['semantic'].append({
                'note_id': target,
                'title': target_data.get('title', target),
                'similarity': data.get('weight', 0.0),
            })

    # Sort semantic by similarity
    result['semantic'].sort(key=lambda x: x['similarity'], reverse=True)

    # Multi-hop connections if depth > 1
    if depth > 1:
        visited = {note_id}
        current_level = {note_id}

        for d in range(depth):
            next_level = set()
            for node in current_level:
                for neighbor in G.neighbors(node):
                    if neighbor not in visited:
                        next_level.add(neighbor)
                        visited.add(neighbor)

                        # Find shortest path
                        try:
                            path = nx.shortest_path(G, note_id, neighbor)
                            if len(path) > 1:
                                result['paths'][neighbor] = {
                                    'path': path,
                                    'length': len(path) - 1,
                                    'title': G.nodes[neighbor].get('title', neighbor),
                                }
                        except nx.NetworkXNoPath:
                            pass

            current_level = next_level

    return result


def get_graph_stats(G: nx.DiGraph) -> dict:
    """Get statistics about the graph."""
    explicit_edges = sum(1 for _, _, d in G.edges(data=True) if d.get('type') != 'semantic')
    semantic_edges = sum(1 for _, _, d in G.edges(data=True) if d.get('type') == 'semantic')

    # Find isolated nodes
    isolated = [n for n in G.nodes if G.degree(n) == 0]

    # Connectivity
    undirected = G.to_undirected()
    components = list(nx.connected_components(undirected))

    return {
        'total_nodes': G.number_of_nodes(),
        'total_edges': G.number_of_edges(),
        'explicit_edges': explicit_edges,
        'semantic_edges': semantic_edges,
        'isolated_nodes': len(isolated),
        'connected_components': len(components),
        'largest_component': len(max(components, key=len)) if components else 0,
        'avg_degree': sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
    }


def find_hubs(G: nx.DiGraph, top_n: int = 20) -> list[dict]:
    """Find hub notes (most connected)."""
    degree_centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)

    hubs = []
    for node_id, centrality in sorted_nodes[:top_n]:
        node_data = G.nodes[node_id]
        in_degree = G.in_degree(node_id)
        out_degree = G.out_degree(node_id)

        hubs.append({
            'note_id': node_id,
            'title': node_data.get('title', node_id),
            'centrality': centrality,
            'in_degree': in_degree,
            'out_degree': out_degree,
            'total_degree': in_degree + out_degree,
        })

    return hubs


def find_bridges(G: nx.DiGraph, top_n: int = 20) -> list[dict]:
    """Find bridge notes (connect different communities)."""
    # Use betweenness centrality to find bridges
    betweenness = nx.betweenness_centrality(G)
    sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)

    bridges = []
    for node_id, centrality in sorted_nodes[:top_n]:
        if centrality > 0:  # Only include nodes that are actual bridges
            node_data = G.nodes[node_id]
            bridges.append({
                'note_id': node_id,
                'title': node_data.get('title', node_id),
                'betweenness': centrality,
            })

    return bridges


def format_connections(connections: dict) -> str:
    """Format connections for display."""
    lines = []

    lines.append(f"\n{'='*60}")
    lines.append(f"Connections for: {connections['title']}")
    lines.append(f"Note ID: {connections['note_id']}")
    lines.append('='*60)

    # Outgoing
    if connections['outgoing']:
        lines.append(f"\n-> OUTGOING ({len(connections['outgoing'])} notes this links to):")
        for conn in connections['outgoing']:
            type_marker = "[S]" if conn['type'] == 'semantic' else "[L]"
            weight = f" ({conn['weight']:.1%})" if conn['type'] == 'semantic' else ""
            lines.append(f"   {type_marker} {conn['title']}{weight}")

    # Incoming
    if connections['incoming']:
        lines.append(f"\n<- INCOMING ({len(connections['incoming'])} notes linking here):")
        for conn in connections['incoming']:
            type_marker = "[S]" if conn['type'] == 'semantic' else "[L]"
            weight = f" ({conn['weight']:.1%})" if conn['type'] == 'semantic' else ""
            lines.append(f"   {type_marker} {conn['title']}{weight}")

    # Semantic (top similar)
    if connections['semantic']:
        lines.append(f"\n~ SEMANTIC SIMILARITY ({len(connections['semantic'])} similar notes):")
        for conn in connections['semantic'][:10]:
            lines.append(f"   [{conn['similarity']:.1%}] {conn['title']}")

    # Paths (multi-hop)
    if connections['paths']:
        lines.append(f"\n... MULTI-HOP PATHS ({len(connections['paths'])} reachable notes):")
        sorted_paths = sorted(connections['paths'].items(), key=lambda x: x[1]['length'])
        for target_id, path_info in sorted_paths[:10]:
            path_str = " -> ".join(Path(p).stem for p in path_info['path'])
            lines.append(f"   [{path_info['length']} hops] {path_info['title']}")
            lines.append(f"      Path: {path_str}")

    lines.append(f"\n{'='*60}")
    lines.append("Legend: [L] = explicit link, [S] = semantic similarity")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Find connections for a note')
    parser.add_argument('query', nargs='?', help='Note name or path to search for')
    parser.add_argument('--depth', '-d', type=int, default=1,
                        help='Connection depth (default: 1)')
    parser.add_argument('--semantic-only', action='store_true',
                        help='Show only semantic connections')
    parser.add_argument('--explicit-only', action='store_true',
                        help='Show only explicit link connections')
    parser.add_argument('--stats', action='store_true',
                        help='Show graph statistics')
    parser.add_argument('--hubs', action='store_true',
                        help='Find hub notes (most connected)')
    parser.add_argument('--bridges', action='store_true',
                        help='Find bridge notes (connect communities)')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    G = load_graph()

    # Stats mode
    if args.stats:
        stats = get_graph_stats(G)
        if args.json:
            print(json.dumps(stats, indent=2, cls=NumpyEncoder))
        else:
            print("\nGraph Statistics:")
            print("="*40)
            print(f"Total notes:         {stats['total_nodes']}")
            print(f"Total edges:         {stats['total_edges']}")
            print(f"  - Explicit links:  {stats['explicit_edges']}")
            print(f"  - Semantic edges:  {stats['semantic_edges']}")
            print(f"Isolated notes:      {stats['isolated_nodes']}")
            print(f"Connected components:{stats['connected_components']}")
            print(f"Largest component:   {stats['largest_component']}")
            print(f"Average degree:      {stats['avg_degree']:.2f}")
        return

    # Hubs mode
    if args.hubs:
        hubs = find_hubs(G)
        if args.json:
            print(json.dumps(hubs, indent=2, cls=NumpyEncoder))
        else:
            print("\nHub Notes (Most Connected):")
            print("="*60)
            for hub in hubs:
                print(f"[{hub['total_degree']:3d}] {hub['title']}")
                print(f"      in: {hub['in_degree']}, out: {hub['out_degree']}")
        return

    # Bridges mode
    if args.bridges:
        bridges = find_bridges(G)
        if args.json:
            print(json.dumps(bridges, indent=2, cls=NumpyEncoder))
        else:
            print("\nBridge Notes (Connect Communities):")
            print("="*60)
            for bridge in bridges:
                print(f"[{bridge['betweenness']:.4f}] {bridge['title']}")
        return

    # Connection mode (requires query)
    if not args.query:
        parser.error("Query required unless using --stats, --hubs, or --bridges")

    note_id = find_note_id(G, args.query)
    if not note_id:
        print(f"Error: Note not found matching: {args.query}")
        print("\nTry searching with a different term or use --stats to see graph info.")
        sys.exit(1)

    include_semantic = not args.explicit_only
    include_explicit = not args.semantic_only

    connections = get_connections(
        G,
        note_id,
        depth=args.depth,
        include_semantic=include_semantic,
        include_explicit=include_explicit,
    )

    if args.json:
        print(json.dumps(connections, indent=2, cls=NumpyEncoder))
    else:
        print(format_connections(connections))


if __name__ == '__main__':
    main()
