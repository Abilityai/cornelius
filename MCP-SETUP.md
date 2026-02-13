# MCP Server Setup Guide

This guide covers setting up optional MCP (Model Context Protocol) servers for enhanced functionality.

> **Note**: MCP servers are **optional**. The core functionality (semantic search, connection discovery) works with **Local Brain Search** which requires only Python. MCP servers add extra capabilities like diagram generation and ebook processing.

---

## Quick Overview

| MCP Server | Purpose | Required? |
|------------|---------|-----------|
| Mermaid Diagram | Generate PNG/SVG diagrams | Optional |
| Ebook MCP | Process EPUB/PDF files | Optional |

---

## Prerequisites

- Node.js 18+ (for npm-based MCP servers)
- Claude Code installed and working

---

## Configuration File

MCP servers are configured in `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "mermaid-diagram": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-mermaid-diagram"]
    },
    "ebook-mcp": {
      "command": "uvx",
      "args": ["ebook-mcp"]
    }
  }
}
```

A template is provided at `.mcp.json.template` - copy and customize it:

```bash
cp .mcp.json.template .mcp.json
```

---

## Server Setup

### 1. Mermaid Diagram Server (Optional)

Generates PNG/SVG diagrams from Mermaid markdown.

**Install:**
```bash
npm install -g @anthropic/mcp-mermaid-diagram
```

**Usage in Claude:**
```
Create a flowchart showing the relationship between concepts A, B, and C
```

The agent will use the Mermaid server to generate and save the diagram.

---

### 2. Ebook MCP Server (Optional)

Process EPUB and PDF files for content extraction.

**Install:**
```bash
pip install ebook-mcp
# or with uvx (recommended)
uvx ebook-mcp
```

**Usage in Claude:**
```
Extract chapter 3 from /path/to/book.epub
```

---

## Verifying MCP Servers

After configuration, restart Claude Code and check that servers are loaded:

```bash
claude
# Type: /mcp
# Should list configured servers
```

---

## Troubleshooting

### Server not loading

1. Check `.mcp.json` syntax (valid JSON)
2. Verify the command exists: `which npx` or `which uvx`
3. Check Claude Code logs for errors

### Permission errors

Make sure you have write access to the directories where servers store data.

### Path issues on macOS

If using absolute paths, ensure they're correct for your system. Prefer relative paths where possible.

---

## Local Brain Search (Not an MCP Server)

The primary search functionality uses **Local Brain Search** which is a Python-based FAISS system, NOT an MCP server. It runs locally via bash scripts:

```bash
# Semantic search
./resources/local-brain-search/run_search.sh "query"

# Find connections
./resources/local-brain-search/run_connections.sh "Note Name"

# Re-index
./resources/local-brain-search/run_index.sh
```

See [INSTALL.md](INSTALL.md) for Local Brain Search setup.

---

## Previous: Smart Connections (Deprecated)

> **DEPRECATED**: Smart Connections MCP is no longer used. All semantic search functionality is now handled by **Local Brain Search** (FAISS-based, fully local).

If you have Smart Connections configured in `.mcp.json`, you can safely remove it.

The previous setup required:
- Obsidian Smart Connections plugin
- MCP server configuration
- Plugin-based indexing

The new **Local Brain Search** approach provides:
- No Obsidian dependency for search
- Faster indexing
- Graph analytics (hubs, bridges)
- Explicit vs semantic edge distinction
- JSON output for programmatic use

---

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/claude-code)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

---

Once MCP servers are set up (if desired), return to the main README.md to continue with usage.
