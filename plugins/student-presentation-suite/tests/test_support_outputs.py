from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_support_outputs.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_support_outputs", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SupportOutputTests(unittest.TestCase):
    def test_builds_teleprompter_cards_and_references(self) -> None:
        module = load_module()
        data = {
            "meta": {"topic": "Demo", "citation_style": "APA"},
            "evidence_ledger": [
                {
                    "id": "e1",
                    "title": "Source",
                    "locator": "https://example.test",
                    "confidence": "high",
                }
            ],
            "slides": [
                {
                    "id": 1,
                    "title": "Claim",
                    "claim": "Main point",
                    "supporting_points": ["Reason"],
                    "speaker_notes": "Explain it.",
                    "transition": "Continue.",
                    "timing_sec": 30,
                }
            ],
        }
        teleprompter = module.teleprompter_html(data)
        cards = module.training_cards(data)
        references = module.references_markdown(data)
        self.assertIn("Explain it.", teleprompter)
        self.assertIn("Likely question", cards)
        self.assertIn("https://example.test", references)


if __name__ == "__main__":
    unittest.main()
