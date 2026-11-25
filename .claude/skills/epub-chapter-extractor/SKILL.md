---
name: epub-chapter-extractor
description: Extract all chapters from an EPUB file into separate markdown files. Use when the user wants to split an EPUB into individual chapter files, extract EPUB chapters, or convert an ebook to separate markdown documents.
metadata:
  version: "1.1"
  changelog:
    - "1.1: call extract_chapters.py by its project skill path instead of cd-ing into a skills folder (never ~/.claude/skills) (Abilityai/cornelius#20)"
---

# EPUB Chapter Extractor

Extract each chapter from an EPUB file into its own markdown file.

## Instructions

When the user wants to extract chapters from an EPUB, run the extraction script with `uv`
(run from the agent root - the script is called by its project path, no `cd`, so relative book paths still resolve; `uv` is `~/.local/bin/uv` on the Trinity server, installed by `.trinity/setup.sh`):

```bash
UV="$(command -v uv || echo "$HOME/.local/bin/uv")"
"$UV" run --with ebooklib --with beautifulsoup4 --with html2text --with lxml python "$(git rev-parse --show-toplevel)/.claude/skills/epub-chapter-extractor/extract_chapters.py" "/path/to/book.epub" [output_dir]
```

If `output_dir` is omitted, creates a folder named after the EPUB in the same directory.

## Example

User: "Extract chapters from ~/books_raw/mybook.epub"

```bash
UV="$(command -v uv || echo "$HOME/.local/bin/uv")"
"$UV" run --with ebooklib --with beautifulsoup4 --with html2text --with lxml python "$(git rev-parse --show-toplevel)/.claude/skills/epub-chapter-extractor/extract_chapters.py" "$HOME/books_raw/mybook.epub"
```

Output files will be at `~/books_raw/mybook/`:
- `01_introduction.md`
- `02_chapter_one.md`
- etc.

After extraction, report the output folder (on the Mac, `open` it).

## Output Format

Each chapter file contains:

```markdown
# Chapter Title

[Chapter content in markdown format]
```

Files are numbered for proper sorting: `01_`, `02_`, etc.
