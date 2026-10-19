"""Exercise the real wrapper without a daemon, network or search dependencies."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class TestSearchWrapper(unittest.TestCase):
    wrapper_name = "run_search.sh"
    endpoint = "/search?"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "requests.jsonl"
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ["PATH"],
                        REQUEST_LOG=str(self.log), BRAIN_READ_SCOPE="core",
                        BRAIN_DAEMON_PORT="7437", REAL_PYTHON=sys.executable)
        self.env.pop("FAIL_ENCODING", None)
        self.env.pop("STALE_DAEMON", None)
        # Replace only transport: all source parsing and encoding use real Python.
        self.executable(self.bin / "curl", """import json, os, sys
url = sys.argv[-1]
with open(os.environ['REQUEST_LOG'], 'a') as out:
    out.write(json.dumps(url) + '\\n')
if url.endswith('/health'):
    print(json.dumps({'build_id': 0 if os.environ.get('STALE_DAEMON') else 1700000000}))
else:
    print(json.dumps({'results': []}))
""")
        self.executable(self.bin / "python3", """import os, sys
if 'urllib.parse' in sys.argv[2] and os.environ.get('FAIL_ENCODING'):
    kind = os.environ['FAIL_ENCODING']
    if len(sys.argv) > 3 and ((kind == 'query' and sys.argv[3] != 'core') or (kind == 'scope' and sys.argv[3] == 'core')):
        sys.exit(23)
os.execv(os.environ['REAL_PYTHON'], [os.environ['REAL_PYTHON']] + sys.argv[1:])
""")

    def executable(self, path, body):
        path.write_text("#!" + sys.executable + "\n" + body)
        path.chmod(0o755)

    def run_wrapper(self, query, directory="search workspace"):
        workspace = self.root / directory
        workspace.mkdir()
        wrapper = workspace / self.wrapper_name
        shutil.copy2(ROOT / "resources/local-brain-search" / self.wrapper_name, wrapper)
        shutil.copy2(ROOT / "resources/local-brain-search/wrapper_common.sh", workspace)
        (workspace / "data").mkdir()
        index = workspace / "data/brain.faiss"
        index.touch()
        os.utime(index, (1700000000, 1700000000))
        (workspace / "venv/bin").mkdir(parents=True)
        self.executable(workspace / "venv/bin/python", """import json, sys
print(json.dumps({'fallback_args': sys.argv[2:]}))
""")
        result = subprocess.run(["bash", str(wrapper), query, "--json"],
                                env=self.env, capture_output=True, text=True, timeout=10)
        requests = [json.loads(line) for line in self.log.read_text().splitlines()]
        return result, [url for url in requests if self.endpoint in url]

    def test_queries_remain_literal_data(self):
        for number, query in enumerate([
            "tidal decisions", "owner's decisions", "café 日本語 & scope=all",
            "')); print('SYNTHETIC_CODE_EXECUTION_MARKER'); #", "first\nsecond\\third",
        ]):
            with self.subTest(query=query):
                self.log.write_text("")
                result, requests = self.run_wrapper(query, "case " + str(number))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertEqual(len(requests), 1)
                params = parse_qs(urlsplit(requests[0]).query)
                self.assertEqual(params["q"], [query])
                self.assertEqual(params["scope"], ["core"])

    def test_index_path_with_apostrophe_keeps_daemon_path(self):
        result, requests = self.run_wrapper("decisions", "owner's search workspace")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(requests), 1)
        self.assertNotIn("fallback_args", result.stdout)

    def test_encoding_failure_does_not_submit_request(self):
        for kind in ["query", "scope"]:
            with self.subTest(kind=kind):
                self.log.write_text("")
                self.env["FAIL_ENCODING"] = kind
                result, requests = self.run_wrapper("decisions", kind)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(result.stderr.strip())
                self.assertEqual(requests, [])
                self.assertNotIn("fallback_args", result.stdout)

    def test_stale_daemon_preserves_direct_cli_arguments(self):
        self.env["STALE_DAEMON"] = "1"
        result, requests = self.run_wrapper("owner's decisions")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(requests, [])
        self.assertEqual(json.loads(result.stdout)["fallback_args"],
                         ["owner's decisions", "--json"])
