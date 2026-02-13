# Quick Start (5 Minutes)

Get Project Cornelius running with your Obsidian vault in 5 minutes.

## 1. Prerequisites (1 min)

```bash
# Verify Python (3.10+)
python --version

# Verify Git
git --version

# Claude Code should be installed
# Visit: https://claude.ai/claude-code
```

## 2. Clone & Configure (1 min)

```bash
# Clone repository
git clone https://github.com/Abilityai/cornelius.git
cd cornelius

# Create settings from template
cp .claude/settings.md.template .claude/settings.md
```

Edit `.claude/settings.md` and set your vault path:

```
VAULT_BASE_PATH=/Users/yourname/Documents/YourVault
```

## 3. Set Up Local Brain Search (2 min)

```bash
# Navigate to search system
cd resources/local-brain-search

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Index your vault
./run_index.sh
```

## 4. Start & Test (1 min)

```bash
# Go back to project root
cd ../..

# Start Claude Code
claude
```

In Claude Code:
```
/search-vault test
```

If this works, you're done! 🎉

## What You Just Installed

### Skills Available
- `/search-vault <query>` - Quick semantic search
- `/recall <topic>` - Deep 3-layer semantic search
- `/find-connections <note>` - Discover relationships
- `/analyze-kb` - Generate structure report
- `/create-article <topic>` - Write article from notes
- `/auto-discovery` - Find cross-domain connections

### Agents Available
- **vault-manager** - Create/organize notes
- **connection-finder** - Find hidden connections (directed)
- **auto-discovery** - Explore cross-domain patterns (autonomous)
- **insight-extractor** - Extract insights from YOUR content
- **document-insight-extractor** - Extract from external content

## Quick Wins

### Try This Right Now

**Find what you have:**
```
/search-vault [any topic in your vault]
```

**Discover connections:**
```
/find-connections [name of a note you have]
```

**See vault statistics:**
```bash
# In terminal (not Claude Code)
cd resources/local-brain-search
./run_connections.sh --stats
```

**Create a permanent note:**
```
Help me create a permanent note about [idea] with proper formatting
```

## Re-indexing

When you add or change notes, re-index:

```bash
cd resources/local-brain-search
source venv/bin/activate
./run_index.sh
```

Or in Claude Code:
```
/refresh-index
```

## Troubleshooting

### "No results found"

```bash
# Re-index your vault
cd resources/local-brain-search
./run_index.sh
```

### Python issues

```bash
# Use python3 explicitly
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### Permission errors

```bash
# Fix script permissions
chmod +x resources/local-brain-search/*.sh
```

### Skills not loading

- Restart Claude Code
- Verify `.claude/skills/` directory exists
- Check `.claude/settings.md` has correct vault path

## What's Next?

**Start simple:**
1. Create notes in `02-Permanent/`
2. Run `/find-connections` to see relationships
3. Create your first MOC when you have 10+ related notes

**Explore gradually:**
- Read [EXAMPLES.md](EXAMPLES.md) for note templates
- Try `/auto-discovery` for surprise connections
- Use `/create-article` to synthesize notes

## Full Documentation

- **[README.md](README.md)** - Complete overview
- **[INSTALL.md](INSTALL.md)** - Detailed installation
- **[EXAMPLES.md](EXAMPLES.md)** - Sample notes and workflows
- **[FOLDER-STRUCTURE.md](FOLDER-STRUCTURE.md)** - Organization guide
- **[MCP-SETUP.md](MCP-SETUP.md)** - Optional MCP servers

---

**You're ready to go!** Start with `/search-vault` and explore from there.
