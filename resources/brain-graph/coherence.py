"""
Brain Dependency Graph - Coherence Sweep & Report Generation

The coherence sweep walks the entire graph, computing staleness,
detecting lifecycle transitions, finding structural issues, and
generating a comprehensive report.
"""
from __future__ import annotations

import os
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import networkx as nx

from config import (
    get_propagation_config, get_lifecycle_config,
    REPORTS_DIR, BRAIN_PATH,
)
from models import (
    LifecycleTransition, StalenessResult, TensionRecord,
)
from propagation import compute_staleness, update_staleness_scores
from lifecycle import compute_all_lifecycles
from store import load_enriched_graph, load_enrichments, save_enrichments


def _find_recently_changed(
    G: nx.DiGraph,
    enrichments: dict,
    days: int = 7,
) -> list[str]:
    """Find notes modified in the last N days."""
    now = time.time()
    cutoff = now - (days * 86400)
    recent = []

    for note_id in G.nodes:
        node_data = G.nodes.get(note_id, {})
        filepath = node_data.get("filepath")
        if filepath and os.path.exists(filepath):
            mtime = os.path.getmtime(filepath)
            if mtime >= cutoff:
                recent.append(note_id)

    return recent


def _find_orphaned_nodes(G: nx.DiGraph, enrichments: dict) -> list[str]:
    """Find notes with no edges in the enriched graph."""
    orphans = []
    for note_id in G.nodes:
        if G.degree(note_id) == 0:
            orphans.append(note_id)
    return orphans


def _find_hub_overload(G: nx.DiGraph, threshold: int = 50) -> list[tuple[str, int]]:
    """Find notes with more edges than the hub threshold."""
    overloaded = []
    for note_id in G.nodes:
        degree = G.degree(note_id)
        if degree > threshold:
            overloaded.append((note_id, degree))
    overloaded.sort(key=lambda x: -x[1])
    return overloaded[:20]  # Top 20


def _find_cluster_gaps(G: nx.DiGraph, enrichments: dict) -> list[dict]:
    """Find groups of notes without a lens (MOC)."""
    nodes = enrichments.get("nodes", {})

    # Group insights by first vault path component
    clusters = defaultdict(list)
    lens_coverage = set()

    for note_id, ndata in nodes.items():
        layer = ndata.get("layer")
        if layer == "lens":
            # Track what this lens covers (its outbound edges)
            for _, dst in G.out_edges(note_id):
                parts = dst.split("/")
                if parts:
                    lens_coverage.add(parts[0])
        elif layer in ("insight", "framework"):
            parts = note_id.split("/")
            if parts:
                clusters[parts[0]].append(note_id)

    gaps = []
    for cluster_name, members in clusters.items():
        if cluster_name not in lens_coverage and len(members) >= 5:
            gaps.append({
                "cluster": cluster_name,
                "note_count": len(members),
                "sample_notes": [Path(m).stem for m in members[:3]],
            })

    gaps.sort(key=lambda x: -x["note_count"])
    return gaps


def coherence_sweep(
    propagation_days: int = 7,
    include_lifecycle: bool = True,
    include_tensions: bool = False,
) -> dict:
    """
    Run a full coherence sweep across the graph.

    Returns a report dict with:
    - staleness_alerts: notes above staleness threshold
    - lifecycle_transitions: notes that crossed phase boundaries
    - structural_health: orphans, hub overload, cluster gaps
    - tensions: (optional) new productive contradictions
    """
    print("=" * 60)
    print("BRAIN COHERENCE SWEEP")
    print("=" * 60)

    G, enrichments = load_enriched_graph()
    config = get_propagation_config()
    threshold = config["staleness_threshold"]

    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "graph_stats": {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "enriched_nodes": len(enrichments.get("nodes", {})),
            "enriched_edges": len(enrichments.get("edges", {})),
        },
        "staleness_alerts": [],
        "lifecycle_transitions": [],
        "structural_health": {},
        "tensions": [],
    }

    # 1. Staleness propagation from recently changed notes
    print(f"\n[1/4] Propagating staleness from changes in last {propagation_days} days...")
    recent = _find_recently_changed(G, enrichments, days=propagation_days)
    print(f"  Recently changed notes: {len(recent)}")

    all_stale = {}
    nodes_data = enrichments.get("nodes", {})

    for note_id in recent:
        # Only propagate from framework and insight notes
        node_layer = nodes_data.get(note_id, {}).get("layer", "")
        if node_layer not in ("framework", "insight", "signal"):
            continue

        result = compute_staleness(G, enrichments, note_id)
        above = result.above_threshold(threshold)
        for nid, score in above.items():
            if nid in all_stale:
                all_stale[nid] = max(all_stale[nid], score)
            else:
                all_stale[nid] = score

    # Update staleness in enrichments
    for nid, score in all_stale.items():
        if nid in nodes_data:
            nodes_data[nid]["staleness_score"] = score

    # Build alerts with context
    for nid, score in sorted(all_stale.items(), key=lambda x: -x[1]):
        node_enrichment = nodes_data.get(nid, {})
        alert = {
            "note_id": nid,
            "title": Path(nid).stem,
            "staleness_score": round(score, 3),
            "layer": node_enrichment.get("layer", "unknown"),
        }
        report["staleness_alerts"].append(alert)

    print(f"  Stale notes (>{threshold}): {len(report['staleness_alerts'])}")

    # 2. Lifecycle transitions
    if include_lifecycle:
        print("\n[2/4] Computing lifecycle scores...")
        transitions = compute_all_lifecycles(G, enrichments)
        for t in transitions:
            report["lifecycle_transitions"].append({
                "note_id": t.note_id,
                "title": Path(t.note_id).stem,
                "old_score": t.old_score,
                "new_score": t.new_score,
                "old_phase": t.old_phase,
                "new_phase": t.new_phase,
                "signals": t.signals,
            })
    else:
        print("\n[2/4] Lifecycle computation skipped.")

    # 3. Structural health
    print("\n[3/4] Checking structural health...")
    orphans = _find_orphaned_nodes(G, enrichments)
    hub_overload = _find_hub_overload(G)
    cluster_gaps = _find_cluster_gaps(G, enrichments)

    report["structural_health"] = {
        "orphaned_notes": len(orphans),
        "orphan_samples": [Path(o).stem for o in orphans[:10]],
        "hub_overload": [
            {"note": Path(n).stem, "degree": d} for n, d in hub_overload
        ],
        "cluster_gaps": cluster_gaps,
    }
    print(f"  Orphans: {len(orphans)}")
    print(f"  Overloaded hubs: {len(hub_overload)}")
    print(f"  Clusters without MOC: {len(cluster_gaps)}")

    # 4. Tensions (optional - expensive)
    if include_tensions:
        print("\n[4/4] Detecting tensions...")
        from tension import detect_tensions
        new_tensions = detect_tensions(enrichments)
        for t in new_tensions:
            report["tensions"].append(t.to_dict())
            enrichments.setdefault("tensions", []).append(t.to_dict())
    else:
        print("\n[4/4] Tension detection skipped (use --tensions to enable).")

    # Update sweep timestamp and save
    enrichments["last_coherence_sweep"] = datetime.now().isoformat()
    save_enrichments(enrichments)

    return report


