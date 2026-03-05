#!/usr/bin/env python3
"""
Usage-Based Learning for Local Brain Search (Phase 4).

Implements MemRL-inspired Q-value learning:
- Tracks which retrieved notes are actually used
- Computes Q-values based on usage patterns
- Adjusts retrieval ranking based on learned preferences
- Persists learning across sessions

Usage Events:
- retrieved: Note appeared in search results
- read: Note content was read by agent
- referenced: Note was cited in agent output
- linked: Note was linked in new content

Based on MemRL paper (arXiv:2601.03192, January 2026).
"""
import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

from memory_config import MEMORY_CONFIG


# =============================================================================
# DATA STRUCTURES
# =============================================================================

EventType = Literal["retrieved", "read", "referenced", "linked"]


@dataclass
class UsageEvent:
    """A single usage event for a note."""
    timestamp: str  # ISO format
    note_id: str
    query: str
    query_intent: str
    event_type: EventType
    position_in_results: int  # 0-indexed position (for retrieved events)
    session_id: str
    mode: str  # "static" or "spreading"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "UsageEvent":
        return cls(**data)


@dataclass
class LearningStats:
    """Statistics about the learning system."""
    total_events: int
    unique_notes_tracked: int
    notes_with_q_values: int
    avg_q_value: float
    max_q_value: float
    min_q_value: float
    events_by_type: dict[str, int]
    top_notes: list[tuple[str, float]]  # (note_id, q_value)


# =============================================================================
# FILE PATHS
# =============================================================================

def get_q_values_path() -> Path:
    return MEMORY_CONFIG["paths"]["q_values"]


def get_usage_history_path() -> Path:
    return MEMORY_CONFIG["paths"]["usage_history"]


# =============================================================================
# Q-VALUE MANAGEMENT
# =============================================================================

def load_q_values() -> dict[str, float]:
    """Load Q-values from disk."""
    path = get_q_values_path()
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_q_values(q_values: dict[str, float]) -> None:
    """Save Q-values to disk."""
    path = get_q_values_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(q_values, f, indent=2, sort_keys=True)


def update_q_value(
    q_values: dict[str, float],
    note_id: str,
    event_type: EventType,
    position: int = 0,
    learning_rate: Optional[float] = None,
) -> float:
    """
    Update Q-value for a note based on a usage event.

    Uses Q-learning update rule:
    Q(s) = Q(s) + α * (reward * position_factor - Q(s))

    Returns the new Q-value.
    """
    config = MEMORY_CONFIG["learning"]
    lr = learning_rate or config["learning_rate"]
    rewards = config["rewards"]

    # Get reward for this event type
    reward = rewards.get(event_type, 0.0)

    # Position discount - earlier positions get more credit
    # position 0 = 1.0, position 9 = 0.5
    position_factor = 1.0 / (1 + position * 0.05)

    # Current Q-value (default 0)
    current_q = q_values.get(note_id, 0.0)

    # Q-learning update
    new_q = current_q + lr * (reward * position_factor - current_q)

    # Clamp to reasonable range
    new_q = max(-1.0, min(2.0, new_q))

    q_values[note_id] = new_q
    return new_q


def decay_q_values(q_values: dict[str, float], decay_factor: float = 0.99) -> None:
    """Apply decay to all Q-values (for temporal forgetting)."""
    for note_id in q_values:
        q_values[note_id] *= decay_factor


# =============================================================================
# USAGE TRACKING
# =============================================================================

def log_usage_event(event: UsageEvent) -> None:
    """Append a usage event to the history file."""
    path = get_usage_history_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "a") as f:
        f.write(json.dumps(event.to_dict()) + "\n")


def log_retrieval(
    note_ids: list[str],
    query: str,
    intent: str,
    mode: str = "static",
    session_id: Optional[str] = None,
) -> None:
    """
    Log that notes were retrieved in search results.

    Call this after every search to track what was shown to the user/agent.
    """
    if not MEMORY_CONFIG["learning"]["enabled"]:
        return

    session = session_id or _get_session_id()
    timestamp = datetime.now().isoformat()

    q_values = load_q_values()

    for position, note_id in enumerate(note_ids):
        event = UsageEvent(
            timestamp=timestamp,
            note_id=note_id,
            query=query,
            query_intent=intent,
            event_type="retrieved",
            position_in_results=position,
            session_id=session,
            mode=mode,
        )
        log_usage_event(event)

        # Update Q-value (small signal for being retrieved)
        update_q_value(q_values, note_id, "retrieved", position)

    save_q_values(q_values)


