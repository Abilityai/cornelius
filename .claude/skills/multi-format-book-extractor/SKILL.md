---
name: multi-format-book-extractor
description: Extract chapters from PDF, MOBI, and AZW3 book files into individual markdown files. Use when extracting non-EPUB books. PDF uses pymupdf with TOC-based chapter splitting and auto-OCR fallback (Gemini) for scanned/image-only PDFs; MOBI/AZW3 routes through calibre then epub-chapter-extractor.
allowed-tools: [Bash]
user-invocable: true
---

# Multi-Format Book Extractor

Extract chapters from PDF, MOBI, and AZW3 files into individual numbered markdown files.
Mirrors the epub-chapter-extractor pattern for non-EPUB formats.

## Dependencies

- **PDF**: `pymupdf` — auto-installed via `--with pymupdf`
- **Scanned PDF OCR fallback**: `requests` (`--with requests`) + a Gemini key in
  `$GEMINI_API_KEY` / `$GOOGLE_API_KEY` (read from `cornelius/.env` if unset)
- **MOBI / AZW3**: [calibre](https://calibre-ebook.com/download) must be installed
  ```bash
  brew install --cask calibre
  ```

## Single Book

```bash
cd $PROJECT_ROOT/.claude/skills/multi-format-book-extractor && \
uv run --with pymupdf --with requests python extract_book.py "/path/to/book.pdf" [output_dir]
```

If `output_dir` is omitted, creates a folder named after the file in the same directory.

## Scanned / Image-Only PDFs (auto-OCR)

Some PDFs are pure page scans with **no text layer** — `pymupdf` extracts nothing
and would silently write empty files. `extract_book.py` now samples the text layer
first (`_has_text_layer`) and, when a PDF looks image-only, automatically routes it
to **Gemini 2.5 Flash OCR** (`ocr_pdf.py`).

- Renders each page to PNG (~180 DPI), batches pages per API call, transcribes
  verbatim to Markdown (preserves verse line breaks, Sanskrit/Tibetan diacritics,
  footnotes), and writes `NN_pages-S-E.md` chunk files.
- **Resumable**: re-running skips chunk files already written (≥200 chars), so an
  interrupted long book picks up where it left off.
- Cost is ~$0.002/page on Flash (a 300-page book ≈ $0.60).

Run OCR directly (e.g. to tune params or force it):

```bash
cd $PROJECT_ROOT/.claude/skills/multi-format-book-extractor && \
uv run --with pymupdf --with requests python ocr_pdf.py "/path/to/scan.pdf" [output_dir] \
  [--model gemini-2.5-flash] [--dpi 180] [--pages-per-call 5] [--pages-per-file 20] [--concurrency 6]
```

## Batch Extraction (Parallel)

Extract all PDFs, MOBIs, and AZW3s from a directory in parallel:

```bash
SKILL="$PROJECT_ROOT/.claude/skills/multi-format-book-extractor"
UVX="uv"
DIR="/path/to/books"

for book in "$DIR"/*.{pdf,mobi,azw3}; do
  [ -f "$book" ] || continue
  stem="${book%.*}"
  [ -d "$stem" ] && echo "Skipping: $(basename "$book") (already extracted)" && continue
  echo "Starting: $(basename "$book")"
  (cd "$SKILL" && $UVX run --with pymupdf --with requests python extract_book.py "$book") &
done
wait
echo "All done"
```

## Output Format

Each book gets a subfolder named after the file (without extension):

```
book-name/
├── 01_introduction.md
├── 02_chapter-one.md
└── ...
```

- **PDF with TOC**: one file per chapter (uses level-1 TOC; falls through to level-2 if < 5 top-level entries, e.g. books structured as Parts)
- **PDF without TOC**: 20-page chunks (`01_pages-1-20.md`, etc.)
- **Scanned / image-only PDF**: auto-routed to Gemini OCR → 20-page chunks (`01_pages-1-20.md`) with `<!-- page N -->` markers
- **MOBI / AZW3**: same output quality as epub-chapter-extractor (converts via calibre first)

## After Extraction

```bash
open /path/to/books/
```
