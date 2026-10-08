---
name: create-article
description: Create long-form articles from knowledge base insights. Use when writing articles, blog posts, Substack content, or synthesizing knowledge into publishable content. Includes tone of voice, structure templates, and knowledge base integration.
automation: gated
allowed-tools: Read, Grep, Glob, Write, Bash, Task, WebSearch, WebFetch
metadata:
  version: "1.1"
  updated: 2026-07-27
  changelog:
    - "1.1: Add Thought-Leader & Market Scan step (recent external voices via WebSearch under SOURCE-AUTHORITY, with integration proposals recorded in _metadata.md) and an explicit Fact-Check step before finalization"
    - "1.0: Initial version (KB research, index check, tone-of-voice drafting, index update, Drive upload)"
---

# Create Article Skill

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `create-article vX.Y — recent: <summary>`. Then proceed.

Create publication-ready long-form articles by synthesizing insights from the user's knowledge base, following established tone of voice and structural patterns.

## Quick Start

1. **Search knowledge base** for relevant permanent notes on the topic
2. **Check Article Index** to avoid duplicates and see related work
3. **Scan thought leaders** for their most recent takes on the topic; propose integrations
4. **Create article folder** with proper structure
5. **Write article** following tone of voice guidelines
6. **Fact-check the draft** - verify every claim, quote, and statistic
7. **Update Article Index** with new entry
8. **Upload to Google Drive** `Articles/cornelius_drafts` for review

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Permanent Notes | `Brain/02-Permanent/` | ✓ | | Core insights for synthesis |
| AI Extracted Notes | `Brain/AI Extracted Notes/` | ✓ | | AI-extracted insights |
| Document Insights | `Brain/Document Insights/` | ✓ | | Research extracts |
| MOCs | `Brain/03-MOCs/` | ✓ | | Topic overviews |
| Article Index | `Brain/04-Output/Articles/ARTICLE-INDEX.md` | ✓ | ✓ | Registry of all articles |
| Source Authority | `resources/SOURCE-AUTHORITY.md` | ✓ | | Trusted-source diet for the thought-leader scan and fact-checking |
| Web | WebSearch / WebFetch | ✓ | | Recent thought-leader statements; claim verification |
| Tone of Voice | `.claude/skills/create-article/tone-of-voice.md` | ✓ | | Voice DNA and writing style |
| Article Structure | `.claude/skills/create-article/article-structure.md` | ✓ | | Templates and patterns |
| Metadata Template | `.claude/skills/create-article/metadata-template.md` | ✓ | | Template for _metadata.md |
| Article Folder | `Brain/04-Output/Articles/[article-name]/` | | ✓ | Output folder for article |
| Main Article | `Brain/04-Output/Articles/[article-name]/[article-name].md` | | ✓ | The article itself |
| Metadata File | `Brain/04-Output/Articles/[article-name]/_metadata.md` | | ✓ | Creation record |
| Google Drive | `Articles/cornelius_drafts` (shared drive) | | ✓ | Upload article folder for review |
| Drive Folder Map | `.claude/resources/google_drive_folders.md` | ✓ | | Google Drive folder IDs |

## Core Workflow

### Step 1: Research Phase

Search the knowledge base for relevant insights:

```bash
# read role: voice (contract: scope-mount) - an article is the user's voice, so the source pass is pinned to core explicitly
# Semantic search for topic
BRAIN_READ_SCOPE=core resources/local-brain-search/run_search.sh "your topic" --limit 15 --json

# Find connections to existing notes
BRAIN_READ_SCOPE=core resources/local-brain-search/run_connections.sh "Related Note Name" --json
```

**Key locations to search:**
- `Brain/02-Permanent/` - Core insights and permanent notes
- `Brain/AI Extracted Notes/` - AI-extracted insights
- `Brain/Document Insights/` - Research extracts
- `Brain/03-MOCs/` - Maps of Content for topic overviews

**Enrich with BDG context** (optional - reveals which notes are generative frameworks vs reflective):
```bash
resources/brain-graph/run_brain_graph.sh inspect "Key Source Note" --json
```

### Step 2: Check Article Index

**MANDATORY**: Read the Article Index before creating any article:

```
Brain/04-Output/Articles/ARTICLE-INDEX.md
```

- Check for existing articles on similar topics
- Identify gaps in topic coverage
- Note related articles for cross-referencing

### Step 3: Thought-Leader & Market Scan

Search the web for what recognized thought leaders in the article's domain have said MOST RECENTLY (prefer the last 3-6 months) on the article's topics:

- Use WebSearch for recent essays, posts, interviews, talks, and papers
- Apply `resources/SOURCE-AUTHORITY.md` (canonical source diet) to decide which voices and outlets to trust, demote, or reject
- For each relevant voice capture: who, their claim, where/when (link + date)

Then propose how to integrate each into the article:

- **Agrees** - supports the user's thesis: cite as market reinforcement
- **Extends** - adds a dimension the KB doesn't cover: integrate with attribution
- **Contrasts** - opposes the user's view: position the user's take as a deliberate contrarian stance against the named mainstream position

Record the scan and chosen integrations in `_metadata.md` under "External Voices" (see [metadata-template.md](metadata-template.md)). If no relevant recent voices are found, note that too - absence of market conversation is itself a signal.

Purpose: every article demonstrates awareness of the current market conversation - the user's perspective is positioned relative to it, never written in a vacuum.

### Step 4: Create Article Structure

Create folder and files:

```
Brain/04-Output/Articles/[article-name]/
├── [article-name].md          # Main article
├── _metadata.md               # Creation record
└── [images if needed]
```

**Naming:** Use kebab-case (e.g., `cognitive-aware-ai-systems`)

### Step 5: Write Article

