from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillBehaviorContractTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_shared_standards_define_intent_routing(self) -> None:
        text = self.read("references/shared-standards.md")
        self.assertIn("## Intent Routing", text)
        self.assertIn("Use `student-presentation`", text)
        self.assertIn("Use `student-presentation-ppt`", text)
        self.assertIn("Use `student-presentation-review`", text)
        self.assertIn('"PPT 大纲"', text)
        self.assertIn('"帮我优化这个 PPT"', text)

    def test_ppt_skill_defines_vague_request_defaults(self) -> None:
        text = self.read("skills/student-presentation-ppt/SKILL.md")
        self.assertIn("Fast default assumptions", text)
        self.assertIn("7-9 slides", text)
        self.assertIn("no web images", text)
        self.assertIn("If the user asks only for \"PPT 大纲\"", text)
        self.assertIn("existing deck improvement", text)
        self.assertIn("change-summary.md", text)

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

    def test_claude_brief_uses_plugin_root_for_delivery_check(self) -> None:
        text = self.read("scripts/slide_spec_to_pptx_brief.py")
        self.assertIn("From the plugin package root", text)
        self.assertIn("skills/student-presentation-ppt/scripts/pptx_delivery_check.py", text)

    def test_codex_manifest_mentions_deck_improvement(self) -> None:
        text = self.read(".codex-plugin/plugin.json")
        self.assertIn("Existing deck improvement with change summaries", text)


if __name__ == "__main__":
    unittest.main()
