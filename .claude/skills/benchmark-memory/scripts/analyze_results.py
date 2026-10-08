#!/usr/bin/env python3
"""
Analyze benchmark results and generate summary reports.

Usage:
    python analyze_results.py --results ../results/benchmark-*.csv
    python analyze_results.py --results ../results/benchmark-*.csv --output ../analysis/report.md

Generates:
- Summary by configuration
- Summary by query category
- Best config per intent
- Recommendations
"""
import argparse
import csv
import glob
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
RESULTS_DIR = SKILL_DIR / "results"
ANALYSIS_DIR = SKILL_DIR / "analysis"


def load_results(pattern: str) -> list[dict]:
    """Load results from one or more CSV files.

    Args:
        pattern: Glob pattern for result files

    Returns:
        List of result dicts
    """
    results = []

    files = glob.glob(pattern)
    if not files:
        # Try relative to results dir
        files = glob.glob(str(RESULTS_DIR / pattern))

    if not files:
        raise FileNotFoundError(f"No files matching: {pattern}")

    for filepath in files:
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for key in ["latency_ms", "precision_at_5", "precision_at_10",
                           "mrr", "ndcg_at_10", "avg_score", "iterations"]:
                    if key in row and row[key]:
                        try:
                            row[key] = float(row[key])
                        except ValueError:
                            pass

                # Convert boolean
                if "converged" in row:
                    row["converged"] = row["converged"].lower() == "true"

                results.append(row)

    return results


def aggregate_by_config(results: list[dict]) -> dict:
    """Aggregate metrics by configuration.

    Args:
        results: List of result dicts

    Returns:
        Dict mapping config_name -> aggregated metrics
    """
    by_config = defaultdict(list)

    for r in results:
        config = r.get("config_name", "unknown")
        by_config[config].append(r)

    aggregated = {}
    for config, config_results in by_config.items():
        metrics = defaultdict(list)

        for r in config_results:
            for key in ["precision_at_5", "precision_at_10", "mrr",
                       "ndcg_at_10", "avg_score", "latency_ms"]:
                if key in r and isinstance(r[key], (int, float)):
                    metrics[key].append(r[key])

        aggregated[config] = {
            "n_queries": len(config_results),
            **{f"{k}_mean": np.mean(v) for k, v in metrics.items() if v},
            **{f"{k}_std": np.std(v) for k, v in metrics.items() if v},
        }

    return aggregated


def aggregate_by_category(results: list[dict]) -> dict:
    """Aggregate metrics by query category.

    Args:
        results: List of result dicts

    Returns:
        Dict mapping category -> aggregated metrics
    """
    by_category = defaultdict(list)

    for r in results:
        category = r.get("query_category", "unknown")
        by_category[category].append(r)

    aggregated = {}
    for category, category_results in by_category.items():
        metrics = defaultdict(list)

        for r in category_results:
            for key in ["precision_at_5", "precision_at_10", "mrr",
                       "ndcg_at_10", "avg_score", "latency_ms"]:
                if key in r and isinstance(r[key], (int, float)):
                    metrics[key].append(r[key])

        aggregated[category] = {
            "n_queries": len(category_results),
            **{f"{k}_mean": np.mean(v) for k, v in metrics.items() if v},
            **{f"{k}_std": np.std(v) for k, v in metrics.items() if v},
        }

    return aggregated


def aggregate_by_config_and_category(results: list[dict]) -> dict:
    """Aggregate metrics by configuration AND category.

    Args:
        results: List of result dicts

    Returns:
        Dict mapping (config, category) -> aggregated metrics
    """
    by_pair = defaultdict(list)

    for r in results:
        config = r.get("config_name", "unknown")
        category = r.get("query_category", "unknown")
        by_pair[(config, category)].append(r)

    aggregated = {}
    for (config, category), pair_results in by_pair.items():
        metrics = defaultdict(list)

        for r in pair_results:
            for key in ["precision_at_5", "precision_at_10", "mrr",
                       "ndcg_at_10", "avg_score", "latency_ms"]:
                if key in r and isinstance(r[key], (int, float)):
                    metrics[key].append(r[key])

        aggregated[(config, category)] = {
            "n_queries": len(pair_results),
            **{f"{k}_mean": np.mean(v) for k, v in metrics.items() if v},
            **{f"{k}_std": np.std(v) for k, v in metrics.items() if v},
        }

    return aggregated


def find_best_configs(
    by_config_category: dict,
    metric: str = "precision_at_5_mean",
) -> dict:
    """Find the best configuration for each category.

    Args:
        by_config_category: Aggregated metrics by (config, category)
        metric: Metric to optimize

    Returns:
        Dict mapping category -> best config info
    """
    # Group by category
    by_category = defaultdict(list)
    for (config, category), metrics in by_config_category.items():
        by_category[category].append((config, metrics))

    best = {}
    for category, configs in by_category.items():
        # Sort by metric (descending)
        sorted_configs = sorted(
            configs,
            key=lambda x: x[1].get(metric, 0),
            reverse=True,
        )

        if sorted_configs:
            best_config, best_metrics = sorted_configs[0]
            best[category] = {
                "config": best_config,
                "metric": metric,
                "value": best_metrics.get(metric, 0),
                "all_metrics": best_metrics,
            }

    return best


