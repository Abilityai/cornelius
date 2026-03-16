# Temporal Memory Requirements

**Created:** 2026-03-02
**Status:** Draft
**Priority:** High

---

## Problem Statement

1. **No automated value signal** - We cannot reliably track which retrieved notes are actually valuable (read, used, referenced). Without this feedback, automated reinforcement/decay is premature.

2. **Flat retrieval** - All notes weighted equally regardless of their curation status. Permanent notes (validated insights) treated same as raw extractions.

3. **No graduation path** - Insights extracted by AI accumulate in holding folders without systematic review for promotion to permanent notes.

4. **Ephemeral content mixed with evergreen** - News/time-sensitive content stored alongside permanent insights without temporal context.

---

## Design Principles

- **Human-in-the-loop consolidation** - Graduation to permanent requires human judgment
- **Explicit tier encoding** - Use existing folder structure, don't create parallel systems
- **Additive changes only** - Enhance search scoring, don't restructure vault
- **No premature automation** - Skip decay/reinforcement until we have real usage feedback

---

## Requirements

### 1. Tier-Aware Search Scoring

**Goal:** Permanent notes should rank higher than unvalidated extractions at equivalent semantic similarity.

**Implementation:**

Add tier detection and weighting in `search.py`:

```python
TIER_WEIGHTS = {
    'permanent': 1.3,      # 02-Permanent/
    'moc': 1.2,            # 03-MOCs/
    'source': 1.0,         # 01-Sources/
    'extracted': 0.9,      # AI Extracted Notes/
    'document_insight': 0.85,  # Document Insights/
    'inbox': 0.7,          # 00-Inbox/
    'default': 1.0,
}

def get_tier_weight(filepath: str) -> float:
    """Determine tier weight from filepath."""
    if '/02-Permanent/' in filepath:
        return TIER_WEIGHTS['permanent']
    elif '/03-MOCs/' in filepath:
        return TIER_WEIGHTS['moc']
    # ... etc
```

Apply after similarity scoring:
```python
result['score'] = result['similarity'] * get_tier_weight(result['filepath'])
```

**Files to modify:** `search.py`, `memory_config.py` (add TIER_WEIGHTS config)

**Acceptance criteria:**
- [ ] Permanent notes rank higher than extracted notes at same similarity
- [ ] Tier weights configurable in `memory_config.py`
- [ ] No changes to index structure required

---

### 2. Graduation Skill

**Goal:** Regular procedure to review AI-extracted insights and promote valuable ones to permanent notes.

**Skill name:** `/graduate-insights`

**Behavior:**
1. Find notes in `AI Extracted Notes/` older than N days (default: 14)
2. For each candidate:
   - Show note title and content preview
   - Show Q-value if available (indicates retrieval frequency)
   - Show connections to permanent notes
3. User decides: **Promote** / **Archive** / **Skip** / **Delete**
4. Promote action:
   - Move to `02-Permanent/`
   - Update frontmatter with promotion date
   - Optionally refine title/content

**Trigger:** Manual, but recommend weekly cadence

**Files to create:** `.claude/skills/graduate-insights/SKILL.md`

**Acceptance criteria:**
- [ ] Lists candidates with age and Q-value
- [ ] Supports batch review (multiple notes per session)
- [ ] Moves files correctly, updates frontmatter
- [ ] Creates changelog entry for promotions

---

### 3. Ephemeral Content Handling

**Goal:** News and time-sensitive content should be clearly marked so retrieval can interpret recency.

**Approach A - Frontmatter tag:**
```yaml
---
content_type: news
arrival_date: 2026-03-02
expires: 2026-04-02  # Optional
---
```

**Approach B - Dedicated folder:**
```
Brain/
└── 06-Ephemeral/
    └── 2026-03/
        └── article-title.md
```

**Recommendation:** Approach A (frontmatter) - less structural change, metadata travels with note.

**Search behavior:**
- When retrieving ephemeral content, include arrival_date in result metadata
- Agent interprets recency contextually (no automated decay)

**Files to modify:**
- `index_brain.py` - Extract `content_type` and `arrival_date` to metadata
- `search.py` - Include temporal metadata in results

**Acceptance criteria:**
- [ ] Ephemeral notes tagged with arrival date
- [ ] Search results include temporal metadata when present
- [ ] No automated decay or expiration (human decides relevance)

---

### 4. Index Metadata Extension

**Goal:** Store tier and temporal metadata for efficient retrieval.

**Add to chunk metadata:**
```python
{
    # Existing fields...
    'tier': 'permanent' | 'extracted' | 'document_insight' | 'inbox' | ...,
    'content_type': 'evergreen' | 'news' | None,
    'arrival_date': '2026-03-02' | None,  # From frontmatter or file ctime
    'created': '2026-03-02',  # File creation date
}
```

**Files to modify:** `index_brain.py`

**Acceptance criteria:**
- [ ] Tier derived from filepath during indexing
- [ ] Frontmatter `content_type` and `arrival_date` extracted
- [ ] Backward compatible (missing fields default to None)

---

## Out of Scope (Explicitly Deferred)

| Feature | Reason |
|---------|--------|
| Automated decay | No reliable value signal to know what should decay |
| Usage-based reinforcement | Cannot track actual usage (read/reference/link) |
| Automatic promotion | Requires human judgment |
| Danger zone alerts | Premature without decay mechanism |
| Cross-domain detection | Nice-to-have, not core to tier system |

---

## Implementation Order

1. **Index metadata extension** - Add tier/temporal fields (required for steps 2-3)
2. **Tier-aware scoring** - Boost permanent notes in search
3. **Graduation skill** - Manual review process
4. **Ephemeral tagging** - For new news/time-sensitive content

---

## Future Considerations

When we CAN track actual usage (e.g., hook into Read tool, track citations):

1. Re-enable Q-value learning with real signals
2. Implement access-based recency (last_accessed timestamp)
3. Consider automated promotion suggestions based on usage patterns
4. Add decay for low-usage ephemeral content

Until then, human curation remains the consolidation mechanism.

---

*Requirements derived from temporal memory research session 2026-03-02. See `scripts/research/temporal-memory-systems-ai-agents-2026-03-02.md` for research context.*
