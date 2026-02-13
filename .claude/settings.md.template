# Configuration

# Vault base path - set to your Obsidian vault location
# Can be relative (./Brain) or absolute (/Users/yourname/vault)
VAULT_BASE_PATH=./Brain

# Document insights path - where external document insights are stored
DOCUMENT_INSIGHTS_PATH=./Brain/Document Insights

---

## Setup Instructions

1. Copy this file to `settings.md`:
   ```bash
   cp .claude/settings.md.template .claude/settings.md
   ```

2. Edit `settings.md` and set `VAULT_BASE_PATH` to your vault location:
   - Relative path: `./Brain` (if vault is in project)
   - Absolute path: `/Users/yourname/Documents/YourVault`

3. Set up Local Brain Search:
   ```bash
   cd resources/local-brain-search
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ./run_index.sh
   ```

4. Start Claude Code:
   ```bash
   claude
   ```

## Notes

- This file is gitignored to protect your personal paths
- All agents and skills use `$VAULT_BASE_PATH` from this config
- Re-index after changing vault path: `./run_index.sh`
