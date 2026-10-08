#!/usr/bin/env python3
"""
Create a frozen Brain snapshot for reproducible benchmarking.

Usage:
    python create_snapshot.py [--date YYYY-MM-DD] [--force]

The snapshot includes:
- Copy of Brain folder (excluding .obsidian, .trash)
- FAISS index built from the snapshot
- Metadata and graph pickles
- SNAPSHOT-INFO.md with details
"""
import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_DIR = SKILL_DIR.parent.parent.parent  # .claude/skills/benchmark-memory -> .claude/skills -> .claude -> project root
SNAPSHOTS_DIR = SKILL_DIR / "snapshots"
MEMORY_SYSTEM_DIR = PROJECT_DIR / "resources" / "local-brain-search"
DEFAULT_BRAIN_PATH = PROJECT_DIR / "Brain"


def create_snapshot(
    brain_path: Path,
    snapshot_date: str,
    force: bool = False,
) -> Path:
    """Create a frozen Brain snapshot with index."""

    snapshot_name = f"brain-snapshot-{snapshot_date}"
    snapshot_dir = SNAPSHOTS_DIR / snapshot_name

    # Check if snapshot already exists
    if snapshot_dir.exists():
        if force:
            print(f"Removing existing snapshot: {snapshot_dir}")
            shutil.rmtree(snapshot_dir)
        else:
            print(f"Error: Snapshot already exists: {snapshot_dir}")
            print("Use --force to overwrite")
            sys.exit(1)

    # Create directories
    print(f"\n=== Creating snapshot: {snapshot_name} ===\n")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_brain = snapshot_dir / "Brain"
    snapshot_data = snapshot_dir / "data"
    snapshot_data.mkdir(exist_ok=True)

    # Copy Brain folder (excluding .obsidian, .trash)
    print(f"Copying Brain from: {brain_path}")
    print(f"           To: {snapshot_brain}")

    excludes = [".obsidian", ".trash", ".DS_Store"]

    def ignore_patterns(directory, files):
        return [f for f in files if f in excludes]

    shutil.copytree(
        brain_path,
        snapshot_brain,
        ignore=ignore_patterns,
        dirs_exist_ok=True,
    )

    # Count files
    md_files = list(snapshot_brain.rglob("*.md"))
    print(f"Copied {len(md_files)} markdown files")

    # Build index for snapshot
    print(f"\nBuilding FAISS index for snapshot...")

    # We need to run index_brain.py with custom paths
    index_script = MEMORY_SYSTEM_DIR / "index_brain.py"

    if not index_script.exists():
        print(f"Error: Index script not found at {index_script}")
        sys.exit(1)

    # Set environment variable for Brain path and run indexer
    import os
    env = os.environ.copy()
    env["BRAIN_PATH"] = str(snapshot_brain)

    # Use the venv Python from memory system
    venv_python = MEMORY_SYSTEM_DIR / "venv" / "bin" / "python"
    if not venv_python.exists():
        print(f"Error: venv Python not found at {venv_python}")
        print("Run 'python -m venv venv && pip install -r requirements.txt' in local-brain-search/")
        sys.exit(1)

    # Create a temporary config override
    # We'll use subprocess to run the indexer with modified paths
    result = subprocess.run(
        [
            str(venv_python),
            "-c",
            f"""
import sys
sys.path.insert(0, '{MEMORY_SYSTEM_DIR}')

from pathlib import Path
import pickle
import faiss
import networkx as nx
import numpy as np
from sentence_transformers import SentenceTransformer

# Override paths
BRAIN_PATH = Path('{snapshot_brain}')
DATA_DIR = Path('{snapshot_data}')

# Import indexing functions
from index_brain import (
    collect_notes,
    chunk_by_headings,
    build_explicit_graph,
    add_semantic_edges,
)
from memory_config import MEMORY_CONFIG

# Override BRAIN_PATH in the module
import index_brain
import config
index_brain.BRAIN_PATH = BRAIN_PATH
config.BRAIN_PATH = BRAIN_PATH

from config import EMBEDDING_MODEL, EMBEDDING_DIM

print("Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

print("Collecting notes...")
notes = collect_notes()
print(f"Found {{len(notes)}} notes")

# Chunk notes (following the exact pattern from index_brain.py)
print("Chunking by headings...")
all_chunks = []
metadata = []
for note in notes:
    chunks = chunk_by_headings(note['content'], note['filepath'])
    for j, chunk in enumerate(chunks):
        all_chunks.append(chunk['content'])
        metadata.append({{
            'note_id': note['note_id'],
            'title': note['title'],
            'heading': chunk['heading'],
            'filepath': str(note['filepath']),
            'content_hash': note['content_hash'],
            'chunk_index': j,
            'content': chunk['content'],
        }})

print(f"Created {{len(all_chunks)}} chunks")

# Create embeddings
print("Creating embeddings...")
embeddings = model.encode(all_chunks, show_progress_bar=True, normalize_embeddings=True)
embeddings = np.array(embeddings).astype('float32')

# Build FAISS index
print("Building FAISS index...")
index = faiss.IndexFlatIP(EMBEDDING_DIM)
index.add(embeddings)

# Build graph
print("Building knowledge graph...")
G = build_explicit_graph(notes)

# Add semantic edges (using updated signature)
print("Adding semantic edges...")
add_semantic_edges(G, index, metadata, notes, embeddings)

# Save everything
print(f"Saving to {{DATA_DIR}}...")
faiss.write_index(index, str(DATA_DIR / 'brain.faiss'))
with open(DATA_DIR / 'brain_metadata.pkl', 'wb') as f:
    pickle.dump(metadata, f)
with open(DATA_DIR / 'brain_graph.pkl', 'wb') as f:
    pickle.dump(G, f)

print(f"Index: {{index.ntotal}} vectors")
print(f"Graph: {{G.number_of_nodes()}} nodes, {{G.number_of_edges()}} edges")
print("Done!")
"""
        ],
        cwd=MEMORY_SYSTEM_DIR,
        capture_output=True,
        text=True,
        env=env,
    )

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    if result.returncode != 0:
        print(f"Error building index: {result.returncode}")
        sys.exit(1)

    # Create SNAPSHOT-INFO.md
    info_path = snapshot_dir / "SNAPSHOT-INFO.md"
    info_content = f"""# Snapshot Information

**Name:** {snapshot_name}
**Created:** {datetime.now().isoformat()}
**Source:** {brain_path}

## Statistics

- **Markdown files:** {len(md_files)}
- **Index vectors:** (see data/brain.faiss)
- **Graph nodes:** (see data/brain_graph.pkl)

## Files

```
{snapshot_name}/
├── Brain/           # Frozen copy of Brain folder
├── data/
│   ├── brain.faiss          # FAISS index
│   ├── brain_metadata.pkl   # Chunk metadata
│   └── brain_graph.pkl      # Knowledge graph
└── SNAPSHOT-INFO.md         # This file
```

## Usage

Use this snapshot with benchmark-memory:

```bash
python run_benchmark.py --snapshot {snapshot_name}
```
"""
    info_path.write_text(info_content)

    print(f"\n=== Snapshot created successfully ===")
    print(f"Location: {snapshot_dir}")
    print(f"Info: {info_path}")

    return snapshot_dir


def list_snapshots() -> list[Path]:
    """List all available snapshots."""
    if not SNAPSHOTS_DIR.exists():
        return []
    return sorted([d for d in SNAPSHOTS_DIR.iterdir() if d.is_dir()])


def main():
    parser = argparse.ArgumentParser(
        description="Create a frozen Brain snapshot for benchmarking"
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Snapshot date (default: today)",
    )
    parser.add_argument(
        "--brain",
        type=Path,
        default=DEFAULT_BRAIN_PATH,
        help=f"Path to Brain folder (default: {DEFAULT_BRAIN_PATH})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing snapshot",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available snapshots",
    )

    args = parser.parse_args()

    if args.list:
        snapshots = list_snapshots()
        if snapshots:
            print("Available snapshots:")
            for s in snapshots:
                print(f"  - {s.name}")
        else:
            print("No snapshots found")
        return

    if not args.brain.exists():
        print(f"Error: Brain folder not found: {args.brain}")
        sys.exit(1)

    create_snapshot(args.brain, args.date, args.force)


if __name__ == "__main__":
    main()
