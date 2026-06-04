#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf"]
# ///
"""Extract full text from a paper into a markdown file.

Handles three input kinds, auto-detected:
  - arXiv id or URL  (e.g. 2310.06825, arxiv.org/abs/2310.06825, /pdf/2310.06825)
  - any PDF URL       (downloads then extracts)
  - local PDF path

Writes plain UTF-8 text/markdown to the output path (or stdout if omitted) and
prints a one-line summary (char count, page count, detected title) to stderr.

Why a script and not the Read/WebFetch tools: papers are long and WebFetch
summarizes/truncates. This dumps the COMPLETE text deterministically so concept
extraction sees everything. Run via uv (pymupdf auto-installs):

    uv run extract_paper.py <input> [output.md]

Downloads use the system `curl` rather than a Python HTTP library: some uv-managed
interpreters are built without the _ssl module, which breaks requests/urllib over
HTTPS. curl carries its own TLS, so this stays robust across environments.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def resolve_arxiv_pdf(token: str) -> str | None:
    """Return a PDF URL if token looks like an arXiv id/url, else None."""
    if "arxiv.org" in token or ARXIV_ID.fullmatch(token.strip()):
        m = ARXIV_ID.search(token)
        if m:
            return f"https://arxiv.org/pdf/{m.group(1)}{m.group(2) or ''}"
    return None


def download(url: str) -> Path:
    tmp = Path(tempfile.mkstemp(suffix=".pdf")[1])
    result = subprocess.run(
        ["curl", "-sSL", "-A", "Mozilla/5.0 (understand-paper skill)",
         "--fail", "-o", str(tmp), url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed ({result.returncode}): {result.stderr.strip()}")
    return tmp


def pdf_to_text(path: Path) -> tuple[str, int, str]:
    import fitz  # pymupdf

    doc = fitz.open(path)
    pages = [page.get_text("text") for page in doc]
    title = (doc.metadata or {}).get("title") or ""
    return "\n\n".join(pages), doc.page_count, title


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: extract_paper.py <arxiv-id|url|pdf-path> [output.md]", file=sys.stderr)
        return 2

    token = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None

    arxiv_pdf = resolve_arxiv_pdf(token)
    if arxiv_pdf:
        src = download(arxiv_pdf)
    elif token.startswith("http://") or token.startswith("https://"):
        src = download(token)
    else:
        src = Path(token).expanduser()
        if not src.exists():
            print(f"error: file not found: {src}", file=sys.stderr)
            return 1

    text, n_pages, title = pdf_to_text(src)

    if out:
        Path(out).expanduser().write_text(text, encoding="utf-8")
        print(f"wrote {len(text):,} chars, {n_pages} pages -> {out}", file=sys.stderr)
        if title:
            print(f"title: {title}", file=sys.stderr)
    else:
        sys.stdout.write(text)
        print(f"[{len(text):,} chars, {n_pages} pages]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
