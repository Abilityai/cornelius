"""
Keep glibc from hoarding the memory that embedding batches free.

Import this module FIRST - before torch, numpy, faiss or sentence_transformers -
in every process that loads the embedding model (daemon.py, index_brain.py,
search.py):

    import allocator  # noqa: F401  (must stay the first import)

Why: glibc serves allocations above M_MMAP_THRESHOLD with mmap and hands them
back to the OS on free. By default that threshold is *dynamic*: every time a large
mmapped block is freed, glibc raises the threshold to that block's size (up to
32 MB on 64-bit). One encode() pass frees a few large activation tensors, the
threshold climbs, and every later activation tensor comes from the heap instead -
where it stays after free(), because the heap only shrinks from the top. Measured
on all-MiniLM-L6-v2 (CPU torch 2.x, 1,536 chunks in 512-chunk calls): the process
kept ~420 MB of freed activations (RSS 920 MB after encoding vs 500 MB before)
and peaked at 1,050 MB.

Pinning the threshold (which also switches the dynamic adjustment off) keeps every
large tensor on mmap, so it goes back to the OS the moment torch frees it. Same
run: 606 MB after encoding, 753 MB peak. Only *where* memory comes from changes;
no arithmetic does, so embeddings are bit-identical.

The environment variables MALLOC_MMAP_THRESHOLD_ / MALLOC_TRIM_THRESHOLD_ do the
same thing but only if set before the interpreter starts; this module works however
the script is launched (wrapper, skill, or `venv/bin/python script.py`). An explicit
MALLOC_MMAP_THRESHOLD_ in the environment wins. No-op off glibc (macOS, musl).
"""
import ctypes
import ctypes.util
import os

M_TRIM_THRESHOLD = -1
M_MMAP_THRESHOLD = -3

# 128 KiB: glibc's own starting value, held fixed instead of allowed to climb.
MMAP_THRESHOLD = 128 * 1024

_libc = None


def _load_libc():
    global _libc
    if _libc is None:
        try:
            name = ctypes.util.find_library("c")
            lib = ctypes.CDLL(name) if name else None
            # mallopt/malloc_trim exist only in glibc
            _libc = lib if lib is not None and hasattr(lib, "mallopt") and hasattr(lib, "malloc_trim") else False
        except OSError:
            _libc = False
    return _libc or None


def tune():
    """Pin the mmap threshold (disables glibc's dynamic raise). Idempotent."""
    if "MALLOC_MMAP_THRESHOLD_" in os.environ:
        return False
    libc = _load_libc()
    if libc is None:
        return False
    ok = libc.mallopt(M_MMAP_THRESHOLD, MMAP_THRESHOLD) == 1
    libc.mallopt(M_TRIM_THRESHOLD, 2 * MMAP_THRESHOLD)
    return ok


def trim():
    """Return free heap pages to the OS (cheap; call after a large batch)."""
    libc = _load_libc()
    if libc is not None:
        libc.malloc_trim(0)


TUNED = tune()
