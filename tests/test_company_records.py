"""A question to the Brain about a company record finds it (stdlib only).

Origin: a decisions record written by /ref-ingest ("Decisions 2026-11", source: the
weekly sync) was not returned for "What decisions were made in the weekly sync?":
  1. the @lookup mount /recall uses did not include Company/;
  2. the Q-value boost re-scored every chunk of a note to that note's WEAKEST chunk,
     so the decision line (cosine 0.58) was ranked by its Change Log chunk (0.21);
  3. a plain-language question scores far below the threshold against a one-line
     record, so records are also matched by their words.
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


DECISION = ("- 2026-11-27 - Warehouse move confirmed for 2 February; the old site closes in March. "
            "Reason: the lease ends. (source: weekly sync notes; offered by: an agent; unconfirmed)")
META = [
    {"note_id": "Company/decisions/Decisions 2026-11.md", "title": "Decisions 2026-11",
     "heading": "Decisions", "filepath": "x", "content": DECISION},
    {"note_id": "Company/decisions/Decisions 2026-11.md", "title": "Decisions 2026-11",
     "heading": "Change Log", "filepath": "x", "content": "- 2026-11-28 - 1 decision offered"},
    {"note_id": "Document Insights/s/Weekly Rituals.md", "title": "Weekly Rituals",
     "heading": "Weekly Rituals", "filepath": "x", "content": "decisions made in a weekly sync meeting"},
    {"note_id": "Company/people/Someone.md", "title": "Someone", "heading": "Someone",
     "filepath": "x", "content": "Operations lead."},
]


class LookupMountsRecords(unittest.TestCase):
    def test_lookup_includes_company(self):
        with tempfile.TemporaryDirectory() as b:
            got = run(b, "import memory_config as m; print(sorted(m.resolve_read_scope('@lookup')))")
            self.assertIn("'Company'", got)

    def test_bare_search_names_records_it_did_not_search(self):
        with tempfile.TemporaryDirectory() as b:
            p = Path(b) / "Company/decisions/Decisions 2026-11.md"
            p.parent.mkdir(parents=True)
            p.write_text("# Decisions 2026-11\n\n" + DECISION + "\n")
            h = run(b, "import memory_config as m; print(m.empty_vault_hint('core'))")
            self.assertIn("Company (1)", h)
            self.assertIn("BRAIN_READ_SCOPE=@lookup", h)


class ChunkScoresKeepTheirOwnValue(unittest.TestCase):
    def test_strong_chunk_is_not_rescored_to_the_weak_one(self):
        with tempfile.TemporaryDirectory() as b:
            got = run(b, "import record_match as r\n"
                         "res=[{'note_id':'N','similarity':0.58},{'note_id':'M','similarity':0.40},{'note_id':'N','similarity':0.21}]\n"
                         "r.q_adjust_chunks(res, lambda s, read_scope=None: {k: v*1.1 for k, v in s.items()})\n"
                         "print(' '.join(f\"{x['note_id']}={x['similarity']:.3f}\" for x in res))")
            self.assertEqual(got, "N=0.638 M=0.440 N=0.231")


class RecordsMatchedByTheirWords(unittest.TestCase):
    def hits(self, b, query, scope):
        return run(b, "import record_match as r, memory_config as m\n"
                      f"meta={META!r}\n"
                      f"h=r.record_word_hits({query!r}, meta, m.resolve_read_scope({scope!r}), 0.5, 5, cosine_of=lambda i: 0.2)\n"
                      "print('|'.join(f\"{x['note_id']}#{x['heading']}#{x['match']}\" for x in h))")

    def test_question_finds_the_decision_record(self):
        with tempfile.TemporaryDirectory() as b:
            got = self.hits(b, "What decisions were made in the weekly sync?", "@lookup")
            self.assertIn("Company/decisions/Decisions 2026-11.md#Decisions#words", got)

    def test_only_records_never_cognitive_notes(self):
        with tempfile.TemporaryDirectory() as b:
            got = self.hits(b, "What decisions were made in the weekly sync?", "@lookup")
            self.assertNotIn("Document Insights", got)

    def test_records_outside_the_mount_stay_unsearched(self):
        with tempfile.TemporaryDirectory() as b:
            self.assertEqual(self.hits(b, "What decisions were made in the weekly sync?", "core"), "")

    def test_unrelated_question_adds_nothing(self):
        with tempfile.TemporaryDirectory() as b:
            self.assertEqual(self.hits(b, "how does dopamine shape motivation", "@lookup"), "")


class BothSearchPathsUseTheFix(unittest.TestCase):
    def test_cli_and_daemon_static_paths(self):
        for f in ("search.py", "daemon.py"):
            src = (LBS / f).read_text()
            self.assertIn("q_adjust_chunks(", src, f)
            self.assertIn("record_word_hits(", src, f)
            for bad in ("{r['note_id']: r['similarity'] for", '{r["note_id"]: r["similarity"] for'):
                self.assertNotIn(bad, src, f"{f}: per-note score dict over chunks is back")


if __name__ == "__main__":
    unittest.main()
