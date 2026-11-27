"""Every script a playbook tells the agent to run must ship with the template.

A fresh copy of the template has only what is in this repo. A skill, agent or
command that says "run resources/x/y.sh" when y.sh lives only in some private
checkout fails on the first real use (first-boot test 2026-11-27:
/ingest-source called resources/ingest-workspace/score_neighbours.sh, which was
never shipped). This test reads every playbook and fails on any referenced
.sh / .py path that resolves to nothing - from the repo root, or from the
playbook's own folder (skills ship helper scripts beside SKILL.md).

Data files (.json, reports, ledgers) are left out on purpose: playbooks create
them at run time.
"""
import fnmatch
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAYBOOK_GLOBS = [".claude/skills/**/*.md", ".claude/agents/**/*.md",
                  ".claude/commands/**/*.md", ".trinity/*.sh", "CLAUDE.md"]

# A repo-relative path that starts at a top-level folder the template ships,
# not preceded by another path character (so "$ROOT/resources/..." and
# "venv/bin/..." fragments are not misread), ending in a script extension.
REF = re.compile(
    r"(?<![\w/.\-\[$])((?:\./)?(?:resources|\.trinity|\.claude|scripts|tests|library)/[\w./\-]*?\.(?:sh|py))\b")


def playbooks():
    seen = set()
    for g in PLAYBOOK_GLOBS:
        for p in ROOT.glob(g):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def missing_refs():
    out = []
    for f in playbooks():
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in REF.finditer(text):
            ref = m.group(1)
            ref = ref[2:] if ref.startswith("./") else ref
            if "<" in ref or "*" in ref:
                continue
            if (ROOT / ref).exists() or (f.parent / ref).exists():
                continue
            out.append(f"{f.relative_to(ROOT)} -> {ref}")
    return sorted(set(out))


class TemplateReferences(unittest.TestCase):
    def test_every_referenced_script_ships(self):
        missing = missing_refs()
        self.assertEqual(missing, [], "playbooks reference scripts the template does not ship:\n  "
                         + "\n  ".join(missing))

    def test_checker_catches_a_missing_script(self):
        # guard against a regex that silently matches nothing
        self.assertTrue(REF.search("run resources/ingest-workspace/score_neighbours.sh now"))
        self.assertIsNone(REF.search('"$ROOT/resources/x/y.sh"'))

    def test_bootstrap_is_on_the_sweep_allowlist(self):
        # fnmatch against argv joined by spaces - the agent server's own rule
        pats = [l.strip() for l in (ROOT / ".trinity/persistent-processes.allow").read_text().splitlines()
                if l.strip() and not l.lstrip().startswith("#")]
        argv = "bash /home/developer/.trinity/bootstrap.sh"
        self.assertTrue(any(fnmatch.fnmatchcase(argv, p) for p in pats), pats)


if __name__ == "__main__":
    unittest.main()
