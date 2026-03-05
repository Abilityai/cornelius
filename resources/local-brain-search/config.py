"""
Configuration for local brain search system.

NOTE: This file imports from memory_config.py for backward compatibility.
Edit memory_config.py to change settings.
"""
# Import everything from memory_config for backward compatibility
from memory_config import (
    PROJECT_DIR,
    DATA_DIR,
    BRAIN_PATH,
    FAISS_INDEX_PATH,
    METADATA_PATH,
    GRAPH_PICKLE_PATH,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
    SEMANTIC_EDGE_THRESHOLD,
    SEMANTIC_EDGE_TOP_K,
    DEFAULT_SEARCH_LIMIT,
    DEFAULT_SIMILARITY_THRESHOLD,
    CHUNK_BY_HEADING,
    MIN_CHUNK_LENGTH,
    EXCLUDED_FOLDERS,
    INCLUDE_PATTERNS,
    MEMORY_CONFIG,
)

__all__ = [
    "PROJECT_DIR",
    "DATA_DIR",
    "BRAIN_PATH",
    "FAISS_INDEX_PATH",
    "METADATA_PATH",
    "GRAPH_PICKLE_PATH",
    "EMBEDDING_MODEL",
    "EMBEDDING_DIM",
    "SEMANTIC_EDGE_THRESHOLD",
    "SEMANTIC_EDGE_TOP_K",
    "DEFAULT_SEARCH_LIMIT",
    "DEFAULT_SIMILARITY_THRESHOLD",
    "CHUNK_BY_HEADING",
    "MIN_CHUNK_LENGTH",
    "EXCLUDED_FOLDERS",
    "INCLUDE_PATTERNS",
    "MEMORY_CONFIG",
]
