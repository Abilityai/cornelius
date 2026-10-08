#!/usr/bin/env python3
"""
EPUB Chapter Extractor
Extracts all chapters from an EPUB file into separate markdown files.

Usage:
    python extract_chapters.py /path/to/book.epub [output_dir]

If output_dir is not specified, creates a folder named after the EPUB.
"""

import os
import sys
import re
from typing import List, Tuple, Any
from urllib.parse import unquote

# Required: pip install ebooklib beautifulsoup4 html2text
from ebooklib import epub
from bs4 import BeautifulSoup, Comment
import html2text


def get_toc(book: Any) -> List[Tuple[str, str, int]]:
    """
    Extract table of contents with hierarchy level.
    Returns list of (title, href, level) tuples.
    """
    toc_entries = []

    # TOC hrefs are often percent-encoded (e.g. "CR%21..._split.html") while the
    # manifest/spine file names are literal ("CR!..."). Decode so they compare equal.
    for item in book.toc:
        if isinstance(item, tuple):
            chapter = item[0]
            toc_entries.append((chapter.title, unquote(chapter.href), 1))
            for sub_item in item[1]:
                if isinstance(sub_item, tuple):
                    toc_entries.append((sub_item[0].title, unquote(sub_item[0].href), 2))
                else:
                    toc_entries.append((sub_item.title, unquote(sub_item.href), 2))
        else:
            toc_entries.append((item.title, unquote(item.href), 1))

    return toc_entries


def get_spine_hrefs(book: Any) -> List[str]:
    """Get ordered list of file hrefs from the EPUB spine (reading order)."""
    hrefs = []
    for item_id, linear in book.spine:
        item = book.get_item_with_id(item_id)
        if item:
            hrefs.append(unquote(item.file_name))
    return hrefs


def clean_html(html_str: str) -> str:
    """Clean HTML content - remove scripts, styles, images, comments, empty tags."""
    soup = BeautifulSoup(html_str, 'html.parser')

    for tag in soup(['script', 'style', 'img', 'svg', 'iframe', 'video', 'nav']):
        tag.decompose()

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.find_all():
        if not tag.get_text(strip=True) and not tag.find('img') and not tag.name == 'br':
            tag.decompose()

    return str(soup)


