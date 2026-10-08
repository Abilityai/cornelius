#!/usr/bin/env python3
"""
Execute benchmark runs against a Brain snapshot.

Usage:
    python run_benchmark.py --config focused --snapshot brain-snapshot-2026-02-18
    python run_benchmark.py --config single:spreading_default --snapshot brain-snapshot-2026-02-18
    python run_benchmark.py --resume  # Resume incomplete run

This script:
1. Loads query set and configurations
2. Runs searches against the snapshot
3. Scores results using LLM-as-judge
4. Computes metrics
5. Saves results to CSV
"""
import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add memory system to path
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_DIR = SKILL_DIR.parent.parent.parent
MEMORY_SYSTEM_DIR = PROJECT_DIR / "resources" / "local-brain-search"

sys.path.insert(0, str(MEMORY_SYSTEM_DIR))

# Directories
SNAPSHOTS_DIR = SKILL_DIR / "snapshots"
QUERY_SETS_DIR = SKILL_DIR / "query-sets"
RESULTS_DIR = SKILL_DIR / "results"
CONFIGS_DIR = SKILL_DIR / "configs"


def load_configs(config_name: str) -> list[dict]:
    """Load benchmark configurations.

    Args:
        config_name: One of:
            - "focused": Load focused_configs.json
            - "single:NAME": Single configuration by name
            - "all": All configurations (expensive)

    Returns:
        List of configuration dicts
    """
    configs_path = CONFIGS_DIR / "focused_configs.json"

    with open(configs_path) as f:
        all_configs = json.load(f)["configs"]

    if config_name == "focused":
        return all_configs

    if config_name.startswith("single:"):
        name = config_name[7:]
        for cfg in all_configs:
            if cfg["name"] == name:
                return [cfg]
        raise ValueError(f"Configuration not found: {name}")

    if config_name == "all":
        return all_configs

    raise ValueError(f"Unknown config: {config_name}")


def load_query_set(path: Optional[Path] = None) -> dict:
    """Load query set from file.

    Args:
        path: Path to query set JSON, or None for default

    Returns:
        Query set dict
    """
    if path is None:
        # Find default query set
        query_sets = list(QUERY_SETS_DIR.glob("*.json"))
        if not query_sets:
            raise FileNotFoundError(f"No query sets found in {QUERY_SETS_DIR}")
        path = query_sets[0]
        print(f"Using query set: {path.name}")

    with open(path) as f:
        return json.load(f)


