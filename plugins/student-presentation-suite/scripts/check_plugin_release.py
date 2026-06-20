#!/usr/bin/env python3
"""Validate the standalone Codex plugin package."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_RUNTIME_PATHS = [
    ROOT / ".codex-plugin",
    ROOT / "skills",
    ROOT / "references",
]
REQUIRED_FILES = [
    ".codex-plugin/plugin.json",
    "README.md",
    "README-zh.md",
    "requirements.txt",
    "assets/composer-icon.svg",
    "assets/logo.svg",
    "skills/student-presentation/SKILL.md",
    "skills/student-presentation-ppt/SKILL.md",
    "skills/student-presentation-review/SKILL.md",
    "skills/student-presentation/agents/openai.yaml",
    "skills/student-presentation-ppt/agents/openai.yaml",
    "skills/student-presentation-review/agents/openai.yaml",
    "scripts/validate_slide_spec.py",
    "tests/test_pptx_static_core.py",
    "tests/test_pptx_delivery_check.py",
    "tests/test_slide_spec_validation.py",
    "tests/test_skill_behavior_contracts.py",
    "tests/fixtures/routing-cases.yaml",
    "examples/ai-learning-report.yaml",
]
FORBIDDEN_PATHS = [
    ".claude-plugin",
    "requirements-claude-pptx.txt",
    "package.json",
    "package-lock.json",
    "scripts/check_claude_pptx_env.py",
    "scripts/slide_spec_to_pptx_brief.py",
]
FORBIDDEN_DIR_NAMES = {".pytest_cache", "__pycache__", "node_modules"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check standalone Codex plugin structure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def check_structure(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")
    for rel in FORBIDDEN_PATHS:
        if (ROOT / rel).exists():
            errors.append(f"Claude-only path must not exist in Codex plugin: {rel}")


def check_manifest(errors: list[str]) -> None:
    path = ROOT / ".codex-plugin" / "plugin.json"
    if not path.is_file():
        return
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Codex manifest JSON parse failed: {exc}")
        return
    if manifest.get("name") != "student-presentation-suite":
        errors.append("Codex manifest name must be student-presentation-suite")
    if manifest.get("author", {}).get("name") in {None, "", "Local developer"}:
        errors.append("Codex manifest author.name must be publishable")
    capabilities = manifest.get("interface", {}).get("capabilities", [])
    for expected in (
        "Editable PPTX creation and existing-deck improvement",
        "Static PPTX inspection and change summaries",
    ):
        if expected not in capabilities:
            errors.append(f"Codex manifest missing capability: {expected}")
    if any("Claude" in str(item) or "document-skills" in str(item) for item in capabilities):
        errors.append("Codex manifest must not advertise Claude Code capabilities")
    interface = manifest.get("interface", {})
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append("Codex manifest interface.defaultPrompt must contain 1-3 starter prompts")
    elif any(not isinstance(prompt, str) or not prompt.strip() for prompt in prompts):
        errors.append("Codex manifest starter prompts must be non-empty strings")
    elif any(len(prompt) > 128 for prompt in prompts):
        errors.append("Codex manifest starter prompts must be at most 128 characters")
    if len(str(interface.get("longDescription", ""))) > 500:
        errors.append("Codex manifest longDescription should stay under 500 characters")
    if len(capabilities) > 10:
        errors.append("Codex manifest capabilities should stay concise (10 or fewer)")


def check_codex_agent_metadata(errors: list[str]) -> None:
    for skill_name in (
        "student-presentation",
        "student-presentation-ppt",
        "student-presentation-review",
    ):
        path = ROOT / "skills" / skill_name / "agents" / "openai.yaml"
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"Cannot read Codex agent metadata for {skill_name}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"Codex agent metadata for {skill_name} must be an object")
            continue
        default_prompt = data.get("interface", {}).get("default_prompt", "")
        if f"${skill_name}" not in default_prompt:
            errors.append(
                f"Codex agent default_prompt must explicitly invoke ${skill_name}"
            )
        dependencies = data.get("dependencies")
        if dependencies:
            errors.append(
                f"Codex agent metadata for {skill_name} must not declare non-MCP tool dependencies"
            )


def check_behavior(errors: list[str]) -> None:
    schema = (ROOT / "references/slide-spec.schema.json").read_text(encoding="utf-8")
    guide = (ROOT / "references/slide-spec.md").read_text(encoding="utf-8")
    ppt_skill = (ROOT / "skills/student-presentation-ppt/SKILL.md").read_text(encoding="utf-8")
    for expected in (
        "source_deck",
        "edit_intent",
        "review_findings",
        "preserve",
        "change_summary_required",
    ):
        if expected not in schema or expected not in guide:
            errors.append(f"Slide Spec contract missing field: {expected}")
    for expected in ("artifact-tool", "preview/contact sheet", "change-summary.md"):
        if expected not in ppt_skill:
            errors.append(f"Codex PPT skill missing workflow detail: {expected}")
    for expected in (
        "Presentations",
        "missing prerequisite",
        "must not fall back to a text outline",
    ):
        if expected not in ppt_skill:
            errors.append(f"Codex PPT skill missing runtime contract: {expected}")
    production_guide = (
        ROOT / "skills/student-presentation-ppt/references/pptx-production.md"
    ).read_text(encoding="utf-8")
    if "Presentations" not in production_guide or "imagegen" not in production_guide:
        errors.append("Codex PPT production guide must define Presentations/imagegen behavior")


def check_runtime_boundaries(errors: list[str]) -> None:
    forbidden_tokens = (
        ".claude-plugin",
        "document-skills",
        "pptxgenjs",
        "check_claude_pptx_env.py",
        "slide_spec_to_pptx_brief.py",
    )
    for root in ACTIVE_RUNTIME_PATHS:
        if not root.exists():
            continue
        files = [root] if root.is_file() else root.rglob("*")
        for path in files:
            if not path.is_file() or path.suffix.lower() not in {
                ".md",
                ".json",
                ".yaml",
                ".yml",
                ".py",
            }:
                continue
            text = path.read_text(encoding="utf-8")
            for token in forbidden_tokens:
                if token in text:
                    errors.append(
                        f"Active Codex runtime file contains forbidden Claude production token: "
                        f"{path.relative_to(ROOT)} ({token})"
                    )


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
    check_codex_agent_metadata(errors)
    check_behavior(errors)
    check_runtime_boundaries(errors)
    check_tracked_files(errors)
    result = {"ok": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Codex plugin release check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Codex plugin release check passed.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
