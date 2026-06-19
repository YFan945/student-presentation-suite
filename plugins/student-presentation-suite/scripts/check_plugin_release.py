#!/usr/bin/env python3
"""Validate the standalone Claude Code plugin package."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
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
    "scripts/check_claude_pptx_env.py",
    "scripts/slide_spec_to_pptx_brief.py",
    "scripts/validate_slide_spec.py",
    "tests/test_pptx_static_core.py",
    "tests/test_pptx_delivery_check.py",
    "tests/test_slide_spec_bridge.py",
    "tests/test_skill_behavior_contracts.py",
]
FORBIDDEN_PATHS = [
    ".codex-plugin",
    "skills/student-presentation/agents/openai.yaml",
    "skills/student-presentation-ppt/agents/openai.yaml",
    "skills/student-presentation-review/agents/openai.yaml",
]
FORBIDDEN_DIR_NAMES = {".pytest_cache", "__pycache__", "node_modules"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check standalone Claude Code plugin structure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def check_structure(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")
    for rel in FORBIDDEN_PATHS:
        if (ROOT / rel).exists():
            errors.append(f"Codex-only path must not exist in Claude plugin: {rel}")


def check_manifest(errors: list[str]) -> None:
    path = ROOT / ".claude-plugin" / "plugin.json"
    if not path.is_file():
        return
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Claude manifest JSON parse failed: {exc}")
        return
    if manifest.get("name") != "student-presentation-suite":
        errors.append("Claude manifest name must be student-presentation-suite")
    if manifest.get("author", {}).get("name") in {None, "", "Local developer"}:
        errors.append("Claude manifest author.name must be publishable")
    if "document-skills@anthropic-agent-skills" not in manifest.get("dependencies", []):
        errors.append("Claude manifest must depend on document-skills@anthropic-agent-skills")


def check_behavior(errors: list[str]) -> None:
    schema = (ROOT / "references/slide-spec.schema.json").read_text(encoding="utf-8")
    bridge = (ROOT / "scripts/slide_spec_to_pptx_brief.py").read_text(encoding="utf-8")
    ppt_skill = (ROOT / "skills/student-presentation-ppt/SKILL.md").read_text(encoding="utf-8")
    for expected in (
        "source_deck",
        "edit_intent",
        "review_findings",
        "preserve",
        "change_summary_required",
    ):
        if expected not in schema:
            errors.append(f"Slide Spec schema missing field: {expected}")
    for expected in ("Existing Deck Improvement Contract", "outputs/{output_prefix}-change-summary.md"):
        if expected not in bridge:
            errors.append(f"Claude Slide Spec bridge missing detail: {expected}")
    for expected in (
        "document-skills@anthropic-agent-skills",
        "check_claude_pptx_env.py",
        "slide_spec_to_pptx_brief.py",
        "markitdown",
    ):
        if expected not in ppt_skill:
            errors.append(f"Claude PPT skill missing workflow detail: {expected}")
    if "artifact-tool" in ppt_skill or "Presentations` skill" in ppt_skill:
        errors.append("Claude PPT skill still contains Codex production instructions")


def check_tracked_files(errors: list[str]) -> None:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if proc.returncode != 0:
        return
    for rel in proc.stdout.splitlines():
        if any(part in FORBIDDEN_DIR_NAMES for part in Path(rel).parts) or rel.endswith(".pyc"):
            errors.append(f"Generated cache file is tracked by git: {rel}")


def main() -> None:
    args = parse_args()
    errors: list[str] = []
    check_structure(errors)
    check_manifest(errors)
    check_behavior(errors)
    check_tracked_files(errors)
    result = {"ok": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Claude Code plugin release check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Claude Code plugin release check passed.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
