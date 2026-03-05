"""
Unified Memory Configuration for Local Brain Search

This is the SINGLE SOURCE OF TRUTH for all memory retrieval parameters.
Edit this file to tune memory behavior across the entire system.

Configuration is organized into sections:
1. Paths & Storage
2. Embedding & Indexing
3. Static Search
4. Spreading Activation (SYNAPSE-inspired)
5. Intent Classification
6. Graph Structure

Usage:
    from memory_config import MEMORY_CONFIG
    threshold = MEMORY_CONFIG['search']['default_threshold']
"""
from pathlib import Path
import os

# =============================================================================
# BASE PATHS
# =============================================================================

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
BRAIN_PATH = Path(os.environ.get("BRAIN_PATH", PROJECT_DIR.parent.parent / "Brain"))

# =============================================================================
# MEMORY CONFIGURATION
# =============================================================================

MEMORY_CONFIG = {
    # -------------------------------------------------------------------------
    # PATHS & STORAGE
    # -------------------------------------------------------------------------
    "paths": {
        "project_dir": PROJECT_DIR,
        "data_dir": DATA_DIR,
        "brain_path": BRAIN_PATH,
        "faiss_index": DATA_DIR / "brain.faiss",
        "metadata": DATA_DIR / "brain_metadata.pkl",
        "graph": DATA_DIR / "brain_graph.pkl",
        "q_values": DATA_DIR / "q_values.json",  # Future: usage-based learning
        "usage_history": DATA_DIR / "usage_history.jsonl",  # Future: tracking
    },

    # -------------------------------------------------------------------------
    # EMBEDDING & INDEXING
    # -------------------------------------------------------------------------
    "embedding": {
        "model": "all-MiniLM-L6-v2",  # 384 dimensions, fast, good quality
        "dimension": 384,
        "normalize": True,  # Required for cosine similarity via IndexFlatIP
    },

    "indexing": {
        "chunk_by_heading": True,
        "min_chunk_length": 50,  # Characters
        "excluded_folders": ["templates", ".obsidian", ".trash"],
        "include_patterns": ["*.md"],
    },

    # -------------------------------------------------------------------------
    # GRAPH STRUCTURE
    # -------------------------------------------------------------------------
    "graph": {
        # Semantic edge creation during indexing
        "semantic_edge_threshold": 0.65,  # Minimum similarity to create edge
        "semantic_edge_top_k": 5,  # Max semantic edges per note

        # Edge type weights (for spreading activation)
        "edge_weights": {
            "explicit": 1.0,   # Wiki-links (intentional connections)
            "semantic": 0.7,   # Similarity-based (computed)
            "temporal": 0.5,   # Time proximity (future)
            "causal": 0.9,     # Explicit causal markers (future)
        },
    },

    # -------------------------------------------------------------------------
    # STATIC SEARCH (Original vector similarity)
    # -------------------------------------------------------------------------
    "search": {
        "default_limit": 10,
        "default_threshold": 0.5,  # Minimum similarity to return
        "default_mode": "static",  # "static" or "spreading" - static wins on benchmarks
    },

    # -------------------------------------------------------------------------
    # SPREADING ACTIVATION (SYNAPSE-inspired)
    # -------------------------------------------------------------------------
    "spreading": {
        # Global defaults
        "max_iterations": 5,
        "convergence_threshold": 0.01,
        "activation_threshold": 0.1,  # Minimum to spread from node
        "anchor_strength": 0.8,  # Re-injection of seed activation

        # Decay factors by edge type
        "decay_factors": {
            "explicit": 0.8,   # Strong propagation through wiki-links
            "semantic": 0.5,   # Moderate through similarity
            "temporal": 0.3,   # Weak through time proximity
            "causal": 0.9,     # Very strong through causal links
        },

        # Temporal decay (per iteration)
        "temporal_decay": 0.9,

        # Lateral inhibition (prevents hub dominance)
        "inhibition_strength": 0.3,
        "inhibition_percentile": 90,  # Top N% considered "high activation"

        # Intent-specific overrides
        "intent_configs": {
            "factual": {
                "max_iterations": 2,
                "inhibition_strength": 0.5,
                "temporal_decay": 0.95,
                "description": "Focused search, minimal spreading",
            },
            "conceptual": {
                "max_iterations": 5,
                "inhibition_strength": 0.2,
                "temporal_decay": 0.9,
                "description": "Broad exploration, include hubs",
            },
            "synthesis": {
                "max_iterations": 7,
                "inhibition_strength": 0.1,
                "temporal_decay": 0.85,
                "description": "Maximum spreading, prioritize bridges",
            },
            "temporal": {
                "max_iterations": 3,
                "inhibition_strength": 0.3,
                "temporal_decay": 0.7,
                "description": "Time-weighted search",
            },
        },
    },

    # -------------------------------------------------------------------------
    # INTENT CLASSIFICATION
    # -------------------------------------------------------------------------
    "intent": {
        # Confidence threshold for using detected intent
        "confidence_threshold": 0.5,

        # Default intent when confidence is low
        "default_intent": "conceptual",

        # LLM fallback (not yet implemented)
        "use_llm_fallback": False,
        "llm_model": "haiku",
    },

    # -------------------------------------------------------------------------
    # USAGE-BASED LEARNING (Phase 4 - IMPLEMENTED 2026-02-18)
    # -------------------------------------------------------------------------
    "learning": {
        "enabled": True,  # Phase 4 active - tracks usage and adjusts rankings
        "learning_rate": 0.1,
        "discount_factor": 0.9,
        "q_weight": 0.3,  # Blend weight for Q-values in ranking

        # Reward structure
        "rewards": {
            "retrieved": 0.0,
            "read": 0.5,
            "referenced": 1.0,
            "linked": 1.5,
        },
    },

    # -------------------------------------------------------------------------
    # FORESIGHT SIGNALS (Phase 5 - NOT YET IMPLEMENTED)
    # -------------------------------------------------------------------------
    "foresight": {
        "enabled": False,
        "boost_factor": 0.5,  # How much to boost matching foresight
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_spreading_config_for_intent(intent: str) -> dict:
    """Get spreading configuration for a specific intent type."""
    defaults = {
        "max_iterations": MEMORY_CONFIG["spreading"]["max_iterations"],
        "inhibition_strength": MEMORY_CONFIG["spreading"]["inhibition_strength"],
        "temporal_decay": MEMORY_CONFIG["spreading"]["temporal_decay"],
    }

    intent_config = MEMORY_CONFIG["spreading"]["intent_configs"].get(intent, {})
    return {**defaults, **intent_config}


def get_decay_factor(edge_type: str) -> float:
    """Get decay factor for an edge type."""
    return MEMORY_CONFIG["spreading"]["decay_factors"].get(edge_type, 0.5)


def get_edge_weight(edge_type: str) -> float:
    """Get base weight for an edge type."""
    return MEMORY_CONFIG["graph"]["edge_weights"].get(edge_type, 0.5)


# =============================================================================
# BACKWARD COMPATIBILITY EXPORTS
# =============================================================================

# These match the old config.py interface
FAISS_INDEX_PATH = MEMORY_CONFIG["paths"]["faiss_index"]
METADATA_PATH = MEMORY_CONFIG["paths"]["metadata"]
GRAPH_PICKLE_PATH = MEMORY_CONFIG["paths"]["graph"]
EMBEDDING_MODEL = MEMORY_CONFIG["embedding"]["model"]
EMBEDDING_DIM = MEMORY_CONFIG["embedding"]["dimension"]
SEMANTIC_EDGE_THRESHOLD = MEMORY_CONFIG["graph"]["semantic_edge_threshold"]
SEMANTIC_EDGE_TOP_K = MEMORY_CONFIG["graph"]["semantic_edge_top_k"]
DEFAULT_SEARCH_LIMIT = MEMORY_CONFIG["search"]["default_limit"]
DEFAULT_SIMILARITY_THRESHOLD = MEMORY_CONFIG["search"]["default_threshold"]
CHUNK_BY_HEADING = MEMORY_CONFIG["indexing"]["chunk_by_heading"]
MIN_CHUNK_LENGTH = MEMORY_CONFIG["indexing"]["min_chunk_length"]
EXCLUDED_FOLDERS = MEMORY_CONFIG["indexing"]["excluded_folders"]
INCLUDE_PATTERNS = MEMORY_CONFIG["indexing"]["include_patterns"]


if __name__ == "__main__":
    import json

    # Print configuration for inspection
    print("=" * 60)
    print("MEMORY CONFIGURATION")
    print("=" * 60)

    # Convert paths to strings for JSON
    config_printable = {}
    for section, values in MEMORY_CONFIG.items():
        if section == "paths":
            config_printable[section] = {k: str(v) for k, v in values.items()}
        else:
            config_printable[section] = values

    print(json.dumps(config_printable, indent=2, default=str))
