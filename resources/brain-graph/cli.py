#!/usr/bin/env python3
"""
Brain Dependency Graph - CLI

Usage:
    python cli.py bootstrap [--force]     Classify all nodes and type all edges
    python cli.py status                  Show enrichment statistics
    python cli.py inspect <note>          Show single note's graph context
    python cli.py propagate <note>        Compute staleness cascade from a changed note
    python cli.py lifecycle               Compute lifecycle scores for all notes
    python cli.py tensions                Detect productive contradictions
    python cli.py coherence [--tensions]  Full coherence sweep with report
    python cli.py coherence --json        JSON output instead of markdown
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def cmd_bootstrap(args):
    from classify import bootstrap
    bootstrap(force=args.force)


def cmd_status(args):
    from store import load_enrichments, load_lbs_graph
    from models import LifecycleTransition

    enrichments = load_enrichments()

    if not enrichments.get("last_bootstrap"):
        print("Graph not yet bootstrapped. Run: python cli.py bootstrap")
        return

    nodes = enrichments.get("nodes", {})
    edges = enrichments.get("edges", {})
    tensions = enrichments.get("tensions", [])

    # Layer distribution
    layer_counts = {}
    lifecycle_dist = {"reflective": 0, "crystallizing": 0, "generative": 0}

    for nid, ndata in nodes.items():
        layer = ndata.get("layer", "unknown")
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
        lc = ndata.get("lifecycle", 0.0)
        phase = LifecycleTransition.phase_name(lc)
        lifecycle_dist[phase] += 1

    # Edge type distribution
    edge_type_counts = {}
    for ekey, edata in edges.items():
        et = edata.get("edge_type", "unknown")
        edge_type_counts[et] = edge_type_counts.get(et, 0) + 1

    # Stale notes
    stale_count = sum(1 for n in nodes.values() if n.get("staleness_score", 0) >= 0.3)

    if args.json:
        print(json.dumps({
            "last_bootstrap": enrichments.get("last_bootstrap"),
            "last_coherence_sweep": enrichments.get("last_coherence_sweep"),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "tension_count": len(tensions),
            "stale_count": stale_count,
            "layers": layer_counts,
            "lifecycle_phases": lifecycle_dist,
            "edge_types": edge_type_counts,
        }, indent=2, cls=NumpyEncoder))
        return

    print("Brain Dependency Graph - Status")
    print("=" * 50)
    print(f"  Last bootstrap:       {enrichments.get('last_bootstrap', 'never')}")
    print(f"  Last coherence sweep: {enrichments.get('last_coherence_sweep', 'never')}")
    print(f"  Nodes enriched:       {len(nodes)}")
    print(f"  Edges typed:          {len(edges)}")
    print(f"  Tensions tracked:     {len(tensions)}")
    print(f"  Stale notes (>0.3):   {stale_count}")
    print()

    print("Layer Distribution:")
    for layer in ("signal", "impression", "insight", "framework", "lens", "synthesis", "index"):
        count = layer_counts.get(layer, 0)
        print(f"  {layer:12s}: {count:5d}")
    print()

    print("Lifecycle Phases:")
    for phase in ("reflective", "crystallizing", "generative"):
        count = lifecycle_dist.get(phase, 0)
        print(f"  {phase:14s}: {count:5d}")
    print()

    print("Edge Types:")
    for et in ("derives-from", "instantiates", "references", "associates", "tension", "supersedes"):
        count = edge_type_counts.get(et, 0)
        print(f"  {et:15s}: {count:6d}")


def cmd_inspect(args):
    from store import load_enriched_graph, load_enrichments, find_note_id
    from models import LifecycleTransition

    G, enrichments = load_enriched_graph()
    note_id = find_note_id(G, args.note)

    if not note_id:
        print(f"Note not found: {args.note}", file=sys.stderr)
        sys.exit(1)

    nodes = enrichments.get("nodes", {})
    edges = enrichments.get("edges", {})
    node_data = nodes.get(note_id, {})

    lifecycle = node_data.get("lifecycle", 0.0)
    phase = LifecycleTransition.phase_name(lifecycle)

    info = {
        "note_id": note_id,
        "title": G.nodes[note_id].get("title", Path(note_id).stem),
        "layer": node_data.get("layer", "unclassified"),
        "lifecycle": lifecycle,
        "phase": phase,
        "staleness_score": node_data.get("staleness_score", 0.0),
        "classification_confidence": node_data.get("classification_confidence", 0.0),
        "in_degree": G.in_degree(note_id),
        "out_degree": G.out_degree(note_id),
        "outbound_edges": [],
        "inbound_edges": [],
    }

    # Outbound edges
    for _, dst in G.out_edges(note_id):
        edge_key = f"{note_id}||{dst}"
        edata = edges.get(edge_key, {})
        info["outbound_edges"].append({
            "target": Path(dst).stem,
            "edge_type": edata.get("edge_type", "unknown"),
            "authority": edata.get("authority", "none"),
        })

    # Inbound edges
    for src, _ in G.in_edges(note_id):
        edge_key = f"{src}||{note_id}"
        edata = edges.get(edge_key, {})
        info["inbound_edges"].append({
            "source": Path(src).stem,
            "edge_type": edata.get("edge_type", "unknown"),
            "authority": edata.get("authority", "none"),
        })

    # Sort by edge type
    info["outbound_edges"].sort(key=lambda x: x["edge_type"])
    info["inbound_edges"].sort(key=lambda x: x["edge_type"])

    if args.json:
        print(json.dumps(info, indent=2, cls=NumpyEncoder))
        return

    print(f"Note: {info['title']}")
    print(f"  ID:         {info['note_id']}")
    print(f"  Layer:      {info['layer']} (confidence: {info['classification_confidence']:.2f})")
    print(f"  Lifecycle:  {info['lifecycle']:.3f} ({info['phase']})")
    print(f"  Staleness:  {info['staleness_score']:.3f}")
    print(f"  In-degree:  {info['in_degree']}")
    print(f"  Out-degree: {info['out_degree']}")
    print()

    print(f"Outbound Edges ({len(info['outbound_edges'])}):")
    for e in info["outbound_edges"][:20]:
        print(f"  -> {e['target'][:40]:40s}  [{e['edge_type']:15s}]  auth={e['authority']}")
    if len(info["outbound_edges"]) > 20:
        print(f"  ... and {len(info['outbound_edges']) - 20} more")
    print()

    print(f"Inbound Edges ({len(info['inbound_edges'])}):")
    for e in info["inbound_edges"][:20]:
        print(f"  <- {e['source'][:40]:40s}  [{e['edge_type']:15s}]  auth={e['authority']}")
    if len(info["inbound_edges"]) > 20:
        print(f"  ... and {len(info['inbound_edges']) - 20} more")


def cmd_propagate(args):
    from store import load_enriched_graph, load_enrichments, save_enrichments, find_note_id
    from propagation import compute_staleness, update_staleness_scores
    from config import get_propagation_config

    G, enrichments = load_enriched_graph()
    note_id = find_note_id(G, args.note)

    if not note_id:
        print(f"Note not found: {args.note}", file=sys.stderr)
        sys.exit(1)

    config = get_propagation_config()
    result = compute_staleness(
        G, enrichments, note_id,
        change_magnitude=args.magnitude,
    )

    above = result.above_threshold(config["staleness_threshold"])
    update_staleness_scores(enrichments, result, config["staleness_threshold"])
    save_enrichments(enrichments)

    if args.json:
        print(json.dumps({
            "changed_note": note_id,
            "change_magnitude": result.change_magnitude,
            "total_examined": result.total_examined,
            "above_threshold": len(above),
            "affected_notes": [
                {"note_id": nid, "title": Path(nid).stem, "staleness": round(s, 3)}
                for nid, s in above.items()
            ],
        }, indent=2, cls=NumpyEncoder))
        return

    print(f"Staleness Propagation from: {Path(note_id).stem}")
    print(f"  Change magnitude: {result.change_magnitude}")
    print(f"  Notes examined:   {result.total_examined}")
    print(f"  Above threshold:  {len(above)}")
    print()

    if above:
        print(f"Affected Notes (staleness > {config['staleness_threshold']}):")
        print(f"{'#':>3}  {'Note':40s}  {'Staleness':>10}")
        print("-" * 57)
        for i, (nid, score) in enumerate(above.items(), 1):
            print(f"{i:3d}  {Path(nid).stem[:40]:40s}  {score:10.3f}")
    else:
        print("No notes above staleness threshold.")


def cmd_lifecycle(args):
    from store import load_enriched_graph, load_enrichments, save_enrichments
    from lifecycle import compute_all_lifecycles

    G, enrichments = load_enriched_graph()
    transitions = compute_all_lifecycles(G, enrichments)
    save_enrichments(enrichments)

    if args.json:
        print(json.dumps({
            "transitions": [
                {
                    "note_id": t.note_id,
                    "title": Path(t.note_id).stem,
                    "old_score": t.old_score,
                    "new_score": t.new_score,
                    "old_phase": t.old_phase,
                    "new_phase": t.new_phase,
                }
                for t in transitions
            ],
        }, indent=2, cls=NumpyEncoder))
        return

    if transitions:
        print(f"Lifecycle Transitions ({len(transitions)}):")
        print()
        for t in transitions:
            title = Path(t.note_id).stem
            print(f"  {title}")
            print(f"    {t.old_score:.3f} ({t.old_phase}) -> {t.new_score:.3f} ({t.new_phase})")
            print()
    else:
        print("No lifecycle transitions detected.")


def cmd_tensions(args):
    from store import load_enrichments, save_enrichments
    from tension import detect_tensions

    enrichments = load_enrichments()
    new_tensions = detect_tensions(
        enrichments,
        similarity_threshold=args.similarity,
        divergence_threshold=args.divergence,
    )

    # Save new tensions
    for t in new_tensions:
        enrichments.setdefault("tensions", []).append(t.to_dict())
    save_enrichments(enrichments)

    if args.json:
        print(json.dumps({
            "new_tensions": [t.to_dict() for t in new_tensions],
            "total_tensions": len(enrichments.get("tensions", [])),
        }, indent=2, cls=NumpyEncoder))
        return

    if new_tensions:
        print(f"New Tensions Found ({len(new_tensions)}):")
        print()
        for t in new_tensions:
            a = Path(t.note_a).stem
            b = Path(t.note_b).stem
            print(f"  {a}")
            print(f"    <-> {b}")
            print(f"    Similarity: {t.similarity:.3f}, {t.description}")
            print()
    else:
        print("No new tensions detected.")

    print(f"Total tensions tracked: {len(enrichments.get('tensions', []))}")


def cmd_coherence(args):
    from coherence import coherence_sweep, save_report, generate_report_markdown

    report = coherence_sweep(
        propagation_days=args.days,
        include_lifecycle=not args.no_lifecycle,
        include_tensions=args.tensions,
    )

    if args.json:
        print(json.dumps(report, indent=2, cls=NumpyEncoder))
        return

    # Save and display report
    filepath = save_report(report)
    print(f"\n{'=' * 60}")
    print(generate_report_markdown(report))
    print(f"\nReport saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Brain Dependency Graph - Coherence Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # bootstrap
    p_bootstrap = subparsers.add_parser("bootstrap", help="Classify all nodes and type all edges")
    p_bootstrap.add_argument("--force", action="store_true", help="Re-bootstrap even if already done")

    # status
    p_status = subparsers.add_parser("status", help="Show enrichment statistics")
    p_status.add_argument("--json", action="store_true", help="JSON output")

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Show single note's graph context")
    p_inspect.add_argument("note", help="Note name or path")
    p_inspect.add_argument("--json", action="store_true", help="JSON output")

    # propagate
    p_propagate = subparsers.add_parser("propagate", help="Compute staleness from a changed note")
    p_propagate.add_argument("note", help="Note name or path")
    p_propagate.add_argument("--magnitude", type=float, default=1.0, help="Change magnitude (0-1)")
    p_propagate.add_argument("--json", action="store_true", help="JSON output")

    # lifecycle
    p_lifecycle = subparsers.add_parser("lifecycle", help="Compute lifecycle scores")
    p_lifecycle.add_argument("--json", action="store_true", help="JSON output")

    # tensions
    p_tensions = subparsers.add_parser("tensions", help="Detect productive contradictions")
    p_tensions.add_argument("--similarity", type=float, default=0.75, help="Similarity threshold")
    p_tensions.add_argument("--divergence", type=float, default=0.3, help="Divergence threshold")
    p_tensions.add_argument("--json", action="store_true", help="JSON output")

    # coherence
    p_coherence = subparsers.add_parser("coherence", help="Full coherence sweep with report")
    p_coherence.add_argument("--days", type=int, default=7, help="Look back N days for changes")
    p_coherence.add_argument("--tensions", action="store_true", help="Include tension detection")
    p_coherence.add_argument("--no-lifecycle", action="store_true", help="Skip lifecycle computation")
    p_coherence.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "bootstrap": cmd_bootstrap,
        "status": cmd_status,
        "inspect": cmd_inspect,
        "propagate": cmd_propagate,
        "lifecycle": cmd_lifecycle,
        "tensions": cmd_tensions,
        "coherence": cmd_coherence,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
