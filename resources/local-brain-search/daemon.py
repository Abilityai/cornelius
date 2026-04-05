#!/usr/bin/env python3
"""
Brain Search Daemon - keeps FAISS index, metadata, and graph in memory.

Provides HTTP endpoints that mirror search.py and connections.py CLI interfaces.
Wrapper scripts try the daemon first; if it's not running, they fall back to
direct Python invocation (original behavior).

Start:  ./run_daemon.sh start
Stop:   ./run_daemon.sh stop
Reload: ./run_daemon.sh reload   (or: kill -SIGHUP <pid>)

Endpoints:
    GET  /search?q=...&limit=10&threshold=0.5&mode=static&intent=...&explain=0&no_track=0&full=0
    GET  /connections?q=...&depth=1&semantic_only=0&explicit_only=0
    GET  /connections/stats
    GET  /connections/hubs
    GET  /connections/bridges
    GET  /health
    POST /reload
"""
import json
import os
import pickle
import signal
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import faiss
import networkx as nx
import numpy as np
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer

# Add project dir to path so we can import local modules
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from config import (
    DEFAULT_SEARCH_LIMIT,
    DEFAULT_SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    GRAPH_PICKLE_PATH,
    METADATA_PATH,
)
from intent import QueryIntent, classify_intent
from learning import adjust_scores_with_q_values, log_retrieval
from memory_config import MEMORY_CONFIG
from spreading import SpreadingConfig, get_top_activated, spreading_activation


# =============================================================================
# IN-MEMORY STORE
# =============================================================================

class BrainStore:
    """Holds all data in memory."""

    def __init__(self):
        self.index = None
        self.metadata = None
        self.graph = None
        self.model = None
        self.loaded_at = None

    def load(self):
        """Load everything from disk into memory."""
        t0 = time.time()

        print("Loading FAISS index...", flush=True)
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        print("Loading metadata...", flush=True)
        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        print("Loading graph...", flush=True)
        with open(GRAPH_PICKLE_PATH, "rb") as f:
            self.graph = pickle.load(f)

        print("Loading embedding model...", flush=True)
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.loaded_at = time.time()
        elapsed = self.loaded_at - t0
        print(
            f"Brain loaded in {elapsed:.1f}s: "
            f"{self.index.ntotal} chunks, "
            f"{len(self.metadata)} metadata entries, "
            f"{self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges",
            flush=True,
        )

    def reload(self):
        """Reload all data from disk (after re-index)."""
        print("Reloading brain data...", flush=True)
        self.load()


store = BrainStore()


# =============================================================================
# NUMPY JSON ENCODER
# =============================================================================

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# =============================================================================
# APP LIFECYCLE
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    store.load()

    # Handle SIGHUP for reload
    def handle_sighup(signum, frame):
        store.reload()

    signal.signal(signal.SIGHUP, handle_sighup)

    yield


app = FastAPI(title="Brain Search Daemon", lifespan=lifespan)


# =============================================================================
# SEARCH ENDPOINTS
# =============================================================================

@app.get("/search")
def search_endpoint(
    q: str,
    limit: int = Query(default=DEFAULT_SEARCH_LIMIT),
    threshold: float = Query(default=DEFAULT_SIMILARITY_THRESHOLD),
    mode: str = Query(default=MEMORY_CONFIG["search"]["default_mode"]),
    intent: Optional[str] = Query(default=None),
    explain: bool = Query(default=False),
    no_track: bool = Query(default=False),
    full: bool = Query(default=False),
):
    """Semantic search - mirrors search.py CLI."""
    # Encode query
    query_embedding = store.model.encode([q], normalize_embeddings=True)
    query_embedding = np.array(query_embedding).astype("float32")

    if mode == "spreading":
        results, meta = _spreading_search(
            q, query_embedding, limit, threshold, intent, explain, not no_track
        )
    else:
        results = _static_search(
            q, query_embedding, limit, threshold, not no_track
        )
        meta = {"mode": "static", "learning_enabled": MEMORY_CONFIG["learning"]["enabled"]}

    return JSONResponse(
        content=json.loads(json.dumps(
            {"query": q, "mode": mode, "results": results, "metadata": meta},
            cls=NumpyEncoder,
        ))
    )


