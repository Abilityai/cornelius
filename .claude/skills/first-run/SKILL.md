---
name: first-run
description: First-install playbook for a fresh Cornelius - lets the person choose an empty brain (the default) or the seed library, builds the local search engine (Python venv + FAISS + the embedding model), starts the search daemon, rebuilds the index so its stored paths match this machine, runs one smoke search and reports what works. Idempotent - run it again any time to verify. On Trinity, the same bootstrap starts on its own at first boot; this playbook finishes it and proves it.
allowed-tools: Bash, Read
user-invocable: true
argument-hint: "[--empty | --with-library] [--verify-only]"
metadata:
  version: "1.3"
  created: 2026-10-08
  author: Ability.ai
  changelog:
    - "1.3: Start with an empty brain (Abilityai/cornelius#21). The seed library (~1,050 notes) now lives in library/, outside the vault, the index and the Brain Orb. Step 0 asks once - empty is the default, unattended runs get empty - and --with-library copies it in (also later, any time). The smoke search accepts an empty vault (0 results + the plain empty-vault hint). No prebuilt index ships any more; Step 3 builds it"
    - "1.2: Install in the foreground of one streaming Bash call, never detached - on Trinity v0.9.5 the agent-server orphan sweeper kills unowned background processes ~90 s after container start (the boot-time bootstrap dies at the first long step after pip). Lock-file guidance updated"
    - "1.1: Reindex before the daemon, daemon start bounded by timeout, fastapi/uvicorn added to requirements (the daemon imported them but nothing installed them). From the first fresh-fork test on a 4 GB droplet"
    - "1.0: Initial - from the Agent-Native Agency workshop session 3 (2026-10-08). A fresh fork of the template ships the prebuilt index but not the Python that reads it, and the index remembers the build machine's paths, so 8 of 9 search-backed playbooks fail cold. This playbook is the one-command fix: venv (CPU-only torch, no pip cache - the install must fit a 4 GB box), daemon, reindex, smoke search, report. Pairs with .trinity/bootstrap.sh, which runs the same steps detached at container start."
---

# First Run

> ℹ️ Print one line first: `first-run v1.3 - recent: you choose an empty brain (default) or the seed library`. Then proceed.

## Purpose

A fresh copy of Cornelius starts with an **empty brain**: the vault (`Brain/`) holds only its folders, READMEs and templates. A seed library of about 1,050 notes on decision-making and cognitive science ships beside it in `library/` - outside the vault, so it is not searched, not indexed and not drawn in the Brain Orb until the person asks for it. The copy also lacks the Python environment that runs search. Until that is built, `/recall`, `/advise`, `/decide`, `/find-connections`, `/extract-insights` and every other search-backed playbook return nothing or fail. This playbook takes the vault from "cloned" to "answers questions" in one command, and reports honestly what it found at every step.

Safe to run repeatedly: every step checks before it acts.

## State Dependencies

| Source | Location | Read | Write |
|--------|----------|------|-------|
| Search engine | `resources/local-brain-search/` (venv, `requirements.txt`, `run_daemon.sh`, `run_index.sh`, `run_search.sh`) | ✓ | ✓ (venv, daemon, index files) |
| Index manifest | `resources/local-brain-search/data/manifest.json` | ✓ | via reindex |
| Bootstrap log and marker (Trinity) | `~/.trinity-bootstrap.log`, `~/.trinity-bootstrap.done`, `~/.trinity-bootstrap.lock` | ✓ | ✓ |
| The vault | `$VAULT_BASE_PATH` (default `./Brain`) | ✓ | ✓ (only with `--with-library`: library notes copied in, never overwriting) |
| Seed library | `library/` (same folder layout as `Brain/`) | ✓ | |
| Brain Orb data | `resources/agent-visualization/data.json` | | ✓ (re-exported when the library is added) |

## Process

Work from the agent root (the folder that holds `Brain/` and `resources/`). Keep every Bash call short (under 60 s): long installs run detached and are polled, so the platform's stall watchdog never fires.

### Step 0 - Empty brain or seed library?