def generate_report_markdown(report: dict) -> str:
    """Generate a markdown coherence report."""
    lines = []
    lines.append(f"# Brain Coherence Report - {report['date']}")
    lines.append("")

    stats = report["graph_stats"]
    lines.append(f"**Graph:** {stats['total_nodes']} nodes, {stats['total_edges']} edges")
    lines.append(f"**Enriched:** {stats['enriched_nodes']} nodes, {stats['enriched_edges']} edges")
    lines.append("")

    # Staleness alerts
    alerts = report["staleness_alerts"]
    lines.append(f"## Staleness Alerts ({len(alerts)} notes above threshold)")
    lines.append("")
    if alerts:
        lines.append("| # | Note | Layer | Staleness |")
        lines.append("|---|------|-------|-----------|")
        for i, alert in enumerate(alerts[:30], 1):
            lines.append(
                f"| {i} | {alert['title']} | {alert['layer']} | {alert['staleness_score']:.3f} |"
            )
        if len(alerts) > 30:
            lines.append(f"| ... | *{len(alerts) - 30} more* | | |")
    else:
        lines.append("No stale notes detected. The graph is coherent.")
    lines.append("")

    # Lifecycle transitions
    transitions = report["lifecycle_transitions"]
    lines.append(f"## Lifecycle Transitions ({len(transitions)} notes)")
    lines.append("")
    if transitions:
        for t in transitions:
            lines.append(f"### {t['title']}")
            lines.append(f"- **Score:** {t['old_score']:.3f} -> {t['new_score']:.3f}")
            lines.append(f"- **Phase:** {t['old_phase']} -> {t['new_phase']}")
            signals = t.get("signals", {})
            if signals:
                lines.append(f"- **Citations (30d):** {signals.get('citation_frequency', 0)}")
                lines.append(f"- **Generative ratio:** {signals.get('generative_ratio', 0)}")
                lines.append(f"- **Cross-domain reach:** {signals.get('cross_domain_reach', 0)}")
            lines.append("")
    else:
        lines.append("No lifecycle transitions detected.")
    lines.append("")

    # Structural health
    health = report["structural_health"]
    lines.append("## Structural Health")
    lines.append("")
    lines.append(f"- **Orphaned notes:** {health.get('orphaned_notes', 0)}")
    if health.get("orphan_samples"):
        lines.append(f"  - Samples: {', '.join(health['orphan_samples'][:5])}")

    lines.append(f"- **Overloaded hubs:** {len(health.get('hub_overload', []))}")
    for hub in health.get("hub_overload", [])[:5]:
        lines.append(f"  - {hub['note']} ({hub['degree']} edges)")

    lines.append(f"- **Clusters without MOC:** {len(health.get('cluster_gaps', []))}")
    for gap in health.get("cluster_gaps", [])[:5]:
        lines.append(f"  - {gap['cluster']} ({gap['note_count']} notes)")
    lines.append("")

    # Tensions
    tensions = report.get("tensions", [])
    if tensions:
        lines.append(f"## Productive Tensions ({len(tensions)} new)")
        lines.append("")
        for t in tensions:
            a_name = Path(t["note_a"]).stem
            b_name = Path(t["note_b"]).stem
            lines.append(f"- **{a_name}** <-> **{b_name}**")
            lines.append(f"  - {t.get('description', '')}")
        lines.append("")

    lines.append("---")
    lines.append(f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by Brain Dependency Graph coherence engine.*")

    return "\n".join(lines)


def save_report(report: dict) -> Path:
    """Save the coherence report as markdown."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = REPORTS_DIR / f"coherence-report-{report['date']}.md"
    content = generate_report_markdown(report)
    filepath.write_text(content)
    return filepath
