#!/usr/bin/env python3
"""
Gemini OCR for image-only (scanned) PDFs → markdown chunks.

Used as the fallback path of multi-format-book-extractor when a PDF has no text
layer. Renders each page to PNG, sends batches to Gemini 2.5 Flash for verbatim
transcription, and writes numbered page-range chunk files matching the
no-TOC output format of extract_book.py.

Designed for Buddhist scholarly texts: preserves Sanskrit/Tibetan diacritics,
verse line breaks, and footnotes. Resumable (skips already-written chunk files)
and parallelised across calls within a book.

Usage:
    uv run --with pymupdf --with requests python ocr_pdf.py <file.pdf> [output_dir] \
        [--model gemini-2.5-flash] [--dpi 180] [--pages-per-call 5] \
        [--pages-per-file 20] [--concurrency 6]

API key: read from $GEMINI_API_KEY / $GOOGLE_API_KEY, else from the
cornelius .env file.
"""

import argparse
import base64
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

PAGE_BREAK = "[[PAGE BREAK]]"

PROMPT = f"""You are an expert OCR transcriber for Buddhist scholarly texts (Dzogchen, \
Madhyamaka, Mahamudra). Transcribe the supplied book page image(s) to clean \
Markdown, VERBATIM.

Rules:
- Output ONLY the transcribed text. No preamble, no commentary, no "Here is...".
- Preserve natural reading order and paragraph breaks.
- Preserve verse / stanza line breaks EXACTLY as printed (one printed line = one line).
- Render diacritics precisely: ā ī ū ṛ ṝ ḷ ṃ ṁ ḥ ṅ ñ ṭ ḍ ṇ ś ṣ etc. These matter.
- Transcribe Tibetan (Uchen) or Devanagari script if legible; never invent characters.
- Render visually-apparent headings as Markdown headings (#, ##).
- Move footnotes to a short "Footnotes" block at the end of that page's text.
- Omit running headers/footers and bare page numbers.
- If a page has no readable text, output exactly: [no text]
- When multiple pages are supplied, separate each page's transcription with a line \
containing exactly: {PAGE_BREAK}
"""


# ── API key ─────────────────────────────────────────────────────────────────


def load_api_key() -> str:
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(var):
            return os.environ[var]
    # fall back to the cornelius .env
    for env_path in (
        Path(__file__).resolve().parents[3] / ".env",  # .../cornelius/.env
        Path.home() / "Agents/cornelius/.env",
    ):
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                m = re.match(r"\s*(GEMINI_API_KEY|GOOGLE_API_KEY)\s*=\s*(.+)\s*$", line)
                if m:
                    return m.group(2).strip().strip('"').strip("'")
    print("ERROR: no GEMINI_API_KEY / GOOGLE_API_KEY in env or .env", file=sys.stderr)
    sys.exit(1)


# ── Gemini call ───────────────────────────────────────────────────────────────


def gemini_ocr(images_png: list[bytes], model: str, api_key: str,
               max_retries: int = 5) -> str:
    """Send a batch of PNG page images, return transcribed markdown."""
    import requests

    parts = [{"text": PROMPT}]
    for png in images_png:
        parts.append({
            "inline_data": {
                "mime_type": "image/png",
                "data": base64.b64encode(png).decode("ascii"),
            }
        })
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 16384,
            "topP": 0.95,
        },
    }
    url = API_URL.format(model=model)
    params = {"key": api_key}

    delay = 4.0
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.post(url, params=params, json=payload, timeout=240)
        except requests.RequestException as e:
            if attempt == max_retries:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 60)
            continue

        if r.status_code == 200:
            data = r.json()
            cands = data.get("candidates", [])
            if not cands:
                return "[no text]"
            cand = cands[0]
            text = "".join(
                p.get("text", "") for p in cand.get("content", {}).get("parts", [])
            ).strip()
            if not text and cand.get("finishReason") == "MAX_TOKENS":
                return "[OCR truncated - reduce --pages-per-call]"
            return text or "[no text]"

        if r.status_code in (429, 500, 502, 503, 504):
            if attempt == max_retries:
                raise RuntimeError(f"Gemini {r.status_code} after {max_retries} tries: {r.text[:300]}")
            time.sleep(delay)
            delay = min(delay * 2, 60)
            continue

        raise RuntimeError(f"Gemini error {r.status_code}: {r.text[:500]}")
    raise RuntimeError("unreachable")