Decide once, before anything else:

- `--with-library` → add the library (Step 2b). `--empty` → do not.
- No flag, and the library is already in the vault (`ls "Brain/Document Insights" | grep -v .gitkeep | head -1` prints something) → it was added before; nothing to choose.
- No flag, and a person is in this conversation → ask **one** question and wait for the answer:
  > Start with an empty brain (recommended - only your own notes), or add the seed library (about 1,050 notes on decision-making and cognitive science from published research and books)? You can add the library later with `/first-run --with-library`.

  No answer, or anything other than a clear "add the library" → empty.
- No flag and nobody to ask (headless call, schedule, a Trinity task started by another agent or the platform) → **empty**. Do not ask; say in the report that the library was not added and how to add it.

The boot-time bootstrap (`.trinity/bootstrap.sh`) is unattended, so it never adds the library.

### Step 1 - Is a bootstrap already running or done?

```bash
ls -la ~/.trinity-bootstrap.done ~/.trinity-bootstrap.lock 2>/dev/null; tail -5 ~/.trinity-bootstrap.log 2>/dev/null
```

- `.done` present → the boot-time bootstrap finished (it always leaves the brain empty); skip to Step 5 (verify) - or, if Step 0 chose the library, to Step 2b, then 3, 4, 5.
- `.lock` present and the log still growing → it is running; poll `tail -3 ~/.trinity-bootstrap.log` every 30 s until `.done` appears or the log stops for 2 minutes. A log that stops after "venv built" or "reindex start" with no process behind it means the boot-time bootstrap was swept (see Step 2) - continue with Step 2; every step checks before it acts, so nothing is redone.
- Neither → continue with Step 2.

### Step 2 - The Python environment

```bash
cd resources/local-brain-search && ./venv/bin/python -c "import faiss, sentence_transformers, networkx; print('ok')" 2>&1 | tail -1
```

