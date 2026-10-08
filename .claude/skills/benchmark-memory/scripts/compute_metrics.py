#!/usr/bin/env python3
"""
Compute evaluation metrics from benchmark results.

Usage:
    python compute_metrics.py --results scored_results.json
    python compute_metrics.py --results scored_results.json --k 5

Metrics computed:
- Precision@K: Fraction of results that are relevant
- Recall@K: Fraction of relevant notes found (if ground truth available)
- MRR: Mean Reciprocal Rank
- NDCG@K: Normalized Discounted Cumulative Gain
- Avg Score: Average LLM relevance score
"""
import argparse
import json
import math
import sys
from pathlib import Path
from typing import Optional

import numpy as np


def compute_precision_at_k(scores: list[int], k: int, relevance_threshold: int = 2) -> float:
    """Compute Precision@K.

    Args:
        scores: List of relevance scores (0-3)
        k: Number of results to consider
        relevance_threshold: Minimum score to be considered relevant

    Returns:
        Precision value (0-1)
    """
    if k == 0:
        return 0.0

    scores_at_k = scores[:k]
    relevant = sum(1 for s in scores_at_k if s >= relevance_threshold)
    return relevant / k


def compute_recall_at_k(
    results: list[str],
    ground_truth: list[str],
    k: int,
) -> Optional[float]:
    """Compute Recall@K.

    Args:
        results: List of retrieved note IDs
        ground_truth: List of known relevant note IDs
        k: Number of results to consider

    Returns:
        Recall value (0-1), or None if no ground truth
    """
    if not ground_truth:
        return None

    results_at_k = set(results[:k])
    ground_truth_set = set(ground_truth)

    found = len(results_at_k & ground_truth_set)
    return found / len(ground_truth_set)


def compute_mrr(scores: list[int], relevance_threshold: int = 2) -> float:
    """Compute Mean Reciprocal Rank.

    Args:
        scores: List of relevance scores (0-3)
        relevance_threshold: Minimum score to be considered relevant

    Returns:
        MRR value (0-1)
    """
    for i, score in enumerate(scores):
        if score >= relevance_threshold:
            return 1.0 / (i + 1)
    return 0.0


