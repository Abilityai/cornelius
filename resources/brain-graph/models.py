"""
Brain Dependency Graph - Data Models

Dataclasses for graph enrichments: nodes, edges, tensions.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Layer(Enum):
    """The seven artifact layers."""
    SIGNAL = "signal"           # Layer 1: Raw inputs
    IMPRESSION = "impression"   # Layer 2: Fleeting captures
    INSIGHT = "insight"         # Layer 3: Atomic permanent notes
    FRAMEWORK = "framework"     # Layer 4: Original mental models
    LENS = "lens"               # Layer 5: MOCs, navigation hubs
    SYNTHESIS = "synthesis"     # Layer 6: Articles, essays
    INDEX = "index"             # Layer 7: Meta-structural

    @property
    def number(self) -> int:
        return {
            "signal": 1, "impression": 2, "insight": 3, "framework": 4,
            "lens": 5, "synthesis": 6, "index": 7,
        }[self.value]


class EdgeType(Enum):
    """Six fundamental edge types."""
    DERIVES_FROM = "derives-from"
    INSTANTIATES = "instantiates"
    REFERENCES = "references"
    ASSOCIATES = "associates"
    TENSION = "tension"
    SUPERSEDES = "supersedes"


class Authority(Enum):
    """Which side of an edge is authoritative."""
    SOURCE = "source"   # Source note wins on conflict
    TARGET = "target"   # Target note wins on conflict
    NONE = "none"       # Neither side (bidirectional or unresolved)


@dataclass
class NodeEnrichment:
    """Enrichment metadata for a single note."""
    layer: str                              # Layer enum value
    lifecycle: float = 0.0                  # 0.0 (reflective) to 1.0 (generative)
    staleness_score: float = 0.0            # 0.0 (fresh) to 1.0 (definitely stale)
    last_coherence_check: Optional[str] = None  # ISO date
    classification_confidence: float = 0.5  # How confident the layer classification is

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> NodeEnrichment:
        return cls(**data)


@dataclass
class EdgeEnrichment:
    """Enrichment metadata for a single edge."""
    edge_type: str              # EdgeType enum value
    authority: str = "none"     # Authority enum value
    confidence: float = 0.5     # Confidence in the type classification
    original_type: str = ""     # Original edge type from LBS graph (explicit/semantic)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> EdgeEnrichment:
        return cls(**data)


@dataclass
class TensionRecord:
    """A productive contradiction between two notes."""
    note_a: str
    note_b: str
    similarity: float = 0.0
    description: str = ""
    synthesis_artifacts: list[str] = field(default_factory=list)
    detected: str = ""  # ISO date

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> TensionRecord:
        return cls(**data)


@dataclass
class StalenessResult:
    """Result of staleness propagation from a changed note."""
    changed_note: str
    change_magnitude: float
    affected_notes: dict[str, float]  # note_id -> staleness score
    propagation_depth: int
    total_examined: int

    def above_threshold(self, threshold: float = 0.3) -> dict[str, float]:
        return {k: v for k, v in self.affected_notes.items() if v >= threshold}


@dataclass
class LifecycleTransition:
    """A detected lifecycle phase transition."""
    note_id: str
    old_score: float
    new_score: float
    old_phase: str   # reflective / crystallizing / generative
    new_phase: str
    signals: dict[str, float]  # signal_name -> value

    @staticmethod
    def phase_name(score: float) -> str:
        if score < 0.3:
            return "reflective"
        elif score < 0.6:
            return "crystallizing"
        else:
            return "generative"
