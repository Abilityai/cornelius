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
from typing import NamedTuple
import os

# =============================================================================
# BASE PATHS
# =============================================================================

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
BRAIN_PATH = Path(os.environ.get("BRAIN_PATH", PROJECT_DIR.parent.parent / "Brain"))

# =============================================================================
# SCOPE PRIMITIVE
# A note's scope is its top-level folder, already encoded in its note_id
# (the POSIX path relative to BRAIN_PATH, e.g. "02-Permanent/Foo.md").
# `core` is the curated cognitive-fingerprint corpus; everything else is
# mounted on demand. Read / learn / fingerprint each respect scope.
# This is the canonical home for the PURE primitives (no faiss/networkx here);
# the FAISS IDSelector glue lives in scope.py.
# =============================================================================

# -----------------------------------------------------------------------------
# Scope registry - the "add a new scope TYPE" capability
#
# A scope is a top-level Brain/ folder. Every scope has a KIND that decides how
# the epistemic machinery treats it:
#
#   cognitive - claims / insights. Additive, lifecycle-governed (reflective ->
#               crystallizing -> generative), crystallizable; provenance is one
#               of originated/endorsed/encountered/ai-inferred. The CORE subset
#               (the curated cognitive fingerprint) trains q-values and shapes
#               hubs/centrality. Non-core cognitive folders are encountered
#               material + operational exhaust (read-isolated, learn-gated,
#               fingerprint-excluded by the scope primitive).
#   reference - external facts / records (employees, products, clients,
#               contracts). NOT claims: mutable/overwrite-in-place, provenance
#               `reference`, opted OUT of lifecycle / crystallization / the
#               synthesis pulse, recency beats age. Reference scopes are non-core
#               by construction, so the read-mask / learn-gate / fingerprint-
#               exclusion already cover them for free; the `reference` kind only
#               adds the epistemic opt-out the BDG + crystallize/graduate skills
#               consult (is_reference_scope) and a default `reference` provenance.
#
# Adding a scope = ONE ScopeDef below (built-in) or one register_scope() call
# (a layer/deployment adding its own, e.g. a per-tenant reference scope). The
# derived CORE_FOLDERS / SCOPE_TOKEN_MAP are rebuilt from this list, so the pure
# primitives (resolve_read_scope, is_pure_core, scope_of) never change. Folder
# strings are EXACT (note the spaces in "AI Extracted Notes" - no folder slug).
# -----------------------------------------------------------------------------

SCOPE_KIND_COGNITIVE = "cognitive"
SCOPE_KIND_REFERENCE = "reference"
SCOPE_KINDS = frozenset({SCOPE_KIND_COGNITIVE, SCOPE_KIND_REFERENCE})


class ScopeDef(NamedTuple):
    """One scope: its exact top-folder name, kind, core membership, env slugs."""
    folder: str               # first path segment of a note_id
    kind: str                 # SCOPE_KIND_COGNITIVE | SCOPE_KIND_REFERENCE
    core: bool                # part of the curated cognitive fingerprint
    slugs: tuple = ()         # lowercase env/CLI aliases -> folder
    family: bool = False      # a FAMILY folder yields a sub-scope per child (Books/<slug>)


