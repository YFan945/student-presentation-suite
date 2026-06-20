from __future__ import annotations

import unittest
import json
import subprocess
import sys
from pathlib import Path

import yaml


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

    def test_routing_case_matrix_covers_required_boundaries(self) -> None:
        payload = yaml.safe_load(self.read("tests/fixtures/routing-cases.yaml"))
        cases = payload["cases"]
        expected = {case["expected"] for case in cases}
        self.assertTrue(
            {
                "student-presentation",
                "student-presentation-ppt",
                "student-presentation-review",
                "review-then-student-presentation-ppt",
                "none",
            }.issubset(expected)
        )
        self.assertTrue({"zh", "en"}.issubset({case["language"] for case in cases}))
        none_prompts = [case["prompt"] for case in cases if case["expected"] == "none"]
        self.assertTrue(any("公司" in prompt for prompt in none_prompts))
        self.assertTrue(any("uploaded" in prompt or "上传" in prompt for prompt in none_prompts))

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

    def test_ppt_skill_delegates_defaults_and_qa_to_reference(self) -> None:
        text = self.read("skills/student-presentation-ppt/SKILL.md")
        self.assertIn("If an eligible request asks only for \"PPT 大纲\"", text)
        self.assertIn("existing deck improvement", text)
        self.assertIn("change-summary.md", text)
        self.assertIn("requires the Codex `Presentations` capability", text)
        self.assertIn("must not fall back to a text outline", text)
        self.assertIn("references/pptx-production.md", text)
        self.assertNotIn("Fast default assumptions:", text)

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

    def test_review_checker_cli_can_import_shared_package(self) -> None:
        script = ROOT / "skills/student-presentation-review/scripts/pptx_static_check.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)

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

    def test_codex_manifest_mentions_deck_improvement(self) -> None:
        manifest = json.loads(self.read(".codex-plugin/plugin.json"))
        prompts = manifest["interface"]["defaultPrompt"]
        self.assertEqual(3, len(prompts))
        self.assertTrue(any("大纲" in prompt for prompt in prompts))
        self.assertTrue(any("PPTX" in prompt for prompt in prompts))
        self.assertTrue(any("审查" in prompt for prompt in prompts))

    def test_codex_package_is_runtime_specific(self) -> None:
        codex = json.loads(self.read(".codex-plugin/plugin.json"))
        self.assertEqual("student-presentation-suite", codex["name"])
        self.assertFalse((ROOT / ".claude-plugin").exists())
        self.assertFalse((ROOT / "scripts/check_claude_pptx_env.py").exists())

    def test_plugin_readmes_document_codex_only_runtime(self) -> None:
        for rel in ("README.md", "README-zh.md"):
            text = self.read(rel)
            self.assertIn(".codex-plugin/plugin.json", text)
            self.assertIn("artifact-tool", text)

    def test_codex_agent_metadata_uses_skill_invocation_prompts(self) -> None:
        for skill_name in (
            "student-presentation",
            "student-presentation-ppt",
            "student-presentation-review",
        ):
            data = yaml.safe_load(
                self.read(f"skills/{skill_name}/agents/openai.yaml")
            )
            self.assertIn(
                f"${skill_name}",
                data["interface"]["default_prompt"],
            )
            self.assertNotIn("dependencies", data)

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
