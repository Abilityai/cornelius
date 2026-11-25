---
name: intake
description: Take in one document or link (or everything waiting in the inbox) with no questions asked - work out what it is, convert it if needed, run the playbook that fits (source ingestion, own-words extraction, or just keep it), and end with the same short summary every time. The one-step entry point for "here is a file, deal with it".
automation: autonomous
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Task, Skill, WebFetch]
user-invocable: true
argument-hint: "<file path | link | --all> [--as auto|source|own|keep] [--from <person>]"
effort: high
metadata:
  version: "1.1"
  created: 2026-11-24
  author: trinity-pm (for Cornelius)
  changelog:
    - "1.1: First live run (2026-11-25, three inputs). Fingerprint falls back to sha256sum; --from for a dispatched run; web links keep title/url/date via trafilatura --with-metadata; exact non-book PDF command (absolute paths, chunks concatenated to one file); HTML nav chrome note; session-name convention; an OOM-killed reindex is failed at indexed, resumable; a resumed run appends a new ledger row"
    - "1.0: Initial version. One entry point for a dropped document: decides the treatment, converts Word / PowerPoint / Excel / HTML / web links to markdown, files a PDF as a book only when it is one, delegates to /ingest-source or /extract-insights, never asks, fixed closing summary, --all for the inbox, INTAKE-LEDGER.md (Abilityai/cornelius#19)"
---

# Intake

One document in, a short summary out. This playbook is a **router**: it does no extraction of its own. It works out what was handed over, turns it into something the extraction playbooks can read, runs the one that fits, and reports in a fixed shape.

## Purpose

A person who hands Cornelius a document should not need to know which playbook fits it, and should not be asked anything on the way. They drop a file or paste a link, and come back to a summary of what was written.

It serves three callers the same way:

- a person in a chat ("process this", with a file in the inbox or a path),
- a surface that offers a choice at drop time (it passes `--as`),
- a scheduled or batch run (`--all`).

## The rule that makes it unattended

**Never ask a question.** Nobody may be there to answer. Where a playbook this one calls would stop to ask or offer an interview, skip that part and say so in the summary. Where a decision cannot be made safely without a person, do not guess: **hold** the document (write nothing) and say what it is waiting for.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| The document | argument path or link | ✓ | | Never modified, never deleted |
| Inbox | `~/inbox/<person>/` | ✓ | | Where a hosted agent receives dropped files; one folder per person |
| Working markdown | `resources/ingest-workspace/<slug>/` | ✓ | ✓ | Converted markdown, when a conversion was needed |
| Intake ledger | `resources/ingest-workspace/INTAKE-LEDGER.md` | ✓ | ✓ | One row per document: what it was, what ran, the result |
| Knowledge base | `Brain/` | | via the called playbook | This playbook never writes notes itself |

## Arguments

- **`<file path>` or `<link>`** — the one document to take in.
- **no argument** — the newest file in `~/inbox/*/` that has no ledger row. If the inbox is empty, say so and end.
- **`--all`** — every inbox file with no ledger row, oldest first, one at a time (see *Clearing the inbox*).
- **`--as auto|source|own|keep`** — the treatment. Default `auto`: Cornelius decides.
  - `source` — someone else's material: a book, paper, article, report, video, somebody else's talk.
  - `own` — the person's own words: their notes, their conversations, their voice transcripts.
  - `keep` — keep the file for the conversation; run nothing.
- **`--from <person>`** — whose document this is. Default: the inbox folder name the file sits in, otherwise the vault's owner. When another agent dispatches the run on a person's word, record `<person> (via <agent>)`.

## Process

### Step 1: Resolve the document

```bash
date '+%Y-%m-%d'
LEDGER=resources/ingest-workspace/INTAKE-LEDGER.md
mkdir -p resources/ingest-workspace
test -f "$LEDGER" || printf '| date | from | document | sha | treatment | playbook | result |\n|---|---|---|---|---|---|---|\n' > "$LEDGER"
```

For a file: confirm it exists and is readable, then take its fingerprint with `{ shasum -a 256 "<file>" 2>/dev/null || sha256sum "<file>"; } | cut -c1-12` (`shasum` is a Perl tool that minimal Linux images lack). For a link: the fingerprint is the link itself.

**Already taken in?** If the ledger has a row with the same fingerprint and a result other than `failed`, do not run it again: print the summary with `Treatment: already taken in on <date>` and end. The same file dropped twice costs nothing.

