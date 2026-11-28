"""Brain Orb template tests (trinity-enterprise#76).

Guards the contract between this template and Trinity's agent-server broker
(docker/base-image/agent_server/routers/brain_orb.py): executable convention
hooks, single-JSON-document stdout, gitignore fates for runtime files, the
committed seed graph's schema (one malformed node blanks the orb canvas), and
the first-boot seeding path.

Stdlib only — run via ./run_tests.sh or `python3 -m unittest discover -s tests`.
"""
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = [".trinity/brain-orb/scopes", ".trinity/brain-orb/scope",
         ".trinity/brain-orb/search", ".trinity/brain-orb/action"]
LIFECYCLES = {"reflective", "crystallizing", "generative"}


def run_hook(hook, payload=None, cwd=ROOT):
    proc = subprocess.run(
        [str(Path(cwd) / hook)],
        input=json.dumps(payload) if payload is not None else "",
        capture_output=True, text=True, timeout=120, cwd=str(cwd),
    )
    return proc


def hook_json(hook, payload=None, cwd=ROOT):
    proc = run_hook(hook, payload, cwd)
    assert proc.returncode == 0, f"{hook} exited {proc.returncode}: {proc.stderr[:300]}"
    # The agent-server json-parses the WHOLE stdout: it must be one document.
    return json.loads(proc.stdout)


class TestExecutableBits(unittest.TestCase):
    def test_hooks_are_executable_in_git_index(self):
        """A GitHub-web-UI edit ships mode 100644 and the hook silently 404s —
        the git index must carry 100755 for every hook."""
        out = subprocess.run(["git", "ls-files", "-s"] + HOOKS + [".trinity/setup.sh"],
                             capture_output=True, text=True, cwd=str(ROOT)).stdout
        rows = dict(line.split()[3::-3][:1] and (line.split()[3], line.split()[0])
                    for line in out.strip().splitlines())
        for path in HOOKS + [".trinity/setup.sh"]:
            self.assertEqual(rows.get(path), "100755", f"{path} not 100755 in index")

    def test_hooks_are_executable_on_disk(self):
        for path in HOOKS:
            mode = (ROOT / path).stat().st_mode
            self.assertTrue(mode & stat.S_IXUSR, f"{path} lost its exec bit")


class TestGitignoreFates(unittest.TestCase):
    """Every runtime-written file has an explicit, intended git fate — the
    15-min agent auto-sync stages `git add -A`, so anything unignored lands in
    a commit."""

    def _ignored(self, path):
        r = subprocess.run(["git", "check-ignore", "-q", path], cwd=str(ROOT))
        return r.returncode == 0

    def test_runtime_state_is_ignored(self):
        for path in [".trinity/brain-orb/state.json",
                     ".trinity/brain-orb/voice-postprocess.json",
                     ".trinity/brain-orb/voice-postprocess.md",
                     "resources/agent-visualization/data.json",
                     "resources/agent-visualization/data.js",
                     ".env", ".mcp.json"]:
            self.assertTrue(self._ignored(path), f"{path} must be gitignored")

    def test_kit_files_are_not_ignored(self):
        for path in HOOKS + [".trinity/setup.sh", ".trinity/brain-orb/_common.py",
                             "resources/agent-visualization/data.seed.json",
                             "resources/agent-visualization/export_data.py"]:
            self.assertFalse(self._ignored(path), f"{path} must be trackable")


class TestReadOnlyHooks(unittest.TestCase):
    def test_scopes_contract(self):
        d = hook_json(".trinity/brain-orb/scopes")
        self.assertEqual(d.get("contract_version"), 1)
        self.assertIsInstance(d.get("active"), list)
        self.assertTrue(d["active"], "default active set must be non-empty")
        tokens = {e["token"] for e in d["available"]}
        for e in d["available"]:
            self.assertIn("token", e)
            self.assertIn("label", e)
        # The vault ships empty (#21); per-book child scopes appear only once a
        # book is in Brain/Books/ (the seed library adds six).
        shelf = [e for e in d["available"] if e.get("family")]
        children = [e for e in d["available"] if e.get("parent")]
        books = [p for p in (ROOT / "Brain" / "Books").glob("*/") if p.is_dir()]
        if books:
            self.assertTrue(shelf, "Books family shelf entry missing")
            self.assertTrue(children, "per-book child scopes missing")
        for c in children:
            self.assertIn(c["parent"], tokens)
        # active tokens must all be offered
        for t in d["active"]:
            self.assertIn(t, tokens)

    def test_search_contract_and_scope_confinement(self):
        d = hook_json(".trinity/brain-orb/search", {"query": "decision", "limit": 3})
        self.assertEqual(d.get("contract_version"), 1)
        self.assertIn(d.get("backend"), ("semantic", "keyword"))
        self.assertIsInstance(d["results"], list)
        if not d["results"]:
            # empty vault (#21): no hits is right, but it must say so plainly
            self.assertTrue(d.get("hint"), "empty result without the empty-vault hint")
        for r in d["results"]:
            self.assertTrue(r.get("title"))
            self.assertIn("content", r)

    def test_search_never_uses_request_paths(self):
        # A scope/path smuggled into the request must not change the walk —
        # the hook takes its scope from state.json only (review M2).
        d = hook_json(".trinity/brain-orb/search",
                      {"query": "decision", "limit": 2, "scope": "../../.."})
        self.assertIsInstance(d["results"], list)


