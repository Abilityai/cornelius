#!/usr/bin/env python3
"""
Multi-format book extractor: PDF, MOBI, AZW3 → markdown chapters.
Mirrors the epub-chapter-extractor pattern for non-EPUB formats.

Usage:
    uv run --with pymupdf python extract_book.py <file.pdf|mobi|azw3> [output_dir]

If output_dir is omitted, creates a subfolder named after the file in the same directory.
"""

import re
import sys
import subprocess
import tempfile
from pathlib import Path


SUPPORTED = {".pdf", ".mobi", ".azw3"}

# TOC entries that look like per-page internal IDs rather than real chapter titles
_PER_PAGE_PATTERN = re.compile(
    r"^(page|image|img|clipboard|nlz|pg)[\s_\-]?\d{2,}$"  # page0001, image_0002, clipboard-03
    r"|^\d{3,6}$"                                            # 0001, 00042
    r"|^[a-z]{2,6}_\d{3,6}$",                               # nlz_000, ref_001
    re.IGNORECASE,
)


def _has_text_layer(doc, sample: int = 30, min_chars_per_page: int = 20,
                    min_fraction: float = 0.15) -> bool:
    """Return False if the PDF looks like a scanned/image-only document.

    Samples up to `sample` evenly-spaced pages; if fewer than `min_fraction` of
    them carry meaningful selectable text, the PDF has no usable text layer and
    should be routed to OCR.
    """
    n = doc.page_count
    if n == 0:
        return True
    idxs = range(n) if n <= sample else [round(i * (n - 1) / (sample - 1)) for i in range(sample)]
    idxs = sorted(set(idxs))
    with_text = sum(1 for i in idxs if len(doc[i].get_text("text").strip()) >= min_chars_per_page)
    return (with_text / len(idxs)) >= min_fraction


def _is_per_page_toc(entries: list[tuple], total_pages: int) -> bool:
    """Return True if the TOC looks like per-page internal IDs rather than real chapters."""
    if not entries:
        return False
    # Density: > 40% means roughly one entry per 2-3 pages → per-page structure
    if len(entries) / max(total_pages, 1) > 0.4:
        return True
    # Pattern: if most of the first 8 titles look like internal page IDs
    sample = [t.strip() for t, _ in entries[:8]]
    if sum(1 for t in sample if _PER_PAGE_PATTERN.match(t)) >= min(3, len(sample)):
        return True
    return False


CALIBRE_SEARCH = [
    "/Applications/calibre.app/Contents/MacOS/ebook-convert",
    "/usr/local/bin/ebook-convert",
    "/usr/bin/ebook-convert",
]


def slugify(text: str, max_len: int = 60) -> str:
    text = re.sub(r'[/:*?"<>|\\]', "", str(text)).strip()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:max_len].lower() or "untitled"


def chapter_filename(idx: int, title: str) -> str:
    return f"{idx:02d}_{slugify(title)}.md"


# ── PDF ───────────────────────────────────────────────────────────────────────


def extract_pdf(input_path: Path, output_dir: Path) -> None:
    try:
        import fitz  # pymupdf
    except ImportError:
        print("ERROR: pymupdf not installed. Run with: uv run --with pymupdf python extract_book.py ...")
        sys.exit(1)

    doc = fitz.open(str(input_path))

    # Scanned/image-only PDFs have no usable text layer → route to Gemini OCR.
    if not _has_text_layer(doc):
        n = doc.page_count
        doc.close()
        print(f"  No text layer detected ({n} pages look image-only) — routing to Gemini OCR")
        try:
            import ocr_pdf
        except ImportError:
            print("ERROR: ocr_pdf.py not importable. Run with: "
                  "uv run --with pymupdf --with requests python extract_book.py ...")
            sys.exit(1)
        ocr_pdf.ocr_pdf(input_path, output_dir)
        return

    toc = doc.get_toc()  # [(level, title, page_1indexed), ...]

    # Prefer level-1 TOC; fall through to level-2 if top level looks like parts only (< 5 entries)
    top = [(t, p) for lvl, t, p in toc if lvl == 1]
    if len(top) < 5 and toc:
        top = [(t, p) for lvl, t, p in toc if lvl in (1, 2)]

    # Reject per-page TOC structures (page0001, image_0002, clipboard-03, bare numbers, etc.)
    if _is_per_page_toc(top, len(doc)):
        print(f"  TOC looks per-page ({len(top)} entries / {len(doc)} pages) — falling back to page chunks")
        top = []

    if top:
        chapters = []
        for i, (title, page) in enumerate(top):
            end_page = top[i + 1][1] - 1 if i + 1 < len(top) else len(doc)
            chapters.append((title, page - 1, end_page - 1))  # convert to 0-indexed

        print(f"  TOC: {len(chapters)} chapters")
        for idx, (title, start, end) in enumerate(chapters, 1):
            lines = [f"# {title}\n\n"]
            for pn in range(max(0, start), min(end + 1, len(doc))):
                text = doc[pn].get_text("text").strip()
                if text:
                    lines.append(text + "\n\n")
            fname = chapter_filename(idx, title)
            (output_dir / fname).write_text("".join(lines), encoding="utf-8")
            print(f"  [{idx:02d}/{len(chapters):02d}] {fname}")
    else:
        # No TOC: 20-page chunks
        chunk = 20
        total = len(doc)
        n = (total + chunk - 1) // chunk
        print(f"  No TOC — splitting {total} pages into {n} chunks of {chunk}")
        for i in range(n):
            s, e = i * chunk, min((i + 1) * chunk, total)
            lines = [f"# Pages {s + 1}-{e}\n\n"]
            for pn in range(s, e):
                lines.append(doc[pn].get_text("text").strip() + "\n\n")
            fname = f"{i + 1:02d}_pages-{s + 1}-{e}.md"
            (output_dir / fname).write_text("".join(lines), encoding="utf-8")
            print(f"  [{i + 1:02d}/{n:02d}] {fname}")

    doc.close()


