---
name: self-diagnostic
description: Run self-diagnostics on Cornelius agent to verify skills, commands, agents, and integrations are working. Use when troubleshooting, after configuration changes, or for regular health checks.
allowed-tools: Read, Bash, Grep, Glob, Skill, Task
---

# Cornelius Self-Diagnostic

Run comprehensive diagnostics to verify all agent components are functioning correctly.

## Quick Start

Run full diagnostics:
```
/self-diagnostic
```

Run specific test category:
```
/self-diagnostic commands-only
/self-diagnostic skills-only
/self-diagnostic agents-only
/self-diagnostic dependencies-only
```

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Vault Path | `Brain/` | ✓ | | Verify vault exists |
| Permanent Notes Dir | `Brain/02-Permanent/` | ✓ | | Verify directory exists |
| Article Index | `Brain/04-Output/Articles/ARTICLE-INDEX.md` | ✓ | | Verify index exists |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Search scripts and index |
| Skills Directory | `.claude/skills/*/SKILL.md` | ✓ | | Skill configurations |
| Commands Directory | `.claude/commands/*.md` | ✓ | | Command configurations |
| Agents Directory | `.claude/agents/*.md` | ✓ | | Agent configurations |
| Python Runtime | System | ✓ | | Verify Python3 available |
| uv Package Manager | `~/.local/bin/uv` | ✓ | | Verify uv available |
| Temp Output | `/tmp/cornelius-diagnostic/` | | ✓ | Diagnostic results (optional) |

## Arguments

$ARGUMENTS

## Safety Principles

**CRITICAL: These diagnostics are READ-ONLY and NEVER modify production data.**

- All tests use read-only operations (search, grep, read)
- NO file creation in Brain/ directory during tests
- NO API calls to paid services (HeyGen, Gemini, etc.)
- Test outputs go to `/tmp/cornelius-diagnostic/` only
- NO changelog creation during diagnostics

---

## Diagnostic Categories

### 1. Infrastructure Tests

Verify core infrastructure is accessible:

```bash
# Test 1.1: Check vault path exists
test -d "Brain" && echo "PASS: Vault path exists" || echo "FAIL: Vault path missing"

# Test 1.2: Check permanent notes directory
test -d "Brain/02-Permanent" && echo "PASS: Permanent notes directory exists" || echo "FAIL: Permanent notes directory missing"

# Test 1.3: Check Local Brain Search is available
test -f "resources/local-brain-search/run_search.sh" && echo "PASS: Local Brain Search scripts exist" || echo "FAIL: Local Brain Search scripts missing"

# Test 1.4: Check Article Index exists
test -f "Brain/04-Output/Articles/ARTICLE-INDEX.md" && echo "PASS: Article Index exists" || echo "FAIL: Article Index missing"
```

### 2. Dependency Tests

Verify external dependencies are installed:

```bash
# Test 2.1: Python available
python3 --version 2>/dev/null && echo "PASS: Python3 available" || echo "FAIL: Python3 not found"

# Test 2.2: uv package manager (for epub-chapter-extractor)
uv --version 2>/dev/null && echo "PASS: uv available" || echo "FAIL: uv not found"

# Test 2.3: Check Local Brain Search can run (simple test)
cd resources/local-brain-search && python3 -c "import sqlite3; import json; print('PASS: Core Python modules available')" 2>/dev/null || echo "FAIL: Python modules missing"

# Test 2.4: Check mermaid-diagram MCP is responsive
# (Just verify the skill file exists - actual MCP test would require invocation)
test -f ".claude/agents/diagram-generator.md" && echo "PASS: Diagram generator agent configured" || echo "FAIL: Diagram generator agent missing"
```

### 3. Skills Validation Tests

Verify skills are properly configured (metadata valid):

```bash
# Test 3.1: List all skills and validate structure
for skill_dir in .claude/skills/*/; do
  skill_name=$(basename "$skill_dir")
  if [ -f "${skill_dir}SKILL.md" ]; then
    # Check for required frontmatter
    if head -1 "${skill_dir}SKILL.md" | grep -q "^---"; then
      if grep -q "^name:" "${skill_dir}SKILL.md" && grep -q "^description:" "${skill_dir}SKILL.md"; then
        echo "PASS: Skill '$skill_name' - valid metadata"
      else
        echo "FAIL: Skill '$skill_name' - missing name or description"
      fi
    else
      echo "FAIL: Skill '$skill_name' - missing frontmatter"
    fi
  else
    echo "FAIL: Skill '$skill_name' - missing SKILL.md"
  fi
done
```

### 4. Commands Validation Tests

Verify commands are properly configured:

```bash
# Test 4.1: List all commands and validate structure
for cmd_file in .claude/commands/*.md; do
  cmd_name=$(basename "$cmd_file" .md)
  if head -1 "$cmd_file" | grep -q "^---"; then
    if grep -q "^description:" "$cmd_file"; then
      echo "PASS: Command '/$cmd_name' - valid metadata"
    else
      echo "FAIL: Command '/$cmd_name' - missing description"
    fi
  else
    echo "FAIL: Command '/$cmd_name' - missing frontmatter"
  fi
done
```

### 5. Agents Validation Tests

Verify sub-agents are properly configured:

```bash
# Test 5.1: List all agents and validate structure
for agent_file in .claude/agents/*.md; do
  agent_name=$(basename "$agent_file" .md)
  if head -1 "$agent_file" | grep -q "^---"; then
    if grep -q "^name:" "$agent_file" || grep -q "^description:" "$agent_file"; then
      echo "PASS: Agent '$agent_name' - valid metadata"
    else
      echo "FAIL: Agent '$agent_name' - missing name or description"
    fi
  else
    echo "FAIL: Agent '$agent_name' - missing frontmatter"
  fi
done
```