def compare_static_vs_spreading(results: list[dict]) -> dict:
    """Compare static vs spreading search modes.

    Args:
        results: List of result dicts

    Returns:
        Comparison dict
    """
    static_results = [r for r in results if r.get("mode") == "static"]
    spreading_results = [r for r in results if r.get("mode") == "spreading"]

    def avg_metric(results_list, metric):
        values = [r[metric] for r in results_list
                 if metric in r and isinstance(r[metric], (int, float))]
        return np.mean(values) if values else 0

    comparison = {
        "static": {
            "n_queries": len(static_results),
            "precision_at_5": avg_metric(static_results, "precision_at_5"),
            "precision_at_10": avg_metric(static_results, "precision_at_10"),
            "mrr": avg_metric(static_results, "mrr"),
            "ndcg_at_10": avg_metric(static_results, "ndcg_at_10"),
            "avg_score": avg_metric(static_results, "avg_score"),
            "latency_ms": avg_metric(static_results, "latency_ms"),
        },
        "spreading": {
            "n_queries": len(spreading_results),
            "precision_at_5": avg_metric(spreading_results, "precision_at_5"),
            "precision_at_10": avg_metric(spreading_results, "precision_at_10"),
            "mrr": avg_metric(spreading_results, "mrr"),
            "ndcg_at_10": avg_metric(spreading_results, "ndcg_at_10"),
            "avg_score": avg_metric(spreading_results, "avg_score"),
            "latency_ms": avg_metric(spreading_results, "latency_ms"),
        },
    }

    # Compute improvement percentages
    if comparison["static"]["precision_at_5"] > 0:
        comparison["improvement"] = {
            metric: ((comparison["spreading"][metric] - comparison["static"][metric])
                    / comparison["static"][metric] * 100)
            for metric in ["precision_at_5", "precision_at_10", "mrr", "ndcg_at_10", "avg_score"]
            if comparison["static"][metric] > 0
        }

    return comparison