Derive `<slug>` from the file name or the page title (lowercase, hyphens, 60 characters at most).

### Step 2: Work out what it is

Look before deciding. Read the first pages (for a long file: the first 200 lines of text and the table of contents if there is one). Establish:

1. **Format** — by extension, and by content when the extension lies or is missing.
2. **Kind** — a book; a paper, article, report or other document; a video or talk; a transcript or notes; reference data about a person, an organisation, a product or a deal; something else.
3. **Whose words** — the person's own (`--from`), or somebody else's.

Then choose the treatment. An explicit `--as` wins. With `auto`:

| What it is | Treatment | Playbook |
|---|---|---|
| Somebody else's book, paper, article, report, video, talk or transcript | `source` | `/ingest-source` |
| The person's own notes, conversations or voice transcripts | `own` | `/extract-insights` |
| Reference data about a person, organisation, product or deal | `hold` | none — it belongs in `/ref-ingest`, which needs a person present |
| Unreadable, empty, a format with no path in, or not knowledge at all (an installer, a photo with no text) | `keep` | none |

When it is honestly unclear whether the words are the person's own, choose `source`: a note marked as *encountered* can be promoted by a person later, and a note wrongly written in the person's voice is the worse mistake.

**A PDF is a book only when it is one.** `/ingest-source` files every `.pdf` as a book by its extension. Decide here instead: it is a book when it has chapters and a table of contents, or an ISBN, or runs past about 80 pages of continuous prose. A paper, a contract, a slide export or a ten-page report is not. A non-book PDF is converted to markdown in Step 3 and handed on as markdown, so it lands with the other documents and not on the book shelf.

### Step 3: Convert what the next playbook cannot read

`/ingest-source` reads `.epub`, `.mobi`, `.azw3`, book PDFs, YouTube links, `.md` and `.txt` by itself. `/extract-insights` reads text. Everything else is turned into markdown first, into `resources/ingest-workspace/<slug>/<name>.md`.

```bash
UV="$(command -v uv || echo "$HOME/.local/bin/uv")"
OUT="resources/ingest-workspace/<slug>"; mkdir -p "$OUT"
```

| Input | Conversion |
|---|---|
| `.docx` `.pptx` `.xlsx` `.html` `.htm` | `"$UV" run --with 'markitdown[docx,pptx,xlsx]' markitdown "<file>" -o "$OUT/<name>.md"` |
| a PDF that is not a book | `(cd "$(git rev-parse --show-toplevel)/.claude/skills/multi-format-book-extractor" && "$UV" run --with pymupdf --with requests python extract_book.py "<absolute path to pdf>" "$PWD/$OUT")` — absolute paths both, because the command runs inside the skill folder. It writes chapter or 20-page chunk files (`01_pages-1-20.md` ...): concatenate them in order into one `$OUT/<slug>.md` (source line first) and delete the chunks, because `/ingest-source` takes one path. Hand on that markdown, never the PDF |
| a web link that is not YouTube | `"$UV" run --with trafilatura trafilatura -u "<link>" --markdown --with-metadata > "$OUT/<name>.md"` (without `--with-metadata` the title, date and URL are lost; the frontmatter it writes counts as the source line); if the result is empty or under 500 characters, read the page with WebFetch and write its main text to the same file |
| `.rtf`, `.odt`, an email export | try the `markitdown` line above; if it fails, `keep` with the reason |
| a scanned document or an image of text | needs an OCR-capable model key (`GEMINI_API_KEY`); without one, `keep` with that reason |

After any conversion, check the result before going on: the file exists, has more than 500 characters, and reads as prose, not as markup or an error page. A page that is a login wall, a cookie notice or a "enable JavaScript" stub is a failed conversion: `keep`, with the reason. Put the source link or the original file name in the first line of the markdown (or in a `url:` frontmatter field, as trafilatura writes it), so the notes can cite where it came from. `markitdown` on a saved web page keeps the site's navigation links at the top; that is fine, judge the body, and tell the extractor to ignore the navigation lines.

If `uv` is missing, say so in the summary (`Skipped: no uv on this machine — run /first-run`) and `keep`.

### Step 4: Run the playbook

Run exactly one, with the Skill tool, and let it finish:

