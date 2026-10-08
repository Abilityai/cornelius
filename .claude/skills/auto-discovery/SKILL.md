---
name: auto-discovery
description: Discover non-obvious cross-domain connections through random sampling and pattern analysis
automation: autonomous
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Auto-Discovery

Autonomous cross-domain connection hunter. Samples notes from different thematic clusters and finds meaningful relationships that semantic similarity alone would miss.

## Purpose

Find **non-obvious, cross-domain connections** - notes with modest semantic similarity but high conceptual strength. These are the hidden patterns in the knowledge base.

> **Calibration correction (2026-09-02).** This skill's historic sweet spot of "0.50-0.70 = the
> non-obvious tail" was **inverted**: measured on the live index, 0.50-0.70 is the *typical* band
> (median best-neighbour 0.724 vault-wide), and the 0.85+ band it told you to skip as "too obvious"
> is dominated by boilerplate twins rather than real conceptual overlap. The discriminator was never
> the number - it is **cross-domain reasoning after reading the notes**. Use similarity only to
> assemble a candidate pool, never to grade a discovery. Contract + live figures: `resources/local-brain-search/SIMILARITY-CALIBRATION.md`.

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
# --no-track: autonomous weekly loop; its cross-domain samples must NOT train q-values (scope-primitive learning hygiene).
# BRAIN_READ_SCOPE=<wide>: cross-domain (non-core) sampling is this skill's PURPOSE, so it must read past
#   the core fingerprint. Set it wide rather than letting it fail closed to core once enforcement is on.
#   Only the learn axis is closed (--no-track); the read axis is deliberately wide.
BRAIN_READ_SCOPE=core,Books,document-insights,meta,inbox,output resources/local-brain-search/run_search.sh "dopamine" --limit 5 --no-track --json
BRAIN_READ_SCOPE=core,Books,document-insights,meta,inbox,output resources/local-brain-search/run_search.sh "uncertainty" --limit 5 --no-track --json
BRAIN_READ_SCOPE=core,Books,document-insights,meta,inbox,output resources/local-brain-search/run_search.sh "identity" --limit 5 --no-track --json
```

Pick seed notes from different clusters.

### Step 3: Get Connections for Seeds

For each seed note (same wide read-scope - the seeds and their neighbors live across domains):

```bash
BRAIN_READ_SCOPE=core,Books,document-insights,meta,inbox,output resources/local-brain-search/run_connections.sh "Note Name" --json
```

Identify notes with similarity ~0.45-0.70 from DIFFERENT domains (candidate pool - see the calibration correction above).

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
- Non-obvious connections (similarity < 0.70): [N]   ← report the count, but note this is near the median on this index, not the tail
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
- Semantic similarity roughly 0.45-0.70 (a *pool*, not a grade - see the calibration note above)
- Clear conceptual link across domains
- "Aha!" factor - non-obvious insight
- Actionable synthesis opportunity

**SKIP:**
- High similarity (0.85+) - usually shared boilerplate (frontmatter/changelog twins), not insight
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
- [ ] Non-obvious discoveries documented (similarity < 0.70) **and justified by cross-domain reasoning, not by the score alone**
- [ ] Dated changelog created in `Brain/05-Meta/Changelogs/`
- [ ] Master changelog updated with summary