def log_read(
    note_id: str,
    query: str = "",
    intent: str = "",
    position: int = 0,
    session_id: Optional[str] = None,
) -> None:
    """Log that a note's content was read."""
    if not MEMORY_CONFIG["learning"]["enabled"]:
        return

    session = session_id or _get_session_id()

    event = UsageEvent(
        timestamp=datetime.now().isoformat(),
        note_id=note_id,
        query=query,
        query_intent=intent,
        event_type="read",
        position_in_results=position,
        session_id=session,
        mode="",
    )
    log_usage_event(event)

    q_values = load_q_values()
    update_q_value(q_values, note_id, "read", position)
    save_q_values(q_values)


def log_reference(
    note_id: str,
    query: str = "",
    intent: str = "",
    position: int = 0,
    session_id: Optional[str] = None,
) -> None:
    """Log that a note was referenced/cited in output."""
    if not MEMORY_CONFIG["learning"]["enabled"]:
        return

    session = session_id or _get_session_id()

    event = UsageEvent(
        timestamp=datetime.now().isoformat(),
        note_id=note_id,
        query=query,
        query_intent=intent,
        event_type="referenced",
        position_in_results=position,
        session_id=session,
        mode="",
    )
    log_usage_event(event)

    q_values = load_q_values()
    update_q_value(q_values, note_id, "referenced", position)
    save_q_values(q_values)


def log_linked(
    note_id: str,
    query: str = "",
    intent: str = "",
    position: int = 0,
    session_id: Optional[str] = None,
) -> None:
    """Log that a note was linked in new content."""
    if not MEMORY_CONFIG["learning"]["enabled"]:
        return

    session = session_id or _get_session_id()

    event = UsageEvent(
        timestamp=datetime.now().isoformat(),
        note_id=note_id,
        query=query,
        query_intent=intent,
        event_type="linked",
        position_in_results=position,
        session_id=session,
        mode="",
    )
    log_usage_event(event)

    q_values = load_q_values()
    update_q_value(q_values, note_id, "linked", position)
    save_q_values(q_values)