SCOPE_REGISTRY = [
    # --- core cognitive (the curated fingerprint) ----------------------------
    ScopeDef("02-Permanent",       SCOPE_KIND_COGNITIVE, True,  ("permanent", "02-permanent")),
    ScopeDef("03-MOCs",            SCOPE_KIND_COGNITIVE, True,  ("mocs", "03-mocs")),
    ScopeDef("AI Extracted Notes", SCOPE_KIND_COGNITIVE, True,  ("ai-extracted", "ai extracted notes")),
    ScopeDef("01-Sources",         SCOPE_KIND_COGNITIVE, True,  ("sources", "01-sources")),
    # --- non-core cognitive (encountered material + operational exhaust) ------
    ScopeDef("Document Insights",  SCOPE_KIND_COGNITIVE, False, ("document-insights", "document insights")),
    ScopeDef("05-Meta",            SCOPE_KIND_COGNITIVE, False, ("meta", "05-meta")),
    ScopeDef("00-Inbox",           SCOPE_KIND_COGNITIVE, False, ("inbox", "00-inbox")),
    ScopeDef("04-Output",          SCOPE_KIND_COGNITIVE, False, ("output", "04-output")),
    # --- non-core cognitive scope FAMILY (per-book sub-scopes: Books/<slug>) ---
    # A FAMILY folder yields one sub-scope per child folder: Books/atomic-habits is
    # its own pluggable scope, distinct from Books/superforecasting. Books are claims
    # (cognitive: lifecycle/crystallization-eligible, the gems graduate to core via
    # the human /graduate-insights act) but NON-CORE - they never shape the published
    # fingerprint or train q-values. Mount one book with BRAIN_READ_SCOPE=core,Books/
    # <slug>; mount the whole shelf with core,Books. scope_of() stays the top folder
    # ("Books") so the registry-KIND lookups resolve a book note to cognitive; the
    # fine-grained per-book scope is scope_id() and only the read-membership predicate
    # in_read_scope() is family-aware. See scope_id / in_read_scope below.
    ScopeDef("Books",              SCOPE_KIND_COGNITIVE, False, ("books",), family=True),
    # --- reference scope FAMILY (external facts/records; connection targets) ---
    # First reference scope: the company brain. A FAMILY (like Books) - each child
    # folder (Company/people, Company/orgs, Company/products, Company/engagements,
    # Company/market) is its own pluggable sub-scope, mountable alone
    # (core,Company/orgs) or whole (core,Company). scope_of() stays "Company" so
    # every child resolves to the reference KIND (epistemic opt-out); scope_id()
    # gives the per-child mount. A CRM still owns queries; this is a layer of
    # insight/connection targets the personal brain discovers bridges to.
    # See resources/layered-brains/COMPANY-BRAIN-SCHEMA.md + manage-reference-data.
    ScopeDef("Company",            SCOPE_KIND_REFERENCE, False, ("company",), family=True),
    # --- reference scope: CANON (the org's DECIDED direction, git-mirrored) -----
    # Second reference scope, and a different shape from Company: not entity-shaped
    # and not a family - a FLAT mirror of a fixed document surface (the canon-proper
    # files in your-org/source-of-truth). Notes are overwritten in place by the
    # `canon-sync` playbook from a gitignored sidecar clone; each carries canon_commit/
    # canon_path/canon_surface (decision|bet|spec) on top of the reference contract.
    # Reference KIND gives the epistemic opt-out for free (never crystallized/lifecycle/
    # q-trained/fingerprinted/default-mounted); the one thing the kind does NOT give -
    # authority ranking on direction questions - is a skill-level rule, not an engine
    # change (CLAUDE.md canon section §5.3). Mount with BRAIN_READ_SCOPE=core,Canon.
    # See resources/layered-brains/CANON-SCOPE-SCHEMA.md + the canon-sync playbook.
    ScopeDef("Canon",              SCOPE_KIND_REFERENCE, False, ("canon",)),
    # --- reference scope FAMILY: DemoCRM (fake CRM demo data) -------------------
    # A self-contained, obviously-fake CRM used to demonstrate the reference-scope
    # primitive on entity+relationship data WITHOUT touching the real Company scope.
    # A FAMILY like Company: each child (DemoCRM/people, /orgs, /leads,
    # /opportunities) is its own mountable sub-scope; relations are wiki-links that
    # join them (person→org, opportunity→org×person×owner, lead→converts_to→opp).
    # Non-core reference kind → provenance:reference, fingerprint-excluded, no
    # q-learning, never crystallized/lifecycle-classified, mounted on demand only
    # (BRAIN_READ_SCOPE=core,DemoCRM for all, core,DemoCRM/opportunities for one).
    # See resources/layered-brains/DEMO-CRM-SCHEMA.md.
    ScopeDef("DemoCRM",            SCOPE_KIND_REFERENCE, False, ("demo-crm", "democrm"), family=True),
    # --- reference scope: THINKERS (external minds worth modeling) --------------
    # FLAT (like Canon, unlike Company): one note per thinker, no sub-scopes. Holds
    # *character notes* - who a thinker is, their signature analytical move, scored
    # track record, epistemic style and characteristic error mode. These are FACTS
    # ABOUT A PERSON (mutable, as_of-stamped, overwrite-in-place), NOT their ideas:
    # a thinker's actual claims live as `encountered` notes in Document Insights/
    # (or a Books/<slug> scope), and only cross into endorsed knowledge through
    # the user's own /graduate-insights act. Keeping the two apart is what stops
    # "Cornelius knows how Aschenbrenner thinks" from decaying into "Cornelius
    # thinks what Aschenbrenner thinks".
    # Reference KIND gives the epistemic opt-out for free (never crystallized /
    # lifecycle-classified / q-trained / fingerprint-shaping / default-mounted).
    # Mount with BRAIN_READ_SCOPE=core,Thinkers.
    # See resources/layered-brains/THINKERS-SCOPE-SCHEMA.md.
    ScopeDef("Thinkers",           SCOPE_KIND_REFERENCE, False, ("thinkers", "minds")),
]


