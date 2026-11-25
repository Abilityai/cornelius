"""Brain-graph config tests (Abilityai/cornelius#15). Run: python test_config.py

1. brain_graph_config.yaml exists and carries every key config.py reads.
2. A missing file fails with an actionable message that names the path.
3. The architecture doc's "Central Graph Definition" block is a subset of the
   shipped yaml, so the doc and the file cannot drift apart silently.
"""
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

import config  # noqa: E402

DOC = HERE / "BRAIN-DEPENDENCY-GRAPH-ARCHITECTURE.md"


def doc_block():
    text = DOC.read_text()
    sec = text.split("### Central Graph Definition", 1)[1]
    m = re.search(r"```yaml\n(.*?)```", sec, re.S)
    return yaml.safe_load(m.group(1))


@unittest.skipIf(yaml is None, "PyYAML not installed")
class TestBrainGraphConfig(unittest.TestCase):
    def setUp(self):
        config._config_cache = None

    def test_shipped_config_loads_with_all_keys(self):
        self.assertTrue(config.CONFIG_PATH.is_file(), f"{config.CONFIG_PATH} is not shipped")
        cfg = config.load_config()
        for k in config.REQUIRED_KEYS:
            self.assertIn(k, cfg)
        # every accessor works
        config.get_propagation_config()
        config.get_lifecycle_config()
        config.get_artifact_types()
        config.get_default_edges()
        config.get_framework_detection()

    def test_missing_config_names_the_path(self):
        real = config.CONFIG_PATH
        config.CONFIG_PATH = HERE / "does-not-exist.yaml"
        try:
            with self.assertRaises(FileNotFoundError) as cm:
                config.load_config()
            self.assertIn("does-not-exist.yaml", str(cm.exception))
            self.assertIn("git checkout", str(cm.exception))
        finally:
            config.CONFIG_PATH = real
            config._config_cache = None

    def test_doc_block_is_subset_of_shipped_yaml(self):
        doc, cfg = doc_block(), config.load_config()
        self.assertEqual(doc["propagation"], cfg["propagation"], "doc vs yaml: propagation drifted")
        self.assertEqual(doc["lifecycle"], cfg["lifecycle"], "doc vs yaml: lifecycle drifted")
        self.assertEqual(set(doc["artifact_types"]), set(cfg["artifact_types"]))
        for name, t in doc["artifact_types"].items():
            c = cfg["artifact_types"][name]
            self.assertEqual((t["layer"], t["default_mode"]), (c["layer"], c["default_mode"]), name)
            self.assertTrue(set(t["vault_paths"]) <= set(c["vault_paths"]), name)
        for e in doc["default_edges"]:
            self.assertIn(e, cfg["default_edges"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
