#!/usr/bin/env python3
"""Persistent scope switch for role reads (@reasoning / @lookup).

    python3 scope_toggles.py status          # effective mount + toggles
    python3 scope_toggles.py on  <token>     # add a scope to every reasoning/lookup read
    python3 scope_toggles.py off <token>     # remove one (also suppresses trigger mounts)
    python3 scope_toggles.py reset           # back to the standing mounts
    python3 scope_toggles.py off-list        # one resolved folder per line (for resolve_mount.sh)

Tokens: books, document-insights, company, canon, thinkers, Books/<slug>, Company/<sub>.
Voice, perception, ingestion and maintenance reads use literal mounts and are never
affected. Contract: .claude/skills/scope-mount/SKILL.md.
"""
import json
import sys

from memory_config import (
    BRAIN_PATH, CORE_FOLDERS, NEVER_ROLE_MOUNT, ROLE_MOUNTS, SCOPE_FAMILIES,
    SCOPE_TOGGLES_PATH, _SCOPE_BY_FOLDER, _family_children, _scope_token_folder, load_scope_toggles,
    resolve_read_scope,
)

STANDING = {_scope_token_folder(t) for t in ROLE_MOUNTS["@reasoning"].split(",") if t != "core"}


def _save(toggles):
    SCOPE_TOGGLES_PATH.write_text(json.dumps(toggles, indent=2) + "\n")


def _validate(token, mode):
    """Return the token's folder, or exit with the reason it cannot be switched."""
    if token.lower() == "core":
        sys.exit("refused: core is always mounted - it is the fingerprint, not a switchable scope")
    f = _scope_token_folder(token)
    fam = f.split("/", 1)[0]
    if f in CORE_FOLDERS or fam in CORE_FOLDERS:
        sys.exit(f"refused: {f} is part of core and cannot be switched")
    if fam not in _SCOPE_BY_FOLDER:
        sys.exit(f"unknown scope: {token} (see SCOPE_REGISTRY in memory_config.py)")
    if "/" in f and (fam not in SCOPE_FAMILIES or not (BRAIN_PATH / f).exists()):
        sys.exit(f"unknown sub-scope: {f}")
    if mode == "on" and fam in NEVER_ROLE_MOUNT:
        sys.exit(f"refused: {fam} is on the never-mount list for reasoning/lookup reads "
                 "(operational exhaust / unprocessed / derivative / demo data)")
    return f


def _keep(lst, folder):
    return [t for t in lst if _scope_token_folder(t) != folder]


def status():
    t = load_scope_toggles()
    folders = resolve_read_scope("@reasoning")
    shown = sorted(f for f in folders if "/" not in f or f.split("/", 1)[0] not in SCOPE_FAMILIES)
    for fam in sorted(SCOPE_FAMILIES):
        kids = {f.split("/", 1)[1] for f in folders if f.startswith(fam + "/")}
        if kids:
            missing = set(_family_children(fam)) - kids
            shown.append(fam + (f" (minus {', '.join(sorted(missing))})" if missing else ""))
    mount = ", ".join(shown)
    print(f"@reasoning / @lookup -> {mount}")
    print(f"  on:  {', '.join(t['on']) or '-'}")
    print(f"  off: {', '.join(t['off']) or '-'}  (also suppresses trigger mounts)")
    print("voice / perception / ingestion / maintenance: literal mounts, toggles never apply")
    print(f"state: {SCOPE_TOGGLES_PATH}")


def main(argv):
    if not argv or argv[0] == "status":
        return status()
    cmd, arg = argv[0], (argv[1] if len(argv) > 1 else None)
    t = load_scope_toggles()
    if cmd == "off-list":
        for tok in t["off"]:
            print(_scope_token_folder(tok))
        return
    if cmd == "reset":
        _save({"on": [], "off": []})
        return status()
    if cmd not in ("on", "off") or not arg:
        sys.exit(__doc__)
    f = _validate(arg, cmd)
    t["on"], t["off"] = _keep(t["on"], f), _keep(t["off"], f)
    if cmd == "off":
        t["off"].append(f)                    # also suppresses trigger mounts of f
    else:
        fam = f.split("/", 1)[0]
        offs = {_scope_token_folder(x) for x in t["off"]}
        if not (f in STANDING or (fam in STANDING and fam not in offs)):
            t["on"].append(f)                 # not already covered by the standing mount
    _save(t)
    status()


if __name__ == "__main__":
    main(sys.argv[1:])