---

## Functional Tests (Safe Invocations)

These tests invoke actual skills/commands with READ-ONLY operations.

### Test: /search-vault Command

This tests the semantic search and grep functionality:

```
Invoke /search-vault with query: "dopamine"
Expected: Returns at least 1 result from permanent notes
```

**Run this test:**
Use the Skill tool to invoke `search-vault` with args "dopamine"

**Success criteria:**
- Command executes without error
- Returns at least 1 search result
- Does NOT create any files

### Test: /recall Command

Tests 3-layer semantic search:

```
Invoke /recall with query: "decision making"
Expected: Returns layered results with connections
```

**Run this test:**
Use the Skill tool to invoke `recall` with args "decision making"

**Success criteria:**
- Command executes without error
- Returns Layer 1, Layer 2, and Layer 3 results
- Does NOT create any files

### Test: /find-connections Command

Tests connection discovery:

```
Invoke /find-connections with query: "Dopamine"
Expected: Returns connections for the Dopamine note
```

**Run this test:**
Use the Skill tool to invoke `find-connections` with args "Dopamine"

**Success criteria:**
- Command executes without error
- Returns explicit and semantic connections
- Does NOT create any files

### Test: /get-perspective-on Command

Tests perspective extraction:

```
Invoke /get-perspective-on with query: "AI agents"
Expected: Returns Eugene's perspective with note citations
```

**Run this test:**
Use the Skill tool to invoke `get-perspective-on` with args "AI agents"

**Success criteria:**
- Command executes without error
- Returns perspective text with [[note citations]]
- Does NOT create any files

### Test: Local Brain Search Direct

Tests local brain search scripts directly:

```bash
# Run semantic search
resources/local-brain-search/run_search.sh "consciousness" --limit 3 --json

# Run connections query
resources/local-brain-search/run_connections.sh --stats --json

# Run hub discovery
resources/local-brain-search/run_connections.sh --hubs --limit 5 --json
```

**Success criteria:**
- All three commands return valid JSON
- Search returns results with similarity scores
- Stats returns note count and connection count

---

## Skipped Tests (Would Modify Data or Cost Money)

These tests are INTENTIONALLY SKIPPED to avoid side effects:

| Test | Reason Skipped |
|------|----------------|
| /create-article | Would create files in Brain/04-Output/ |
| /update-changelog | Would create changelog file |
| /analyze-kb | May update knowledge-base-analysis.md |
| /deep-research | Uses external APIs (Gemini, Apollo) - costs money |
| /synthesize-insights | May create output files |
| /talk | Interactive mode - not suitable for automated testing |
| nano-banana-image-generator | Uses Gemini API - costs $0.039/image |
| epub-chapter-extractor | Requires actual EPUB file |
| vault-manager (write ops) | Would modify vault notes |
| auto-discovery | Creates changelog files |
| insight-extractor | Creates notes in AI Extracted Notes/ |
| document-insight-extractor | Creates notes in Document Insights/ |

---

## Diagnostic Execution Instructions

### Full Diagnostic Run

1. **Run infrastructure tests** (bash commands above)
2. **Run dependency tests** (bash commands above)
3. **Run skill validation tests** (bash commands above)
4. **Run command validation tests** (bash commands above)
5. **Run agent validation tests** (bash commands above)
6. **Run functional tests** (invoke skills via Skill tool)
7. **Compile results** into summary report

### Output Format

Present results as:

```markdown
# Cornelius Self-Diagnostic Report
**Run Date:** [current date/time]
**Agent Version:** 01.25

## Summary
| Category | Passed | Failed | Skipped |
|----------|--------|--------|---------|
| Infrastructure | X | X | 0 |
| Dependencies | X | X | 0 |
| Skills | X | X | 0 |
| Commands | X | X | 0 |
| Agents | X | X | 0 |
| Functional Tests | X | X | X |

## Detailed Results

### Infrastructure Tests
[Results...]

### Dependency Tests
[Results...]

### Skills Validation
[Results...]

### Commands Validation
[Results...]

### Agents Validation
[Results...]

### Functional Tests
[Results...]

### Skipped Tests
[List with reasons...]

## Recommendations
[Any issues found and suggested fixes]
```

---

## Argument Handling

Based on $ARGUMENTS:

- **No arguments or "full"**: Run all safe tests
- **"commands-only"**: Only test commands validation + functional
- **"skills-only"**: Only test skills validation
- **"agents-only"**: Only test agents validation
- **"dependencies-only"**: Only test infrastructure + dependencies
- **"quick"**: Only run validation tests (no functional invocations)

---

## Notes

- This diagnostic is designed to be safe and repeatable
- Run after any configuration changes to verify agent health
- If functional tests fail, check the underlying dependency first
- Diagnostic output can be saved to `/tmp/cornelius-diagnostic/` for review

## Completion Checklist

- [ ] Infrastructure tests executed (vault path, permanent notes, Local Brain Search, Article Index)
- [ ] Dependency tests executed (Python3, uv, core modules, diagram agent)
- [ ] Skills validation completed (frontmatter, name, description for all skills)
- [ ] Commands validation completed (frontmatter, description for all commands)
- [ ] Agents validation completed (frontmatter, name/description for all agents)
- [ ] Functional tests executed (search-vault, recall, find-connections, get-perspective-on, Local Brain Search)
- [ ] Summary report generated with pass/fail/skip counts
- [ ] Recommendations provided for any failures
