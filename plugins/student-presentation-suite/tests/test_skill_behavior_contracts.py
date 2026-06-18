from __future__ import annotations

import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillBehaviorContractTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_shared_standards_define_intent_routing(self) -> None:
        text = self.read("references/shared-standards.md")
        self.assertIn("## Intent Routing", text)
        self.assertIn(
            "require both a clear student-owned academic context and an explicit PPT intent",
            text,
        )
        self.assertIn("Use `student-presentation`", text)
        self.assertIn("Use `student-presentation-ppt`", text)
        self.assertIn("Use `student-presentation-review`", text)
        self.assertIn('"PPT 大纲"', text)
        self.assertIn('"帮我优化这个 PPT"', text)

    def test_skill_descriptions_require_student_context_and_ppt_intent(self) -> None:
        expectations = {
            "skills/student-presentation/SKILL.md": (
                "Use only when",
                "student context",
                "PPT/slide outline",
            ),
            "skills/student-presentation-ppt/SKILL.md": (
                "Use only when",
                "student context",
                "PPT, PPTX, PowerPoint, or slide deck",
            ),
            "skills/student-presentation-review/SKILL.md": (
                "Use only when",
                "student context",
                "review, audit, score, or critique",
            ),
        }
        for rel, required_phrases in expectations.items():
            frontmatter = self.read(rel).split("---", 2)[1]
            for phrase in required_phrases:
                self.assertIn(phrase, frontmatter, rel)

    def test_ppt_skill_defines_vague_request_defaults(self) -> None:
        text = self.read("skills/student-presentation-ppt/SKILL.md")
        self.assertIn("Fast default assumptions", text)
        self.assertIn("7-9 slides", text)
        self.assertIn("no web images", text)
        self.assertIn("If an eligible request asks only for \"PPT 大纲\"", text)
        self.assertIn("existing deck improvement", text)
        self.assertIn("change-summary.md", text)
        self.assertIn("show every available direction", text)
        self.assertIn("Do not ask whether an outline is needed first", text)
        self.assertIn("Stable general knowledge may be used", text)

    def test_planning_skill_allows_low_risk_assumptions(self) -> None:
        text = self.read("skills/student-presentation/SKILL.md")
        self.assertIn("state low-risk assumptions and continue", text)
        self.assertIn("Route to `student-presentation-ppt`", text)

    def test_review_skill_does_not_overwrite_original_deck(self) -> None:
        text = self.read("skills/student-presentation-review/SKILL.md")
        self.assertIn("Do not overwrite the original deck", text)
        self.assertIn("Default review depth", text)
        self.assertIn("Do not block the review", text)
        self.assertIn("skills/student-presentation-review/scripts/pptx_static_check.py", text)
        self.assertIn("change-summary.md", text)

    def test_review_output_format_supports_edit_handoff(self) -> None:
        text = self.read("skills/student-presentation-review/references/review-output-format.md")
        self.assertIn("## Edit Plan", text)
        self.assertIn("## Change Summary Handoff", text)
        self.assertIn("student-presentation-ppt", text)

    def test_slide_spec_schema_supports_existing_deck_improvement(self) -> None:
        schema = self.read("references/slide-spec.schema.json")
        guide = self.read("references/slide-spec.md")
        for expected in (
            "source_deck",
            "edit_intent",
            "review_findings",
            "preserve",
            "change_summary_required",
        ):
            self.assertIn(expected, schema)
            self.assertIn(expected, guide)

    def test_claude_brief_uses_plugin_root_for_delivery_check(self) -> None:
        text = self.read("scripts/slide_spec_to_pptx_brief.py")
        self.assertIn("From the plugin package root", text)
        self.assertIn("skills/student-presentation-ppt/scripts/pptx_delivery_check.py", text)
        self.assertIn("Existing Deck Improvement Contract", text)

    def test_codex_manifest_mentions_deck_improvement(self) -> None:
        text = self.read(".codex-plugin/plugin.json")
        self.assertIn("Existing deck improvement with change summaries", text)

    def test_runtime_versions_match(self) -> None:
        codex = json.loads(self.read(".codex-plugin/plugin.json"))
        claude = json.loads(self.read(".claude-plugin/plugin.json"))
        marketplace = json.loads(
            (ROOT.parents[1] / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(claude["version"], codex["version"])
        self.assertEqual(claude["version"], marketplace["plugins"][0]["version"])

    def test_plugin_readmes_use_shared_marketplace_name(self) -> None:
        for rel in ("README.md", "README-zh.md"):
            text = self.read(rel)
            self.assertIn("student-presentation-suite@personal", text)
            self.assertNotIn("student-presentation-suite@student-presentation-suite", text)

    def test_visual_style_menu_lists_every_style(self) -> None:
        menu = self.read("skills/student-presentation-ppt/references/visual-style-menu.md")
        style_dir = ROOT / "skills" / "student-presentation-ppt" / "references" / "visual-styles"
        style_files = sorted(style_dir.glob("*.md"))
        self.assertGreaterEqual(len(style_files), 14)
        for style_file in style_files:
            style_text = style_file.read_text(encoding="utf-8")
            heading = style_text.splitlines()[0].removeprefix("# ")
            english_name = heading.split("（", 1)[0]
            self.assertIn(english_name, menu)
            for control in (
                "**Color roles:**",
                "**Geometry:**",
                "**Slide recipes:**",
                "**Image treatment:**",
                "**Density control:**",
                "**Acceptance checks:**",
            ):
                self.assertIn(control, style_text, f"{style_file.name}: {control}")

    def test_style_menu_defines_executable_application_contract(self) -> None:
        menu = self.read("skills/student-presentation-ppt/references/visual-style-menu.md")
        self.assertIn("## Applying A Style File", menu)
        self.assertIn("palette roles", menu)
        self.assertIn("slide-type recipes", menu)
        self.assertIn("acceptance checks", menu)


if __name__ == "__main__":
    unittest.main()
