from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "manage_versions.py"


def load_module():
    spec = importlib.util.spec_from_file_location("manage_versions", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ManageVersionsTests(unittest.TestCase):
    def test_snapshot_and_restore_candidate(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "outputs"
            output.mkdir()
            deck = output / "demo.pptx"
            deck.write_bytes(b"demo")
            saved = module.snapshot(output, "r1", [deck])
            deck.write_bytes(b"changed")
            restored = module.restore_candidate(output, "r1")
            candidate = Path(restored["restored_root"]) / "demo.pptx"
            self.assertEqual(b"demo", candidate.read_bytes())
            self.assertEqual(b"changed", deck.read_bytes())
            self.assertTrue(Path(saved["revision_root"]).is_dir())


if __name__ == "__main__":
    unittest.main()
