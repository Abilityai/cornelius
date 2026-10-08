---
name: first-run
description: First-install playbook for a fresh Cornelius - builds the local search engine (Python venv + FAISS + the embedding model), starts the search daemon, rebuilds the index so its stored paths match this machine, runs one smoke search and reports what works. Idempotent - run it again any time to verify. On Trinity, the same bootstrap starts on its own at first boot; this playbook finishes it and proves it.
allowed-tools: Bash, Read
user-invocable: true
argument-hint: "[--verify-only]"
metadata:
  version: "1.2"
  created: 2026-10-08
  author: Ability.ai
  changelog:
    - "1.2: Install in the foreground of one streaming Bash call, never detached - on Trinity v0.9.5 the agent-server orphan sweeper kills unowned background processes ~90 s after container start (the boot-time bootstrap dies at the first long step after pip). Lock-file guidance updated"
    - "1.1: Reindex before the daemon, daemon start bounded by timeout, fastapi/uvicorn added to requirements (the daemon imported them but nothing installed them). From the first fresh-fork test on a 4 GB droplet"
    - "1.0: Initial - from the Agent-Native Agency workshop session 3 (2026-10-08). A fresh fork of the template ships the prebuilt index but not the Python that reads it, and the index remembers the build machine's paths, so 8 of 9 search-backed playbooks fail cold. This playbook is the one-command fix: venv (CPU-only torch, no pip cache - the install must fit a 4 GB box), daemon, reindex, smoke search, report. Pairs with .trinity/bootstrap.sh, which runs the same steps detached at container start."
---

# First Run

> ℹ️ Print one line first: `first-run v1.2 - recent: foreground install, never detached (orphan sweeper)`. Then proceed.

## Purpose

A fresh copy of Cornelius has the whole seeded knowledge base and a prebuilt search index, but not the Python environment that reads it, and the index still carries the file paths of the machine that built it. Until both are fixed, `/recall`, `/advise`, `/decide`, `/find-connections`, `/extract-insights` and every other search-backed playbook return nothing or fail. This playbook takes the vault from "cloned" to "answers questions" in one command, and reports honestly what it found at every step.

Safe to run repeatedly: every step checks before it acts.

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Search engine | `resources/local-brain-search/` (venv, `requirements.txt`, `run_daemon.sh`, `run_index.sh`, `run_search.sh`) | ✓ | ✓ (venv, daemon, index files) |
| Index manifest | `resources/local-brain-search/data/manifest.json` | ✓ | via reindex |
| Bootstrap log and marker (Trinity) | `~/.trinity-bootstrap.log`, `~/.trinity-bootstrap.done`, `~/.trinity-bootstrap.lock` | ✓ | ✓ |
| The vault | `$VAULT_BASE_PATH` (default `./Brain`) | ✓ | |

## Process

Work from the agent root (the folder that holds `Brain/` and `resources/`). Keep every Bash call short (under 60 s): long installs run detached and are polled, so the platform's stall watchdog never fires.

### Step 1 - Is a bootstrap already running or done?

```bash
ls -la ~/.trinity-bootstrap.done ~/.trinity-bootstrap.lock 2>/dev/null; tail -5 ~/.trinity-bootstrap.log 2>/dev/null
```

- `.done` present → the boot-time bootstrap finished; skip to Step 5 (verify).
- `.lock` present and the log still growing → it is running; poll `tail -3 ~/.trinity-bootstrap.log` every 30 s until `.done` appears or the log stops for 2 minutes. A log that stops after "venv built" or "reindex start" with no process behind it means the boot-time bootstrap was swept (see Step 2) - continue with Step 2; every step checks before it acts, so nothing is redone.
- Neither → continue with Step 2.

### Step 2 - The Python environment

```bash
cd resources/local-brain-search && ./venv/bin/python -c "import faiss, sentence_transformers, networkx; print('ok')" 2>&1 | tail -1
```

If that prints `ok`, skip to Step 3. Otherwise build it in the **foreground of one Bash call**, with output streaming (pip prints as it goes, so the platform's stall watchdog does not fire; on a 2-vCPU box with the CPU-only torch wheel this takes 1-2 minutes, ~1.5 GB):

```bash
cd resources/local-brain-search && python3 -m venv venv && ./venv/bin/pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt 2>&1 | grep -v -E "Downloading|Using cached|^\s+━" ; ./venv/bin/python -c "import faiss, sentence_transformers; print('ok')"
```

Tell the user it is installing before you run it. On an error, paste the last 20 lines and stop - do not retry blindly. **Do not run the install detached (`nohup … &`) on Trinity**: the agent-server's orphan sweeper kills background processes it does not own ~90 s after container start, which is exactly how the boot-time bootstrap gets cut off mid-way - this playbook exists to finish the job inside an execution the platform owns.

### Step 3 - Rebuild the index once (before the daemon)

The shipped index remembers the paths of the machine that built it. One rebuild reuses the shipped embeddings and rewrites the paths; it takes seconds to a couple of minutes and downloads the embedding model (~90 MB) on first use.

```bash
cd resources/local-brain-search && ./run_index.sh 2>&1 | tail -8
```

### Step 4 - The search daemon

```bash
cd resources/local-brain-search && timeout 120 ./run_daemon.sh start
```

"Daemon already running" is success. "started but not yet responding" → wait 20 s and run `./run_daemon.sh status`. If the daemon will not come up, searches still work through the CLI fallback, only slower - do not block on it.

### Step 5 - Verify with one smoke search

```bash
cd resources/local-brain-search && BRAIN_READ_SCOPE=core,books,document-insights ./run_search.sh "decision under uncertainty" --limit 3 --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); r=d.get('results',d); print(len(r),'results'); [print('-', x.get('title') or x.get('note') or x.get('path')) for x in r[:3]]"
```

(The scope is widened on purpose: the engine's default read scope is `core`, your own notes, which is nearly empty on a fresh copy; the seed lives in the reading pile. `/recall` and `/advise` mount the wider scope themselves.)

Three titles → the engine, the index and the seed are all there. Zero results → the index was not rebuilt (go back to Step 4) or the daemon is serving the old one (reload it). An import error → Step 2 did not finish.

Also confirm the orb data exists: `ls -la resources/agent-visualization/data.json` (on Trinity, `.trinity/setup.sh` copies it from the seed at boot; locally the Brain Orb does not apply).

### Step 6 - Report

One short block, no prose padding:

```
First run - <date>
Python env     : ok (faiss, sentence-transformers, torch) | built now in <m> min | FAILED: <reason>
Search daemon  : running (pid <n>) | not responding
Index          : rebuilt now | already current - <notes> notes, <edges> edges (manifest.json)
Smoke search   : 3 results - <title 1> · <title 2> · <title 3>
Brain Orb data : present | n/a
Try next       : /recall <topic>   ·   /advise <a problem you are weighing>   ·   /decide <a choice with options>
```

If `--verify-only` was passed, run Steps 1, 2 (check only), 3 (status only), 5 and 6 and change nothing.

## Refusals and limits

- Never run the install in the foreground of a single Bash call; it would exceed the stall watchdog and look like a hang.
- Never delete or rebuild the venv when the import check passes.
- If the machine has under ~1.2 GB free (`free -m`), say so before installing: the install may be killed and the install should be retried after stopping other containers.
- Does not touch the vault, the git state, or any credential.

## Verification (for the author)

- Fresh fork on Trinity v0.9.5, 4 GB droplet: `/first-run` completes in 4-8 minutes, `/recall sunk cost` then returns three cited notes.
- Second run: every step reports "already", nothing is rebuilt, the report still shows three titles.
