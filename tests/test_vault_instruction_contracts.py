"""Run scoped path enumeration and root lookup recipes on disposable vaults."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]


class KeywordRecipeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vault recipe ")
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name) / "Brain with spaces"
        self.notes = {
            "02-Permanent/Core.md": "CORE",
            "Company/people/Person.md": "REFERENCE",
            "Company/orgs/Organization.md": "OTHER_REFERENCE",
            "Document Insights/Session/Document.md": "DOCUMENT",
            "Books/first book/Chapter.md": "BOOK",
            "Books/second/Chapter.md": "OTHER_BOOK",
        }
        for name, marker in self.notes.items():
            path = self.vault / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("before\ntidal " + marker + " café\nafter\n", encoding="utf-8")
        skill = (ROOT / ".claude/skills/search-vault/SKILL.md").read_text()
        blocks = re.findall(r"```bash\n(.*?)```", skill, re.S)
        self.recipe = next(textwrap.dedent(block) for block in blocks
                           if "from memory_config import" in block)

    def run_recipe(self, scope=""):
        env = dict(os.environ, BRAIN_PATH=str(self.vault),
                   BRAIN_READ_SCOPE=scope)
        return subprocess.run(["bash", "-c", self.recipe], cwd=ROOT,
                              env=env, capture_output=True, text=True)

    def names(self, scope=""):
        result = self.run_recipe(scope)
        self.assertEqual(result.returncode, 0, result.stderr)
        return {Path(path).relative_to(self.vault).as_posix()
                for path in json.loads(result.stdout)}

    def test_default_is_core(self):
        self.assertEqual(self.names(), {"02-Permanent/Core.md"})

    def test_reference_family_mount_excludes_siblings(self):
        self.assertEqual(self.names("core,Company/people"),
                         {"02-Permanent/Core.md", "Company/people/Person.md"})

    def test_document_alias_and_book_mount(self):
        self.assertEqual(self.names("document-insights,Books/first book"),
                         {"Document Insights/Session/Document.md",
                          "Books/first book/Chapter.md"})
        self.assertEqual(self.names("books"),
                         {"Books/first book/Chapter.md", "Books/second/Chapter.md"})

    def test_unknown_and_all_scopes_do_not_widen(self):
        for scope in ["all", "typo", "--scope=core"]:
            with self.subTest(scope=scope):
                self.assertEqual(self.names(scope), set())

    def test_enumeration_does_not_read_content_or_filter_keywords(self):
        note = self.vault / "02-Permanent" / "Binary café.md"
        note.write_bytes(b"\xff\xfe")
        self.assertEqual(self.names(), {"02-Permanent/Core.md", "02-Permanent/Binary café.md"})

    def test_file_symlinks_are_not_eligible_even_with_allowed_targets(self):
        outside = Path(self.temp.name) / "Outside.md"
        outside.write_text("SYNTHETIC_OUTSIDE")
        targets = {
            "Allowed alias.md": self.vault / "02-Permanent/Core.md",
            "Excluded alias.md": self.vault / "Company/people/Person.md",
            "Outside alias.md": outside,
            "Broken alias.md": self.vault / "missing.md",
        }
        for name, target in targets.items():
            (self.vault / "02-Permanent" / name).symlink_to(target)
        self.assertEqual(self.names("core"), {"02-Permanent/Core.md"})

    def test_directory_symlinks_are_not_eligible(self):
        outside = Path(self.temp.name) / "Outside"
        outside.mkdir()
        (outside / "Outside.md").write_text("SYNTHETIC_OUTSIDE")
        for name, target in {
            "Allowed": self.vault / "02-Permanent",
            "Excluded": self.vault / "Company",
            "Outside": outside,
        }.items():
            (self.vault / "02-Permanent" / name).symlink_to(target,
                                                             target_is_directory=True)
        self.assertEqual(self.names("core"), {"02-Permanent/Core.md"})

    def test_symlink_vault_root_is_supported(self):
        alias = Path(self.temp.name) / "Vault alias"
        alias.symlink_to(self.vault, target_is_directory=True)
        self.vault = alias
        result = self.run_recipe("core")
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = [Path(path).resolve() for path in json.loads(result.stdout)]
        self.assertEqual(paths, [alias.resolve() / "02-Permanent/Core.md"])

    def test_missing_vault_is_an_error(self):
        self.vault = self.vault / "missing"
        result = self.run_recipe()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Vault not found", result.stderr)

    def test_all_eligible_files_are_enumerated(self):
        for number in range(8):
            (self.vault / "02-Permanent" / f"Extra {number}.md").write_text("unrelated")
        (self.vault / "02-Permanent" / "directory.md").mkdir()
        self.assertEqual(len(json.loads(self.run_recipe().stdout)), 9)


class VaultRootRecipeTests(unittest.TestCase):
    def test_analysis_uses_configured_root(self):
        with tempfile.TemporaryDirectory(prefix="root recipe ") as directory:
            vault = Path(directory) / "Brain"
            note = vault / "02-Permanent" / "Fixture Tidal Decisions.md"
            note.parent.mkdir(parents=True)
            note.write_text("# Fixture Tidal Decisions\n")
            env = dict(os.environ, VAULT_BASE_PATH=str(vault),
                       ARGUMENTS="Fixture Tidal Decisions")
            for skill, prefix in [("analyze-kb", "find ")]:
                text = (ROOT / f".claude/skills/{skill}/SKILL.md").read_text()
                command = next(line.strip() for line in text.splitlines()
                               if line.strip().startswith(prefix))
                result = subprocess.run(["bash", "-c", command], env=env,
                                        cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(str(note), result.stdout)
            self.assertFalse((vault / "Brain").exists())


if __name__ == "__main__":
    unittest.main()
