#!/usr/bin/env python3
"""
Representational redundancy metric ("crowding").

Answers: are the notes in a scope spreading out, or piling onto the same ideas?

Motivation (2026-08-12, from Spisak & Friston, arXiv:2505.22749 - see
Brain/Document Insights/2026-08-12 Self-Orthogonalizing Attractor Networks (FEP)/):
a store that jointly optimizes predictive accuracy AND model complexity spreads
its representations apart, because overlapping representations blur into each
other. A knowledge base does not optimize anything - so this is a DIAGNOSTIC,
not a mechanism claim. It measures whether accumulation is outpacing digestion.

The measure: mean cosine similarity between each note and its NEAREST neighbour
within the same scope (NN1). Note-level vectors are the mean of a note's chunk
vectors, renormalized.

WHY MATCHED-n IS MANDATORY
--------------------------
Raw NN1 rises with note count for free: more notes means a closer nearest
neighbour, redundancy or not. A raw NN1 time series over a growing vault
therefore ALWAYS trends up and means nothing. Every reported figure here is
computed on random subsamples of a FIXED size (REF_N), averaged over REPS draws,
so values are comparable across scopes and across time. Raw NN1 is also emitted,
clearly labelled, for reference only - never compare it across scopes or dates.

Mean PAIRWISE similarity is deliberately not reported: in 384 dimensions it sits
at ~0.000 for every scope and carries no signal.

Usage:
    python redundancy.py                 # report + append to history
    python redundancy.py --no-write      # report only
    python redundancy.py --json          # machine-readable
    python redundancy.py --ref-n 250     # different matched sample size
"""

import argparse
import json
import pickle
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import faiss
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory_config import CORE_FOLDERS  # noqa: E402

DATA = SCRIPT_DIR / "data"
INDEX_PATH = DATA / "brain.faiss"
META_PATH = DATA / "brain_metadata.pkl"
MANIFEST_PATH = DATA / "manifest.json"
HISTORY_PATH = DATA / "redundancy_history.jsonl"

REF_N = 300      # matched sample size; scopes smaller than this report null
REPS = 20        # subsample repetitions averaged per figure
SEED = 20260812  # fixed so runs are reproducible

# Scopes worth tracking individually, beyond the aggregate core figure.
TRACKED = [
    "02-Permanent",
    "AI Extracted Notes",
    "01-Sources",
    "03-MOCs",
    "Document Insights",
    "Books",
    "05-Meta",
]


def note_vectors():
    """Note-level unit vectors (mean of chunk vectors) + their scope."""
    meta = pickle.load(open(META_PATH, "rb"))
    idx = faiss.read_index(str(INDEX_PATH))
    V = idx.reconstruct_n(0, idx.ntotal).astype("float32")
    faiss.normalize_L2(V)

    acc = defaultdict(lambda: np.zeros(idx.d, dtype="float32"))
    cnt = defaultdict(int)
    scope = {}
    for i, m in enumerate(meta):
        nid = m["note_id"]
        acc[nid] += V[i]
        cnt[nid] += 1
        scope[nid] = nid.split("/")[0] if "/" in nid else nid

    ids = list(acc.keys())
    M = np.stack([acc[n] / cnt[n] for n in ids]).astype("float32")
    faiss.normalize_L2(M)
    return ids, M, scope, idx.d


def nn1(X, dim):
    """Mean similarity from each row to its nearest other row."""
    ix = faiss.IndexFlatIP(dim)
    ix.add(X)
    D, _ = ix.search(X, 2)
    return float(D[:, 1].mean())


def matched_nn1(X, dim, ref_n, reps, rng):
    """NN1 on random subsamples of exactly ref_n rows. Returns (mean, std)."""
    n = X.shape[0]
    if n < ref_n:
        return None, None
    vals = [nn1(X[rng.choice(n, ref_n, replace=False)], dim) for _ in range(reps)]
    return float(np.mean(vals)), float(np.std(vals))