def _build_token_map(registry):
    """Build the {slug.lower(): folder} env/CLI alias map from a registry list.

    "core" is intentionally NOT a key here - it is a meta-token expanded by
    resolve_read_scope() into CORE_FOLDERS. Unknown tokens pass through verbatim
    (treated as literal folder names) so a real folder is never silently
    dropped; there is deliberately NO token meaning "all".
    """
    token_map = {}
    for d in registry:
        for slug in d.slugs:
            token_map[slug.lower()] = d.folder
    return token_map


# Derived from SCOPE_REGISTRY - DO NOT edit by hand; add a ScopeDef above.
# CORE_FOLDERS is computed once at import and stays a stable frozenset (other
# modules `from memory_config import CORE_FOLDERS`; runtime core-widening is
# deliberately impossible - see register_scope). SCOPE_TOKEN_MAP is a live dict
# mutated in place by register_scope so the in-module resolver sees new slugs.
_SCOPE_BY_FOLDER = {d.folder: d for d in SCOPE_REGISTRY}
CORE_FOLDERS = frozenset(d.folder for d in SCOPE_REGISTRY if d.core)
SCOPE_TOKEN_MAP = _build_token_map(SCOPE_REGISTRY)
# Folders whose children are each their own scope (e.g. "Books"). Frozen at import,
# parallel to CORE_FOLDERS: register_scope() never adds a family (it builds non-family
# ScopeDefs), so families are declared in the SCOPE_REGISTRY literal above only.
SCOPE_FAMILIES = frozenset(d.folder for d in SCOPE_REGISTRY if d.family)


def scope_of(note_id) -> str:
    """A note's scope = its top-level folder.

    note_id is the POSIX path relative to BRAIN_PATH (index_brain.get_note_id).
    Root-level files (e.g. "README.md") have no folder; their scope is the
    filename itself, which is therefore never in CORE_FOLDERS (correct: not
    core). Backslashes are normalized so a Windows-built index can't break it.
    """
    return str(note_id).replace("\\", "/").split("/", 1)[0]