- **`source`** → `/ingest-source <prepared path or original file or YouTube link> "<session name>"` — add `--book` only for a book. It is already unattended. Session name: `"YYYY-MM-DD <Title> - <Author or organisation>"`, today's date.
- **`own`** → `/extract-insights <prepared path>` — it may offer an interview or ask a follow-up at the end: do not take it up and do not wait. Note the offer in the summary's `Skipped` line.
- **`hold`** / **`keep`** → run nothing.

If the called playbook rejects the source at its own gate (a content farm, machine-written filler), that is a result, not a failure: report `Treatment: rejected at the door` with its reason.

If it fails partway, do not retry here and do not clean up its checkpoint: record `failed` with the step it reached. Running `/intake` on the same file again resumes through that playbook's own checkpoint.

### Step 5: Ledger

Append one row:

```markdown
| YYYY-MM-DD | <from> | <file name or link> | <sha> | source / own / keep / hold / rejected | <playbook or -> | <N notes in <dir>> / kept / held: <why> / failed at <step> |
```

`<from>` is who handed the document over. It is the only record of whose material fed which notes, so always fill it in. A resumed run (the same document after a `failed` row) appends a new row and leaves the `failed` row as history; the newest row for a fingerprint is its state.

### Step 6: The summary

End with exactly this block and nothing after it. Six lines at most; leave a line out only when it has nothing to say.

```
INTAKE  <file name or link>
What it is:  <one line: kind, author or origin, length>
Treatment:   <source | own words | kept | held | rejected at the door | already taken in on DATE | failed>
Playbook:    </ingest-source | /extract-insights | none>
Written:     <N notes in <directory> — up to three titles> | nothing
Skipped:     <what was not done and why, or what it is waiting for> 
```

Examples of a good `Skipped` line: `interview offer not taken (unattended run)` · `scanned PDF, no OCR key` · `reference data about a client — run /ref-ingest with a person present` · `after the last source of a batch: /detect-tensions, /coherence-sweep, /graduate-insights`.

## Clearing the inbox (`--all`)

1. List every file under `~/inbox/*/` with no ledger row, oldest first. Print the count.
2. Take them **one at a time**, Steps 1–6 each, with `--from` set from the inbox folder. Each document gets its own summary block.
3. Stop starting new documents once 40 minutes have passed. What is left stays for the next run; nothing is half-done, because the ledger row is written per document.
4. End with one line after the last block: `INBOX  <done> taken in, <left> left, <failed> failed`.

Never run two documents at once: each one is extracted against the index the previous one just refreshed.

## What this playbook never does

- Ask a question, or wait for an answer.
- Write a note itself, or edit one the called playbook wrote.
- Delete, move or rename the document it was given.
- Promote anything to permanent notes. That stays a person's act (`/graduate-insights`).
- Take in reference data about people, organisations or deals without a person present.

## Error Recovery

| Situation | Do |
|---|---|
| File not found, or the link does not answer | `Treatment: failed`, `Skipped: <the error in plain words>`, ledger row `failed at resolve` |
| Conversion produced nothing usable | `keep`, with the reason; the original stays where it is |
| Search engine not installed (the called playbook reports an import error or an empty index) | `failed`, `Skipped: run /first-run, then /intake again` |
| The called playbook stopped at its time limit | `failed at <its checkpoint phase>`; the next `/intake` of the same file resumes |
| The index rebuild was killed (`run_index.sh: ... Killed`, out of memory - often another execution running at the same time) | `failed at indexed`: the notes are written and the vector index saved, but the graph is not, so nothing is linked. Do not retry in this run; the next `/intake` of the same document resumes at the index step |
| The inbox folder does not exist | not an error on a local machine: say `no inbox here — pass a path or a link` |

## Completion Checklist

- [ ] No question was asked
- [ ] Exactly one playbook ran, or none for `keep` / `hold`
- [ ] A PDF went to the book shelf only if it is a book
- [ ] The original document is untouched
- [ ] One ledger row was appended, with `<from>` filled in
- [ ] The closing block is the last thing printed, in the fixed shape

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: was a format refused that should have a path in? Did a conversion command fail as written?
- [ ] **Scope check**: only tactical changes — a new row in the conversion table, a clearer rule in Step 2 — never a change to "never ask"
- [ ] **Apply improvement** (if identified): edit this SKILL.md, bump `metadata.version`, prepend the changelog entry
- [ ] **Version control**: stage `.claude/skills/intake/` by path and commit
