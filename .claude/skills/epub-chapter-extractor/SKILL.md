---
name: epub-chapter-extractor
description: Extract all chapters from an EPUB file into separate markdown files. Use when the user wants to split an EPUB into individual chapter files, extract EPUB chapters, or convert an ebook to separate markdown documents.
---

# EPUB Chapter Extractor

Extract each chapter from an EPUB file into its own markdown file.

## Instructions

When the user wants to extract chapters from an EPUB, run the extraction script with `uv`:

```bash
cd ~/.claude/skills/epub-chapter-extractor && /Users/eugene/.local/bin/uv run --with ebooklib --with beautifulsoup4 --with html2text --with lxml python extract_chapters.py "/path/to/book.epub" [output_dir]
```

If `output_dir` is omitted, creates a folder named after the EPUB in the same directory.

## Example

User: "Extract chapters from /Users/eugene/Books/mybook.epub"

```bash
cd ~/.claude/skills/epub-chapter-extractor && /Users/eugene/.local/bin/uv run --with ebooklib --with beautifulsoup4 --with html2text --with lxml python extract_chapters.py "/Users/eugene/Books/mybook.epub"
```

Output files will be at `/Users/eugene/Books/mybook/`:
- `01_introduction.md`
- `02_chapter_one.md`
- etc.

After extraction, open the output folder:

```bash
open /Users/eugene/Books/mybook
```

## Output Format

Each chapter file contains:

```markdown
# Chapter Title

[Chapter content in markdown format]
```

Files are numbered for proper sorting: `01_`, `02_`, etc.
