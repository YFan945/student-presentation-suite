#!/usr/bin/env python3
"""Check repository structure before publishing the plugin to GitHub."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    "README.md",
    "README-zh.md",
    "requirements.txt",
    "requirements-claude-pptx.txt",
    "package.json",
    "package-lock.json",
    "skills/student-presentation/SKILL.md",
    "skills/student-presentation-ppt/SKILL.md",
    "skills/student-presentation-review/SKILL.md",
    "skills/student-presentation-ppt/agents/openai.yaml",
    "scripts/check_claude_pptx_env.py",
    "scripts/slide_spec_to_pptx_brief.py",
    "scripts/validate_slide_spec.py",
    "tests/test_pptx_static_core.py",
    "tests/test_slide_spec_bridge.py",
    "tests/test_skill_behavior_contracts.py",
]


FORBIDDEN_DIR_NAMES = {".pytest_cache", "__pycache__"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check GitHub-ready plugin structure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_required_files(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")
    for rel in ("marketplace.json", ".claude-plugin/marketplace.json"):
        if (ROOT / rel).exists():
            errors.append(
                f"Do not publish local marketplace file inside the single-plugin repository: {rel}"
            )


def check_manifests(errors: list[str]) -> None:
    codex_path = ROOT / ".codex-plugin" / "plugin.json"
    claude_path = ROOT / ".claude-plugin" / "plugin.json"
    if not codex_path.is_file() or not claude_path.is_file():
        return
    try:
        codex = read_json(codex_path)
        claude = read_json(claude_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Manifest JSON parse failed: {exc}")
        return

    if codex.get("name") != "student-presentation-suite":
        errors.append(".codex-plugin/plugin.json name must be student-presentation-suite")
    if claude.get("name") != "student-presentation-suite":
        errors.append(".claude-plugin/plugin.json name must be student-presentation-suite")

    capabilities = codex.get("interface", {}).get("capabilities", [])
    if "Codex PPTX production uses the default Presentations skill/artifact-tool workflow" not in capabilities:
        errors.append("Codex manifest must explicitly preserve the default Presentations/artifact-tool workflow")
    if "Uses document-skills pptx skill for Claude Code PPTX production" not in capabilities:
        errors.append("Codex manifest should document the Claude Code document-skills route")
    if "Existing deck improvement with change summaries" not in capabilities:
        errors.append("Codex manifest should document existing deck improvement with change summaries")

    dependencies = claude.get("dependencies", [])
    if "document-skills" not in dependencies:
        errors.append("Claude manifest must depend on document-skills")


def check_codex_agent_dependencies(errors: list[str]) -> None:
    text = (ROOT / "skills" / "student-presentation-ppt" / "agents" / "openai.yaml").read_text(
        encoding="utf-8"
    )
    for item in ("Presentations", "artifact-tool", "imagegen"):
        if f'- "{item}"' not in text:
            errors.append(f"Codex PPT agent dependency missing: {item}")
    if "document-skills" in text:
        errors.append("Codex agent dependency file must not depend on document-skills")


def check_docs(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README-zh.md").read_text(encoding="utf-8")
    for label, text in (("README.md", readme), ("README-zh.md", readme_zh)):
        for expected in (
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
            "document-skills",
            "requirements-claude-pptx.txt",
            "npm install",
            "student-presentation-ppt",
        ):
            if expected not in text:
                errors.append(f"{label} missing install/compatibility detail: {expected}")
    if "Presentations" not in readme or "artifact-tool" not in readme:
        errors.append("README.md must mention Codex Presentations/artifact-tool compatibility")
    if "Presentations" not in readme_zh or "artifact-tool" not in readme_zh:
        errors.append("README-zh.md must mention Codex Presentations/artifact-tool compatibility")


def check_behavior_contracts(errors: list[str]) -> None:
    schema = (ROOT / "references" / "slide-spec.schema.json").read_text(encoding="utf-8")
    slide_spec = (ROOT / "references" / "slide-spec.md").read_text(encoding="utf-8")
    bridge = (ROOT / "scripts" / "slide_spec_to_pptx_brief.py").read_text(encoding="utf-8")
    review_format = (
        ROOT / "skills" / "student-presentation-review" / "references" / "review-output-format.md"
    ).read_text(encoding="utf-8")
    for expected in (
        "source_deck",
        "edit_intent",
        "review_findings",
        "preserve",
        "change_summary_required",
    ):
        if expected not in schema:
            errors.append(f"Slide Spec schema missing existing-deck improvement field: {expected}")
        if expected not in slide_spec:
            errors.append(f"Slide Spec docs missing existing-deck improvement field: {expected}")
    for expected in ("Existing Deck Improvement Contract", "outputs/{output_prefix}-change-summary.md"):
        if expected not in bridge:
            errors.append(f"Slide Spec bridge missing improvement handoff detail: {expected}")
    for expected in ("## Edit Plan", "## Change Summary Handoff", "student-presentation-ppt"):
        if expected not in review_format:
            errors.append(f"Review output format missing edit handoff detail: {expected}")


def check_forbidden_tracked_files(errors: list[str]) -> None:
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return
    if proc.returncode != 0:
        return
    for rel in proc.stdout.splitlines():
        parts = Path(rel).parts
        if any(part in FORBIDDEN_DIR_NAMES for part in parts) or rel.endswith(".pyc"):
            errors.append(f"Generated cache file is tracked by git: {rel}")


def main() -> None:
    args = parse_args()
    errors: list[str] = []
    check_required_files(errors)
    check_manifests(errors)
    check_codex_agent_dependencies(errors)
    check_docs(errors)
    check_behavior_contracts(errors)
    check_forbidden_tracked_files(errors)

    result = {"ok": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Plugin release check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Plugin release check passed.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