# ── MOBI / AZW3 ──────────────────────────────────────────────────────────────


def find_calibre() -> str | None:
    for p in CALIBRE_SEARCH:
        if Path(p).exists():
            return p
    r = subprocess.run(["which", "ebook-convert"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def extract_mobi_azw3(input_path: Path, output_dir: Path) -> None:
    calibre = find_calibre()
    if not calibre:
        print(
            "ERROR: calibre ebook-convert not found.\n"
            "  Install: brew install --cask calibre\n"
            "  Or:      https://calibre-ebook.com/download"
        )
        sys.exit(1)

    epub_extractor = (
        Path(__file__).parent.parent / "epub-chapter-extractor" / "extract_chapters.py"
    )
    if not epub_extractor.exists():
        print(f"ERROR: epub-chapter-extractor not found at {epub_extractor}")
        sys.exit(1)

    uv = Path.home() / ".local/bin/uv"
    if not uv.exists():
        uv = Path("uv")

    with tempfile.TemporaryDirectory() as tmp:
        epub_tmp = Path(tmp) / (input_path.stem + ".epub")

        print(f"  Converting {input_path.suffix.upper()} to EPUB via calibre...")
        r = subprocess.run(
            [str(calibre), str(input_path), str(epub_tmp)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode != 0:
            print(f"  Calibre conversion failed:\n{r.stderr[-500:]}")
            sys.exit(1)

        print("  Extracting chapters from converted EPUB...")
        r = subprocess.run(
            [
                str(uv), "run",
                "--with", "ebooklib",
                "--with", "beautifulsoup4",
                "--with", "html2text",
                "--with", "lxml",
                "python", str(epub_extractor),
                str(epub_tmp),
                str(output_dir),
            ],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(epub_extractor.parent),
        )
        if r.returncode != 0:
            print(f"  Extraction failed:\n{r.stderr[-500:]}")
            sys.exit(1)
        if r.stdout:
            print(r.stdout.rstrip())


# ── Entry point ───────────────────────────────────────────────────────────────


def extract(input_path: Path, output_dir: Path | None = None) -> None:
    suffix = input_path.suffix.lower()
    if suffix not in SUPPORTED:
        print(f"ERROR: unsupported format '{suffix}'. Supported: {', '.join(sorted(SUPPORTED))}")
        sys.exit(1)

    if output_dir is None:
        output_dir = input_path.parent / input_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'─' * 60}")
    print(f"Input:  {input_path.name}")
    print(f"Output: {output_dir}")

    if suffix == ".pdf":
        extract_pdf(input_path, output_dir)
    else:
        extract_mobi_azw3(input_path, output_dir)

    files = list(output_dir.glob("*.md"))
    print(f"Done: {len(files)} files written to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_book.py <file.pdf|mobi|azw3> [output_dir]")
        print("\nExtracts chapters from PDF, MOBI, or AZW3 books into markdown files.")
        sys.exit(1)

    src = Path(sys.argv[1]).resolve()
    dst = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None

    if not src.exists():
        print(f"ERROR: not found: {src}")
        sys.exit(1)

    extract(src, dst)
