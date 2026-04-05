"""
Brain Dependency Graph - Configuration

Loads brain_graph_config.yaml and defines paths.
"""
from pathlib import Path

import yaml


# =============================================================================
# PATHS
# =============================================================================

BRAIN_GRAPH_DIR = Path(__file__).parent
DATA_DIR = BRAIN_GRAPH_DIR / "data"
REPORTS_DIR = BRAIN_GRAPH_DIR / "reports"
CONFIG_PATH = BRAIN_GRAPH_DIR / "brain_graph_config.yaml"
ENRICHMENTS_PATH = DATA_DIR / "graph_enrichments.json"

# Local Brain Search paths
LBS_DIR = BRAIN_GRAPH_DIR.parent / "local-brain-search"
LBS_DATA_DIR = LBS_DIR / "data"
LBS_GRAPH_PATH = LBS_DATA_DIR / "brain_graph.pkl"
LBS_METADATA_PATH = LBS_DATA_DIR / "brain_metadata.pkl"
LBS_FAISS_PATH = LBS_DATA_DIR / "brain.faiss"

# Vault path
BRAIN_PATH = BRAIN_GRAPH_DIR.parent.parent / "Brain"


# =============================================================================
# CONFIG LOADING
# =============================================================================

_config_cache = None


def load_config() -> dict:
    """Load and cache the brain graph configuration."""
    global _config_cache
    if _config_cache is None:
        with open(CONFIG_PATH) as f:
            _config_cache = yaml.safe_load(f)
    return _config_cache


def get_propagation_config() -> dict:
    return load_config()["propagation"]


def get_lifecycle_config() -> dict:
    return load_config()["lifecycle"]


def get_artifact_types() -> dict:
    return load_config()["artifact_types"]


def get_default_edges() -> list:
    return load_config()["default_edges"]


def get_framework_detection() -> dict:
    return load_config()["framework_detection"]
