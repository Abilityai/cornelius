---
name: sync-to-public
description: Sync capability updates from cornelius-internal (private) to cornelius (public) repo, excluding personal/private skills and sanitizing paths
automation: gated
allowed-tools: [Bash, Read, Glob, Grep, Edit, Write]
user-invocable: true
---

# Sync to Public Repo

Syncs updated skills, agents, and core files from the private `cornelius-internal` repo to the public `cornelius` repo on GitHub — excluding personal/private capabilities.

## Purpose

Keep the public Cornelius template up to date with capability improvements made in the private instance, without leaking personal data, private integrations, or personal brand content.

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Private repo | `/Users/eugene/Dropbox/Agents/Cornelius/` | ✅ | ❌ |
| Public repo clone | `/tmp/cornelius-public-sync/` | ✅ | ✅ |
| GitHub remote | `https://github.com/Abilityai/cornelius` | pull | push |

## Exclusion List (NEVER sync these)

**Skills (private/personal):**
- `economist-analyze` - personal economist workflow
- `gjopen` / `gjopen-heartbeat` / `gjopen-lookup` / `gjopen-refresh` - personal forecasting
- `fork-to-client` - internal client tool
- `trinity-compatibility` / `trinity-remote` / `trinity-schedules` / `trinity-sync` - Trinity platform internals

**Agents:**
- `article-scraper` - used by economist-analyze, personal workflow

**Root files (public has better template versions — do NOT overwrite):**
- `CLAUDE.md` - public version is the clean template (03.26); private has personal paths
- `EXAMPLES.md`, `FOLDER-STRUCTURE.md`, `INSTALL.md`, `MCP-SETUP.md`, `LICENSE`, `QUICKSTART.md` - public-only docs
- `.env.example`, `AUTONOMOUS-AGENT-ARCHITECTURE.md`, `EPUB_EXTRACTION_*`, `run_extraction.sh`

**Resource files (personal):**
- `resources/gjopen_*.py`, `resources/update_gjopen.py`
- `resources/epub_*.py`, `resources/extract_*.py`, `resources/run_extraction.sh`
- `resources/upload-to-cloudinary.py`, `resources/process-remaining-videos.sh`
- `resources/spiritual-transformation-plan/`
- `resources/temp-documents/`, `resources/test-extraction/`
- `resources/local-brain-search/data/` (FAISS index, Q-values - machine-specific)
- `resources/local-brain-search/venv/`, `resources/local-brain-search/__pycache__/`
- `resources/local-brain-search/tmp/`, `resources/local-brain-search/search_fix.patch`
- `resources/benchmark-memory/` data dirs

## Prerequisites

- `gh` CLI authenticated
- Write access to `Abilityai/cornelius`

## Process

### Step 1: Pull Latest Public Repo

```bash
# Clone fresh or pull if already exists
if [ -d /tmp/cornelius-public-sync/.git ]; then
  cd /tmp/cornelius-public-sync && git pull origin main
else
  gh repo clone Abilityai/cornelius /tmp/cornelius-public-sync -- --depth=1
fi
```

### Step 2: Sync Agents

Copy all agent files from private to public, **except** `article-scraper`:

```bash
PRIVATE=".claude/agents"
PUBLIC="/tmp/cornelius-public-sync/.claude/agents"

for agent_file in $PRIVATE/*.md; do
  name=$(basename "$agent_file")
  if [ "$name" != "article-scraper.md" ]; then
    cp "$agent_file" "$PUBLIC/$name"
    echo "  synced agent: $name"
  else
    echo "  SKIPPED agent: $name (excluded)"
  fi
done
```

### Step 3: Sync Skills

Copy skill SKILL.md files from private to public, applying the exclusion list.

```bash
PRIVATE_SKILLS=".claude/skills"
PUBLIC_SKILLS="/tmp/cornelius-public-sync/.claude/skills"

# Skills to exclude
EXCLUDE=(
  "economist-analyze"
  "gjopen"
  "gjopen-heartbeat"
  "gjopen-lookup"
  "gjopen-refresh"
  "fork-to-client"
  "trinity-compatibility"
  "trinity-remote"
  "trinity-schedules"
  "trinity-sync"
)

for skill_dir in $PRIVATE_SKILLS/*/; do
  skill_name=$(basename "$skill_dir")

  # Check if excluded
  excluded=false
  for ex in "${EXCLUDE[@]}"; do
    [ "$skill_name" = "$ex" ] && excluded=true && break
  done

  if $excluded; then
    echo "  SKIPPED skill: $skill_name (excluded)"
    continue
  fi

  # Create dir if new, copy SKILL.md
  mkdir -p "$PUBLIC_SKILLS/$skill_name"
  cp "$skill_dir/SKILL.md" "$PUBLIC_SKILLS/$skill_name/SKILL.md"
  echo "  synced skill: $skill_name"
done
```

