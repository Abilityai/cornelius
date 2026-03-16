---
name: create-article
description: Create long-form articles from knowledge base insights. Use when writing articles, blog posts, Substack content, or synthesizing knowledge into publishable content. Includes tone of voice, structure templates, and knowledge base integration.
automation: gated
allowed-tools: Read, Grep, Glob, Write, Bash, Task
---

# Create Article Skill

Create publication-ready long-form articles by synthesizing insights from Eugene's knowledge base, following established tone of voice and structural patterns.

## Quick Start

1. **Search knowledge base** for relevant permanent notes on the topic
2. **Check Article Index** to avoid duplicates and see related work
3. **Create article folder** with proper structure
4. **Write article** following tone of voice guidelines
5. **Update Article Index** with new entry

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Permanent Notes | `Brain/02-Permanent/` | ✓ | | Core insights for synthesis |
| AI Extracted Notes | `Brain/AI Extracted Notes/` | ✓ | | AI-extracted insights |
| Document Insights | `Brain/Document Insights/` | ✓ | | Research extracts |
| MOCs | `Brain/03-MOCs/` | ✓ | | Topic overviews |
| Article Index | `Brain/04-Output/Articles/ARTICLE-INDEX.md` | ✓ | ✓ | Registry of all articles |
| Tone of Voice | `.claude/skills/create-article/tone-of-voice.md` | ✓ | | Voice DNA and writing style |
| Article Structure | `.claude/skills/create-article/article-structure.md` | ✓ | | Templates and patterns |
| Metadata Template | `.claude/skills/create-article/metadata-template.md` | ✓ | | Template for _metadata.md |
| Article Folder | `Brain/04-Output/Articles/[article-name]/` | | ✓ | Output folder for article |
| Main Article | `Brain/04-Output/Articles/[article-name]/[article-name].md` | | ✓ | The article itself |
| Metadata File | `Brain/04-Output/Articles/[article-name]/_metadata.md` | | ✓ | Creation record |

## Core Workflow

### Step 1: Research Phase

Search the knowledge base for relevant insights:

```bash
# Semantic search for topic
/Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search/run_search.sh "your topic" --limit 15 --json

# Find connections to existing notes
/Users/eugene/Dropbox/Agents/Cornelius/resources/local-brain-search/run_connections.sh "Related Note Name" --json
```

**Key locations to search:**
- `Brain/02-Permanent/` - Core insights and permanent notes
- `Brain/AI Extracted Notes/` - AI-extracted insights
- `Brain/Document Insights/` - Research extracts
- `Brain/03-MOCs/` - Maps of Content for topic overviews

### Step 2: Check Article Index

**MANDATORY**: Read the Article Index before creating any article:

```
Brain/04-Output/Articles/ARTICLE-INDEX.md
```

- Check for existing articles on similar topics
- Identify gaps in topic coverage
- Note related articles for cross-referencing

### Step 3: Create Article Structure

Create folder and files:

```
Brain/04-Output/Articles/[article-name]/
├── [article-name].md          # Main article
├── _metadata.md               # Creation record
└── [images if needed]
```

**Naming:** Use kebab-case (e.g., `cognitive-aware-ai-systems`)

### Step 4: Write Article

Follow the tone of voice and structure guidelines in:
- [tone-of-voice.md](tone-of-voice.md) - Voice DNA and writing style
- [article-structure.md](article-structure.md) - Templates and patterns

### Step 5: Update Article Index

Add entry to `ARTICLE-INDEX.md`:
- Article name and link
- Created date
- Topic category
- Status (Draft)
- Notes

## File References

For detailed guidance, see:

| File | Purpose |
|------|---------|
| [tone-of-voice.md](tone-of-voice.md) | Complete voice DNA, do's/don'ts, vocabulary |
| [article-structure.md](article-structure.md) | Templates for different article types |
| [metadata-template.md](metadata-template.md) | Template for _metadata.md files |

## Key Principles

### Voice Summary

Eugene's long-form voice transforms complex research into actionable business insights through methodical, evidence-based teaching. He challenges assumptions with data while maintaining accessibility, creating structured learning experiences that bridge academic rigor with practical application.

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

## Ruby Agent Integration

This skill can be called headlessly by Ruby agent for content production:

```bash
cd /Users/eugene/Dropbox/Agents/Cornelius
claude -p "/create-article <topic> for <platform>" --output-format json
```

**Response format for Ruby:**
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

When called by Ruby:
- Return article text directly (don't save to file)
- Include cited notes list
- Focus on Eugene's unique/contrarian perspectives

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
- [ ] Article folder created with kebab-case naming
- [ ] Main article written following tone of voice guidelines
- [ ] _metadata.md created with source insights and thinking process
- [ ] Article Index updated with new entry (date, topic, status)
- [ ] Article folder opened in Finder for user review