def _get_session_id() -> str:
    """Get or create a session ID from environment."""
    return os.environ.get("CLAUDE_SESSION_ID", f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")


# =============================================================================
# RANKING ADJUSTMENT
# =============================================================================

def adjust_scores_with_q_values(
    scores: dict[str, float],
    q_weight: Optional[float] = None,
) -> dict[str, float]:
    """
    Blend activation/similarity scores with learned Q-values.

    Args:
        scores: {note_id: score} from search/spreading
        q_weight: How much to weight Q-values (default from config)

    Returns:
        Adjusted scores
    """
    if not MEMORY_CONFIG["learning"]["enabled"]:
        return scores

    config = MEMORY_CONFIG["learning"]
    weight = q_weight if q_weight is not None else config["q_weight"]

    q_values = load_q_values()

    result = {}
    for note_id, score in scores.items():
        q = q_values.get(note_id, 0.0)
        # Blend: (1 - weight) * score + weight * q
        # But Q-values are in different range, so we use them as a multiplier boost
        # q=0 -> no change, q=1 -> +30% boost, q=-0.5 -> -15% penalty
        adjustment = 1.0 + (q * weight)
        result[note_id] = score * adjustment

    return result


def get_q_value_boost(note_id: str) -> float:
    """Get the Q-value boost factor for a single note."""
    if not MEMORY_CONFIG["learning"]["enabled"]:
        return 1.0

    q_values = load_q_values()
    q = q_values.get(note_id, 0.0)
    weight = MEMORY_CONFIG["learning"]["q_weight"]
    return 1.0 + (q * weight)


# =============================================================================
# STATISTICS & ANALYSIS
# =============================================================================

def get_learning_stats() -> LearningStats:
    """Get statistics about the learning system."""
    q_values = load_q_values()

    # Count events by type
    events_by_type: dict[str, int] = {
        "retrieved": 0,
        "read": 0,
        "referenced": 0,
        "linked": 0,
    }
    unique_notes = set()
    total_events = 0

    history_path = get_usage_history_path()
    if history_path.exists():
        with open(history_path, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        event = json.loads(line)
                        events_by_type[event["event_type"]] = events_by_type.get(event["event_type"], 0) + 1
                        unique_notes.add(event["note_id"])
                        total_events += 1
                    except (json.JSONDecodeError, KeyError):
                        continue

    # Q-value statistics
    q_list = list(q_values.values()) if q_values else [0.0]

    # Top notes by Q-value
    sorted_notes = sorted(q_values.items(), key=lambda x: x[1], reverse=True)[:10]

    return LearningStats(
        total_events=total_events,
        unique_notes_tracked=len(unique_notes),
        notes_with_q_values=len(q_values),
        avg_q_value=sum(q_list) / len(q_list) if q_list else 0.0,
        max_q_value=max(q_list) if q_list else 0.0,
        min_q_value=min(q_list) if q_list else 0.0,
        events_by_type=events_by_type,
        top_notes=sorted_notes,
    )


def reset_learning() -> None:
    """Reset all learned Q-values and usage history."""
    q_path = get_q_values_path()
    history_path = get_usage_history_path()

    if q_path.exists():
        # Backup before delete
        backup_path = q_path.with_suffix(".json.bak")
        q_path.rename(backup_path)
        print(f"Q-values backed up to: {backup_path}")

    if history_path.exists():
        backup_path = history_path.with_suffix(".jsonl.bak")
        history_path.rename(backup_path)
        print(f"Usage history backed up to: {backup_path}")

    # Create empty files
    save_q_values({})
    print("Learning state reset. Empty Q-values created.")


def export_learning_data() -> dict:
    """Export all learning data for analysis."""
    q_values = load_q_values()

    events = []
    history_path = get_usage_history_path()
    if history_path.exists():
        with open(history_path, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

    return {
        "q_values": q_values,
        "events": events,
        "stats": asdict(get_learning_stats()) if get_learning_stats() else {},
        "config": MEMORY_CONFIG["learning"],
    }


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Usage-based learning management")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show learning statistics")
    status_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset all learned data")
    reset_parser.add_argument("--confirm", action="store_true", help="Confirm reset")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export learning data")
    export_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # Top command
    top_parser = subparsers.add_parser("top", help="Show top notes by Q-value")
    top_parser.add_argument("--limit", "-n", type=int, default=20, help="Number of notes")
    top_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # Log command (for manual testing)
    log_parser = subparsers.add_parser("log", help="Manually log a usage event")
    log_parser.add_argument("event_type", choices=["read", "referenced", "linked"])
    log_parser.add_argument("note_id", help="Note ID")
    log_parser.add_argument("--query", default="", help="Associated query")

    # Enable/disable
    enable_parser = subparsers.add_parser("enable", help="Enable learning")
    disable_parser = subparsers.add_parser("disable", help="Disable learning")

    args = parser.parse_args()

    if args.command == "status":
        stats = get_learning_stats()
        enabled = MEMORY_CONFIG["learning"]["enabled"]

        if args.json:
            output = {
                "enabled": enabled,
                **asdict(stats),
            }
            print(json.dumps(output, indent=2))
        else:
            print("=" * 60)
            print("USAGE-BASED LEARNING STATUS")
            print("=" * 60)
            print(f"\nEnabled: {enabled}")
            print(f"\nEvent Statistics:")
            print(f"  Total events: {stats.total_events}")
            print(f"  Unique notes tracked: {stats.unique_notes_tracked}")
            print(f"  Events by type:")
            for event_type, count in stats.events_by_type.items():
                print(f"    - {event_type}: {count}")
            print(f"\nQ-Value Statistics:")
            print(f"  Notes with Q-values: {stats.notes_with_q_values}")
            print(f"  Average Q-value: {stats.avg_q_value:.4f}")
            print(f"  Max Q-value: {stats.max_q_value:.4f}")
            print(f"  Min Q-value: {stats.min_q_value:.4f}")
            if stats.top_notes:
                print(f"\nTop 5 Notes by Q-value:")
                for note_id, q in stats.top_notes[:5]:
                    print(f"  [{q:.4f}] {note_id}")

    elif args.command == "reset":
        if not args.confirm:
            print("This will reset all learned Q-values and usage history.")
            print("Run with --confirm to proceed.")
            return
        reset_learning()

    elif args.command == "export":
        data = export_learning_data()
        output = json.dumps(data, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Exported to: {args.output}")
        else:
            print(output)

    elif args.command == "top":
        q_values = load_q_values()
        sorted_notes = sorted(q_values.items(), key=lambda x: x[1], reverse=True)[:args.limit]

        if args.json:
            print(json.dumps(sorted_notes, indent=2))
        else:
            print(f"Top {args.limit} notes by Q-value:")
            print("-" * 60)
            for i, (note_id, q) in enumerate(sorted_notes, 1):
                print(f"{i:3}. [{q:+.4f}] {note_id}")

    elif args.command == "log":
        if args.event_type == "read":
            log_read(args.note_id, args.query)
        elif args.event_type == "referenced":
            log_reference(args.note_id, args.query)
        elif args.event_type == "linked":
            log_linked(args.note_id, args.query)
        print(f"Logged {args.event_type} event for: {args.note_id}")

    elif args.command == "enable":
        print("To enable learning, set 'enabled': True in memory_config.py")
        print("Location: MEMORY_CONFIG['learning']['enabled']")

    elif args.command == "disable":
        print("To disable learning, set 'enabled': False in memory_config.py")
        print("Location: MEMORY_CONFIG['learning']['enabled']")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
