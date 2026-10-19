# Recommended Folder Structure

This guide provides a recommended folder structure for your Obsidian vault when using the Claude Code Second Brain system. This structure is based on the PARA method and Zettelkasten principles, optimized for knowledge work.

## Core Philosophy

The folder structure should support:
1. **Clear stages** in the knowledge refinement pipeline
2. **Easy navigation** between raw inputs and refined outputs
3. **Flexibility** to adapt to your workflow
4. **Scalability** as your vault grows

## Recommended Structure

```
your-vault/
├── .claude/                          # Claude Code configuration
│   ├── agents/                       # Sub-agent definitions
│   ├── commands/                     # Slash commands
│   └── settings.local.json          # Permissions & MCP config
│
├── .obsidian/                        # Obsidian settings (standard)
│   └── plugins/
│       └── smart-connections/       # For semantic search
│
├── CLAUDE.md                         # System instructions
├── knowledge-base-analysis.md       # KB structure report (auto-generated)
│
├── Inbox/                            # Capture & staging
│   ├── Quick Captures/              # Fleeting notes
│   ├── Content Extractions/         # AI-processed sources
│   └── To Process/                  # Unprocessed material
│
├── Sources/                          # Source material
│   ├── Books/                       # Book notes
│   ├── Articles/                    # Article summaries
│   ├── Videos/                      # Video notes
│   └── Podcasts/                    # Podcast notes
│
├── Permanent/                        # Permanent notes (your insights)
│   └── [All atomic notes]           # Core knowledge atoms
│
├── MOCs/                             # Maps of Content
│   ├── MOC - Master Navigation.md   # Top-level index
│   └── [Topic-specific MOCs]        # Thematic navigation hubs
│
├── Output/                           # Published/synthesized work
│   ├── Articles/                    # Long-form writing
│   ├── Frameworks/                  # Original models
│   ├── Insights/                    # Short-form insights
│   └── Projects/                    # Open research questions
│
├── Meta/                             # Workflow & evolution
│   ├── Changelogs/                  # Discovery session logs
│   ├── Templates/                   # Note templates
│   └── Workflows/                   # Process documentation
│
└── AI Extracted Notes/               # Separate provenance
    └── [AI-generated notes]         # Clear AI vs human distinction
```

## Codex Project Files

The opt-in [Codex path](docs/CODEX.md) uses the same note folders. Its additional
files live at the Cornelius project root, which may be separate from an external
Obsidian vault:

```text
cornelius/
├── AGENTS.md                 # Codex entry point; reads shared instructions
├── CLAUDE.md                 # Shared identity and memory rules
├── docs/CODEX.md             # Codex workflow limits and execution rules
├── .agents/skills/<name>     # Relative symlink to ../../.claude/skills/<name>
└── .claude/
    ├── skills/<name>/        # Canonical skills and companion files
    ├── agents/              # Canonical specialist prompts
    └── settings.md          # Local vault settings, shared by both runtimes
```

Only the workflows listed in `docs/CODEX.md` have discovery links. Preserve the
links in a Git checkout; do not copy skill bodies into a second catalog. Merge
existing owner instructions manually, and keep Codex runtime state and
credentials outside the checkout. `VAULT_BASE_PATH` is the note root; an external
vault also requires the engine's `BRAIN_PATH` to point to the same root.

## Folder Purposes

### .claude/
**Purpose**: Claude Code configuration and agent definitions

**Contents**:
- `agents/`: Specialized sub-agent prompt files
- `commands/`: Slash command definitions
- `settings.local.json`: Permissions and MCP configuration

**Notes**:
- Keep in git if sharing setup
- Add `settings.local.json` to `.gitignore` for privacy

### Inbox/
**Purpose**: Capture ideas quickly without friction

