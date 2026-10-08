#!/usr/bin/env python3
"""
Build and manage test query sets for benchmarking.

Usage:
    python build_query_set.py --count 50 --output ../query-sets/core-50.json
    python build_query_set.py --list
    python build_query_set.py --validate ../query-sets/core-50.json

Query categories:
- factual (10): Single concept lookup
- conceptual (10): Topic exploration
- synthesis (15): Cross-domain connections
- temporal (5): Recent/historical focus
- needle (5): Specific note retrieval
- broad (5): High-level topic
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
QUERY_SETS_DIR = SKILL_DIR / "query-sets"

# Default query templates by category
DEFAULT_QUERIES = {
    "factual": [
        {"id": "f001", "query": "What is dopamine?", "notes": "Core concept, should find Dopamine.md"},
        {"id": "f002", "query": "What is anatta?", "notes": "Buddhist concept of no-self"},
        {"id": "f003", "query": "What is intermittent reinforcement?", "notes": "Behavioral concept"},
        {"id": "f004", "query": "What is lateral inhibition?", "notes": "Neural mechanism"},
        {"id": "f005", "query": "What is the DMN?", "notes": "Default mode network"},
        {"id": "f006", "query": "What is flow state?", "notes": "Psychology concept"},
        {"id": "f007", "query": "What is reward prediction error?", "notes": "Dopamine mechanism"},
        {"id": "f008", "query": "What is ergodicity?", "notes": "Taleb concept"},
        {"id": "f009", "query": "What is duhkha?", "notes": "Buddhist suffering"},
        {"id": "f010", "query": "What is belief updating?", "notes": "Bayesian concept"},
    ],
    "conceptual": [
        {"id": "c001", "query": "How does motivation work?", "notes": "Should explore dopamine system"},
        {"id": "c002", "query": "Why is changing minds so hard?", "notes": "Identity + dopamine"},
        {"id": "c003", "query": "How do habits form?", "notes": "Behavioral patterns"},
        {"id": "c004", "query": "What causes addiction?", "notes": "Dopamine, pleasure-pain"},
        {"id": "c005", "query": "How does attention work?", "notes": "Cognitive mechanism"},
        {"id": "c006", "query": "Why do we procrastinate?", "notes": "Decision-making"},
        {"id": "c007", "query": "How does learning happen?", "notes": "Memory consolidation"},
        {"id": "c008", "query": "What makes decisions difficult?", "notes": "Uncertainty, biases"},
        {"id": "c009", "query": "How does social media affect the brain?", "notes": "Dopamine + attention"},
        {"id": "c010", "query": "Why do beliefs persist despite evidence?", "notes": "Identity protection"},
    ],
    "synthesis": [
        {"id": "s001", "query": "Connect Buddhism and neuroscience", "notes": "Core bridge"},
        {"id": "s002", "query": "How do dopamine and identity relate?", "notes": "Belief confirmation"},
        {"id": "s003", "query": "What links flow states to Buddhist practice?", "notes": "Selflessness"},
        {"id": "s004", "query": "Connect decision-making biases to AI adoption", "notes": "Enterprise AI"},
        {"id": "s005", "query": "How does uncertainty relate to dopamine and belief?", "notes": "Three-way"},
        {"id": "s006", "query": "What connects content marketing to psychology?", "notes": "Attention trust"},
        {"id": "s007", "query": "Link scaling to identity transformation", "notes": "10x thinking"},
        {"id": "s008", "query": "How do attention and evolution relate?", "notes": "Selection pressure"},
        {"id": "s009", "query": "Connect AI agents to cognitive science", "notes": "Agent architecture"},
        {"id": "s010", "query": "What links meditation to decision quality?", "notes": "Bias reduction"},
        {"id": "s011", "query": "How does social media relate to Buddhism?", "notes": "Attachment"},
        {"id": "s012", "query": "Connect Kahneman's biases to behavior change", "notes": "Decision-making"},
        {"id": "s013", "query": "What links dopamine to content strategy?", "notes": "Engagement loops"},
        {"id": "s014", "query": "How do memory systems relate to AI?", "notes": "RAG, retrieval"},
        {"id": "s015", "query": "Connect identity to enterprise transformation", "notes": "Change barriers"},
    ],
    "temporal": [
        {"id": "t001", "query": "Recent notes about AI agents", "notes": "Time-based filter"},
        {"id": "t002", "query": "What have I learned recently about memory?", "notes": "Recent insights"},
        {"id": "t003", "query": "New insights about enterprise AI", "notes": "Document Insights"},
        {"id": "t004", "query": "Recent thoughts on content creation", "notes": "Output notes"},
        {"id": "t005", "query": "Latest notes on spreading activation", "notes": "Memory system"},
    ],
    "needle": [
        {"id": "n001", "query": "Note about intermittent reinforcement schedules", "notes": "Specific retrieval"},
        {"id": "n002", "query": "The note on pilot purgatory", "notes": "Enterprise AI term"},
        {"id": "n003", "query": "My note about MCP tool accuracy", "notes": "Specific metric"},
        {"id": "n004", "query": "The Taleb note about skin in the game", "notes": "Source note"},
        {"id": "n005", "query": "Note connecting duhkha to craving cycles", "notes": "Specific bridge"},
    ],
    "broad": [
        {"id": "b001", "query": "Identity", "notes": "Single word, broad topic"},
        {"id": "b002", "query": "Consciousness", "notes": "Philosophical domain"},
        {"id": "b003", "query": "Decision making", "notes": "Cognitive domain"},
        {"id": "b004", "query": "AI agents", "notes": "Technical domain"},
        {"id": "b005", "query": "Buddhism", "notes": "Philosophical domain"},
    ],
}


def create_query_set(
    snapshot: Optional[str] = None,
    output: Optional[Path] = None,
    custom_queries: Optional[dict] = None,
) -> dict:
    """Create a new query set with default or custom queries."""

    queries = custom_queries or DEFAULT_QUERIES

    # Flatten all queries with category info
    all_queries = []
    for category, category_queries in queries.items():
        for q in category_queries:
            all_queries.append({
                "id": q["id"],
                "query": q["query"],
                "category": category,
                "expected_intent": category if category in ["factual", "conceptual", "synthesis", "temporal"] else "conceptual",
                "notes": q.get("notes", ""),
                "ground_truth_notes": q.get("ground_truth_notes", []),
            })

    query_set = {
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "snapshot": snapshot or "unspecified",
        "description": "Core benchmark query set for Local Brain Search",
        "category_counts": {cat: len(qs) for cat, qs in queries.items()},
        "total_queries": len(all_queries),
        "queries": all_queries,
    }

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            json.dump(query_set, f, indent=2)
        print(f"Query set saved to: {output}")

    return query_set


def validate_query_set(path: Path) -> bool:
    """Validate a query set file."""
    try:
        with open(path) as f:
            data = json.load(f)

        required_fields = ["version", "queries"]
        for field in required_fields:
            if field not in data:
                print(f"Error: Missing required field: {field}")
                return False

        queries = data["queries"]
        print(f"Query set: {path.name}")
        print(f"Version: {data.get('version', 'unknown')}")
        print(f"Created: {data.get('created', 'unknown')}")
        print(f"Total queries: {len(queries)}")

        # Count by category
        categories = {}
        for q in queries:
            cat = q.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1

        print("\nCategory breakdown:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

        # Check for issues
        issues = []
        ids_seen = set()
        for q in queries:
            if "id" not in q:
                issues.append(f"Query missing ID: {q.get('query', 'unknown')[:30]}")
            elif q["id"] in ids_seen:
                issues.append(f"Duplicate ID: {q['id']}")
            else:
                ids_seen.add(q["id"])

            if "query" not in q:
                issues.append(f"Query missing 'query' field: {q.get('id', 'unknown')}")

        if issues:
            print(f"\nIssues found ({len(issues)}):")
            for issue in issues[:10]:
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
            return False

        print("\nValidation passed!")
        return True

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        return False


def list_query_sets() -> list[Path]:
    """List available query sets."""
    if not QUERY_SETS_DIR.exists():
        return []
    return sorted(QUERY_SETS_DIR.glob("*.json"))


def add_ground_truth(query_set_path: Path, query_id: str, notes: list[str]) -> None:
    """Add ground truth notes to a specific query."""
    with open(query_set_path) as f:
        data = json.load(f)

    for q in data["queries"]:
        if q["id"] == query_id:
            q["ground_truth_notes"] = notes
            break
    else:
        print(f"Error: Query ID not found: {query_id}")
        return

    with open(query_set_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Added {len(notes)} ground truth notes to {query_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Build and manage benchmark query sets"
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create a new query set with defaults",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output path for query set",
    )
    parser.add_argument(
        "--snapshot",
        help="Snapshot name to associate with query set",
    )
    parser.add_argument(
        "--validate",
        type=Path,
        help="Validate a query set file",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available query sets",
    )
    parser.add_argument(
        "--add-ground-truth",
        nargs=3,
        metavar=("QUERY_SET", "QUERY_ID", "NOTES_JSON"),
        help="Add ground truth notes (as JSON array) to a query",
    )

    args = parser.parse_args()

    if args.list:
        query_sets = list_query_sets()
        if query_sets:
            print("Available query sets:")
            for qs in query_sets:
                print(f"  - {qs.name}")
        else:
            print("No query sets found")
            print(f"Create one with: python build_query_set.py --create -o {QUERY_SETS_DIR / 'core-50.json'}")
        return

    if args.validate:
        valid = validate_query_set(args.validate)
        sys.exit(0 if valid else 1)

    if args.add_ground_truth:
        query_set_path, query_id, notes_json = args.add_ground_truth
        try:
            notes = json.loads(notes_json)
        except json.JSONDecodeError:
            print("Error: NOTES_JSON must be a valid JSON array")
            sys.exit(1)
        add_ground_truth(Path(query_set_path), query_id, notes)
        return

    if args.create:
        output = args.output or (QUERY_SETS_DIR / "core-50.json")
        create_query_set(snapshot=args.snapshot, output=output)
        return

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
