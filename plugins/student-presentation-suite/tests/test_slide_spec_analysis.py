from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_slide_spec.py"
SPEC = importlib.util.spec_from_file_location("analyze_slide_spec", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SlideSpecAnalysisTests(unittest.TestCase):
    def test_detects_structure_evidence_and_timing_risks(self) -> None:
        data = {
            "meta": {
                "duration_min": 1,
                "quality_tier": "high-score",
            },
            "slides": [
                {
                    "id": 1,
                    "title": "Analysis",
                    "layout": "data",
                    "content": "A " * 20,
                    "timing_sec": 40,
                    "owner": "Individual",
                },
                {
                    "id": 2,
                    "title": "Analysis",
                    "layout": "comparison",
                    "content": "B",
                    "evidence": [
                        {
                            "type": "data",
                            "claim": "B is better",
                            "status": "to-verify",
                        }
                    ],
                    "timing_sec": 40,
                    "owner": "Individual",
                },
            ],
        }
        result = MODULE.analyze(data)
        codes = {item["code"] for item in result["findings"]}
        self.assertTrue(
            {
                "generic-title",
                "missing-evidence",
                "evidence-to-verify",
                "duplicate-title",
                "missing-transition",
                "missing-close",
                "timing-overrun",
            }.issubset(codes)
        )

    def test_accepts_complete_basic_flow(self) -> None:
        data = {
            "meta": {"duration_min": 1, "quality_tier": "basic"},
            "slides": [
                {
                    "id": 1,
                    "title": "A clear problem drives this project",
                    "layout": "problem",
                    "content": "Problem",
                    "transition": "Next, we show the result.",
                    "timing_sec": 30,
                    "owner": "Individual",
                },
                {
                    "id": 2,
                    "kind": "closing",
                    "title": "Conclusion",
                    "layout": "closing",
                    "content": "Takeaway",
                    "timing_sec": 30,
                    "owner": "Individual",
                },
            ],
        }
        result = MODULE.analyze(data)
        self.assertEqual([], result["findings"])


if __name__ == "__main__":
    unittest.main()
