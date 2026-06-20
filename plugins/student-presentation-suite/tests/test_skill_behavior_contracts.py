from __future__ import annotations

import json
import importlib.util
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
MARKETPLACE_CHECK = REPO_ROOT / "scripts" / "check_marketplace_release.py"


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1])


def load_marketplace_check():
    spec = importlib.util.spec_from_file_location(
        "check_marketplace_release", MARKETPLACE_CHECK
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SkillBehaviorContractTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_manifest_and_marketplace_are_claude_specific(self) -> None:
        manifest = json.loads(self.read(".claude-plugin/plugin.json"))
        marketplace = json.loads(
            (REPO_ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        entry = marketplace["plugins"][0]
        self.assertEqual("claude-personal", marketplace["name"])
        self.assertEqual("0.3.0", manifest["version"])
        self.assertEqual(manifest["version"], entry["version"])
        self.assertEqual(manifest["name"], entry["name"])
        self.assertIn("document-skills@anthropic-agent-skills", manifest["dependencies"])
        for field in ("homepage", "repository", "license", "keywords"):
            self.assertTrue(manifest[field])
            self.assertTrue(entry[field])
        self.assertFalse((ROOT / ".codex-plugin").exists())
        self.assertFalse(any(ROOT.glob("skills/*/agents/openai.yaml")))

    def test_marketplace_release_accepts_prs_targeting_claude_code(self) -> None:
        check = load_marketplace_check()
        self.assertIsNone(
            check.release_branch_error(
                "codex/claude-plugin-0.3.0",
                "codex/claude-plugin-0.3.0",
                "claude-code",
                "1/merge",
            )
        )
        self.assertIn(
            "must target claude-code",
            check.release_branch_error("feature", "feature", "main", "1/merge"),
        )
        self.assertIsNone(check.release_branch_error("claude-code", "", "", ""))
        self.assertIn(
            "must be released from claude-code",
            check.release_branch_error("main", "", "", ""),
        )

    def test_skill_frontmatter_has_distinct_intents(self) -> None:
        planning = frontmatter(ROOT / "skills/student-presentation/SKILL.md")
        ppt = frontmatter(ROOT / "skills/student-presentation-ppt/SKILL.md")
        review = frontmatter(ROOT / "skills/student-presentation-review/SKILL.md")
        self.assertIn("outline", planning["description"])
        self.assertIn("editable", ppt["description"])
        self.assertIn("review", review["description"])

    def test_runtime_and_output_contracts_are_portable(self) -> None:
        planning = self.read("skills/student-presentation/SKILL.md")
        ppt = self.read("skills/student-presentation-ppt/SKILL.md")
        review = self.read("skills/student-presentation-review/SKILL.md")
        self.assertIn("${CLAUDE_PLUGIN_ROOT}", ppt)
        self.assertIn("${CLAUDE_PROJECT_DIR}", ppt)
        self.assertIn("run_with_pptxgenjs.js", ppt)
        self.assertIn("blocked", ppt)
        self.assertIn("incomplete", ppt)
        self.assertIn("Never write deliverables into `${CLAUDE_PLUGIN_ROOT}`", planning)
        self.assertIn("${CLAUDE_PLUGIN_ROOT}", review)
        self.assertIn("${CLAUDE_PROJECT_DIR}", review)

    def test_cross_skill_handoff_is_deterministic(self) -> None:
        shared = self.read("references/shared-standards.md")
        self.assertIn("Outline-only work never creates", shared)
        self.assertIn("“看看问题” means review only", shared)
        self.assertIn("“直接改好” means review diagnosis followed by PPTX editing", shared)
        review = self.read("skills/student-presentation-review/SKILL.md")
        self.assertIn("diagnose first, then hand off", review)
        self.assertIn("Never overwrite the original deck", review)

    def test_pptx_intake_is_a_hard_gate(self) -> None:
        intake = self.read("references/presentation-intake.md")
        ppt = self.read("skills/student-presentation-ppt/SKILL.md")
        production = self.read(
            "skills/student-presentation-ppt/references/pptx-production.md"
        )
        for field in (
            "Topic",
            "Course/context",
            "Presentation type",
            "Audience",
            "Language",
            "Duration",
            "Slide count",
            "Format",
            "Rubric/required sections",
            "Source material",
            "Template/branding",
            "Image strategy",
            "Visual style",
            "Deliverables",
        ):
            self.assertIn(f"| {field} |", intake)
        self.assertIn("Never ask for a confirmed item again", intake)
        self.assertIn("Do not run environment checks", intake)
        self.assertIn("Delegation does not itself move the state", intake)
        self.assertIn("explicit confirmation", ppt)
        self.assertIn("Do not run environment checks or generation commands", ppt)
        self.assertIn("Do not use this reference to bypass intake", production)

    def test_workflow_states_are_consistent(self) -> None:
        intake = self.read("references/presentation-intake.md")
        ppt = self.read("skills/student-presentation-ppt/SKILL.md")
        states = (
            "intake_pending → intake_confirmed → planned → producing → qa → complete"
        )
        self.assertIn(states, intake)
        self.assertIn(states, ppt)
        for terminal in ("incomplete", "blocked"):
            self.assertIn(terminal, intake)
            self.assertIn(terminal, ppt)

    def test_review_and_outline_use_intake_without_overreaching(self) -> None:
        planning = self.read("skills/student-presentation/SKILL.md")
        review = self.read("skills/student-presentation-review/SKILL.md")
        self.assertIn("outline-only intake mode", planning)
        self.assertIn("review-only intake mode", review)
        self.assertIn("must not modify files", review)
        self.assertIn("full intake and Production Summary confirmation", review)

    def test_skill_files_stay_compact_and_reference_canonical_rules(self) -> None:
        paths = [
            ROOT / "skills/student-presentation/SKILL.md",
            ROOT / "skills/student-presentation-ppt/SKILL.md",
            ROOT / "skills/student-presentation-review/SKILL.md",
        ]
        for path in paths:
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertLessEqual(
                len(lines), 75, f"{path.name} should stay as a compact entrypoint"
            )
            self.assertIn(
                "references/presentation-intake.md",
                path.read_text(encoding="utf-8"),
            )
        shared = self.read("references/shared-standards.md")
        self.assertIn("`presentation-intake.md` owns clarification", shared)
        self.assertNotIn("## Confirmed Constraints", shared)

    def test_style_selection_contract(self) -> None:
        menu = self.read("skills/student-presentation-ppt/references/visual-style-menu.md")
        styles = sorted(
            (ROOT / "skills/student-presentation-ppt/references/visual-styles").glob("*.md")
        )
        self.assertEqual(14, len(styles))
        self.assertIn("three best topic-fit choices", menu)
        self.assertIn("complete 14-style menu only", menu)
        for style in styles:
            heading = style.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
            self.assertIn(heading.split("（", 1)[0], menu)

    def test_six_scenario_examples_exist(self) -> None:
        names = {
            "chinese-coursework.md",
            "english-class-report.md",
            "thesis-defense.md",
            "group-presentation.md",
            "review-only.md",
            "existing-deck-improvement.md",
        }
        self.assertTrue(names.issubset({path.name for path in (ROOT / "examples").glob("*.md")}))

    def test_readmes_use_new_install_id(self) -> None:
        for path in (REPO_ROOT / "README.md", REPO_ROOT / "README-zh.md", ROOT / "README.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("student-presentation-suite@claude-personal", text)
            self.assertNotIn("student-presentation-suite@personal", text)

    def test_install_script_has_safe_migration_contract(self) -> None:
        script = (REPO_ROOT / "scripts/install_claude_plugin.ps1").read_text(encoding="utf-8")
        self.assertIn("$Marketplace = \"claude-personal\"", script)
        self.assertIn("$OldPluginId = \"$Plugin@personal\"", script)
        self.assertIn("plugin marketplace remove personal", script)
        self.assertIn("Remove-PluginCache -MarketplaceName \"personal\"", script)
        self.assertNotIn("Remove-Item -LiteralPath $InstallRoot", script)

    def test_review_edit_handoff_requires_separate_outputs(self) -> None:
        review = self.read("skills/student-presentation-review/SKILL.md")
        ppt = self.read("skills/student-presentation-ppt/SKILL.md")
        self.assertIn("diagnose first, then hand off", review)
        self.assertIn("separate improved deck and change summary", review)
        self.assertIn("Do not overwrite an existing source deck", ppt)


if __name__ == "__main__":
    unittest.main()
