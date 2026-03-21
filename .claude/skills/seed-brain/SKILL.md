---
name: seed-brain
description: Ingest foundational documents into the Brain - decompose into source notes, atomic permanent notes, and MOCs
automation: gated
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
user-invocable: true
metadata:
  version: "1.0"
  created: 2026-03-21
  author: Cornelius
---

# Seed Brain

## Purpose

Ingest a set of foundational documents and decompose them into a fully linked knowledge graph - source notes, atomic permanent notes, and Maps of Content - then index everything for semantic search.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Source documents | User-specified path(s) | ✓ | | Raw documents to ingest |
| Source notes | `$VAULT_BASE_PATH/01-Sources/` | | ✓ | Full documents stored as reference |
| Permanent notes | `$VAULT_BASE_PATH/02-Permanent/` | ✓ | ✓ | Atomic insight notes |
| MOCs | `$VAULT_BASE_PATH/03-MOCs/` | ✓ | ✓ | Maps of Content |
| Master Navigation | `$VAULT_BASE_PATH/03-MOCs/MOC - Master Navigation.md` | ✓ | ✓ | Top-level vault navigation |
| Changelogs | `$VAULT_BASE_PATH/05-Meta/Changelogs/` | | ✓ | Session record |
| CHANGELOG.md | `$VAULT_BASE_PATH/CHANGELOG.md` | ✓ | ✓ | Master changelog |
| Brain Search Index | `resources/local-brain-search/data/` | | ✓ | FAISS index and graph |

## Prerequisites

- Brain folder exists with standard Zettelkasten structure (00-Inbox through 05-Meta)
- Source documents are accessible as markdown, text, or PDF files
- Local Brain Search venv is set up (if re-indexing is desired)

## Inputs

- `$0`: Path to source documents - can be a directory (all .md files inside) or a list of specific file paths
- `$1`: (Optional) Theme or domain name for the seeding session (e.g., "Luminous Foundational Documents")

---

## Process

### Step 1: Read and Catalogue Source Documents

1. Read all documents from the provided path(s)
2. For each document, extract:
   - Title
   - Word count
   - Key themes and sections
   - Type of content (manifesto, framework, profile, strategy, etc.)
3. Present catalogue to user:

```
## Source Documents Found

| # | Document | Words | Type | Key Themes |
|---|----------|-------|------|------------|
| 1 | [title] | [count] | [type] | [themes] |
| ... | ... | ... | ... | ... |

Total: N documents, ~X words
```

### Step 2: Check Existing Brain State

1. Count existing notes in `02-Permanent/`
2. Count existing MOCs in `03-MOCs/`
3. Count existing source notes in `01-Sources/`
4. Check for potential duplicates - search existing permanent note titles against key concepts in new documents
5. Report current state:

```
## Current Brain State

- Permanent notes: N
- Source documents: N
- MOCs: N
- Potential overlaps: [list any]
```

### Step 3: Design Decomposition Plan

Analyse all source documents and produce a decomposition plan:

1. **Source notes** - One per document, stored in `01-Sources/`
2. **Permanent notes** - Atomic insights extracted from each document. For each proposed note:
   - Title (states the insight)
   - Source document
   - Tags
   - Related notes (cross-links to other proposed notes AND existing notes)
3. **MOCs** - Thematic clusters that emerge from the permanent notes
4. **Cross-links** - Map the connection network between all proposed notes

**Design principles:**
- One idea per permanent note (50-300 words)
- Titles state the insight, not the topic (e.g., "Wealth is energy - integrity is compass" not "About wealth")
- Every note links back to its source
- Every note links forward to 2-3 related permanent notes
- Use hyphens (-) not em-dashes
- Match the voice and tone of the source material
- British English unless sources use American English
- Tags: 3-5 per note, lowercase, hyphenated

Present the full plan:

```
## Decomposition Plan

### Source Notes (N files)
[list with filenames]

### Permanent Notes (N files)
Grouped by source document:

**From [Document 1] (N notes):**
1. [Title] - [one-line description]
   Tags: [tags]
   Links to: [[Note A]], [[Note B]]
2. ...

**From [Document 2] (N notes):**
...

### Proposed MOCs (N)
1. [MOC Name] - [what it covers] (N notes)
2. ...

### Network Summary
- Total notes: N
- Cross-links: N connections
- Average links per note: N
```

### Step 4: Review Decomposition Plan

[APPROVAL GATE] - Review proposed notes before creation

**Present to user:**
- Full decomposition plan from Step 3
- Highlight any notes that might overlap with existing content
- Note any source material that was intentionally NOT decomposed (and why)

**User options:**
1. **Approve** - Create all proposed notes
2. **Modify** - Add, remove, rename, or restructure proposed notes
3. **Abort** - Cancel seeding

If modifications requested:
- Apply changes to the plan
- Return to this gate for re-review