def scope_id(note_id) -> str:
    """A note's FINE-GRAINED scope: two segments under a scope FAMILY, else its folder.

    For most notes this equals scope_of() (the top folder). For a note under a
    registered family folder (SCOPE_FAMILIES, e.g. "Books"), the scope is the first
    TWO segments - so "Books/atomic-habits/ch1.md" is the scope "Books/atomic-habits"
    (its own pluggable sub-scope). A loose file directly under the family root
    ("Books/loose.md") degrades to "Books/loose.md".

    scope_of() and the registry-KIND helpers deliberately keep using the top folder,
    so a book note still resolves to the "Books" ScopeDef (cognitive). Backslashes are
    normalized so a Windows-built index can't break it.
    """
    parts = str(note_id).replace("\\", "/").split("/")
    if parts[0] in SCOPE_FAMILIES and len(parts) >= 2:
        return parts[0] + "/" + parts[1]
    return parts[0]


def in_read_scope(note_id, read_scope) -> bool:
    """THE canonical read-membership predicate: is this note visible under read_scope?

    Family-aware: a book note "Books/atomic-habits/ch1.md" is in scope when read_scope
    contains its fine-grained scope ("Books/atomic-habits", a per-book mount) OR the
    family folder ("Books", the whole-shelf mount). For every non-family note
    scope_id == scope_of, so this is exactly `scope_of(note_id) in read_scope` and is
    byte-identical to the pre-family behavior.

    Use this anywhere a read is gated by scope (FAISS row-mask, subgraph node filter,
    visualization render gate). Do NOT hand-roll `scope_of(x) in read_scope` - that
    silently drops per-book-mounted notes.

    read_scope MUST be a resolved set. A raw mount STRING (e.g. "core,Company/people")
    is coerced via resolve_read_scope first: without this, `in` does substring matching,
    so scope_of=="Company" would spuriously match the substring "Company" inside
    "core,Company/people" and leak every sibling sub-scope (a silent isolation break).
    """
    if isinstance(read_scope, str):
        read_scope = resolve_read_scope(read_scope)
    return scope_id(note_id) in read_scope or scope_of(note_id) in read_scope


def resolve_read_scope(raw=None) -> frozenset:
    """Resolve the active read-scope to a set of top folders. FAIL-CLOSED.

    raw is None  -> read os.environ["BRAIN_READ_SCOPE"] (CLI / fresh process).
    raw is a str -> parse it directly (daemon per-request param).

    Rules:
      - None / "" / whitespace            -> CORE_FOLDERS
      - comma-separated tokens; "core" expands to CORE_FOLDERS
      - slugs map via SCOPE_TOKEN_MAP; unknown tokens pass through verbatim
      - there is NO token meaning "all"; the only way to widen is to name
        folders explicitly. You can never accidentally un-scope the whole brain.
    """
    if raw is None:
        raw = os.environ.get("BRAIN_READ_SCOPE", "")
    if raw is None or not str(raw).strip():
        return CORE_FOLDERS
    folders = set()
    for tok in str(raw).split(","):
        t = tok.strip()
        if not t:
            continue
        if t.lower() == "core":
            folders |= set(CORE_FOLDERS)
        else:
            folders.add(SCOPE_TOKEN_MAP.get(t.lower(), t))
    return frozenset(folders) if folders else CORE_FOLDERS


def is_pure_core(scope) -> bool:
    """THE canonical pure-core predicate (learn-gate + any default-scope check).

    True iff the read-scope is exactly the core set (nothing mounted). Note the
    literal alias string {"core"} is NOT pure core - resolve_read_scope expands
    "core" first, so the comparison is always against the four folder names.
    Comparing against {"core"} directly would never fire: the documented #1
    silent-failure hazard.
    """
    return frozenset(scope) == CORE_FOLDERS


# --- scope KIND helpers (the reference-vs-cognitive axis) --------------------
# These read the registry, not the retrieval engine. A reference scope is non-
# core by construction, so read/learn/fingerprint already exclude it; these
# predicates are the hook the BDG + crystallize/graduate skills consult to apply
# the epistemic opt-out (no lifecycle, no crystallization, no synthesis pulse,
# provenance: reference). Folder-or-note_id in, normalized via scope_of.

def scope_def(folder_or_note_id):
    """The ScopeDef for a folder (or a note_id's folder), or None if unregistered."""
    return _SCOPE_BY_FOLDER.get(scope_of(folder_or_note_id))


