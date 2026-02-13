# Installation Guide

Detailed guide to get Project Cornelius running with your Obsidian vault.

## Prerequisites Checklist

- [ ] [Claude Code](https://claude.ai/claude-code) installed
- [ ] [Obsidian](https://obsidian.md/) with an existing vault
- [ ] Python 3.10+ installed (`python --version`)
- [ ] Git installed (`git --version`)

**Optional:**
- [ ] Node.js 18+ (for optional MCP servers like Mermaid diagrams)

## Installation Steps

### Step 1: Clone the Repository

```bash
# Clone this repository
git clone https://github.com/Abilityai/cornelius.git
cd cornelius
```

This creates a standalone directory that will connect to your existing Obsidian vault.

### Step 2: Configure Vault Path

1. **Create settings file from template:**
   ```bash
   cp .claude/settings.md.template .claude/settings.md
   ```

2. **Edit settings.md:**
   ```bash
   # Open in your editor
   code .claude/settings.md
   # or
   nano .claude/settings.md
   ```

3. **Update VAULT_BASE_PATH:**
   Change this line:
   ```
   VAULT_BASE_PATH=./Brain
   ```

   To your actual vault path (relative or absolute):
   ```
   VAULT_BASE_PATH=/Users/yourname/Documents/YourVault
   ```

### Step 3: Set Up Local Brain Search (REQUIRED)

This is the core search engine - FAISS-based vector search that runs locally.

```bash
# Navigate to the search system
cd resources/local-brain-search

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

**Dependencies installed:**
- `sentence-transformers` - Embedding model
- `faiss-cpu` - Vector search
- `networkx` - Graph analytics

### Step 4: Index Your Vault

```bash
# Still in resources/local-brain-search with venv activated

# Set your vault path (if different from config)
export BRAIN_PATH=/path/to/your/vault

# Run indexing
./run_index.sh

# Or manually:
python index_brain.py
```

This creates:
- FAISS index for semantic search
- Knowledge graph with explicit + semantic edges
- Metadata for all notes

**First indexing may take a few minutes** depending on vault size.

### Step 5: Test Local Brain Search

```bash
# Test semantic search
./run_search.sh "knowledge management"

# Test connection finding
./run_connections.sh "Some Note Name"

# Get graph statistics
./run_connections.sh --stats
```

If these work, search is ready!

### Step 6: Start Claude Code

```bash
# Navigate back to project root
cd ../..

# Start Claude Code
claude
```

### Step 7: Test Installation

In Claude Code, try these commands:

```bash
# Test semantic search
/search-vault knowledge management

# Test connection finding
/find-connections "Note Name"

# Test knowledge base analysis
/analyze-kb
```

If these work, you're done! 🎉

## Verification Checklist

- [ ] Python venv created in `resources/local-brain-search/`
- [ ] Index created (`data/brain.faiss` exists)
- [ ] `./run_search.sh` returns results
- [ ] `./run_connections.sh --stats` shows statistics
- [ ] Claude Code starts
- [ ] `/search-vault` command works
- [ ] `/find-connections` command works

## Optional: MCP Servers

MCP servers add extra capabilities but are **not required** for core functionality.

### Mermaid Diagram Server

For generating PNG/SVG diagrams:

```bash
npm install -g @anthropic/mcp-mermaid-diagram
```

### Ebook MCP

For processing EPUB/PDF files:

```bash
pip install ebook-mcp
# or
uvx ebook-mcp
```

See [MCP-SETUP.md](MCP-SETUP.md) for configuration details.

## Folder Structure

If your vault doesn't have a structure yet, create recommended folders:

```bash
cd /path/to/your/vault

mkdir -p 00-Inbox
mkdir -p 01-Sources/Books
mkdir -p 01-Sources/Articles
mkdir -p 02-Permanent
mkdir -p 03-MOCs
mkdir -p "04-Output/Articles"
mkdir -p "04-Output/Draft Posts"
mkdir -p 05-Meta/Changelogs
mkdir -p 05-Meta/Templates
mkdir -p "AI Extracted Notes"
mkdir -p "Document Insights"
```

Or create them in Obsidian's UI. See [FOLDER-STRUCTURE.md](FOLDER-STRUCTURE.md) for details.

## Troubleshooting

### Python/pip Issues

**Issue**: `python: command not found` or wrong version

**Solutions**:
```bash
# Check Python version
python3 --version

# Use python3 explicitly
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### FAISS Installation Issues

**Issue**: `pip install faiss-cpu` fails

**Solutions**:
```bash
# Try conda instead
conda install -c pytorch faiss-cpu

# Or install specific version
pip install faiss-cpu==1.7.4
```

### Index Creation Fails

**Issue**: `run_index.sh` errors

**Solutions**:
1. Check BRAIN_PATH is set correctly
2. Verify vault contains `.md` files
3. Check disk space (index can be large)
4. Try with smaller test vault first

### Search Returns No Results

**Issue**: Searches return empty

**Solutions**:
1. Re-run indexing: `./run_index.sh`
2. Check vault path in config.py
3. Verify notes exist in indexed directories
4. Check excluded folders in config.py

### Skills/Commands Not Found

**Issue**: `/search-vault: not found`

**Solutions**:
1. Verify `.claude/skills/` directory exists
2. Check skill files are `.md` format
3. Restart Claude Code
4. Check file permissions

### Permission Errors

**Issue**: `Permission denied`

**Solutions**:
```bash
# Fix script permissions
chmod +x resources/local-brain-search/*.sh

# Check vault permissions
ls -la /path/to/vault
```

## Updating

### Re-index After Adding Notes

When you add or modify notes, re-index:

```bash
cd resources/local-brain-search
source venv/bin/activate
./run_index.sh
```

### Update Project Cornelius

```bash
# Backup your settings
cp .claude/settings.md .claude/settings.md.backup

# Pull updates
git pull origin main

# Restore settings
cp .claude/settings.md.backup .claude/settings.md
```

### Update Dependencies

```bash
cd resources/local-brain-search
source venv/bin/activate
pip install -U -r requirements.txt
```

## Uninstalling

```bash
# Simply delete the project directory
rm -rf /path/to/cornelius

# Your vault remains untouched
# The FAISS index is inside the project directory
```

## Getting Help

- **Search issues**: Check `resources/local-brain-search/README.md`
- **MCP issues**: See [MCP-SETUP.md](MCP-SETUP.md)
- **Workflow questions**: See [EXAMPLES.md](EXAMPLES.md)
- **Folder organization**: See [FOLDER-STRUCTURE.md](FOLDER-STRUCTURE.md)

---

**Ready to start?** Try `/search-vault` with any topic from your vault!