# ── PDF rendering ─────────────────────────────────────────────────────────────


def render_page(doc, page_index: int, dpi: int) -> bytes:
    zoom = dpi / 72.0
    import fitz
    pix = doc[page_index].get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return pix.tobytes("png")


# ── Orchestration ─────────────────────────────────────────────────────────────


def chunk_done(output_dir: Path, fname: str, min_chars: int = 200) -> bool:
    f = output_dir / fname
    return f.exists() and len(f.read_text(encoding="utf-8")) >= min_chars


def ocr_pdf(input_path: Path, output_dir: Path, model: str = "gemini-2.5-flash",
            dpi: int = 180, pages_per_call: int = 5, pages_per_file: int = 20,
            concurrency: int = 6) -> int:
    import fitz

    api_key = load_api_key()
    doc = fitz.open(str(input_path))
    total = doc.page_count
    output_dir.mkdir(parents=True, exist_ok=True)

    n_files = (total + pages_per_file - 1) // pages_per_file
    print(f"  OCR via {model}: {total} pages → {n_files} chunk files "
          f"({pages_per_file} pg/file, {pages_per_call} pg/call, dpi={dpi}, conc={concurrency})")

    written = 0
    for fi in range(n_files):
        fs = fi * pages_per_file
        fe = min(fs + pages_per_file, total)
        fname = f"{fi + 1:02d}_pages-{fs + 1}-{fe}.md"
        if chunk_done(output_dir, fname):
            print(f"  [{fi + 1:02d}/{n_files:02d}] {fname} — already done, skip")
            written += 1
            continue

        # plan calls (sub-batches) for this file's page range
        calls = []  # list of (start_page, [png bytes])
        for cs in range(fs, fe, pages_per_call):
            ce = min(cs + pages_per_call, fe)
            imgs = [render_page(doc, p, dpi) for p in range(cs, ce)]
            calls.append((cs, ce, imgs))

        results: dict[int, str] = {}

        def run_call(call):
            cs, ce, imgs = call
            txt = gemini_ocr(imgs, model, api_key)
            return cs, ce, txt

        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            for cs, ce, txt in ex.map(run_call, calls):
                results[cs] = txt

        # assemble in page order, tagging page boundaries
        body = [f"# Pages {fs + 1}-{fe}\n\n"]
        for cs in sorted(results):
            ce = min(cs + pages_per_call, fe)
            pages_txt = results[cs].split(PAGE_BREAK)
            for offset, ptxt in enumerate(pages_txt):
                pno = cs + offset + 1
                ptxt = ptxt.strip()
                if not ptxt or ptxt == "[no text]":
                    continue
                body.append(f"<!-- page {pno} -->\n\n{ptxt}\n\n")

        (output_dir / fname).write_text("".join(body), encoding="utf-8")
        chars = sum(len(b) for b in body)
        print(f"  [{fi + 1:02d}/{n_files:02d}] {fname} — {chars} chars")
        written += 1

    doc.close()
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description="Gemini OCR for scanned PDFs → markdown")
    ap.add_argument("pdf")
    ap.add_argument("output_dir", nargs="?", default=None)
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--dpi", type=int, default=180)
    ap.add_argument("--pages-per-call", type=int, default=5)
    ap.add_argument("--pages-per-file", type=int, default=20)
    ap.add_argument("--concurrency", type=int, default=6)
    args = ap.parse_args()

    src = Path(args.pdf).resolve()
    if not src.exists():
        print(f"ERROR: not found: {src}", file=sys.stderr)
        sys.exit(1)
    dst = Path(args.output_dir).resolve() if args.output_dir else src.parent / src.stem

    print(f"{'─' * 60}\nOCR:    {src.name}\nOutput: {dst}")
    n = ocr_pdf(src, dst, args.model, args.dpi, args.pages_per_call,
                args.pages_per_file, args.concurrency)
    print(f"Done: {n} chunk files in {dst}")


if __name__ == "__main__":
    main()