def scope_kind(folder_or_note_id) -> str:
    """Kind of a scope: 'cognitive' | 'reference' | 'unknown'.

    Unregistered (ad-hoc) folders are 'unknown' - the epistemic machinery
    neither governs nor exempts them. They are still non-core unless their name
    is literally in CORE_FOLDERS, so retrieval scoping is unaffected either way.
    """
    d = _SCOPE_BY_FOLDER.get(scope_of(folder_or_note_id))
    return d.kind if d is not None else "unknown"


def is_reference_scope(folder_or_note_id) -> bool:
    """True iff this is a registered REFERENCE-kind scope (external facts/records).

    Reference scopes opt OUT of the epistemic machinery: never crystallized,
    lifecycle-classified, or used as a synthesis-pulse source; new notes default
    to provenance: reference; recency beats age. They are ALSO non-core, so the
    read-mask / learn-gate / fingerprint-exclusion already cover them - this is
    the hook for the opt-out the engine cannot express (lifecycle lives in the
    BDG; crystallization lives in skills).
    """
    return scope_kind(folder_or_note_id) == SCOPE_KIND_REFERENCE


def reference_folders() -> frozenset:
    """The set of registered reference-kind folder names."""
    return frozenset(d.folder for d in SCOPE_REGISTRY if d.kind == SCOPE_KIND_REFERENCE)


def scope_default_provenance(folder_or_note_id):
    """Default `provenance:` for a NEW note in this scope, or None to defer.

    Reference scopes pin 'reference' (records, never 'originated'). Cognitive
    scopes return None: the writing skill decides (encountered for external
    extractions, ai-inferred for AI synthesis), and the encountered->endorsed
    boundary stays a human act.
    """
    return "reference" if is_reference_scope(folder_or_note_id) else None


def register_scope(folder, kind=SCOPE_KIND_REFERENCE, core=False, slugs=()):
    """Register a new scope at runtime - the 'add a new scope TYPE' capability.

    The SCOPE_REGISTRY literal is the source of truth for built-in scopes; this
    lets a layer/deployment add its own (e.g. a per-tenant reference scope)
    without editing this module. Returns the ScopeDef; re-registering an
    existing folder replaces its def (idempotent).

    FAIL-CLOSED: refuses to add a CORE scope at runtime. CORE_FOLDERS is the
    published fingerprint, frozen at import; a runtime core-widen would also
    strand every `from memory_config import CORE_FOLDERS` snapshot. Declare core
    scopes in SCOPE_REGISTRY and reindex instead.
    """
    if core:
        raise ValueError(
            "register_scope cannot add a CORE scope at runtime; declare it in "
            "SCOPE_REGISTRY and reindex (CORE_FOLDERS is frozen at import)."
        )
    if kind not in SCOPE_KINDS:
        raise ValueError(
            f"unknown scope kind {kind!r}; expected one of {sorted(SCOPE_KINDS)}"
        )
    d = ScopeDef(folder, kind, False, tuple(slugs))
    global SCOPE_REGISTRY
    SCOPE_REGISTRY = [x for x in SCOPE_REGISTRY if x.folder != folder] + [d]
    _SCOPE_BY_FOLDER[folder] = d                       # in-place: live references hold
    for slug in d.slugs:
        SCOPE_TOKEN_MAP[slug.lower()] = folder         # in-place: resolver sees new slugs
    return d


# Read-only scoped subgraph view for the spreading walk + fingerprint axis.
# Cached per (graph identity, edge count, scope) so a reloaded/changed graph
# never serves a stale view. No networkx import needed - G.subgraph is a method
# on the passed graph object.
_SCOPED_SUBGRAPH_CACHE = {}