Follow the tone of voice and structure guidelines in:
- [tone-of-voice.md](tone-of-voice.md) - Voice DNA and writing style
- [article-structure.md](article-structure.md) - Templates and patterns

Weave in the integrations chosen in Step 3 - external voices appear with attribution (name, source, date), and the user's position is stated relative to them.

### Step 6: Fact-Check the Draft

Verify every factual claim before finalizing:

- **Internal claims**: statements sourced from KB notes match what the notes actually say (spot-check each [[citation]])
- **External claims**: statistics, dates, quotes, and attributions verified via WebSearch against `resources/SOURCE-AUTHORITY.md`-tier sources
- **Thought-leader quotes**: exact wording, correct attribution, working link
- **Recency**: any "current state" claims checked against the latest available data

Fix or remove anything that fails verification. If a claim is load-bearing but unverifiable, flag it in `_metadata.md` and either hedge it explicitly in the text or cut it.

### Step 7: Update Article Index

Add entry to `ARTICLE-INDEX.md`:
- Article name and link
- Created date
- Topic category
- Status (Draft)
- Notes

### Step 8: Upload to Google Drive

Upload the article folder to `Articles/cornelius_drafts` on the shared Google Drive:

```bash
# Upload the entire article folder (with images, metadata, etc.)
python3 .claude/scripts/google/google_drive.py upload-folder "Brain/04-Output/Articles/[article-name]" 1fxxbEwS86gguYXA1hJsFesr13ruXx80S --recursive
```

**Google Drive folder IDs**: See `.claude/resources/google_drive_folders.md`

- `Articles/cornelius_drafts` folder ID: `1fxxbEwS86gguYXA1hJsFesr13ruXx80S`
- This puts the article where the user and a content agent can access it for review and publishing
- The folder preserves the same structure as the local article folder

## File References

For detailed guidance, see:

| File | Purpose |
|------|---------|
| [tone-of-voice.md](tone-of-voice.md) | Complete voice DNA, do's/don'ts, vocabulary |
| [article-structure.md](article-structure.md) | Templates for different article types |
| [metadata-template.md](metadata-template.md) | Template for _metadata.md files |

## Key Principles

### Voice Summary

the user's long-form voice transforms complex research into actionable business insights through methodical, evidence-based teaching. He challenges assumptions with data while maintaining accessibility, creating structured learning experiences that bridge academic rigor with practical application.

### Essential Do's

- Open with clear learning objectives or discoveries
- Cite specific research, studies, and data points
- Use numbered lists and bullet points for complex info
- Include TL;DR or summary sections
- Define technical terms immediately after introducing them
- Build arguments systematically from evidence to conclusion
- Provide actionable frameworks readers can apply

### Essential Don'ts

- Never make claims without supporting evidence
- Avoid emotional appeals without data backing
- Don't use jargon without clear explanations
- Never hedge with "maybe" or passive voice
- Avoid corporate buzzwords ("synergy", "leverage", "utilize")

## Platform-Specific Guidelines

Adjust content based on target platform:

| Platform | Word Count | Depth | Structure |
|----------|------------|-------|-----------|
| **Substack** | 1,500-3,000 | Deep dive, full research | Long-form template with TL;DR |
| **Medium** | 1,500-2,500 | Comprehensive but focused | Clear sections, strong hook |
| **LinkedIn** | 800-1,200 | Punchy, business-focused | Shorter paragraphs, bold insights |
| **Blog** | 1,200-2,500 | Flexible | Depends on audience |

### Platform Adjustments

**Substack/Newsletter:**
- More personal voice allowed
- Can use "I've found..." openings
- Encourage replies/engagement at end
- Include "Further reading" section

**Medium:**
- Strong SEO-friendly title
- Compelling subtitle
- Use images/diagrams
- End with clear takeaway

**LinkedIn:**
- Shorter paragraphs (2-3 sentences)
- More white space
- Lead with insight, not setup
- Business application focus
- End with question to drive engagement

---

## Content-Agent Integration

This skill can be called headlessly by content agent for content production:

```bash
cd $PROJECT_ROOT
claude -p "/create-article <topic> for <platform>" --output-format json
```

> **Caller scope:** this is the *workstation* invocation path - a content agent runs on the user's machine with an
> authenticated Claude Code CLI. A caller running **inside a Trinity container cannot use `claude -p`**
> (turn-scoped credentials, plus the ent#643 no-CLI-subprocess rule); it must call
> `chat_with_agent("cornelius", "...")` over Trinity MCP instead.

**Response format for a content agent:**
```json
{
  "result": "[Full article text with [[note citations]]]",
  "metadata": {
    "word_count": 1847,
    "platform": "substack",
    "cited_notes": ["Note 1", "Note 2", "Note 3"]
  }
}
```

When called by a content agent:
- Return article text directly (don't save to file)
- Include cited notes list
- Focus on the user's unique/contrarian perspectives

---

## Output Location

All articles go to: `Brain/04-Output/Articles/[article-name]/`

After creation, open the folder:
```bash
open "Brain/04-Output/Articles/[article-name]/"
```

## Completion Checklist

- [ ] Knowledge base searched for relevant permanent notes
- [ ] Article Index checked for duplicates and related work
- [ ] Thought-leader scan completed; external voices integrated or their absence noted in _metadata.md
- [ ] Article folder created with kebab-case naming
- [ ] Main article written following tone of voice guidelines
- [ ] All factual claims fact-checked; quotes and statistics verified with working links
- [ ] _metadata.md created with source insights, external voices, and thinking process
- [ ] Article Index updated with new entry (date, topic, status)
- [ ] Article folder uploaded to Google Drive `Articles/cornelius_drafts`
- [ ] Article folder opened in Finder for user review