def measure(ref_n=REF_N, reps=REPS):
    ids, M, scope, dim = note_vectors()
    rng = np.random.default_rng(SEED)

    def block(mask):
        X = M[mask]
        n = int(X.shape[0])
        if n < 2:
            return {"n": n, "matched_nn1": None, "matched_std": None, "raw_nn1": None}
        mean, std = matched_nn1(X, dim, ref_n, reps, rng)
        return {"n": n, "matched_nn1": mean, "matched_std": std, "raw_nn1": nn1(X, dim)}

    scopes = {"CORE": block(np.array([scope[i] in CORE_FOLDERS for i in ids]))}
    for f in TRACKED:
        scopes[f] = block(np.array([scope[i] == f for i in ids]))

    build = {}
    if MANIFEST_PATH.exists():
        try:
            m = json.load(open(MANIFEST_PATH))
            build = {k: m.get(k) for k in ("builder_version", "edge_formula") if k in m}
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "total_notes": len(ids),
        "ref_n": ref_n,
        "reps": reps,
        "build": build,
        "scopes": scopes,
    }


def previous():
    if not HISTORY_PATH.exists():
        return None
    prev = None
    for line in open(HISTORY_PATH):
        line = line.strip()
        if line:
            try:
                prev = json.loads(line)
            except json.JSONDecodeError:
                continue
    return prev


def report(cur, prev):
    print(f"Representational redundancy - {cur['date']}")
    print(f"  {cur['total_notes']} notes indexed - matched sample n={cur['ref_n']}, {cur['reps']} reps")
    print()
    print(f"  {'scope':22s} {'n':>6s}  {'matched NN1':>13s}  {'delta':>8s}   {'raw NN1':>8s}")
    print(f"  {'-'*22} {'-'*6}  {'-'*13}  {'-'*8}   {'-'*8}")

    alarms = []
    for name, s in cur["scopes"].items():
        if s["matched_nn1"] is None:
            raw = f"{s['raw_nn1']:.4f}" if s["raw_nn1"] is not None else "   -  "
            print(f"  {name:22s} {s['n']:6d}  {'(below n)':>13s}  {'':>8s}   {raw:>8s}")
            continue

        delta_s = ""
        if prev:
            p = prev.get("scopes", {}).get(name, {})
            if p.get("matched_nn1") is not None and p.get("ref_n", prev.get("ref_n")) == cur["ref_n"]:
                d = s["matched_nn1"] - p["matched_nn1"]
                delta_s = f"{d:+.4f}"
                # Flag only moves larger than sampling noise.
                noise = 2 * max(s["matched_std"] or 0, p.get("matched_std") or 0)
                grew = s["n"] > p.get("n", s["n"])
                if d > max(noise, 0.005) and grew:
                    alarms.append((name, d, p["n"], s["n"]))

        print(f"  {name:22s} {s['n']:6d}  {s['matched_nn1']:13.4f}  {delta_s:>8s}   {s['raw_nn1']:8.4f}")

    print()
    if alarms:
        print("  ALARM - count up AND crowding up (accumulating without digesting):")
        for name, d, pn, n in alarms:
            print(f"    {name}: {pn} -> {n} notes, matched NN1 {d:+.4f}")
    elif prev:
        print("  No scope is both growing and getting more crowded.")
    else:
        print("  Baseline recorded - deltas appear from the next run onward.")
    print()
    print("  Higher matched NN1 = notes sit closer to their nearest neighbour = more")
    print("  redundant. Compare matched NN1 only; raw NN1 rises with n for free.")


def main():
    ap = argparse.ArgumentParser(description="Representational redundancy (crowding) metric")
    ap.add_argument("--ref-n", type=int, default=REF_N, help=f"matched sample size (default {REF_N})")
    ap.add_argument("--reps", type=int, default=REPS, help=f"subsample repetitions (default {REPS})")
    ap.add_argument("--no-write", action="store_true", help="report without appending to history")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if not INDEX_PATH.exists() or not META_PATH.exists():
        print("ERROR: index not found - run run_index.sh first", file=sys.stderr)
        return 1

    cur = measure(args.ref_n, args.reps)
    prev = previous()

    if args.json:
        print(json.dumps(cur, indent=2))
    else:
        report(cur, prev)

    if not args.no_write:
        with open(HISTORY_PATH, "a") as f:
            f.write(json.dumps(cur) + "\n")
        if not args.json:
            print(f"  Appended to {HISTORY_PATH.relative_to(SCRIPT_DIR.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
