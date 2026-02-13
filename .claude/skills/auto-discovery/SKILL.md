---
name: auto-discovery
description: Discover non-obvious cross-domain connections through random sampling and pattern analysis
automation: autonomous
schedule: "0 20 * * 0"
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Auto-Discovery

Autonomous cross-domain connection hunter. Samples notes from different thematic clusters and finds meaningful relationships that semantic similarity alone would miss.

## Purpose

Find **non-obvious, cross-domain connections** - notes with low semantic similarity (0.50-0.70) but high conceptual strength. These are the hidden patterns in the knowledge base.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Permanent Notes | `Brain/02-Permanent/` | ✓ | | Sampling source |
| AI Extracted Notes | `Brain/AI Extracted Notes/` | ✓ | | Sampling source |
| Document Insights | `Brain/Document Insights/` | ✓ | | Sampling source |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Similarity scores, connections |
| Session Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Dated discovery log |
| Master Changelog | `Brain/CHANGELOG.md` | ✓ | ✓ | Summary entry |

## Prerequisites

- Local Brain Search index up-to-date (`/refresh-index`)
- Brain vault accessible

## Process

### Step 1: Get Current Date

```bash
date '+%Y-%m-%d'
```

Use for changelog filename.

### Step 2: Strategic Sampling

Sample from 3-5 diverse domains using Local Brain Search:

```bash
resources/local-brain-search/run_search.sh "dopamine" --limit 5 --json
resources/local-brain-search/run_search.sh "uncertainty" --limit 5 --json
resources/local-brain-search/run_search.sh "identity" --limit 5 --json
```

Pick seed notes from different clusters.

### Step 3: Get Connections for Seeds

For each seed note:

```bash
resources/local-brain-search/run_connections.sh "Note Name" --json
```

Identify notes with similarity 0.50-0.70 from DIFFERENT domains.

### Step 4: Cross-Domain Analysis

For each cross-domain pair:
1. Read both notes fully
2. Record ACTUAL similarity score from search
3. Analyze for:
   - Shared structural patterns
   - Common mechanisms
   - Meta-principles
   - Paradoxes

Rate conceptual strength (1-5 stars).

**Target:** Low semantic similarity + high conceptual strength = valuable discovery.

### Step 5: Document Discoveries

For each strong connection:

```markdown
## CROSS-DOMAIN CONNECTION

**Node A**: [[Note X]] (Domain: Neuroscience)
**Node B**: [[Note Y]] (Domain: Economics)
**Semantic Similarity**: 0.63 (actual from search)
**Conceptual Strength**: ⭐⭐⭐⭐⭐

**The Link**: [2-3 sentences explaining WHY they connect]
**Shared Pattern**: [The underlying principle]
**Synthesis Opportunity**: [Potential new note title]
```

### Step 6: Create Dated Changelog

Write to `Brain/05-Meta/Changelogs/CHANGELOG - Auto-Discovery Session YYYY-MM-DD.md`:

```markdown
## Auto-Discovery Session: YYYY-MM-DD

### Session Parameters
- Notes sampled: [N] from [X] clusters
- Domains analyzed: [list]

### Discoveries Made
**Strong Connections**: [N]
1. [[A]] ↔ [[B]] - [pattern]

**Meta-Patterns**: [N]
**Consilience Zones**: [N]

### Session Statistics
- Total notes analyzed: [N]
- Non-obvious connections (similarity < 0.70): [N]
```

### Step 7: Update Master Changelog

Add brief summary to `Brain/CHANGELOG.md`:

```markdown
## YYYY-MM-DD - Auto-Discovery Session

See: [[CHANGELOG - Auto-Discovery Session YYYY-MM-DD]]
- [N] connections discovered
- [N] meta-patterns identified
```

## Quality Standards

**GOOD discoveries:**
- Semantic similarity 0.50-0.70
- Clear conceptual link across domains
- "Aha!" factor - non-obvious insight
- Actionable synthesis opportunity

**SKIP:**
- High similarity (0.85+) - too obvious
- Same domain - not cross-domain
- Already linked in vault

## Error Handling

| Error | Recovery |
|-------|----------|
| Search returns empty | Try different seed terms |
| All high similarity | Note in changelog, try broader clusters |
| Index outdated | Run `/refresh-index` first |

## Completion Checklist

- [ ] Notes sampled from 3+ different clusters
- [ ] ACTUAL similarity scores recorded (not estimated)
- [ ] Cross-domain connections with conceptual analysis
- [ ] Non-obvious discoveries documented (similarity < 0.70)
- [ ] Dated changelog created in `Brain/05-Meta/Changelogs/`
- [ ] Master changelog updated with summary
