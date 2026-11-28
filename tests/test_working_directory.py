"""Playbooks leave the session at the repo root; a missing engine is said plainly.

Origin: /first-run ran `cd resources/local-brain-search && ...` in Steps 2-5. The
shell keeps its folder between commands, so afterwards every repo-root path
(`resources/local-brain-search/run_search.sh`, `.../venv/bin/python`) answered
`No such file or directory` and the Brain said the search engine was not set up -
while the daemon was healthy and serving.
"""
import http.server
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LBS = ROOT / "resources" / "local-brain-search"
ROOT_CD = re.compile(r'^cd\s+("?\$PROJECT_ROOT"?|/path/to/\S+)\s*$')


def parked_cds(text):
    """Lines in a fenced shell block that `cd` somewhere outside a subshell."""
    bad, inblock, depth = [], False, 0
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if s.startswith("```"):
            inblock, depth = not inblock, 0
            continue
        if not inblock:
            continue
        if s == "(":
            depth += 1
        elif s == ")":
            depth = max(0, depth - 1)
        elif s.startswith("cd ") and depth == 0 and not ROOT_CD.match(s):
            bad.append((n, s[:90]))
    return bad


class PlaybooksStayAtTheRepoRoot(unittest.TestCase):
    def test_no_playbook_parks_the_shell(self):
        found = []
        for p in list((ROOT / ".claude").rglob("*.md")) + [ROOT / "CLAUDE.md"]:
            found += [f"{p.relative_to(ROOT)}:{n}: {s}" for n, s in parked_cds(p.read_text())]
        self.assertEqual(found, [], "wrap these in a subshell: (cd X && ...)\n" + "\n".join(found))

    def test_checker_catches_a_parked_cd(self):
        self.assertTrue(parked_cds("```bash\ncd resources/local-brain-search && ./run_index.sh\n```"))
        self.assertFalse(parked_cds("```bash\n(cd resources/local-brain-search && ./run_index.sh)\n```"))
        self.assertFalse(parked_cds("```bash\n(\ncd resources/x\n./y\n)\n```"))


def sandbox():
    d = Path(tempfile.mkdtemp(prefix="lbs-wrapper-"))
    for f in ("run_search.sh", "run_daemon.sh"):
        shutil.copy2(LBS / f, d / f)
    (d / "data").mkdir()
    (d / "data" / "brain.faiss").write_bytes(b"x")
    return d


def free_port():
    import socket
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class SearchWrapper(unittest.TestCase):
    def run_search(self, d, port):
        env = dict(os.environ, BRAIN_DAEMON_PORT=str(port), BRAIN_DAEMON_WAIT="0",
                   BRAIN_DAEMON_AUTOSTART="0", BRAIN_READ_SCOPE="@lookup")
        return subprocess.run(["bash", str(d / "run_search.sh"), "weekly sync", "--json"],
                              env=env, capture_output=True, text=True, timeout=60)

    def test_healthy_daemon_never_needs_the_venv(self):
        d = sandbox()
        build_id = int(os.path.getmtime(d / "data" / "brain.faiss"))

        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                body = ({"status": "ok", "build_id": build_id, "role_aliases": True}
                        if self.path.startswith("/health") else
                        {"query": "weekly sync", "mode": "static", "results": [{"note_id": "Company/x.md"}]})
                raw = json.dumps(body).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(raw)

            def log_message(self, *a):
                pass

        srv = http.server.ThreadingHTTPServer(("127.0.0.1", free_port()), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            out = self.run_search(d, srv.server_address[1])
        finally:
            srv.shutdown()
            shutil.rmtree(d, ignore_errors=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("Company/x.md", out.stdout)
        self.assertNotIn("No such file", out.stderr)

    def test_missing_engine_is_said_plainly(self):
        d = sandbox()
        try:
            out = self.run_search(d, free_port())
        finally:
            shutil.rmtree(d, ignore_errors=True)
        self.assertEqual(out.returncode, 3)
        self.assertIn("Search engine not installed", out.stderr)
        self.assertNotIn("No such file", out.stderr)


if __name__ == "__main__":
    unittest.main()
