---
name: changelog-protocol
description: Protocol for creating dated changelog files after significant agent sessions. Use when completing vault operations, discovery sessions, insight extraction, or any work requiring documentation.
user-invocable: false
---

# Changelog Protocol

**All sub-agents MUST create separate dated changelog files after each significant session.**

## File Location & Naming

- **Directory:** `/Users/eugene/Dropbox/Agents/Cornelius/Brain/05-Meta/Changelogs/`
- **Naming Format:** `CHANGELOG - [Session Type] YYYY-MM-DD.md`
- **Examples:**
  - `CHANGELOG - Auto-Discovery Sessions 2025-10-25.md`
  - `CHANGELOG - Connection Discovery Session 2025-10-24.md`
  - `CHANGELOG - Vault Management Session 2025-10-26.md`
  - `CHANGELOG - Insight Extraction Session 2025-10-27.md`

## Timestamp Requirements

**MANDATORY:** Before starting any session, call:
```bash
date '+%Y-%m-%d %H:%M:%S %Z'
```

Include this timestamp at the top of the changelog file. Use the date from this command in the filename.

## Changelog Content Structure

Each changelog file must include:

1. **Session header** with date, time, and session type
2. **Session overview** with key statistics
3. **Major discoveries/connections/changes** documented in detail
4. **Emergent patterns** or meta-insights
5. **Synthesis opportunities** identified
6. **Session statistics** (notes analyzed, connections found, etc.)
7. **Recommended next actions**

## When to Create Changelogs

| Agent | Trigger |
|-------|---------|
| **Auto-Discovery Agent** | After every discovery session (mandatory) |
| **Connection Finder Agent** | After every connection mapping session (mandatory) |
| **Vault Manager Agent** | After significant CRUD operations affecting 3+ notes |
| **Insight Extractor Agent** | After extracting insights from significant content |

## Dual Logging System

- **Dated files:** Individual session logs in `/05-Meta/Changelogs/` folder (primary, detailed)
- **Master CHANGELOG.md:** Summary entries in `/Brain/CHANGELOG.md` (secondary, brief)

The dated changelog files are the **primary record** - comprehensive and detailed. The master CHANGELOG.md serves as a **quick reference index** with brief entries pointing to the detailed session files.