def generate_report(results: list[dict], output_path: Optional[Path] = None) -> str:
    """Generate a comprehensive analysis report.

    Args:
        results: List of result dicts
        output_path: Optional path to save report

    Returns:
        Report as markdown string
    """
    by_config = aggregate_by_config(results)
    by_category = aggregate_by_category(results)
    by_config_category = aggregate_by_config_and_category(results)
    best_configs = find_best_configs(by_config_category)
    mode_comparison = compare_static_vs_spreading(results)

    lines = [
        "# Benchmark Analysis Report",
        f"\n**Generated:** {datetime.now().isoformat()}",
        f"**Total results:** {len(results)}",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
    ]

    # Mode comparison summary
    if mode_comparison.get("improvement"):
        imp = mode_comparison["improvement"]
        lines.append("### Static vs Spreading Comparison")
        lines.append("")
        lines.append("| Metric | Static | Spreading | Improvement |")
        lines.append("|--------|--------|-----------|-------------|")
        for metric in ["precision_at_5", "precision_at_10", "mrr", "ndcg_at_10", "avg_score"]:
            static_val = mode_comparison["static"].get(metric, 0)
            spread_val = mode_comparison["spreading"].get(metric, 0)
            imp_val = imp.get(metric, 0)
            lines.append(f"| {metric} | {static_val:.3f} | {spread_val:.3f} | {imp_val:+.1f}% |")
        lines.append("")

    # Best configs per category
    lines.append("### Best Configuration per Category")
    lines.append("")
    lines.append("| Category | Best Config | Precision@5 | MRR | NDCG@10 |")
    lines.append("|----------|-------------|-------------|-----|---------|")
    for category, info in sorted(best_configs.items()):
        config = info["config"]
        metrics = info["all_metrics"]
        lines.append(
            f"| {category} | {config} | "
            f"{metrics.get('precision_at_5_mean', 0):.3f} | "
            f"{metrics.get('mrr_mean', 0):.3f} | "
            f"{metrics.get('ndcg_at_10_mean', 0):.3f} |"
        )
    lines.append("")

    # Config rankings
    lines.append("---")
    lines.append("")
    lines.append("## 2. Configuration Rankings")
    lines.append("")
    lines.append("### By Precision@5 (higher is better)")
    lines.append("")
    lines.append("| Rank | Config | P@5 | P@10 | MRR | NDCG | Avg Score | Latency |")
    lines.append("|------|--------|-----|------|-----|------|-----------|---------|")

    sorted_configs = sorted(
        by_config.items(),
        key=lambda x: x[1].get("precision_at_5_mean", 0),
        reverse=True,
    )

    for i, (config, metrics) in enumerate(sorted_configs, 1):
        lines.append(
            f"| {i} | {config} | "
            f"{metrics.get('precision_at_5_mean', 0):.3f} | "
            f"{metrics.get('precision_at_10_mean', 0):.3f} | "
            f"{metrics.get('mrr_mean', 0):.3f} | "
            f"{metrics.get('ndcg_at_10_mean', 0):.3f} | "
            f"{metrics.get('avg_score_mean', 0):.2f} | "
            f"{metrics.get('latency_ms_mean', 0):.0f}ms |"
        )
    lines.append("")

    # Category analysis
    lines.append("---")
    lines.append("")
    lines.append("## 3. Query Category Analysis")
    lines.append("")
    lines.append("| Category | N | P@5 | P@10 | MRR | NDCG | Avg Score |")
    lines.append("|----------|---|-----|------|-----|------|-----------|")

    for category, metrics in sorted(by_category.items()):
        lines.append(
            f"| {category} | {metrics['n_queries']} | "
            f"{metrics.get('precision_at_5_mean', 0):.3f} | "
            f"{metrics.get('precision_at_10_mean', 0):.3f} | "
            f"{metrics.get('mrr_mean', 0):.3f} | "
            f"{metrics.get('ndcg_at_10_mean', 0):.3f} | "
            f"{metrics.get('avg_score_mean', 0):.2f} |"
        )
    lines.append("")

    # Recommendations
    lines.append("---")
    lines.append("")
    lines.append("## 4. Recommendations")
    lines.append("")

    # Generate recommendations based on findings
    if mode_comparison.get("improvement"):
        if mode_comparison["improvement"].get("precision_at_5", 0) > 5:
            lines.append("- **Spreading outperforms static**: Use spreading mode as default")
        elif mode_comparison["improvement"].get("precision_at_5", 0) < -5:
            lines.append("- **Static outperforms spreading**: Consider using static mode")
        else:
            lines.append("- **Modes perform similarly**: Choose based on latency requirements")
        lines.append("")

    # Per-category recommendations
    lines.append("### Intent-Specific Configurations")
    lines.append("")
    for category, info in sorted(best_configs.items()):
        lines.append(f"- **{category}**: Use `{info['config']}`")
    lines.append("")

    # Key insights
    lines.append("### Key Insights")
    lines.append("")

    # Find categories where synthesis_optimized does best
    synthesis_best = [cat for cat, info in best_configs.items()
                     if "synthesis" in info["config"]]
    if synthesis_best:
        lines.append(f"- Synthesis-optimized config excels at: {', '.join(synthesis_best)}")

    factual_best = [cat for cat, info in best_configs.items()
                   if "factual" in info["config"]]
    if factual_best:
        lines.append(f"- Factual-optimized config excels at: {', '.join(factual_best)}")

    lines.append("")

    report = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
        print(f"Report saved to: {output_path}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Analyze benchmark results and generate reports"
    )
    parser.add_argument(
        "--results",
        required=True,
        help="Glob pattern for result CSV files",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output path for report (markdown)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Print only high-level summary",
    )

    args = parser.parse_args()

    # Load results
    try:
        results = load_results(args.results)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Loaded {len(results)} results")

    if args.summary_only:
        by_config = aggregate_by_config(results)
        mode_comparison = compare_static_vs_spreading(results)

        print("\n=== Quick Summary ===\n")
        print("Top 5 Configurations by Precision@5:")
        sorted_configs = sorted(
            by_config.items(),
            key=lambda x: x[1].get("precision_at_5_mean", 0),
            reverse=True,
        )[:5]
        for i, (config, metrics) in enumerate(sorted_configs, 1):
            print(f"  {i}. {config}: {metrics.get('precision_at_5_mean', 0):.3f}")

        if mode_comparison.get("improvement"):
            print("\nMode Comparison:")
            print(f"  Static P@5: {mode_comparison['static']['precision_at_5']:.3f}")
            print(f"  Spreading P@5: {mode_comparison['spreading']['precision_at_5']:.3f}")
            print(f"  Improvement: {mode_comparison['improvement'].get('precision_at_5', 0):+.1f}%")
        return

    if args.format == "json":
        output = {
            "by_config": aggregate_by_config(results),
            "by_category": aggregate_by_category(results),
            "best_per_category": find_best_configs(aggregate_by_config_and_category(results)),
            "mode_comparison": compare_static_vs_spreading(results),
        }
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w") as f:
                json.dump(output, f, indent=2, default=str)
            print(f"JSON saved to: {args.output}")
        else:
            print(json.dumps(output, indent=2, default=str))
    else:
        output_path = args.output
        if not output_path:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_path = ANALYSIS_DIR / f"report-{timestamp}.md"

        report = generate_report(results, output_path)
        if not args.output:
            print(report)


if __name__ == "__main__":
    main()