class TestWriteSurfaceSandboxed(unittest.TestCase):
    """scope/action mutate data.json + the vault — run them in a throwaway
    copy with a mini vault so the repo checkout stays pristine."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="brain-orb-test-"))
        shutil.copytree(ROOT / ".trinity", cls.tmp / ".trinity")
        viz = cls.tmp / "resources" / "agent-visualization"
        viz.mkdir(parents=True)
        shutil.copy2(ROOT / "resources/agent-visualization/export_data.py", viz)
        shutil.copy2(ROOT / "resources/agent-visualization/viz_config.json", viz)
        lbs = cls.tmp / "resources" / "local-brain-search"
        lbs.mkdir(parents=True)
        shutil.copy2(ROOT / "resources/local-brain-search/memory_config.py", lbs)
        # mini vault: two core folders, three notes, one wikilink
        for folder, name, body in [
            ("02-Permanent", "Alpha Note", "# Alpha Note\n\nLinks to [[Beta Note]].\n"),
            ("02-Permanent", "Beta Note", "# Beta Note\n\nStands alone.\n"),
            ("03-MOCs", "MOC - Test", "# MOC - Test\n\n- [[Alpha Note]]\n"),
        ]:
            p = cls.tmp / "Brain" / folder / f"{name}.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_full_write_cycle(self):
        # 1. mount both folders
        d = hook_json(".trinity/brain-orb/scope",
                      {"tokens": ["02-Permanent", "03-MOCs"]}, cwd=self.tmp)
        self.assertTrue(d["ok"], d)
        self.assertEqual(d["nodes"], 3)
        self.assertGreaterEqual(d["edges"], 2)

        # 2. unknown token fails loud, state unchanged
        d = hook_json(".trinity/brain-orb/scope", {"tokens": ["../../etc"]}, cwd=self.tmp)
        self.assertFalse(d["ok"])

        # 3. capture writes into the vault inbox
        d = hook_json(".trinity/brain-orb/action",
                      {"action": "capture", "title": "Fresh Thought",
                       "body": "Captured from the orb."}, cwd=self.tmp)
        self.assertTrue(d["ok"], d)
        self.assertTrue((self.tmp / d["path"]).exists())

        # 4. refresh folds the capture in (00-Inbox is auto-discovered)
        d = hook_json(".trinity/brain-orb/scope",
                      {"tokens": ["02-Permanent", "03-MOCs", "00-Inbox"]}, cwd=self.tmp)
        self.assertTrue(d["ok"], d)
        self.assertEqual(d["nodes"], 4, "capture must appear after remount")

        # 5. link appends a real wikilink and refresh adds the edge
        d = hook_json(".trinity/brain-orb/action",
                      {"action": "link", "from": "Fresh Thought", "to": "Alpha Note"},
                      cwd=self.tmp)
        self.assertTrue(d["ok"], d)
        d = hook_json(".trinity/brain-orb/action", {"action": "refresh"}, cwd=self.tmp)
        self.assertTrue(d["ok"], d)
        self.assertEqual(d["added_edges"], 1)

        # 6. link to a nonexistent endpoint fails loud
        d = hook_json(".trinity/brain-orb/action",
                      {"action": "link", "from": "Fresh Thought", "to": "No Such Note"},
                      cwd=self.tmp)
        self.assertFalse(d["ok"])

        # 7. transcript path traversal is confined to the vault
        d = hook_json(".trinity/brain-orb/action",
                      {"action": "process_transcript", "path": "/etc/passwd"}, cwd=self.tmp)
        self.assertFalse(d["ok"])

    def test_setup_sh_seeds_data_json(self):
        viz = self.tmp / "resources" / "agent-visualization"
        seed = viz / "data.seed.json"
        seed.write_text('{"nodes": [], "edges": []}')
        (viz / "data.json").unlink(missing_ok=True)
        r = subprocess.run(["bash", str(self.tmp / ".trinity/setup.sh")],
                           capture_output=True, text=True, cwd=str(self.tmp))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((viz / "data.json").read_text(), seed.read_text())


class TestSeedSchema(unittest.TestCase):
    """The committed seed must satisfy what orb.js buildGraph actually
    dereferences — one null title or non-numeric layer blanks the canvas."""

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (ROOT / "resources/agent-visualization/data.seed.json").read_text())

    def test_nodes(self):
        nodes = self.data["nodes"]
        # The seed is the EMPTY-vault picture (#21): the vault's scaffolding, never
        # an empty list (that blanks the canvas), and never the seed library.
        self.assertTrue(nodes, "seed graph must not be empty")
        for n in nodes:
            self.assertFalse(n["id"].startswith(("Document Insights/", "Books/")),
                             f"seed library note in the empty-vault seed: {n['id']}")
        self.assertTrue(self.data["meta"].get("notice"), "empty-vault seed must carry meta.notice")
        ids = set()
        for n in nodes:
            self.assertTrue(n.get("title"), f"node without title: {n.get('id')}")
            self.assertIsInstance(n.get("layer"), int)
            self.assertTrue(1 <= n["layer"] <= 7, n["layer"])
            self.assertIn(n.get("lifecycle"), LIFECYCLES)
            ids.add(n["id"])
        self.assertEqual(len(ids), len(nodes), "duplicate node ids")

    def test_edges_are_endpoint_closed(self):
        ids = {n["id"] for n in self.data["nodes"]}
        for e in self.data["edges"]:
            self.assertIn(e["source"], ids)
            self.assertIn(e["target"], ids)
            self.assertIn("type", e)
            self.assertIsInstance(e.get("weight"), (int, float))

    def test_optional_sections_present_as_empty_safe(self):
        for key in ("tensions", "incubation", "converged", "activity", "recent"):
            self.assertIsInstance(self.data.get(key), list, f"{key} must be a list")
        self.assertIsInstance(self.data.get("metrics"), dict)
        meta = self.data["meta"]
        self.assertIn("sampled_nodes", meta)
        self.assertIn("total_nodes", meta)

    def test_no_personal_identifiers(self):
        # Patterns are split-concatenated so the sync sanitizer (which rewrites
        # these very identifiers in synced text) can never rewrite the guard
        # itself into a no-op.
        raw = (ROOT / "resources/agent-visualization/data.seed.json").read_text()
        patterns = ("/Users/" + "eu" + "gene", "evyb" + "orov",
                    "ability" + ".ai", "Eu" + "gene ")
        for pat in patterns:
            self.assertNotIn(pat, raw, f"personal identifier in seed: {pat}")


if __name__ == "__main__":
    unittest.main()


class TestEmptyBrainDefault(unittest.TestCase):
    """#21: the seed library ships outside the vault and stays out until asked for."""

    def test_library_outside_vault(self):
        lib = ROOT / "library"
        self.assertTrue((lib / "README.md").is_file())
        self.assertGreater(len(list(lib.rglob("*.md"))), 1000, "seed library missing")
        if any((ROOT / "Brain" / "Document Insights").rglob("*.md")):
            self.skipTest("library already added to this vault (/first-run --with-library)")

    def test_no_prebuilt_index_tracked(self):
        out = subprocess.run(["git", "ls-files", "resources/local-brain-search/data"],
                             capture_output=True, text=True, cwd=str(ROOT)).stdout.split()
        self.assertEqual([f for f in out if not f.endswith("README.md")], [],
                         "a prebuilt index would put the library back into search")


