---
name: brain-merge
description: Compare and selectively merge Brain directories across any two agent instances. Supports diff (see what's unique where), pull (import from another brain), and learn (bidirectional exchange).
automation: gated
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Agent]
user-invocable: true
---

# Brain Merge

Compare and selectively merge knowledge between any two Brain directories. Works across any agent instances - not tied to specific paths.

## Purpose

Agent brains develop independently and accumulate unique insights. This playbook lets you see what each brain has that the other doesn't, and move knowledge between them safely.

## Modes

- **diff** - Compare two brains, see what's unique to each
- **pull** - Import files from a source brain into a target brain
- **learn** - Bidirectional exchange with approval at each direction

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Source brain | User-specified path | ✓ | - |
| Target brain | User-specified path (defaults to current) | ✓ | ✓ |
| FAISS index | `[agent-root]/resources/local-brain-search/data/` | - | ✓ |

## Process

### Step 0: Resolve inputs

Ask the user for:
1. **Source brain path** - the brain to compare against or pull from
2. **Target brain path** - the brain to compare or import into (default: current agent's `./Brain`)
3. **Mode** - diff, pull, or learn (infer from user's message if obvious)

If paths are ambiguous (user says "moltbook" or "the other one"), scan parent directories for Brain/ folders and present a pick list:

```bash
find . -maxdepth 3 -name "Brain" -type d 2>/dev/null | sort
```

---

### DIFF MODE

**Goal:** Show what each brain has that the other doesn't, grouped by folder.

#### Step 1: Inventory both brains

```bash
SOURCE="[SOURCE_BRAIN_PATH]"
TARGET="[TARGET_BRAIN_PATH]"

find "$SOURCE" -name "*.md" | sed "s|$SOURCE/||" | sort > /tmp/brain_source.txt
find "$TARGET" -name "*.md" | sed "s|$TARGET/||" | sort > /tmp/brain_target.txt

echo "Source: $(wc -l < /tmp/brain_source.txt) files"
echo "Target: $(wc -l < /tmp/brain_target.txt) files"
```

#### Step 2: Generate diff lists

```bash
comm -23 /tmp/brain_source.txt /tmp/brain_target.txt > /tmp/unique_to_source.txt
comm -13 /tmp/brain_source.txt /tmp/brain_target.txt > /tmp/unique_to_target.txt
comm -12 /tmp/brain_source.txt /tmp/brain_target.txt > /tmp/in_both.txt

echo "Unique to source: $(wc -l < /tmp/unique_to_source.txt)"
echo "Unique to target: $(wc -l < /tmp/unique_to_target.txt)"
echo "In both: $(wc -l < /tmp/in_both.txt)"
```

#### Step 3: Group by folder and present

```bash
echo "=== UNIQUE TO SOURCE ==="
awk -F'/' '{print $1}' /tmp/unique_to_source.txt | sort | uniq -c | sort -rn

echo "=== UNIQUE TO TARGET ==="
awk -F'/' '{print $1}' /tmp/unique_to_target.txt | sort | uniq -c | sort -rn
```

For each folder, show a few sample filenames so the user gets a sense of what's there.

Present as a clean table. Note any folders that exist in one brain but not the other (structural differences).

**Gate 1:** Present report. Ask: "Want to pull any of this into your brain? Which folders or files?"

---

### PULL MODE

**Goal:** Import specific files from source into target, safely.

#### Step 1: Run diff if not already done

#### Step 2: Clarify scope

If not specified, ask: "Which folders or files to pull? (e.g., `02-Permanent`, `AI Extracted Notes`, all unique files, or specific filenames)"

**Gate 2:** Confirm scope before touching anything:
> "About to copy [N] files from [source] → [target]. Files already in target will be SKIPPED. Proceed?"

#### Step 3: Execute copy

```bash
rsync -av --ignore-existing \
  "[SOURCE]/[SELECTED_FOLDER]/" \
  "[TARGET]/[SELECTED_FOLDER]/"
```

For full unique-file pull:
```bash
while IFS= read -r file; do
  dest="[TARGET]/$file"
  mkdir -p "$(dirname "$dest")"
  cp -n "[SOURCE]/$file" "$dest"
done < /tmp/unique_to_source.txt
```

#### Step 4: Refresh index in target

```bash
cd [TARGET_AGENT_ROOT]
python3 resources/local-brain-search/build_index.py
```

Report total files copied, skipped, and confirm index refreshed.

---

### LEARN MODE

**Goal:** Bidirectional exchange - each brain gets what the other has.

#### Step 1: Run diff (both directions)

#### Step 2: Source → Target

Show what source has that target doesn't.

**Gate 3:** "Source has [N] unique files. Pull into target? (y/n/select folders)"

If approved, run pull source → target.

#### Step 3: Target → Source

Show what target has that source doesn't.

**Gate 4:** "Target has [M] unique files. Push into source? (y/n/select folders)"

If approved:
```bash
rsync -av --ignore-existing \
  "[TARGET]/[SELECTED_FOLDER]/" \
  "[SOURCE]/[SELECTED_FOLDER]/"
```

#### Step 4: Refresh indexes in both agents

```bash
cd [TARGET_AGENT_ROOT] && python3 resources/local-brain-search/build_index.py
cd [SOURCE_AGENT_ROOT] && python3 resources/local-brain-search/build_index.py
```

Report: files exchanged in each direction, both indexes refreshed.

---

## Tips

- **Start with diff** - understand what you're working with before moving anything
- **Safe by default** - `--ignore-existing` / `cp -n` never overwrites existing files
- **Content conflicts** - files with the same name but different content are flagged but not auto-resolved; manual review recommended
- **Structural differences** - folders that exist in one brain but not the other are worth noting (may indicate the agent evolved differently)
- **Index refresh** - always runs after file changes so FAISS stays current

## Error Recovery

- If copy fails mid-way: re-run - `--ignore-existing` makes it idempotent
- If index build fails: run `/refresh-index` manually in that agent
- If paths not found: re-run Step 0 discovery scan

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could error handling, step ordering, or instructions be clearer?
- [ ] **Scope check**: Only tactical/execution changes - NOT changes to core purpose or goals
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control**:
  - [ ] Stage: `git add .claude/skills/brain-merge/SKILL.md`
  - [ ] Commit: `git commit -m "refactor(brain-merge): <brief improvement description>"`