def run_search(
    query: str,
    config: dict,
    snapshot_dir: Path,
    limit: int = 10,
) -> dict:
    """Run a search with specified configuration against a snapshot.

    Args:
        query: Search query
        config: Configuration dict with mode and params
        snapshot_dir: Path to snapshot directory
        limit: Number of results to return

    Returns:
        Dict with results, latency, and metadata
    """
    mode = config.get("mode", "spreading")
    params = config.get("params", {})

    # Import search module dynamically with modified paths
    import importlib.util
    import pickle

    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer

    # Load snapshot data
    snapshot_data_dir = snapshot_dir / "data"
    snapshot_brain_dir = snapshot_dir / "Brain"

    try:
        # Load FAISS index
        index = faiss.read_index(str(snapshot_data_dir / "brain.faiss"))

        # Load metadata
        with open(snapshot_data_dir / "brain_metadata.pkl", "rb") as f:
            metadata = pickle.load(f)

        # Load graph
        with open(snapshot_data_dir / "brain_graph.pkl", "rb") as f:
            G = pickle.load(f)

    except FileNotFoundError as e:
        return {
            "error": f"Snapshot data not found: {e}",
            "results": [],
            "latency_ms": 0,
        }

    # Import spreading module
    spec = importlib.util.spec_from_file_location(
        "spreading",
        MEMORY_SYSTEM_DIR / "spreading.py"
    )
    spreading_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(spreading_module)

    # Import intent module
    intent_spec = importlib.util.spec_from_file_location(
        "intent",
        MEMORY_SYSTEM_DIR / "intent.py"
    )
    intent_module = importlib.util.module_from_spec(intent_spec)
    intent_spec.loader.exec_module(intent_module)

    # Load embedding model
    from memory_config import MEMORY_CONFIG
    model = SentenceTransformer(MEMORY_CONFIG["embedding"]["model"])

    start_time = time.time()

    try:
        # Encode query
        query_embedding = model.encode([query], normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype("float32")

        # Get seed nodes from FAISS
        k = min(10, index.ntotal)
        distances, indices = index.search(query_embedding, k)

        # Aggregate to note level
        note_scores = {}
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(metadata):
                continue
            note_id = metadata[idx]["note_id"]
            similarity = float(dist)
            if note_id not in note_scores or similarity > note_scores[note_id]:
                note_scores[note_id] = similarity

        seed_nodes = [(nid, score) for nid, score in note_scores.items() if score >= 0.5]

        if mode == "static":
            # Static search - just return top similar
            results = []
            for note_id, similarity in sorted(note_scores.items(), key=lambda x: -x[1])[:limit]:
                # Find metadata entry
                for m in metadata:
                    if m["note_id"] == note_id:
                        results.append({
                            "note_id": note_id,
                            "title": m.get("title", note_id),
                            "filepath": m.get("filepath", ""),
                            "similarity": similarity,
                            "content": m.get("content", "")[:500],
                        })
                        break

            latency_ms = (time.time() - start_time) * 1000
            return {
                "results": results,
                "latency_ms": latency_ms,
                "iterations": 0,
                "converged": True,
                "mode": "static",
            }

        # Spreading search
        # Build config with parameter overrides
        spread_config = spreading_module.SpreadingConfig(
            max_iterations=params.get("max_iterations", 5),
            inhibition_strength=params.get("inhibition_strength", 0.3),
            temporal_decay=params.get("temporal_decay", 0.9),
            convergence_threshold=0.01,
            activation_threshold=0.1,
            anchor_strength=0.8,
        )

        # Run spreading activation
        result = spreading_module.spreading_activation(
            G,
            seed_nodes=seed_nodes,
            config=spread_config,
            track_traces=False,
        )

        # Get top activated
        top_results = spreading_module.get_top_activated(result, G, limit=limit)

        # Enrich results with content
        for r in top_results:
            note_id = r.get("note_id")
            for m in metadata:
                if m["note_id"] == note_id:
                    r["content"] = m.get("content", "")[:500]
                    r["filepath"] = m.get("filepath", "")
                    break

        latency_ms = (time.time() - start_time) * 1000
        return {
            "results": top_results,
            "latency_ms": latency_ms,
            "iterations": result.iterations,
            "converged": result.converged,
            "mode": "spreading",
        }

    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        return {
            "error": str(e),
            "results": [],
            "latency_ms": latency_ms,
        }


def score_results(
    query: str,
    intent: str,
    results: list[dict],
    judge,
    delay: float = 0.5,
) -> list[dict]:
    """Score search results using LLM judge.

    Args:
        query: Original query
        intent: Query intent (factual, conceptual, etc.)
        results: Search results
        judge: LLMJudge instance
        delay: Delay between API calls

    Returns:
        Results with scores added
    """
    scored = []

    for result in results:
        note_title = result.get("title", result.get("note_id", "Unknown"))
        note_content = result.get("content", "")

        if not note_content:
            # Try to load content from file
            filepath = result.get("filepath", "")
            if filepath:
                try:
                    with open(filepath) as f:
                        note_content = f.read()[:1000]
                except:
                    note_content = ""

        score_result = judge.score(
            query=query,
            note_title=note_title,
            note_content=note_content,
            intent=intent,
        )

        scored.append({
            **result,
            "relevance_score": score_result["score"],
            "score_reasoning": score_result.get("reasoning", ""),
            "score_error": score_result.get("error"),
        })

        time.sleep(delay)

    return scored


def write_results_csv(
    results: list[dict],
    output_path: Path,
    append: bool = False,
):
    """Write benchmark results to CSV.

    Args:
        results: List of result dicts
        output_path: Output CSV path
        append: Whether to append to existing file
    """
    if not results:
        return

    # Define columns
    base_columns = [
        "timestamp", "config_name", "query_id", "query", "query_category",
        "query_intent", "mode", "latency_ms", "iterations", "converged",
    ]

    # Add result columns (up to 10 results)
    result_columns = []
    for i in range(1, 11):
        result_columns.extend([
            f"result_{i}_note", f"result_{i}_score", f"result_{i}_activation",
        ])

    # Add metric columns
    metric_columns = [
        "precision_at_5", "precision_at_10", "mrr", "ndcg_at_10", "avg_score",
    ]

    columns = base_columns + result_columns + metric_columns

    output_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"

    with open(output_path, mode, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")

        if not append or output_path.stat().st_size == 0:
            writer.writeheader()

        for result in results:
            row = {
                "timestamp": result.get("timestamp", datetime.now().isoformat()),
                "config_name": result.get("config_name", ""),
                "query_id": result.get("query_id", ""),
                "query": result.get("query", ""),
                "query_category": result.get("query_category", ""),
                "query_intent": result.get("query_intent", ""),
                "mode": result.get("mode", ""),
                "latency_ms": result.get("latency_ms", 0),
                "iterations": result.get("iterations", 0),
                "converged": result.get("converged", False),
            }

            # Add result columns
            search_results = result.get("search_results", [])
            for i, r in enumerate(search_results[:10], 1):
                row[f"result_{i}_note"] = r.get("note_id", r.get("title", ""))
                row[f"result_{i}_score"] = r.get("relevance_score", -1)
                row[f"result_{i}_activation"] = r.get("activation", r.get("similarity", 0))

            # Add metrics
            metrics = result.get("metrics", {})
            for col in metric_columns:
                row[col] = metrics.get(col, "")

            writer.writerow(row)


def run_benchmark(
    configs: list[dict],
    query_set: dict,
    snapshot_dir: Path,
    output_path: Path,
    judge_model: str = "sonnet",
    delay: float = 0.5,
    resume: bool = False,
    dry_run: bool = False,
) -> dict:
    """Run full benchmark suite.

    Args:
        configs: List of configurations to test
        query_set: Query set dict
        snapshot_dir: Path to snapshot directory
        output_path: Path for results CSV
        judge_model: Model for LLM-as-judge
        delay: Delay between API calls
        resume: Resume from previous run
        dry_run: Don't actually run, just show plan

    Returns:
        Summary dict with stats
    """
    from score_results import LLMJudge
    from compute_metrics import compute_all_metrics

    queries = query_set["queries"]
    total_runs = len(configs) * len(queries)

    print(f"\n=== Benchmark Plan ===")
    print(f"Configurations: {len(configs)}")
    print(f"Queries: {len(queries)}")
    print(f"Total runs: {total_runs}")
    print(f"Results per query: 10")
    print(f"Total LLM scores: {total_runs * 10}")
    print(f"Snapshot: {snapshot_dir.name}")
    print(f"Output: {output_path}")

    if dry_run:
        print("\nDry run - no actual execution")
        return {"dry_run": True, "total_runs": total_runs}

    # Initialize judge
    print(f"\nInitializing LLM judge ({judge_model})...")
    judge = LLMJudge(model=judge_model)

    # Track completed runs for resume
    completed = set()
    if resume and output_path.exists():
        import csv
        with open(output_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row['config_name']}|{row['query_id']}"
                completed.add(key)
        print(f"Resuming: {len(completed)} runs already completed")

    # Run benchmark
    results = []
    run_count = 0
    start_time = time.time()

    for config in configs:
        config_name = config["name"]
        print(f"\n--- Config: {config_name} ---")

        for query_data in queries:
            query_id = query_data["id"]
            query = query_data["query"]
            category = query_data["category"]
            intent = query_data.get("expected_intent", category)

            # Check if already completed
            key = f"{config_name}|{query_id}"
            if key in completed:
                continue

            run_count += 1
            pct = (run_count / total_runs) * 100
            print(f"  [{run_count}/{total_runs}] ({pct:.1f}%) {query_id}: {query[:40]}...")

            # Run search
            search_result = run_search(query, config, snapshot_dir)

            if "error" in search_result:
                print(f"    Error: {search_result['error'][:100]}")
                continue

            # Score results
            scored_results = score_results(
                query=query,
                intent=intent,
                results=search_result["results"],
                judge=judge,
                delay=delay,
            )

            # Compute metrics
            scores = [r["relevance_score"] for r in scored_results]
            ground_truth = query_data.get("ground_truth_notes", [])
            metrics = compute_all_metrics(
                scored_results, scores, ground_truth, k_values=[5, 10]
            )

            # Build result record
            result = {
                "timestamp": datetime.now().isoformat(),
                "config_name": config_name,
                "query_id": query_id,
                "query": query,
                "query_category": category,
                "query_intent": intent,
                "mode": search_result.get("mode", config.get("mode", "")),
                "latency_ms": search_result.get("latency_ms", 0),
                "iterations": search_result.get("iterations", 0),
                "converged": search_result.get("converged", False),
                "search_results": scored_results,
                "metrics": metrics,
            }

            results.append(result)

            # Write incrementally
            write_results_csv([result], output_path, append=True)

    elapsed = time.time() - start_time

    summary = {
        "total_runs": run_count,
        "elapsed_seconds": elapsed,
        "results_path": str(output_path),
        "configs_tested": [c["name"] for c in configs],
    }

    print(f"\n=== Benchmark Complete ===")
    print(f"Runs: {run_count}")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"Results: {output_path}")

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Execute benchmark runs against a Brain snapshot"
    )
    parser.add_argument(
        "--config",
        default="focused",
        help="Config to run: 'focused', 'single:NAME', or 'all'",
    )
    parser.add_argument(
        "--snapshot",
        help="Snapshot name (e.g., brain-snapshot-2026-02-18)",
    )
    parser.add_argument(
        "--query-set",
        type=Path,
        help="Path to query set JSON",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output CSV path",
    )
    parser.add_argument(
        "--model",
        default="sonnet",
        choices=["haiku", "sonnet", "opus"],
        help="Model for LLM-as-judge (default: sonnet for quality)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between API calls",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from previous run",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show plan without executing",
    )
    parser.add_argument(
        "--list-configs",
        action="store_true",
        help="List available configurations",
    )
    parser.add_argument(
        "--list-snapshots",
        action="store_true",
        help="List available snapshots",
    )

    args = parser.parse_args()

    # List snapshots
    if args.list_snapshots:
        if SNAPSHOTS_DIR.exists():
            snapshots = sorted(SNAPSHOTS_DIR.iterdir())
            print("Available snapshots:")
            for s in snapshots:
                if s.is_dir():
                    print(f"  - {s.name}")
        else:
            print("No snapshots found")
        return

    # List configs
    if args.list_configs:
        configs = load_configs("focused")
        print("Available configurations:")
        for c in configs:
            print(f"  - {c['name']}: {c.get('description', '')}")
        return

    # Validate snapshot
    if not args.snapshot:
        # Try to find latest snapshot
        if SNAPSHOTS_DIR.exists():
            snapshots = sorted([d for d in SNAPSHOTS_DIR.iterdir() if d.is_dir()])
            if snapshots:
                args.snapshot = snapshots[-1].name
                print(f"Using latest snapshot: {args.snapshot}")
            else:
                print("Error: No snapshots found. Run create_snapshot.py first.")
                sys.exit(1)
        else:
            print("Error: No snapshots directory. Run create_snapshot.py first.")
            sys.exit(1)

    snapshot_dir = SNAPSHOTS_DIR / args.snapshot
    if not snapshot_dir.exists():
        print(f"Error: Snapshot not found: {snapshot_dir}")
        sys.exit(1)

    # Load configs
    configs = load_configs(args.config)

    # Load query set
    query_set = load_query_set(args.query_set)

    # Set output path
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_path = RESULTS_DIR / f"benchmark-{timestamp}.csv"

    # Run benchmark
    summary = run_benchmark(
        configs=configs,
        query_set=query_set,
        snapshot_dir=snapshot_dir,
        output_path=output_path,
        judge_model=args.model,
        delay=args.delay,
        resume=args.resume,
        dry_run=args.dry_run,
    )

    if not args.dry_run:
        # Save summary
        summary_path = output_path.with_suffix(".summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