def _static_search(query, query_embedding, limit, threshold, track_usage):
    k = min(limit * 2, store.index.ntotal)
    distances, indices = store.index.search(query_embedding, k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(store.metadata):
            continue
        meta = store.metadata[idx]
        similarity = float(dist)
        if similarity < threshold:
            continue
        results.append({
            "similarity": similarity,
            "title": meta["title"],
            "heading": meta["heading"],
            "filepath": meta["filepath"],
            "note_id": meta["note_id"],
            "content": meta["content"],
        })
        if len(results) >= limit:
            break

    # Q-value adjustment
    if MEMORY_CONFIG["learning"]["enabled"] and results:
        scores = {r["note_id"]: r["similarity"] for r in results}
        adjusted = adjust_scores_with_q_values(scores)
        for r in results:
            r["similarity"] = adjusted.get(r["note_id"], r["similarity"])
        results.sort(key=lambda x: x["similarity"], reverse=True)

    # Log retrieval
    if track_usage and results:
        note_ids = [r["note_id"] for r in results]
        log_retrieval(note_ids, query, intent="static", mode="static")

    return results


def _spreading_search(query, query_embedding, limit, threshold, intent_override, explain, track_usage):
    # Classify intent
    intent_result = classify_intent(query)
    if intent_override:
        try:
            intent_val = QueryIntent(intent_override)
        except ValueError:
            intent_val = intent_result.intent
    else:
        intent_val = intent_result.intent

    # Get seed nodes
    k = min(10, store.index.ntotal)
    distances, indices = store.index.search(query_embedding, k)

    note_scores = {}
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(store.metadata):
            continue
        note_id = store.metadata[idx]["note_id"]
        similarity = float(dist)
        if note_id not in note_scores or similarity > note_scores[note_id]:
            note_scores[note_id] = similarity

    seed_nodes = [(nid, score) for nid, score in note_scores.items() if score >= threshold]

    if not seed_nodes:
        return [], {
            "intent": intent_val.value,
            "confidence": intent_result.confidence,
            "reasoning": intent_result.reasoning,
            "seed_count": 0,
            "iterations": 0,
            "converged": False,
            "learning_enabled": MEMORY_CONFIG["learning"]["enabled"],
        }

    # Spreading activation using in-memory graph
    config = SpreadingConfig.from_intent(intent_val)
    result = spreading_activation(
        store.graph, seed_nodes=seed_nodes, config=config, track_traces=explain
    )

    top_results = get_top_activated(result, store.graph, limit=limit)

    # Q-value adjustment
    if MEMORY_CONFIG["learning"]["enabled"] and top_results:
        scores = {r["note_id"]: r["activation"] for r in top_results}
        adjusted = adjust_scores_with_q_values(scores)
        for r in top_results:
            r["activation"] = adjusted.get(r["note_id"], r["activation"])

    top_results.sort(key=lambda x: x.get("activation", 0), reverse=True)
    top_results = top_results[:limit]

    # Log retrieval
    if track_usage and top_results:
        note_ids = [r["note_id"] for r in top_results]
        log_retrieval(note_ids, query, intent=intent_val.value, mode="spreading")

    meta = {
        "intent": intent_val.value,
        "confidence": intent_result.confidence,
        "reasoning": intent_result.reasoning,
        "seed_count": len(seed_nodes),
        "iterations": result.iterations,
        "converged": result.converged,
        "learning_enabled": MEMORY_CONFIG["learning"]["enabled"],
        "config": {
            "max_iterations": config.max_iterations,
            "inhibition_strength": config.inhibition_strength,
            "temporal_decay": config.temporal_decay,
        },
    }

    if explain and result.traces:
        meta["traces"] = {
            note_id: {
                "path": trace.path,
                "contributing_edges": trace.contributing_edges[:5],
            }
            for note_id, trace in list(result.traces.items())[:5]
        }

    return top_results, meta


# =============================================================================
# CONNECTIONS ENDPOINTS
# =============================================================================

def _find_note_id(query: str) -> Optional[str]:
    """Find note ID by name, title, or partial match."""
    G = store.graph
    query_lower = query.lower()

    if query in G.nodes:
        return query

    for node_id in G.nodes:
        node_data = G.nodes[node_id]
        title = node_data.get("title", "").lower()
        stem = Path(node_id).stem.lower()
        if query_lower == title or query_lower == stem:
            return node_id
        if query_lower in title or query_lower in stem:
            return node_id

    return None


@app.get("/connections")
def connections_endpoint(
    q: str,
    depth: int = Query(default=1),
    semantic_only: bool = Query(default=False),
    explicit_only: bool = Query(default=False),
):
    """Find connections for a note - mirrors connections.py CLI."""
    G = store.graph
    note_id = _find_note_id(q)
    if not note_id:
        return JSONResponse(
            status_code=404,
            content={"error": f"Note not found matching: {q}"},
        )

    include_semantic = not explicit_only
    include_explicit = not semantic_only

    result = {
        "note_id": note_id,
        "title": G.nodes[note_id].get("title", note_id),
        "outgoing": [],
        "incoming": [],
        "semantic": [],
        "paths": {},
    }

    for _, target, data in G.out_edges(note_id, data=True):
        edge_type = data.get("type", "explicit")
        if edge_type == "semantic" and not include_semantic:
            continue
        if edge_type == "explicit" and not include_explicit:
            continue
        result["outgoing"].append({
            "note_id": target,
            "title": G.nodes[target].get("title", target),
            "type": edge_type,
            "weight": data.get("weight", 1.0),
        })

    for source, _, data in G.in_edges(note_id, data=True):
        edge_type = data.get("type", "explicit")
        if edge_type == "semantic" and not include_semantic:
            continue
        if edge_type == "explicit" and not include_explicit:
            continue
        result["incoming"].append({
            "note_id": source,
            "title": G.nodes[source].get("title", source),
            "type": edge_type,
            "weight": data.get("weight", 1.0),
        })

    for _, target, data in G.out_edges(note_id, data=True):
        if data.get("type") == "semantic":
            result["semantic"].append({
                "note_id": target,
                "title": G.nodes[target].get("title", target),
                "similarity": data.get("weight", 0.0),
            })
    result["semantic"].sort(key=lambda x: x["similarity"], reverse=True)

    if depth > 1:
        visited = {note_id}
        current_level = {note_id}
        for d in range(depth):
            next_level = set()
            for node in current_level:
                for neighbor in G.neighbors(node):
                    if neighbor not in visited:
                        next_level.add(neighbor)
                        visited.add(neighbor)
                        try:
                            path = nx.shortest_path(G, note_id, neighbor)
                            if len(path) > 1:
                                result["paths"][neighbor] = {
                                    "path": path,
                                    "length": len(path) - 1,
                                    "title": G.nodes[neighbor].get("title", neighbor),
                                }
                        except nx.NetworkXNoPath:
                            pass
            current_level = next_level

    return JSONResponse(
        content=json.loads(json.dumps(result, cls=NumpyEncoder))
    )


@app.get("/connections/stats")
def stats_endpoint():
    """Graph statistics."""
    G = store.graph
    explicit_edges = sum(1 for _, _, d in G.edges(data=True) if d.get("type") != "semantic")
    semantic_edges = sum(1 for _, _, d in G.edges(data=True) if d.get("type") == "semantic")
    isolated = [n for n in G.nodes if G.degree(n) == 0]
    undirected = G.to_undirected()
    components = list(nx.connected_components(undirected))

    stats = {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "explicit_edges": explicit_edges,
        "semantic_edges": semantic_edges,
        "isolated_nodes": len(isolated),
        "connected_components": len(components),
        "largest_component": len(max(components, key=len)) if components else 0,
        "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
    }
    return JSONResponse(content=json.loads(json.dumps(stats, cls=NumpyEncoder)))


@app.get("/connections/hubs")
def hubs_endpoint(top_n: int = Query(default=20)):
    """Find hub notes."""
    G = store.graph
    degree_centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)

    hubs = []
    for node_id, centrality in sorted_nodes[:top_n]:
        node_data = G.nodes[node_id]
        hubs.append({
            "note_id": node_id,
            "title": node_data.get("title", node_id),
            "centrality": centrality,
            "in_degree": G.in_degree(node_id),
            "out_degree": G.out_degree(node_id),
            "total_degree": G.in_degree(node_id) + G.out_degree(node_id),
        })
    return JSONResponse(content=json.loads(json.dumps(hubs, cls=NumpyEncoder)))


