"""Source labels and the not-searched hint (stdlib only).

A person's question about their notes must not come back empty just because the
notes were made from a document (Document Insights/) and a bare search mounts only
core. The engine stays fail-closed; it must SAY what it left out, and label every
hit with where it comes from.
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LBS = Path(__file__).resolve().parent.parent / "resources" / "local-brain-search"


def run(brain, code):
    env = dict(os.environ, BRAIN_PATH=str(brain), SCOPE_TOGGLES_PATH=str(Path(brain) / "no-toggles.json"))
    env.pop("BRAIN_READ_SCOPE", None)
    out = subprocess.run([sys.executable, "-I", "-c", f"import sys; sys.path.insert(0, {str(LBS)!r}); " + code],
                         env=env, capture_output=True, text=True, timeout=60)
    if out.returncode:
        raise AssertionError(out.stderr)
    return out.stdout.strip()


def note(brain, rel, body="x"):
    p = Path(brain) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"# {p.stem}\n\n{body}\n")


class SourceLabels(unittest.TestCase):
    def test_kinds(self):
        with tempfile.TemporaryDirectory() as b:
            got = run(b, "import memory_config as m; print('|'.join(m.source_kind(n) for n in "
                         "['02-Permanent/a.md', 'Document Insights/s/a.md', 'Books/x/a.md', 'Company/decisions/D.md']))")
            self.assertEqual(got, "your thinking|read, not endorsed|read, not endorsed|record")

    def test_label_sources_adds_fields(self):
        with tempfile.TemporaryDirectory() as b:
            got = run(b, "import memory_config as m; r=[{'note_id': 'Books/atomic/ch1.md'}]; m.label_sources(r); "
                         "print(r[0]['source'], '|', r[0]['source_kind'])")
            self.assertEqual(got, "Books/atomic | read, not endorsed")


class NotSearchedHint(unittest.TestCase):
    def hint(self, b, scope):
        return run(b, f"import memory_config as m; print(m.empty_vault_hint({scope!r}))")

    def test_only_document_notes(self):
        with tempfile.TemporaryDirectory() as b:
            note(b, "Document Insights/s/Delegation.md")
            h = self.hint(b, "core")
            self.assertIn("Document Insights (1)", h)
            self.assertIn("BRAIN_READ_SCOPE=@lookup", h)

    def test_core_has_notes_but_documents_were_not_searched(self):
        with tempfile.TemporaryDirectory() as b:
            note(b, "02-Permanent/Sleep.md")
            note(b, "Document Insights/s/Delegation.md")
            note(b, "Document Insights/s/Owners.md")
            h = self.hint(b, "core")
            self.assertIn("Nothing matched in the mounted read scope (1 note)", h)
            self.assertIn("2 notes outside it were not searched", h)

    def test_lookup_no_match_is_a_real_no_match(self):
        with tempfile.TemporaryDirectory() as b:
            note(b, "02-Permanent/Sleep.md")
            note(b, "Document Insights/s/Delegation.md")
            note(b, "05-Meta/Changelogs/log.md")      # exhaust is never pointed at
            self.assertEqual(self.hint(b, "@lookup"), "None")

    def test_empty_vault(self):
        with tempfile.TemporaryDirectory() as b:
            self.assertIn("Your brain is empty", self.hint(b, "core"))


if __name__ == "__main__":
    unittest.main()
