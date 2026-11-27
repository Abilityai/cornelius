#!/usr/bin/env python3
"""Preflight and smoke test for document intake (/intake, /first-run).

Runs under the SYSTEM python3 so it can report on a venv that is missing or
broken. It never installs anything.

    python3 -I resources/local-brain-search/intake_check.py
        One line per missing thing, naming it exactly, then exit 1.
        Prints "intake tools: ok" and exits 0 when nothing is missing.

    python3 -I resources/local-brain-search/intake_check.py --convert-test
        The preflight, then a real round trip: writes a small PDF (with
        pymupdf) and a small .docx (plain OOXML), converts both with the same
        commands /intake uses (extract_book.py for the PDF, markitdown for the
        .docx) and checks the marker text came through. Prints one line per
        format: "PDF conversion: ok" / "docx conversion: FAILED - <why>".

Why this exists (2026-11-27): conversions used to go through `uv run`, which a
fresh Trinity container does not have, and the intake summary then blamed "the
search engine" when only uv was missing. Conversions now run from the search
venv the bootstrap already builds, and this script names the actual gap.
"""
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

LBS = Path(__file__).resolve().parent
ROOT = LBS.parent.parent
VENV_PY = LBS / "venv" / "bin" / "python"
MARKITDOWN = LBS / "venv" / "bin" / "markitdown"
EXTRACT_BOOK = ROOT / ".claude" / "skills" / "multi-format-book-extractor" / "extract_book.py"
INDEX = LBS / "data" / "brain.faiss"
MARKER = "Cornelius intake smoke test marker"

# module -> what to call it in the report
MODULES = [
    ("faiss", "faiss (search engine)"),
    ("sentence_transformers", "sentence-transformers (search engine)"),
    ("markitdown", "markitdown (docx/pptx/xlsx/html conversion)"),
    ("pymupdf", "pymupdf (PDF conversion)"),
    ("trafilatura", "trafilatura (web page conversion)"),
]


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def preflight() -> list[str]:
    missing = []
    if not VENV_PY.exists():
        return [f"no search venv at {rel(VENV_PY)} - run /first-run"]
    probe = (
        "import importlib.util,sys\n"
        "for m in sys.argv[1:]:\n"
        "    print(m, importlib.util.find_spec(m) is not None)\n"
    )
    r = subprocess.run([str(VENV_PY), "-I", "-c", probe, *[m for m, _ in MODULES]],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return [f"search venv at {rel(VENV_PY)} does not run ({(r.stderr or '').strip()[-200:]}) - run /first-run"]
    found = dict(line.split() for line in r.stdout.splitlines() if line.strip())
    for mod, label in MODULES:
        if found.get(mod) != "True":
            missing.append(f"{label} not installed in the search venv - run /first-run")
    if found.get("markitdown") == "True" and not MARKITDOWN.exists():
        missing.append(f"markitdown command missing at {rel(MARKITDOWN)} - run /first-run")
    if not EXTRACT_BOOK.exists():
        missing.append(f"PDF extractor missing at {rel(EXTRACT_BOOK)}")
    if not INDEX.exists():
        missing.append(f"search index not built ({rel(INDEX)} missing) - run /first-run")
    return missing


def make_docx(path: Path) -> None:
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
           f'<w:p><w:r><w:t>{MARKER} (docx).</w:t></w:r></w:p>'
           '</w:body></w:document>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)


def convert_test() -> int:
    bad = 0
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
        tmp = Path(tmp)
        # PDF: written by pymupdf itself, then read back by the intake command
        pdf = tmp / "sample.pdf"
        mk = subprocess.run([str(VENV_PY), "-I", "-c",
                             "import pymupdf,sys; d=pymupdf.open(); p=d.new_page(); "
                             "p.insert_text((72,72), sys.argv[2]); d.save(sys.argv[1])",
                             str(pdf), f"{MARKER} (pdf)."], capture_output=True, text=True)
        out = tmp / "pdf-out"
        out.mkdir()
        if mk.returncode != 0:
            print(f"PDF conversion: FAILED - could not write a test PDF ({mk.stderr.strip()[-200:]})")
            bad += 1
        else:
            r = subprocess.run([str(VENV_PY), str(EXTRACT_BOOK), str(pdf), str(out)],
                               capture_output=True, text=True, cwd=str(EXTRACT_BOOK.parent), timeout=120)
            text = "".join(f.read_text(errors="replace") for f in sorted(out.glob("*.md")))
            if MARKER in text:
                print("PDF conversion: ok (extract_book.py from the search venv)")
            else:
                print(f"PDF conversion: FAILED - {(r.stdout + r.stderr).strip()[-300:] or 'no text came out'}")
                bad += 1
        # docx
        docx = tmp / "sample.docx"
        make_docx(docx)
        md = tmp / "sample.md"
        r = subprocess.run([str(MARKITDOWN), str(docx), "-o", str(md)],
                           capture_output=True, text=True, timeout=120)
        text = md.read_text(errors="replace") if md.exists() else ""
        if MARKER in text:
            print("docx conversion: ok (markitdown from the search venv)")
        else:
            print(f"docx conversion: FAILED - {(r.stdout + r.stderr).strip()[-300:] or 'no text came out'}")
            bad += 1
    return bad


def main() -> int:
    missing = preflight()
    for m in missing:
        print(f"missing: {m}")
    if not missing:
        print("intake tools: ok")
    if "--convert-test" in sys.argv[1:]:
        if not VENV_PY.exists():
            print("PDF conversion: not tested - no search venv")
            print("docx conversion: not tested - no search venv")
            return 1
        return 1 if (convert_test() or missing) else 0
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