**Contents**:
- **Quick Captures/**: Fleeting notes, raw thoughts
- **Content Extractions/**: AI-processed content awaiting review
- **To Process/**: Material waiting to become permanent notes

**Workflow**:
1. Capture quickly to Quick Captures
2. Process into permanent notes regularly
3. Delete or archive after processing

### Sources/
**Purpose**: Reference material and source notes

**Contents**:
- **Books/**: Comprehensive book notes with key quotes
- **Articles/**: Article summaries with main arguments
- **Videos/**: Video notes with timestamps
- **Podcasts/**: Podcast notes with key points

**Best Practices**:
- One file per source
- Include metadata (author, date, URL)
- Link to permanent notes that reference it
- Use frontmatter for structured metadata

**Example Source Note**:
```markdown
---
type: book
author: Author Name
year: 2024
tags: [topic1, topic2]
---

# Book Title

## Key Arguments
- Main point 1
- Main point 2

## Permanent Notes
- [[Note 1]] - About topic X
- [[Note 2]] - About topic Y
```

### Permanent/
**Purpose**: Atomic permanent notes—your knowledge atoms

**Contents**:
- Single-idea notes in your own words
- Each note is independently understandable
- Connected via wikilinks to other permanent notes

**Best Practices**:
- **One idea per note**: Keep atomic and focused
- **Clear titles**: State the insight explicitly
- **Your own words**: Paraphrase, don't copy
- **Source attribution**: Link back to source notes
- **Date stamp**: Include creation date in frontmatter
- **Average length**: 50-300 words ideal

**Example Permanent Note**:
```markdown
---
created: 2025-10-27
tags: [neuroscience, motivation]
---

# Dopamine drives motivation, not pleasure

Dopamine is responsible for the *desire* to act, not the enjoyment of the action itself. This explains why we can be motivated to do things we don't enjoy.

The "wanting" (dopamine) system is separate from the "liking" (opioid) system in the brain.

**Source**: [[Dopamine Nation - Book Notes]]

**Related**:
- [[Pleasure and pain balance in the brain]]
- [[Reward prediction error]]
- [[Motivation vs. willpower]]
```

### MOCs/ (Maps of Content)
**Purpose**: Navigation hubs for thematic clusters

**Contents**:
- **MOC - Master Navigation**: Top-level index to all MOCs
- **Thematic MOCs**: Topic-specific navigation (e.g., "MOC - Decision Making")

**Best Practices**:
- Create when you have 15+ notes on a theme
- Group related permanent notes
- Add brief context for each section
- Update regularly as knowledge grows
- Link to related MOCs

**Example MOC Structure**:
```markdown
# MOC - Decision Making

## Core Concepts
- [[Judgment as measurement]]
- [[Noise in judgments]]
- [[Bias vs. noise]]

## Cognitive Biases
- [[Confirmation bias]]
- [[Anchoring bias]]
- [[Availability heuristic]]

## Frameworks
- [[Mental models taxonomy]]
- [[Thinking in bets]]
- [[Expected value calculation]]

## Related MOCs
- [[MOC - Cognitive Science]]
- [[MOC - Investing]]
```

### Output/
**Purpose**: Finished work and synthesis

**Contents**:
- **Articles/**: Long-form published pieces
- **Frameworks/**: Original models and taxonomies
- **Insights/**: Short-form insights (LinkedIn, Twitter)
- **Projects/**: Open research questions and ongoing work

**Best Practices**:
- Link back to permanent notes used
- Include publication date and status
- Track revisions in git
- Archive outdated versions

### Meta/
**Purpose**: Workflow documentation and evolution tracking

**Contents**:
- **Changelogs/**: Discovery session logs from agents
- **Templates/**: Note templates for consistency
- **Workflows/**: Process documentation

**Changelog Structure**:
```
Changelogs/
├── CHANGELOG - Auto-Discovery Sessions 2025-10-27.md
├── CHANGELOG - Connection Discovery 2025-10-26.md
└── CHANGELOG - Vault Management 2025-10-25.md
```

### AI Extracted Notes/
**Purpose**: Clear provenance for AI-generated content

**Contents**:
- Permanent notes created by insight-extractor agent
- Clearly separated from human-created notes

**Best Practices**:
- Review and edit AI extractions
- Merge with permanent notes if validated
- Maintain clear provenance
- Use frontmatter to tag as AI-extracted

## Optional Folders

### People/
**Purpose**: Network documentation

**Contents**: Notes about people you interact with
- Professional contacts
- Collaborators
- Authors you follow

### Projects/
**Purpose**: Active project management

**Contents**:
- Project plans
- Meeting notes
- Task tracking

### Archive/
**Purpose**: Completed or outdated material

**Contents**:
- Old versions of notes
- Completed projects
- Deprecated frameworks

## Information Flow

The recommended structure supports this knowledge pipeline:

```
CAPTURE → PROCESS → ORGANIZE → SYNTHESIZE → CREATE

Inbox/      Sources/      Permanent/    MOCs/         Output/
           ↓             ↓             ↓             ↓
Quick → Source Notes → Permanent → MOCs → Articles
Captures              Notes         Connection   Insights
                                    Maps         Frameworks
```

## Customization Guidelines

### Adapt to Your Needs

This structure is a starting point. Customize based on:

1. **Volume**: More subdirectories if you have 1000+ notes
2. **Workflow**: Adjust stages to match your process
3. **Domain**: Add specialized folders for your field
4. **Team**: Consider shared vs. personal folders

### Principles to Maintain

Whatever structure you choose, maintain:

1. **Clear stages**: Distinguish raw inputs from refined outputs
2. **Atomic permanent notes**: Keep core insights separate
3. **Navigation aids**: MOCs or indexes for finding notes
4. **Evolution tracking**: Changelogs or similar
5. **Source attribution**: Link notes back to origins

## Migration Strategy

### From Existing Vault

1. **Don't reorganize everything at once**
2. **Start with new notes** in the new structure
3. **Gradually move frequently accessed notes**
4. **Use aliases for old paths** during transition
5. **Update links with search-replace** carefully

### From Other Systems

- **Roam/Logseq**: Export to markdown, then organize by type
- **Notion**: Export pages, create permanent notes from key insights
- **Evernote**: Export notes, use insight-extractor to process
- **OneNote**: Manual migration, extract atomic notes

## Maintenance

### Regular Tasks

**Daily**: Empty Inbox/Quick Captures into permanent notes

**Weekly**:
- Review new permanent notes
- Update relevant MOCs
- Run `/find-connections` on recent notes

**Monthly**:
- Run auto-discovery agent
- Review changelogs
- Clean up outdated temporary notes
- Update MOC - Master Navigation

**Quarterly**:
- Run `/analyze-kb` for structural analysis
- Review and refine folder structure
- Archive completed projects
- Evaluate what's working

## Examples

See `EXAMPLES.md` for:
- Sample notes in each folder
- Example MOC structures
- Changelog templates
- Information flow examples

## Next Steps

1. Create the basic folder structure
2. Configure `.claude/settings.local.json` with your paths
3. Start capturing in Inbox/
4. Process into Permanent/ regularly
5. Create MOCs when themes emerge
6. Use agents to discover connections

---

Remember: The structure serves the workflow, not the other way around. Start simple and evolve as your needs become clear.
