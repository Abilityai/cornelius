"""
Brain Dependency Graph - Configuration

Loads brain_graph_config.yaml and defines paths.

brain_graph_config.yaml is a TRACKED file that ships with the repo
(Abilityai/cornelius#15: it was once missing from the template, so every
brain-graph command died on a bare FileNotFoundError). Its shape is described
in BRAIN-DEPENDENCY-GRAPH-ARCHITECTURE.md -> "Central Graph Definition";
test_config.py keeps the two from drifting.
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

# Every top-level key an accessor below reads.
REQUIRED_KEYS = ("artifact_types", "default_edges", "propagation", "lifecycle", "framework_detection")


class BrainGraphConfigError(FileNotFoundError):
    """The brain-graph config is missing or incomplete (subclass of FileNotFoundError)."""


def load_config() -> dict:
    """Load and cache the brain graph configuration.

    Fails with an actionable message naming the file, instead of a bare
    FileNotFoundError / KeyError deep in an import chain.
    """
    global _config_cache
    if _config_cache is None:
        if not CONFIG_PATH.is_file():
            raise BrainGraphConfigError(
                f"Brain-graph config not found: {CONFIG_PATH}\n"
                "It ships with the repo - restore it with "
                "`git checkout -- resources/brain-graph/brain_graph_config.yaml` "
                "(or re-clone). Its schema is in BRAIN-DEPENDENCY-GRAPH-ARCHITECTURE.md "
                "-> 'Central Graph Definition'."
            )
        with open(CONFIG_PATH) as f:
            cfg = yaml.safe_load(f) or {}
        missing = [k for k in REQUIRED_KEYS if k not in cfg]
        if missing:
            raise BrainGraphConfigError(
                f"Brain-graph config {CONFIG_PATH} is missing required keys: {', '.join(missing)}. "
                "Restore the shipped file with "
                "`git checkout -- resources/brain-graph/brain_graph_config.yaml`."
            )
        _config_cache = cfg
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