def scoped_subgraph(G, read_scope):
    """Read-only view of G restricted to nodes whose scope is in read_scope."""
    key = (id(G), G.number_of_edges(), frozenset(read_scope))
    cached = _SCOPED_SUBGRAPH_CACHE.get(key)
    if cached is not None:
        return cached
    nodes = [n for n in G.nodes if in_read_scope(n, read_scope)]
    H = G.subgraph(nodes)
    _SCOPED_SUBGRAPH_CACHE[key] = H
    return H


def core_subgraph(G):
    """Convenience: scoped_subgraph(G, CORE_FOLDERS) - the fingerprint view."""
    return scoped_subgraph(G, CORE_FOLDERS)


def clear_scoped_subgraph_cache():
    """Invalidate the subgraph cache (call at every graph-reload site)."""
    _SCOPED_SUBGRAPH_CACHE.clear()

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
        "manifest": DATA_DIR / "manifest.json",  # Build provenance stamp (edge formula, builder version)
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
        "excluded_folders": ["templates", ".obsidian", ".trash", "Reports", "AI Crystallizations", "Projects", "Lenses"],  # Projects: project specs (2026-09-08); Lenses: segregated ai-inferred interpretive store (2026-09-13), same policy as Reports
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

    # -------------------------------------------------------------------------
    # SCOPE ENFORCEMENT (transitional rollout flag - SCOPE-IMPLEMENTATION-PLAN.md)
    # Master switch for the scope primitive's BEHAVIORAL changes: fingerprint-on-
    # core (Phase 3), and read-mask + learn-gate (Phase 4). While False, every
    # scope edit is a no-op and retrieval is byte-identical to the pre-scope
    # system. The Phase 4e cutover = flip this to True + RESTART the daemon;
    # rollback = flip it back + restart. The dist-fix/reindex (Phase 3 steps 1-3)
    # is NOT gated here - it is an unconditional correctness fix to edge weights.
    # -------------------------------------------------------------------------
    "scope": {
        "enforce": True,  # Phase 4e cutover 2026-06-25: read-mask + learn-gate + core fingerprint now LIVE. Rollback = set False + restart daemon.
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

# Build provenance: bump BUILDER_VERSION whenever indexing or edge logic changes.
# EDGE_FORMULA documents the cosine convention the persisted graph was built with.
MANIFEST_PATH = MEMORY_CONFIG["paths"]["manifest"]
EDGE_FORMULA = "cosine_ip"  # IndexFlatIP inner product == cosine (float(dist)); prior corrupt builds were effectively "inv_l2" (1 - dist/2)
BUILDER_VERSION = 2  # v1 = inverted-distance semantic edges; v2 = float(dist) cosine edges


def scope_enforced() -> bool:
    """Live read of the transitional scope-enforcement flag (Phase 4e cutover).

    Read live (not snapshotted at import) so the one-line flip of
    MEMORY_CONFIG['scope']['enforce'] takes effect on the next call in a fresh
    process. The daemon is long-lived and re-imports only on RESTART, so its
    cutover still requires a restart - per the rollout contract.
    """
    return bool(MEMORY_CONFIG["scope"]["enforce"])


# Documented alias from the implementation plan. SNAPSHOT at import time - do NOT
# use it for live gating (it cannot see a runtime flip). Every behavior gate must
# call scope_enforced() instead. Kept for greppability / parity with the plan.
SCOPE_ENFORCE = MEMORY_CONFIG["scope"]["enforce"]

# Scope primitive (defined near the top of this module): the SCOPE_REGISTRY +
# ScopeDef + SCOPE_KIND_* registry; derived CORE_FOLDERS / SCOPE_TOKEN_MAP /
# SCOPE_FAMILIES; scope_of(), scope_id() (fine-grained, family-aware),
# in_read_scope() (THE canonical read-membership predicate), resolve_read_scope(),
# is_pure_core(); the kind helpers scope_kind()/is_reference_scope()/
# reference_folders()/scope_default_provenance()/scope_def()/register_scope();
# scoped_subgraph()/core_subgraph()/clear_scoped_subgraph_cache() - all import directly.


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
