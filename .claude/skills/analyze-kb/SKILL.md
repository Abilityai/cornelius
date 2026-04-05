---
name: analyze-kb
description: Analyze knowledge base structure and update the knowledge-base-analysis.md report
automation: gated
allowed-tools: Read, Bash, Glob, Grep
---

Analyze the Obsidian knowledge base structure and regenerate a **condensed, manageable** analysis report.

## Local Brain Search

Use Local Brain Search for all semantic search operations.

**Scripts:**
```bash
# Semantic search
resources/local-brain-search/run_search.sh "query" --limit 10 --json

# Find connections
resources/local-brain-search/run_connections.sh "Note Name" --json

# Get graph statistics
resources/local-brain-search/run_connections.sh --stats --json

# Find hub notes
resources/local-brain-search/run_connections.sh --hubs --json

# Find bridge notes
resources/local-brain-search/run_connections.sh --bridges --json
```

Follow these steps:

1. Get vault statistics using Local Brain Search:
   ```bash
   resources/local-brain-search/run_connections.sh --stats --json
   ```

2. List all notes with full directory tree using `Bash` find:
   ```bash
   find $VAULT_BASE_PATH/Brain -name "*.md" -type f | head -50
   ```

3. Use `Glob` to explore directory structure:
   - All notes: `Brain/**/*.md`
   - Permanent notes: `Brain/02-Permanent/*.md`
   - MOCs: `Brain/03-MOCs/*.md`
   - Sources: `Brain/01-Sources/**/*.md`

4. Read key hub notes from major clusters using `Read` tool (Dopamine, Self/Buddhism, Decision-Making, Flow, etc.)

5. Use Local Brain Search to identify hub notes and bridges:
   ```bash
   resources/local-brain-search/run_connections.sh --hubs --json
   resources/local-brain-search/run_connections.sh --bridges --json
   ```

6. Pull BDG statistics for layer distribution and lifecycle phases:
   ```bash
   resources/brain-graph/run_brain_graph.sh status --json
   ```

7. Analyze thematic clusters, hierarchical organization, and conceptual architecture

7. Use `Edit` or `Write` to update the `knowledge-base-analysis.md` file with a **condensed report** (target: ~600-800 lines max):
   - Executive summary with key statistics
   - Hierarchical structure mapping (condensed)
   - 6 major thematic hubs with hub nodes (core thesis + key notes only)
   - Network properties and connectivity (metrics + critical bridges)
   - Content topology and source analysis (top-tier influences only)
   - Intellectual trajectory and maturity assessment (phases + current focus)
   - Recommendations for enhancement (high priority only)

**CRITICAL OUTPUT REQUIREMENTS:**

- **Length target:** 600-800 lines maximum (50% of previous verbose reports)
- **Prioritize:** Core insights, actionable frameworks, critical statistics, key bridge notes
- **Eliminate:** Excessive examples, redundant explanations, verbose elaborations
- **Focus:** What's unique, what's actionable, what's growing, what's next
- **Style:** Bullet points over paragraphs, tables over lists where appropriate
- **No duplication:** Say things once, clearly, then move on

Generate a **condensed, scannable, high-signal** report that reveals the knowledge base's personality, cognitive fingerprint, and growth opportunities without overwhelming detail.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Brain notes | `Brain/**/*.md` | X | | All vault notes for analysis |
| Permanent notes | `Brain/02-Permanent/` | X | | Core insights |
| MOCs | `Brain/03-MOCs/` | X | | Map of Content hubs |
| Sources | `Brain/01-Sources/` | X | | Reference materials |
| AI Insights | `Brain/AI Extracted Notes/` | X | | AI-extracted notes |
| Document Insights | `Brain/Document Insights/` | X | | Research session notes |
| Changelogs | `Brain/05-Meta/Changelogs/` | X | | Session logs |
| Local Brain Search | `resources/local-brain-search/` | X | | Graph statistics, hubs, bridges |
| Knowledge base analysis | `knowledge-base-analysis.md` | X | X | Output report |

## Completion Checklist

- [ ] Vault statistics retrieved from Local Brain Search
- [ ] Directory structure explored with Glob
- [ ] Key hub notes read (Dopamine, Buddhism, Decision-Making, Flow, AI)
- [ ] Hub notes and bridges identified
- [ ] Thematic clusters analyzed
- [ ] knowledge-base-analysis.md updated with condensed report
- [ ] Report is 600-800 lines (not verbose)
- [ ] Executive summary includes key statistics
- [ ] 6 major thematic hubs documented
- [ ] Network properties and bridges noted
- [ ] Recommendations provided (high priority only)