@app.get("/connections/bridges")
def bridges_endpoint(top_n: int = Query(default=20)):
    """Find bridge notes."""
    G = store.graph
    betweenness = nx.betweenness_centrality(G)
    sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)

    bridges = []
    for node_id, centrality in sorted_nodes[:top_n]:
        if centrality > 0:
            node_data = G.nodes[node_id]
            bridges.append({
                "note_id": node_id,
                "title": node_data.get("title", node_id),
                "betweenness": centrality,
            })
    return JSONResponse(content=json.loads(json.dumps(bridges, cls=NumpyEncoder)))


# =============================================================================
# MANAGEMENT ENDPOINTS
# =============================================================================

@app.get("/health")
def health():
    """Health check."""
    return {
        "status": "ok",
        "loaded_at": store.loaded_at,
        "chunks": store.index.ntotal if store.index else 0,
        "nodes": store.graph.number_of_nodes() if store.graph else 0,
        "edges": store.graph.number_of_edges() if store.graph else 0,
    }


@app.post("/reload")
def reload():
    """Reload all data from disk."""
    store.reload()
    return {"status": "reloaded", "loaded_at": store.loaded_at}


# =============================================================================
# MAIN
# =============================================================================

PORT = int(os.environ.get("BRAIN_DAEMON_PORT", "7437"))
PID_FILE = PROJECT_DIR / "daemon.pid"


if __name__ == "__main__":
    import uvicorn

    # Write PID file
    PID_FILE.write_text(str(os.getpid()))

    try:
        uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
    finally:
        if PID_FILE.exists():
            PID_FILE.unlink()