If that prints `ok`, skip to Step 2b. Otherwise build it in the **foreground of one Bash call**, with output streaming (pip prints as it goes, so the platform's stall watchdog does not fire; on a 2-vCPU box with the CPU-only torch wheel this takes 1-2 minutes, ~1.5 GB):

```bash
cd resources/local-brain-search && python3 -m venv venv && ./venv/bin/pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt 2>&1 | grep -v -E "Downloading|Using cached|^\s+━" ; ./venv/bin/python -c "import faiss, sentence_transformers; print('ok')"
```

Tell the user it is installing before you run it. On an error, paste the last 20 lines and stop - do not retry blindly. **Do not run the install detached (`nohup … &`) on Trinity**: the agent-server's orphan sweeper kills background processes it does not own ~90 s after container start, which is exactly how the boot-time bootstrap gets cut off mid-way - this playbook exists to finish the job inside an execution the platform owns.

### Step 2b - Add the seed library (only if Step 0 chose it)

Copy `library/` into the vault without overwriting anything already there (a note the person changed stays theirs):

```bash
python3 -c "
import shutil, pathlib
src, dst = pathlib.Path('library'), pathlib.Path('Brain')
new = kept = 0
for f in src.rglob('*'):
    if f.is_file() and f.name != 'README.md':
        t = dst / f.relative_to(src)
        if t.exists(): kept += 1; continue
        t.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, t); new += 1
print(f'library: {new} notes added, {kept} already present')"
```

The library stays in `library/` as the source; the vault copies are the person's from now on. Later, any time: `/first-run --with-library` runs this step, then Steps 3-5, and touches nothing else.

### Step 3 - Build the index (before the daemon)

No index ships with the template; this builds it from whatever is in the vault right now - a handful of templates for an empty brain (seconds), about 6,600 chunks with the library (a few minutes on 2 vCPU). It downloads the embedding model (~90 MB) on first use. Run it again after Step 2b. The indexer embeds at most 500 new notes per call and prints `RESULT ... remaining=<n>`; **repeat the command until it prints `remaining=0`** (the library takes three calls, ~3 minutes each on 2 vCPU - each call reuses what the last one embedded).

```bash
cd resources/local-brain-search && ./run_index.sh 2>&1 | tail -8   # repeat until RESULT shows remaining=0
```

### Step 4 - The search daemon

```bash
cd resources/local-brain-search && timeout 120 ./run_daemon.sh start
```

"Daemon already running" is success. "started but not yet responding" → wait 20 s and run `./run_daemon.sh status`. If the daemon will not come up, searches still work through the CLI fallback, only slower - do not block on it.

### Step 5 - Verify with one smoke search

```bash
cd resources/local-brain-search && BRAIN_READ_SCOPE=@lookup ./run_search.sh "decision under uncertainty" --limit 3 --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); r=d.get('results',[]); print(len(r),'results'); [print('-', x.get('title') or x.get('note') or x.get('path')) for x in r[:3]]; print(d.get('hint',''))"
```

(`@lookup` is the role mount `/recall` and `/search-vault` use: your own notes plus the reading pile, where the library lands.)

- **Library added:** three titles → the engine, the index and the library are all there. Zero results → the index was not rebuilt after Step 2b (run Step 3 again) or the daemon is serving the old one (`./run_daemon.sh restart`).
- **Empty brain:** `0 results` followed by the line `Your brain is empty - ...` is the **pass**: search works and says so plainly. Zero results *without* that line means the vault has notes but none matched - fine too.
- An import error → Step 2 did not finish.

Then refresh the Brain Orb so it draws what is actually in the vault (on Trinity, `.trinity/setup.sh` copies an empty-vault `data.seed.json` at first boot; after Step 2b that picture is out of date):

```bash
resources/local-brain-search/venv/bin/python resources/agent-visualization/export_data.py 2>&1 | tail -3
```

On an empty brain the export draws the vault's scaffolding and sets `meta.notice` to the same empty-vault line, so the orb says the brain is empty instead of showing nothing.

### Step 6 - Report

One short block, no prose padding:

```
First run - <date>
Python env     : ok (faiss, sentence-transformers, torch) | built now in <m> min | FAILED: <reason>
Search daemon  : running (pid <n>) | not responding
Index          : rebuilt now | already current - <notes> notes, <edges> edges (manifest.json)
Brain          : empty (seed library not added - /first-run --with-library adds it) | library added - <n> notes (<k> already present)
Smoke search   : 3 results - <title 1> · <title 2> · <title 3> | empty brain - search answered plainly
Brain Orb data : refreshed - <n> nodes | n/a
Try next       : empty → write a note in Brain/02-Permanent/ or /intake <a file or link>   ·   library → /recall <topic>   ·   /advise <a problem you are weighing>
```

If `--verify-only` was passed, run Steps 1, 2 (check only), 3 (status only), 5 and 6 and change nothing (no Step 0 question, no Step 2b).

## Refusals and limits

- Never run the install in the foreground of a single Bash call; it would exceed the stall watchdog and look like a hang.
- Never delete or rebuild the venv when the import check passes.
- If the machine has under ~1.2 GB free (`free -m`), say so before installing: the install may be killed and the install should be retried after stopping other containers.
- Does not touch the git state or any credential. Touches the vault only in Step 2b, and only by adding library files that are not there yet - it never overwrites or deletes a note.
- Never adds the library without `--with-library` or a person's clear yes in Step 0.

## Verification (for the author)

- Fresh fork on Trinity v0.9.5, 4 GB droplet: `/first-run` completes in 4-8 minutes, `/recall sunk cost` then returns three cited notes (1.2, with the library in the vault).
- 1.3, scratch clone, both ways (2026-11-25): unattended `bootstrap.sh` → empty brain, index of 11 scaffolding files in 14 s, smoke search `0 results` + the empty-vault line (CLI, daemon and orb search hook), orb export with `meta.notice`, marker written. Then `--with-library` on the same clone → 1,056 files copied (second copy: 0 added), three index calls (500/500/56 notes, ~7 min), daemon fresh, smoke search three library titles, orb re-exported (1,067 nodes, notice null).
- Second run: every step reports "already", nothing is rebuilt, the report still shows three titles.
