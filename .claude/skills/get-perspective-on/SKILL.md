---
name: get-perspective-on
description: Extract the user's perspective on a topic (called by a content agent or user)
automation: autonomous
---

# Get Perspective On

Extract the user's unique perspective on a topic from the knowledge base. Returns brief, focused insights (not full article). Can be called directly by user or via content agent in headless mode.

## Usage

```
/get-perspective-on <topic or question>
```

## Parameters

- **topic or question**: What perspective to retrieve
  - Specific topic
  - Question format
  - Comparison
  - Application

## Examples

```
/get-perspective-on AI agent adoption barriers
/get-perspective-on Why do companies resist AI?
/get-perspective-on How dopamine relates to social media
/get-perspective-on What's contrarian about my AI views?
```

## Workflow

1. **Search Knowledge Base** - **read role: voice** (contract: `scope-mount`): this is the user's perspective, so the read is pinned to `core` explicitly, never widened and never inherited. `Books/` and `Document Insights/` are what he has *read*, not his view - they do not belong in a perspective answer.
   ```bash
   BRAIN_READ_SCOPE=core resources/local-brain-search/run_search.sh "<topic>" --mode spreading --limit 8 --json
   BRAIN_READ_SCOPE=core resources/local-brain-search/run_connections.sh "<top note>" --json
   ```
   - Find 3-5 most relevant permanent notes
   - Look for contrarian or non-obvious angles

2. **Synthesize Perspective**
   - Brief format (1-3 paragraphs)
   - Focus on unique angles
   - Cite specific permanent notes
   - Include "why this matters"

3. **Return Response**
   - For direct user: Display perspective with citations
   - For a content agent headless: Return text for content use

## Output Format

```
🧠 the user's Perspective: [Topic]

[1-3 paragraphs synthesizing unique insights from permanent notes]

Key insights:
- [Insight 1 from [[Note A]]]
- [Insight 2 from [[Note B]]]
- [Insight 3 connecting [[Note C]] and [[Note D]]]

Why this matters:
[Brief explanation of significance or application]

📝 Cited Notes:
- [[Note Title 1]]
- [[Note Title 2]]
- [[Note Title 3]]
```

## Integration with a content agent

When a content agent calls via headless mode:
```bash
cd $PROJECT_ROOT
claude -p "/get-perspective-on 'AI adoption barriers'" --output-format json
```

> **Caller scope:** this is the *workstation* invocation path - a content agent runs on the user's machine with an
> authenticated Claude Code CLI. A caller running **inside a Trinity container cannot use `claude -p`**
> (turn-scoped credentials, plus the ent#643 no-CLI-subprocess rule); it must call
> `chat_with_agent("cornelius", "...")` over Trinity MCP instead.

a content agent receives:
```json
{
  "result": "[Perspective text with citations]",
  "total_cost_usd": 0.34
}
```

## Quality Criteria

Good perspective:
✅ Cites 3-5 specific permanent notes
✅ Highlights contrarian or non-obvious angles
✅ Connects to broader themes
✅ Includes concrete examples
✅ Authentic your voice

Weak perspective (regenerate):
❌ Generic AI knowledge
❌ No specific note citations
❌ Surface-level analysis
❌ Lacks unique angles

## Use Cases

- Quick content ideas for social posts
- Video script foundations
- Article brainstorming
- Perspective validation
- Connection discovery

## Notes

- Keep brief (1-3 paragraphs)
- Focus on what's unique to the user's thinking
- Always cite permanent notes
- Emphasize non-obvious connections
- Cost: ~$0.30-0.40 per call

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | Permanent notes for perspective synthesis |
| AI Insights | `Brain/AI Extracted Notes/` | X | | AI-extracted unique perspectives |
| Document Insights | `Brain/Document Insights/` | X | | Research-based insights |
| Local Brain Search | `resources/local-brain-search/` | X | | Semantic search for relevance |

## Completion Checklist

- [ ] Knowledge base searched for topic
- [ ] 3-5 most relevant permanent notes identified
- [ ] Contrarian or non-obvious angles prioritized
- [ ] Perspective synthesized (1-3 paragraphs)
- [ ] Specific permanent notes cited
- [ ] "Why this matters" included
- [ ] Output formatted for user or a content agent consumption