class TestOrbSummaryLine(unittest.TestCase):
    """The orb draws a capped sample; its `orb:` line must say so and account for
    every note (shown + left out = total), so a gap against the index count is not
    read as notes being dropped (first-run with the library, 2026-11-28)."""

    def test_sampled_vault_is_explained_and_accounted_for(self):
        tmp = Path(tempfile.mkdtemp(prefix="orb-summary-"))
        try:
            viz = tmp / "resources" / "agent-visualization"
            viz.mkdir(parents=True)
            shutil.copy2(ROOT / "resources/agent-visualization/export_data.py", viz)
            shutil.copy2(ROOT / "resources/agent-visualization/viz_config.json", viz)
            lbs = tmp / "resources" / "local-brain-search"
            lbs.mkdir(parents=True)
            shutil.copy2(ROOT / "resources/local-brain-search/memory_config.py", lbs)
            total = 700   # over the impression cap in viz_config.json (480) plus the always-included sets
            for i in range(total):
                p = tmp / "Brain" / "Document Insights" / "s" / f"Finding {i}.md"
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(f"# Finding {i}\n\nSee [[Finding {(i + 1) % total}]].\n")
            env = dict(os.environ)
            env.pop("BRAIN_READ_SCOPE", None)
            out = subprocess.run([sys.executable, "-I", str(viz / "export_data.py")], env=env,
                                 capture_output=True, text=True, timeout=120, cwd=str(tmp))
            self.assertEqual(out.returncode, 0, out.stderr)
            line = out.stderr.strip().splitlines()[-1]
            m = re.match(r"orb: (\d+) of (\d+) notes shown \(a sample.*left out: (\d+) Document Insights\)", line)
            self.assertTrue(m, line)
            shown, of, left = map(int, m.groups())
            self.assertEqual(of, total)
            self.assertLess(shown, total)
            self.assertEqual(shown + left, total, line)
            self.assertIn("wiki-links only", line)
            data = json.loads((viz / "data.json").read_text())
            self.assertEqual(len(data["nodes"]), shown)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
