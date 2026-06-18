from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "slide_spec_to_pptx_brief.py"


def load_bridge_module():
    spec = importlib.util.spec_from_file_location("slide_spec_to_pptx_brief", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SlideSpecBridgeTests(unittest.TestCase):
    def test_builds_claude_pptx_brief_from_valid_spec(self) -> None:
        bridge = load_bridge_module()
        data = {
            "meta": {
                "presentation_type": "coursework report",
                "language": "Chinese",
                "duration_min": 3,
                "slide_count": 1,
                "format": "individual",
                "image_source": "diagram-only",
                "output_prefix": "ai-class-demo",
            },
            "slides": [
                {
                    "id": 1,
                    "title": "AI 帮助我们更快形成初稿",
                    "layout": "process",
                    "content": {"bullets": ["提出想法", "整理结构", "人工修改"]},
                    "visual": {
                        "type": "three-step-process",
                        "purpose": "Show a responsible AI writing workflow",
                    },
                    "note_goal": "Explain AI as support, not replacement",
                    "transition": "接下来说明边界。",
                    "timing_sec": 180,
                    "owner": "A",
                }
            ],
        }

        brief = bridge.build_brief(data, Path("input.yaml"))

        self.assertIn("document-skills", brief)
        self.assertIn("Target skill: `pptx`", brief)
        self.assertIn("pptxgenjs.md", brief)
        self.assertIn("outputs/ai-class-demo-presentation.pptx", brief)
        self.assertIn("AI 帮助我们更快形成初稿", brief)
        self.assertIn("python -m markitdown output.pptx", brief)

    def test_builds_existing_deck_improvement_brief(self) -> None:
        bridge = load_bridge_module()
        data = {
            "meta": {
                "presentation_type": "coursework report",
                "language": "Chinese",
                "duration_min": 5,
                "format": "individual",
                "output_prefix": "improved-demo",
            },
            "source_deck": "original-demo.pptx",
            "edit_intent": "review-fix",
            "preserve": ["course logo", "approved section order"],
            "change_summary_required": True,
            "review_findings": [
                {
                    "severity": "Major",
                    "target": "Slide 2",
                    "problem": "The title is generic.",
                    "fix": "Rewrite it as a claim-style title.",
                }
            ],
            "slides": [
                {
                    "id": 1,
                    "title": "AI 工具只负责加速初稿",
                    "layout": "process",
                    "content": {"bullets": ["输入目标", "生成初稿", "人工修订"]},
                    "visual": {
                        "type": "three-step-process",
                        "purpose": "Show the corrected workflow",
                    },
                    "note_goal": "Explain the improved message",
                    "transition": "接下来说明边界。",
                    "timing_sec": 300,
                    "owner": "A",
                }
            ],
        }

        errors = bridge.validate_spec(
            data,
            ROOT / "references" / "slide-spec.schema.json",
            __import__("jsonschema"),
        )
        brief = bridge.build_brief(data, Path("input.yaml"))

        self.assertEqual([], errors)
        self.assertIn("Existing Deck Improvement Contract", brief)
        self.assertIn("original-demo.pptx", brief)
        self.assertIn("Use `editing.md`", brief)
        self.assertIn("outputs/improved-demo-change-summary.md", brief)
        self.assertIn("Rewrite it as a claim-style title", brief)

    def test_script_writes_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "spec.yaml"
            output_path = Path(tmp) / "brief.md"
            spec_path.write_text(
                """
meta:
  presentation_type: coursework report
  language: Chinese
  duration_min: 3
  slide_count: 1
  format: individual
  image_source: diagram-only
  output_prefix: demo
slides:
  - id: 1
    title: Demo
    layout: title
    content:
      bullets:
        - Point
    visual:
      type: title-card
      purpose: Introduce the topic
    note_goal: Open naturally
    transition: Continue.
    timing_sec: 180
    owner: A
""",
                encoding="utf-8",
            )

            bridge = load_bridge_module()
            exit_code = None
            try:
                with unittest.mock.patch(
                    "sys.argv",
                    ["slide_spec_to_pptx_brief.py", str(spec_path), "--output", str(output_path)],
                ):
                    bridge.main()
            except SystemExit as exc:
                exit_code = exc.code

            self.assertIn(exit_code, (None, 0))
            self.assertTrue(output_path.is_file())
            self.assertIn("outputs/demo-presentation.pptx", output_path.read_text(encoding="utf-8"))

    def test_semantic_validation_rejects_cross_field_mismatches(self) -> None:
        bridge = load_bridge_module()
        data = {
            "meta": {
                "duration_min": 5,
                "slide_count": 3,
                "format": "group",
                "members": ["A", "B"],
            },
            "review_findings": [
                {
                    "severity": "Major",
                    "target": "Slide 1",
                    "problem": "Generic title",
                    "fix": "Use a specific title",
                }
            ],
            "slides": [
                {
                    "id": 2,
                    "title": "First",
                    "layout": "content",
                    "content": "Point",
                    "timing_sec": 20,
                    "owner": "C",
                }
            ],
        }

        errors = bridge.validate_spec(
            data,
            ROOT / "references" / "slide-spec.schema.json",
            __import__("jsonschema"),
        )
        messages = "\n".join(error["message"] for error in errors)

        self.assertIn("contiguous", messages)
        self.assertIn("slide_count", messages)
        self.assertIn("inconsistent with duration_min", messages)
        self.assertIn("not listed in meta.members", messages)
        self.assertIn("source_deck is required", messages)

    def test_schema_rejects_unknown_slide_fields(self) -> None:
        bridge = load_bridge_module()
        data = {
            "slides": [
                {
                    "id": 1,
                    "title": "Demo",
                    "layout": "content",
                    "content": "Point",
                    "timing_sec": 30,
                    "owner": "Individual",
                    "timing_seconds": 30,
                }
            ]
        }

        errors = bridge.validate_spec(
            data,
            ROOT / "references" / "slide-spec.schema.json",
            __import__("jsonschema"),
        )

        self.assertTrue(any("Additional properties" in error["message"] for error in errors))


if __name__ == "__main__":
    unittest.main()