### Step 5: Create Source Notes

For each source document, create a source note in `01-Sources/`:

1. Read the original file
2. Write to `$VAULT_BASE_PATH/01-Sources/[Document Title].md` with:

```yaml
---
created: [today]
updated: [today]
created_by: [model-name]
updated_by: [model-name]
agent_version: [current version from CLAUDE.md]
type: source
---
```

3. Preserve the full original content below the frontmatter

**Parallelisation:** Use vault-manager agents to create source notes in parallel batches.

### Step 6: Create Permanent Notes

For each approved permanent note, create in `02-Permanent/`:

1. Write to `$VAULT_BASE_PATH/02-Permanent/[Note Title].md` with:

```yaml
---
created: [today]
updated: [today]
created_by: [model-name]
updated_by: [model-name]
agent_version: [current version from CLAUDE.md]
tags: [tags from plan]
type: permanent
---
```

2. Content structure:
   - H1 title (same as filename without .md)
   - 2-4 paragraphs expressing the insight (50-300 words)
   - `**Source**: [[Source Note Name]]`
   - `**Related concepts**:` with wikilinks and brief connection descriptions

**Writing guidelines:**
- Write in the voice of the source material
- Use the user's language and framing where possible
- Each note must stand alone - a reader unfamiliar with the source should understand the insight
- Link descriptions explain HOW the notes connect, not just that they do

**Parallelisation:** Use vault-manager agents to create permanent notes in parallel batches of 15-20 notes each.

### Step 7: Create MOCs

For each proposed MOC:

1. Write to `$VAULT_BASE_PATH/03-MOCs/MOC - [Theme Name].md` with:

```yaml
---
created: [today]
updated: [today]
created_by: [model-name]
updated_by: [model-name]
agent_version: [current version from CLAUDE.md]
type: moc
---
```

2. Content structure:
   - H1 title
   - 1-2 sentence overview
   - Sections grouping related permanent notes with wikilinks and brief context
   - Related MOCs section
   - Key Sources section

### Step 8: Update Master Navigation

Read `MOC - Master Navigation.md` and update:

1. Add new MOCs to the appropriate section
2. Update vault statistics (permanent notes count, source count, MOC count)
3. Update the "Last Updated" date
4. Preserve any existing content that is still valid

### Step 9: Create Changelog

1. Create session changelog at `$VAULT_BASE_PATH/05-Meta/Changelogs/CHANGELOG - Brain Seeding [date].md`:
   - List all source documents ingested
   - Count of notes created by type
   - Table of permanent notes grouped by source
   - Knowledge graph structure summary

2. Update `$VAULT_BASE_PATH/CHANGELOG.md` with a summary entry

### Step 10: Re-index Brain Search

Run the Local Brain Search indexer:

```bash
./resources/local-brain-search/run_index.sh
```

If the venv is not set up, inform the user:

```bash
cd resources/local-brain-search
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run_index.sh
```

Report index results:
- Notes indexed
- Chunks created
- Graph edges (explicit + semantic)

### Step 11: Verify

Run verification checks:

1. Count files: source notes, permanent notes, MOCs match the plan
2. Spot-check 2-3 permanent notes for proper frontmatter, links, and content quality
3. Run a test search against a key concept from the source documents
4. Report final state:

```
## Brain Seeding Complete

### Created
- Source notes: N
- Permanent notes: N
- MOCs: N (+ Master Navigation updated)
- Changelog: 1

### Knowledge Graph
- Total notes: N (was: M)
- Graph edges: N (explicit: X, semantic: Y)

### Verification
- Frontmatter: ✓
- Cross-links: ✓
- Search test: ✓ (query: "[term]" returned N results)
```

---

## Outputs

- Source notes in `01-Sources/`
- Permanent notes in `02-Permanent/`
- MOCs in `03-MOCs/`
- Updated Master Navigation
- Session changelog
- Updated FAISS index

## Error Recovery

If this playbook fails mid-execution:

**Before Step 4 (approval gate):**
- No files created yet
- Safe to re-run from beginning

**During Steps 5-7 (file creation):**
- Partially created notes exist
- Check what was created: `find Brain/02-Permanent -newer Brain/CHANGELOG.md -name "*.md"`
- Delete incomplete batch and re-run from Step 5

**After Step 9 (changelog written):**
- All content created successfully
- If index failed, just run `./resources/local-brain-search/run_index.sh` manually

## Completion Checklist

- [ ] All source documents read and catalogued
- [ ] Existing brain state checked for duplicates
- [ ] Decomposition plan approved by user
- [ ] Source notes created
- [ ] Permanent notes created with proper frontmatter, links, and content
- [ ] MOCs created linking to all relevant permanent notes
- [ ] Master Navigation updated
- [ ] Changelog written
- [ ] Brain Search index rebuilt
- [ ] Verification checks passed
