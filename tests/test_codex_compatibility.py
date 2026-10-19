"""Codex discovery packaging contracts. Stdlib only; no model or API calls.

Exercise the actual aliases and Git file modes, including after a clone to a
path containing spaces. Live instruction and workflow checks are separate.
"""
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "start-here", "quick-search", "recall", "search-vault", "find-connections",
    "advise", "extract-insights", "graduate-insights", "refresh-index",
    "analyze-kb",
}


class TestCodexPackaging(unittest.TestCase):
    def assert_discovery(self, root):
        discovery = root / ".agents/skills"
        self.assertTrue(discovery.is_dir(), "Codex discovery directory missing")
        self.assertEqual({p.name for p in discovery.iterdir()}, SKILLS)
        for name in sorted(SKILLS):
            with self.subTest(skill=name):
                alias = discovery / name
                canonical = root / ".claude/skills" / name
                self.assertTrue(alias.is_symlink(), str(alias))
                self.assertEqual(str(alias.readlink()), "../../.claude/skills/" + name)
                self.assertEqual(alias.resolve(strict=True), canonical.resolve())
                self.assertTrue((alias / "SKILL.md").is_file())
                for resource in canonical.rglob("*"):
                    if resource.is_file():
                        exposed = alias / resource.relative_to(canonical)
                        self.assertEqual(exposed.read_bytes(), resource.read_bytes())

    def test_supported_skills_share_canonical_directories(self):
        self.assert_discovery(ROOT)

    def test_clone_preserves_aliases_and_companion_resources(self):
        # Snapshot the current index, as upstream's mode tests do. This checks
        # a candidate before committing without including untracked user data.
        with tempfile.TemporaryDirectory() as tmp:
            origin = Path(tmp) / "candidate repository"
            origin.mkdir()
            subprocess.run(["git", "init", "-q", str(origin)], check=True)
            subprocess.run([
                "git", "checkout-index", "--all", "--prefix=" + str(origin) + "/",
            ], cwd=ROOT, check=True)
            subprocess.run(["git", "add", "-A"], cwd=origin, check=True)
            subprocess.run([
                "git", "-c", "user.name=Fixture", "-c",
                "user.email=fixture@example.invalid", "commit", "-qm", "fixture",
            ], cwd=origin, check=True)
            clone = Path(tmp) / "clone with spaces"
            subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True)
            self.assert_discovery(clone)

    def test_source_files_have_expected_git_modes(self):
        result = subprocess.run([
            "git", "ls-files", "-s", "AGENTS.md", "docs/CODEX.md", ".agents/skills",
        ], cwd=ROOT, capture_output=True, text=True, check=True)
        entries = {}
        for row in result.stdout.splitlines():
            metadata, path = row.split("\t", 1)
            entries[path] = metadata.split()[0]
        self.assertEqual(entries.get("AGENTS.md"), "100644")
        self.assertEqual(entries.get("docs/CODEX.md"), "100644")
        for name in SKILLS:
            self.assertEqual(entries.get(".agents/skills/" + name), "120000")

    def test_codex_runtime_state_is_ignored_but_sources_are_not(self):
        for path in [".codex/auth.json", ".codex/config.toml",
                     ".codex/sessions/run.jsonl", ".codex/log/codex.log"]:
            with self.subTest(path=path):
                result = subprocess.run(["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT)
                self.assertEqual(result.returncode, 0)
        for path in ["AGENTS.md", "docs/CODEX.md", ".agents/skills/advise",
                     ".codex/agents/example.toml"]:
            with self.subTest(path=path):
                result = subprocess.run(["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT)
                self.assertEqual(result.returncode, 1)