### Step 4: Sync Core Resource Files

Only sync the core search engine files (not personal data):

```bash
PUBLIC_LBS="/tmp/cornelius-public-sync/resources/local-brain-search"

# Updated search engine
cp resources/local-brain-search/search.py "$PUBLIC_LBS/search.py"
cp resources/local-brain-search/README.md "$PUBLIC_LBS/README.md"

# Check for other non-personal resource files
# memory_config.py, wrapper scripts if they exist
for f in resources/local-brain-search/*.py resources/local-brain-search/*.sh resources/local-brain-search/*.md; do
  fname=$(basename "$f")
  # Skip data files and dev artifacts
  case "$fname" in
    search_fix.patch) continue ;;
    *) cp "$f" "$PUBLIC_LBS/$fname" 2>/dev/null && echo "  synced: $fname" ;;
  esac
done
```

### Step 5: Sync Config Files

```bash
PUBLIC="/tmp/cornelius-public-sync"

# These have changed and are safe to sync
cp .gitignore "$PUBLIC/.gitignore"
cp .mcp.json.template "$PUBLIC/.mcp.json.template"
cp template.yaml "$PUBLIC/template.yaml"
```

### Step 6: Review CLAUDE.md Manually

The public `CLAUDE.md` is version **03.26** (clean template with `$VAULT_BASE_PATH`).
The private version is **01.25** with hardcoded personal paths.

**Do NOT overwrite the public CLAUDE.md automatically.**

Instead, identify new capabilities in the private version that should be added to the public template:

```bash
# Show what's new in private CLAUDE.md vs public
diff /tmp/cornelius-public-sync/CLAUDE.md CLAUDE.md | grep "^>" | head -30
```

Present the user with a summary of new capability mentions (e.g., `advise` skill, `quick-search`) that should be manually added to the public CLAUDE.md. Ask if they want to edit now.

### Step 7: Show Diff Summary (APPROVAL GATE)

```bash
cd /tmp/cornelius-public-sync
git diff --stat
echo "---"
git status --short
```

Present a clean summary:
- Files changed (updated)
- Files added (new skills/agents)
- Files removed (if any)

**Ask for approval before proceeding:**
> "Ready to commit and push these changes to `Abilityai/cornelius`. Proceed?"

### Step 8: Commit and Push

Only proceed after explicit user approval.

```bash
cd /tmp/cornelius-public-sync

# Stage all changes
git add -A

# Get count of changes for commit message
CHANGED=$(git diff --cached --name-only | wc -l | tr -d ' ')

git commit -m "$(cat <<'EOF'
sync: update skills, agents, and core files from internal

Synced capability updates from cornelius-internal. Excludes personal
workflows (economist, gjopen, trinity internals, fork-to-client).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"

git push origin main
```

### Step 9: Confirm

Report the commit SHA and GitHub URL to the user.

```bash
cd /tmp/cornelius-public-sync
git log -1 --oneline
echo "https://github.com/Abilityai/cornelius/commits/main"
```

## Completion Checklist

- [ ] All excluded skills confirmed absent from public
- [ ] New skills (`advise`, `quick-search`) confirmed present in public
- [ ] No personal paths (`/Users/eugene/`) leaked into synced files
- [ ] `CLAUDE.md` reviewed - new capabilities noted, no personal content added
- [ ] Push confirmed with commit SHA

## Error Recovery

- **Push fails (branch protection):** Create a PR instead: `gh pr create --title "sync: capability updates from internal" --base main`
- **Merge conflicts:** Pull latest, resolve conflicts manually, then re-run from Step 5
- **Accidentally synced excluded skill:** `cd /tmp/cornelius-public-sync && git rm .claude/skills/<name>/SKILL.md && git commit -m "revert: remove private skill"`
