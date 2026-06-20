from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = (
    "student-presentation",
    "student-presentation-ppt",
    "student-presentation-review",
)


class SkillBehaviorContractTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_suite_contract_defines_scope_routing_and_ownership(self) -> None:
        text = self.read("references/suite-contract.md")
        for expected in (
            "## Supported Scope",
            "student-owned academic",
            "## Out of Scope",
            "standalone speech, script, Q&A",
            "business, sales, company, teacher-training",
            "student-presentation-ppt",
            "student-presentation-review",
            "## Decision Authority",
            "The original deck is never overwritten",
            "## Ownership",
        ):
            self.assertIn(expected, text)

    def test_shared_standards_delegate_scope_to_suite_contract(self) -> None:
        text = self.read("references/shared-standards.md")
        self.assertIn("suite-contract.md", text)
        self.assertNotIn("## Intent Routing", text)

    def test_routing_case_matrix_covers_boundaries_and_gate_states(self) -> None:
        cases = yaml.safe_load(self.read("tests/fixtures/routing-cases.yaml"))["cases"]
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
        self.assertTrue(any("teacher" in prompt for prompt in none_prompts))
        self.assertTrue(any("上传" in prompt for prompt in none_prompts))
        gate_states = {
            case.get("decision_gate")
            for case in cases
            if case["expected"] == "student-presentation-ppt"
        }
        self.assertTrue({"required", "resolved", "delegated"}.issubset(gate_states))

    def test_skill_frontmatter_uses_strict_student_academic_scope(self) -> None:
        expectations = {
            "student-presentation": ("student academic context", "PPT/slide outline"),
            "student-presentation-ppt": (
                "student academic context",
                "actual PPT/PPTX/PowerPoint deck",
            ),
            "student-presentation-review": (
                "student academic context",
                "review, audit, score, compare, or critique",
            ),
        }
        for skill_name, phrases in expectations.items():
            frontmatter = self.read(f"skills/{skill_name}/SKILL.md").split("---", 2)[1]
            for phrase in phrases:
                self.assertIn(phrase, frontmatter, skill_name)

    def test_skill_entrypoints_stay_within_line_budget(self) -> None:
        for skill_name in SKILL_NAMES:
            lines = self.read(f"skills/{skill_name}/SKILL.md").splitlines()
            self.assertLessEqual(len(lines), 65, skill_name)

    def test_planning_skill_keeps_scripts_and_qa_supporting_only(self) -> None:
        text = self.read("skills/student-presentation/SKILL.md")
        self.assertIn("standalone scripts/Q&A", text)
        self.assertIn("Q&A attached to the eligible PPT", text)
        self.assertIn("hand off to `student-presentation-ppt`", text)

    def test_ppt_skill_enforces_runtime_and_decision_gate(self) -> None:
        text = self.read("skills/student-presentation-ppt/SKILL.md")
        for expected in (
            "mandatory Decision Gate",
            "before creating a slide plan or PPTX",
            "requires Codex `Presentations`",
            "never substitute a Markdown outline",
            "change-summary.md",
            "references/pptx-production.md",
        ):
            self.assertIn(expected, text)

    def test_decision_gate_is_option_based_and_blocking(self) -> None:
        text = self.read("skills/student-presentation-ppt/references/pptx-production.md")
        for expected in (
            "## Mandatory Decision Gate",
            "1–3 highest-impact questions",
            "2–4 mutually exclusive",
            "topic-specific options",
            "(Recommended)",
            "impact or tradeoff",
            "Wait for the user's choices",
            "Do not create the slide plan",
            "Production assumptions",
            "does not waive the gate",
        ):
            self.assertIn(expected, text)

    def test_decision_gate_covers_high_impact_decisions_and_density_options(self) -> None:
        text = self.read("skills/student-presentation-ppt/references/pptx-production.md")
        for expected in (
            "presentation type, purpose, and expected conclusion",
            "audience, course, rubric, and grading emphasis",
            "duration or target slide count",
            "content scope and required sections",
            "visual direction or school template",
            "source material, data, image assets",
            "Standard 8–9 slides (Recommended)",
            "Concise 6–7 slides",
            "Detailed 10–11 slides",
        ):
            self.assertIn(expected, text)

    def test_review_skill_requires_explicit_edit_authorization(self) -> None:
        text = self.read("skills/student-presentation-review/SKILL.md")
        self.assertIn("explicitly requests file modification", text)
        self.assertIn("Never overwrite the source", text)
        self.assertIn("skills/student-presentation-review/scripts/pptx_static_check.py", text)
        self.assertIn("change summary", text)

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

    def test_slide_spec_supports_existing_deck_improvement(self) -> None:
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

    def test_manifest_and_readmes_match_decision_gated_scope(self) -> None:
        manifest = json.loads(self.read(".codex-plugin/plugin.json"))
        prompts = manifest["interface"]["defaultPrompt"]
        self.assertEqual(3, len(prompts))
        self.assertTrue(any("大纲" in prompt for prompt in prompts))
        self.assertTrue(any("PPTX" in prompt for prompt in prompts))
        self.assertTrue(any("审查" in prompt for prompt in prompts))
        self.assertIn(
            "Decision-gated editable PPTX creation and improvement",
            manifest["interface"]["capabilities"],
        )
        for rel in ("README.md", "README-zh.md"):
            text = self.read(rel)
            self.assertIn(".codex-plugin/plugin.json", text)
            self.assertIn("artifact-tool", text)
            self.assertIn("Decision Gate", text)

    def test_codex_package_is_runtime_specific(self) -> None:
        self.assertFalse((ROOT / ".claude-plugin").exists())
        self.assertFalse((ROOT / "scripts/check_claude_pptx_env.py").exists())

    def test_agent_metadata_invokes_matching_skill(self) -> None:
        for skill_name in SKILL_NAMES:
            data = yaml.safe_load(
                self.read(f"skills/{skill_name}/agents/openai.yaml")
            )
            self.assertIn(f"${skill_name}", data["interface"]["default_prompt"])
            self.assertNotIn("dependencies", data)

    def test_markdown_references_resolve(self) -> None:
        pattern = re.compile(r"`([^`\n]+\.(?:md|json|py|yaml|yml))`")
        for path in ROOT.rglob("*.md"):
            for ref in pattern.findall(path.read_text(encoding="utf-8")):
                if (
                    "<" in ref
                    or ">" in ref
                    or " " in ref
                    or ref.startswith(("http://", "https://", "outputs/", "path/to/"))
                ):
                    continue
                self.assertTrue(
                    (path.parent / ref).exists() or (ROOT / ref).exists(),
                    f"{path.relative_to(ROOT)} -> {ref}",
                )

    def test_visual_style_menu_lists_every_style_and_control(self) -> None:
        menu = self.read("skills/student-presentation-ppt/references/visual-style-menu.md")
        style_dir = ROOT / "skills/student-presentation-ppt/references/visual-styles"
        style_files = sorted(style_dir.glob("*.md"))
        self.assertGreaterEqual(len(style_files), 14)
        for style_file in style_files:
            style_text = style_file.read_text(encoding="utf-8")
            heading = style_text.splitlines()[0].removeprefix("# ")
            self.assertIn(heading.split("（", 1)[0], menu)
            for control in (
                "**Color roles:**",
                "**Geometry:**",
                "**Slide recipes:**",
                "**Image treatment:**",
                "**Density control:**",
                "**Acceptance checks:**",
            ):
                self.assertIn(control, style_text, f"{style_file.name}: {control}")
        self.assertIn("## Applying A Style File", menu)
        self.assertIn("acceptance checks", menu)


if __name__ == "__main__":
    unittest.main()
