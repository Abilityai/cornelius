"""
Configuration for local brain search system.
"""
import os
from pathlib import Path

# Paths
PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
# Brain path - relative to project root or set via environment variable
BRAIN_PATH = Path(os.environ.get("BRAIN_PATH", PROJECT_DIR.parent.parent / "Brain"))

# FAISS settings
FAISS_INDEX_PATH = DATA_DIR / "brain.faiss"
METADATA_PATH = DATA_DIR / "brain_metadata.pkl"

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384 dimensions, fast, good quality
EMBEDDING_DIM = 384

# Graph settings
GRAPH_PICKLE_PATH = DATA_DIR / "brain_graph.pkl"
SEMANTIC_EDGE_THRESHOLD = 0.65  # Cosine similarity threshold for weak edges
SEMANTIC_EDGE_TOP_K = 5  # Number of similar notes to consider for weak edges

# Search settings
DEFAULT_SEARCH_LIMIT = 10
DEFAULT_SIMILARITY_THRESHOLD = 0.5

# Indexing settings
CHUNK_BY_HEADING = True  # If True, split notes by headings; if False, use whole note
MIN_CHUNK_LENGTH = 50  # Minimum characters for a chunk to be indexed
EXCLUDED_FOLDERS = [
    "templates",
    ".obsidian",
    ".trash",
]

# File patterns to index
INCLUDE_PATTERNS = ["*.md"]