def compute_ndcg_at_k(scores: list[int], k: int) -> float:
    """Compute Normalized Discounted Cumulative Gain @K.

    Args:
        scores: List of relevance scores (0-3)
        k: Number of results to consider

    Returns:
        NDCG value (0-1)
    """
    scores_at_k = scores[:k]

    if not scores_at_k or max(scores_at_k) == 0:
        return 0.0

    # DCG
    dcg = sum(
        score / math.log2(i + 2)  # log2(rank + 1), rank is 1-indexed
        for i, score in enumerate(scores_at_k)
    )

    # Ideal DCG (sorted scores)
    ideal_scores = sorted(scores_at_k, reverse=True)
    idcg = sum(
        score / math.log2(i + 2)
        for i, score in enumerate(ideal_scores)
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg


def compute_avg_score(scores: list[int]) -> float:
    """Compute average relevance score.

    Args:
        scores: List of relevance scores (0-3)

    Returns:
        Average score
    """
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def compute_diversity(results: list[dict], k: int) -> float:
    """Compute diversity score based on unique note titles/paths.

    This is a simple measure - counts unique notes in top K.

    Args:
        results: List of result dicts with 'filepath' or 'note_id'
        k: Number of results to consider

    Returns:
        Diversity ratio (unique / k)
    """
    results_at_k = results[:k]
    unique_notes = set()

    for r in results_at_k:
        # Extract note identity (use filepath stem or note_id)
        note_id = r.get("note_id") or r.get("filepath", "")
        if "/" in note_id:
            note_id = note_id.rsplit("/", 1)[-1]
        if note_id.endswith(".md"):
            note_id = note_id[:-3]
        unique_notes.add(note_id)

    return len(unique_notes) / k if k > 0 else 0.0


def compute_all_metrics(
    results: list[dict],
    scores: list[int],
    ground_truth: Optional[list[str]] = None,
    k_values: list[int] = [5, 10],
) -> dict:
    """Compute all metrics for a single query.

    Args:
        results: List of result dicts
        scores: List of relevance scores (0-3)
        ground_truth: Optional list of known relevant note IDs
        k_values: List of K values to compute metrics at

    Returns:
        Dict with all computed metrics
    """
    metrics = {}

    # MRR (doesn't depend on K)
    metrics["mrr"] = compute_mrr(scores)

    # Average score
    metrics["avg_score"] = compute_avg_score(scores)

    # Per-K metrics
    for k in k_values:
        metrics[f"precision_at_{k}"] = compute_precision_at_k(scores, k)
        metrics[f"ndcg_at_{k}"] = compute_ndcg_at_k(scores, k)
        metrics[f"diversity_at_{k}"] = compute_diversity(results, k)

        if ground_truth:
            result_ids = [r.get("note_id") or r.get("filepath", "") for r in results]
            metrics[f"recall_at_{k}"] = compute_recall_at_k(result_ids, ground_truth, k)

    return metrics


def aggregate_metrics(all_metrics: list[dict]) -> dict:
    """Aggregate metrics across multiple queries.

    Args:
        all_metrics: List of per-query metric dicts

    Returns:
        Dict with mean and std for each metric
    """
    if not all_metrics:
        return {}

    # Collect all metric names
    metric_names = set()
    for m in all_metrics:
        metric_names.update(m.keys())

    aggregated = {}
    for name in metric_names:
        values = [m[name] for m in all_metrics if name in m and m[name] is not None]
        if values:
            aggregated[f"{name}_mean"] = np.mean(values)
            aggregated[f"{name}_std"] = np.std(values)
            aggregated[f"{name}_min"] = np.min(values)
            aggregated[f"{name}_max"] = np.max(values)

    return aggregated


def format_metrics_table(metrics: dict, title: str = "Metrics") -> str:
    """Format metrics as a readable table.

    Args:
        metrics: Dict of metric_name -> value

    Returns:
        Formatted string
    """
    lines = [f"\n=== {title} ===\n"]

    # Group by base metric name
    base_metrics = {}
    for name, value in sorted(metrics.items()):
        # Skip None values
        if value is None:
            continue

        # Format value
        if isinstance(value, float):
            value_str = f"{value:.4f}"
        else:
            value_str = str(value)

        lines.append(f"  {name}: {value_str}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Compute evaluation metrics from benchmark results"
    )
    parser.add_argument(
        "--results",
        type=Path,
        required=True,
        help="Scored results file (JSON)",
    )
    parser.add_argument(
        "--k",
        type=int,
        nargs="+",
        default=[5, 10],
        help="K values for metrics (default: 5 10)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file for metrics",
    )
    parser.add_argument(
        "--format",
        choices=["json", "table"],
        default="table",
        help="Output format",
    )

    args = parser.parse_args()

    # Load results
    with open(args.results) as f:
        data = json.load(f)

    # Check if it's a single query result or multiple
    if isinstance(data, list):
        # Multiple results - need to group by query
        # Assuming format: list of {query, note_title, note_content, score, ...}
        from collections import defaultdict

        by_query = defaultdict(list)
        for item in data:
            query_id = item.get("query_id") or item.get("query", "")[:50]
            by_query[query_id].append(item)

        all_metrics = []
        for query_id, query_results in by_query.items():
            scores = [r.get("score", 0) for r in query_results]
            ground_truth = query_results[0].get("ground_truth_notes") if query_results else None
            metrics = compute_all_metrics(query_results, scores, ground_truth, args.k)
            metrics["query_id"] = query_id
            all_metrics.append(metrics)

        # Aggregate
        aggregated = aggregate_metrics(all_metrics)

        if args.format == "json":
            output = {
                "per_query": all_metrics,
                "aggregated": aggregated,
            }
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(output, f, indent=2)
            else:
                print(json.dumps(output, indent=2))
        else:
            print(format_metrics_table(aggregated, "Aggregated Metrics"))
            print(f"\n  ({len(all_metrics)} queries)")

    else:
        # Single query result
        scores = data.get("scores", [])
        ground_truth = data.get("ground_truth_notes")
        results = data.get("results", [])

        metrics = compute_all_metrics(results, scores, ground_truth, args.k)

        if args.format == "json":
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(metrics, f, indent=2)
            else:
                print(json.dumps(metrics, indent=2))
        else:
            print(format_metrics_table(metrics, "Query Metrics"))


if __name__ == "__main__":
    main()