def convert_html_to_markdown(html_str: str) -> str:
    """Convert HTML to Markdown."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    return h.handle(html_str)


def extract_chapter_html(book: Any, toc_idx: int, toc_entries: List[Tuple[str, str, int]], spine_hrefs: List[str]) -> str:
    """
    Extract chapter HTML by collecting all spine files between this TOC entry
    and the next one. Handles EPUBs that split chapters across multiple files.
    """
    title, anchor_href, level = toc_entries[toc_idx]
    start_href = anchor_href.split('#')[0] if '#' in anchor_href else anchor_href
    start_anchor = anchor_href.split('#')[1] if '#' in anchor_href else None

    # Find next TOC entry's file to know where to stop
    next_href = None
    if toc_idx + 1 < len(toc_entries):
        next_anchor_href = toc_entries[toc_idx + 1][1]
        next_href = next_anchor_href.split('#')[0] if '#' in next_anchor_href else next_anchor_href

    # If both this and next chapter start in the same file, use anchor-based extraction
    if next_href and start_href == next_href:
        return _extract_anchor_range(book, start_href, start_anchor,
                                     toc_entries[toc_idx + 1][1].split('#')[1] if '#' in toc_entries[toc_idx + 1][1] else None)

    # Collect all spine files from start_href up to (but not including) next_href
    html_parts = []
    collecting = False

    for spine_href in spine_hrefs:
        if spine_href == start_href:
            collecting = True
        if collecting:
            if spine_href == next_href:
                break
            item = book.get_item_with_href(spine_href)
            if item is None:
                # Match on decoded file names (handles percent-encoded manifest hrefs)
                for it in book.get_items():
                    if unquote(it.file_name) == spine_href:
                        item = it
                        break
            if item:
                content = item.get_content().decode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')

                # For the first file, if there's an anchor, start from there
                if spine_href == start_href and start_anchor:
                    anchor_elem = soup.find(id=start_anchor)
                    if anchor_elem:
                        # Get everything from anchor to end of body
                        body = soup.find('body')
                        if body:
                            html_parts.append(str(body))
                        else:
                            html_parts.append(str(soup))
                    else:
                        body = soup.find('body')
                        html_parts.append(str(body) if body else str(soup))
                else:
                    body = soup.find('body')
                    html_parts.append(str(body) if body else str(soup))

    if not html_parts:
        # Fallback: just get the single file
        item = _resolve_item(book, start_href)
        if item:
            content = item.get_content().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            body = soup.find('body')
            html_parts.append(str(body) if body else str(soup))

    combined = '\n'.join(html_parts)
    return clean_html(combined)


def _resolve_item(book: Any, href: str) -> Any:
    """Find a manifest item by href, tolerating percent-encoding mismatches."""
    item = book.get_item_with_href(href)
    if item is None:
        for it in book.get_items():
            if unquote(it.file_name) == href:
                return it
    return item


def _extract_anchor_range(book: Any, href: str, start_anchor: str, end_anchor: str) -> str:
    """Extract content between two anchors in the same file."""
    item = _resolve_item(book, href)
    if item is None:
        raise ValueError(f"Chapter file not found: {href}")

    soup = BeautifulSoup(item.get_content().decode('utf-8'), 'html.parser')

    if not start_anchor:
        # No start anchor - get from beginning to end_anchor
        body = soup.find('body')
        if end_anchor:
            end_elem = soup.find(id=end_anchor)
            if end_elem:
                # Collect everything before end_elem
                elems = []
                for elem in (body or soup).descendants:
                    if elem is end_elem:
                        break
                    if hasattr(elem, 'name') and elem.name:
                        elems.append(str(elem))
                return clean_html('\n'.join(elems))
        return clean_html(str(body) if body else str(soup))

    start_elem = soup.find(id=start_anchor)
    if not start_elem:
        body = soup.find('body')
        return clean_html(str(body) if body else str(soup))

    # Collect elements from start to end anchor (or end of file)
    elems = []
    collecting = False
    for elem in (soup.find('body') or soup).descendants:
        if hasattr(elem, 'get') and elem.get('id') == start_anchor:
            collecting = True
        if collecting:
            if end_anchor and hasattr(elem, 'get') and elem.get('id') == end_anchor:
                break
            if hasattr(elem, 'name') and elem.name:
                elems.append(str(elem))

    if not elems:
        # Fallback: get parent and everything after
        parent = start_elem.parent
        return clean_html(str(parent) if parent else str(start_elem))

    return clean_html('\n'.join(elems))


def sanitize_filename(title: str, max_length: int = 50) -> str:
    """Convert chapter title to safe filename."""
    safe = re.sub(r'[/:*?"<>|\\]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    safe = safe.strip('_')
    if len(safe) > max_length:
        safe = safe[:max_length].rstrip('_')
    return safe.lower()


def extract_all_chapters(epub_path: str, output_dir: str) -> List[str]:
    """Extract all chapters from EPUB to separate markdown files."""
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    print(f"Reading: {epub_path}")
    book = epub.read_epub(epub_path)

    toc_entries = get_toc(book)
    if not toc_entries:
        raise ValueError("EPUB has no table of contents")

    spine_hrefs = get_spine_hrefs(book)
    print(f"Found {len(toc_entries)} chapters ({len(spine_hrefs)} spine items)")

    os.makedirs(output_dir, exist_ok=True)

    created_files = []
    errors = []

    for idx, (title, href, level) in enumerate(toc_entries):
        safe_title = sanitize_filename(title)
        filename = f"{idx + 1:02d}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)

        try:
            html = extract_chapter_html(book, idx, toc_entries, spine_hrefs)
            markdown = convert_html_to_markdown(html)
            content = f"# {title}\n\n{markdown}"

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            created_files.append(filepath)
            print(f"  [{idx + 1:02d}/{len(toc_entries)}] {filename}")

        except Exception as e:
            errors.append((title, str(e)))
            print(f"  [{idx + 1:02d}/{len(toc_entries)}] ERROR: {title} - {e}")

    print(f"\nExtracted {len(created_files)}/{len(toc_entries)} chapters to: {output_dir}")

    if errors:
        print(f"\nFailed chapters ({len(errors)}):")
        for title, error in errors:
            print(f"  - {title}: {error}")

    return created_files


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_chapters.py <epub_path> [output_dir]")
        print("\nExtracts all chapters from an EPUB into separate markdown files.")
        sys.exit(1)

    epub_path = os.path.abspath(sys.argv[1])

    if len(sys.argv) >= 3:
        output_dir = os.path.abspath(sys.argv[2])
    else:
        base_name = os.path.splitext(os.path.basename(epub_path))[0]
        output_dir = os.path.join(os.path.dirname(epub_path), base_name)

    try:
        extract_all_chapters(epub_path, output_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
