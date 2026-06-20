#!/usr/bin/env python3
"""Validate the standalone Codex plugin package."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = (
    "student-presentation",
    "student-presentation-ppt",
    "student-presentation-review",
)
MAX_SKILL_LINES = 65
ACTIVE_RUNTIME_PATHS = [ROOT / ".codex-plugin", ROOT / "skills", ROOT / "references"]
REQUIRED_FILES = [
    ".codex-plugin/plugin.json",
    "README.md",
    "README-zh.md",
    "requirements.txt",
    "assets/composer-icon.svg",
    "assets/logo.svg",
    "references/suite-contract.md",
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def check_structure(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")
    for rel in FORBIDDEN_PATHS:
        if (ROOT / rel).exists():
            errors.append(f"Claude-only path must not exist in Codex plugin: {rel}")


def check_manifest(errors: list[str]) -> None:
    try:
        manifest = json.loads(read(".codex-plugin/plugin.json"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Codex manifest JSON parse failed: {exc}")
        return
    if manifest.get("name") != "student-presentation-suite":
        errors.append("Codex manifest name must be student-presentation-suite")
    if manifest.get("author", {}).get("name") in {None, "", "Local developer"}:
        errors.append("Codex manifest author.name must be publishable")
    interface = manifest.get("interface", {})
    capabilities = interface.get("capabilities", [])
    for expected in (
        "Decision-gated editable PPTX creation and improvement",
        "Static PPTX inspection and review-to-edit change summaries",
    ):
        if expected not in capabilities:
            errors.append(f"Codex manifest missing capability: {expected}")
    if any("Claude" in str(item) or "document-skills" in str(item) for item in capabilities):
        errors.append("Codex manifest must not advertise Claude Code capabilities")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append("Codex manifest interface.defaultPrompt must contain 1-3 prompts")
    elif any(not isinstance(prompt, str) or not prompt.strip() for prompt in prompts):
        errors.append("Codex manifest starter prompts must be non-empty strings")
    elif any(len(prompt) > 128 for prompt in prompts):
        errors.append("Codex manifest starter prompts must be at most 128 characters")
    if len(str(interface.get("longDescription", ""))) > 500:
        errors.append("Codex manifest longDescription should stay under 500 characters")
    if len(capabilities) > 10:
        errors.append("Codex manifest capabilities should stay concise (10 or fewer)")


def check_agent_metadata(errors: list[str]) -> None:
    for skill_name in SKILL_NAMES:
        rel = f"skills/{skill_name}/agents/openai.yaml"
        try:
            data = yaml.safe_load(read(rel))
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"Cannot read Codex agent metadata for {skill_name}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"Codex agent metadata for {skill_name} must be an object")
            continue
        prompt = data.get("interface", {}).get("default_prompt", "")
        if f"${skill_name}" not in prompt:
            errors.append(f"Codex agent default_prompt must invoke ${skill_name}")
        if data.get("dependencies"):
            errors.append(f"Codex agent metadata for {skill_name} must not declare dependencies")


def check_skill_size(errors: list[str]) -> None:
    for skill_name in SKILL_NAMES:
        rel = f"skills/{skill_name}/SKILL.md"
        line_count = len(read(rel).splitlines())
        if line_count > MAX_SKILL_LINES:
            errors.append(f"{rel} has {line_count} lines; maximum is {MAX_SKILL_LINES}")


def check_behavior(errors: list[str]) -> None:
    schema = read("references/slide-spec.schema.json")
    guide = read("references/slide-spec.md")
    for expected in (
        "source_deck",
        "edit_intent",
        "review_findings",
        "preserve",
        "change_summary_required",
    ):
        if expected not in schema or expected not in guide:
            errors.append(f"Slide Spec contract missing field: {expected}")

    ppt_skill = read("skills/student-presentation-ppt/SKILL.md")
    for expected in (
        "Artifact-tool",
        "preview/contact sheet",
        "change-summary.md",
        "Presentations",
        "missing prerequisite",
        "never substitute a Markdown outline",
        "mandatory Decision Gate",
    ):
        if expected not in ppt_skill:
            errors.append(f"Codex PPT skill missing workflow contract: {expected}")

    production = read("skills/student-presentation-ppt/references/pptx-production.md")
    for expected in (
        "Presentations",
        "imagegen",
        "1–3 highest-impact questions",
        "2–4 mutually exclusive",
        "(Recommended)",
        "Wait for the user's choices",
        "Do not create the slide plan",
        "Production assumptions",
    ):
        if expected not in production:
            errors.append(f"PPT Decision Gate/runtime contract missing: {expected}")


def check_scope_consistency(errors: list[str]) -> None:
    contract = read("references/suite-contract.md")
    for expected in (
        "student-owned academic",
        "Supporting outputs such as speaker notes, scripts, transitions, Q&A",
        "generic presentation planning",
        "business, sales, company, teacher-training",
        "Decision Gate",
        "The original deck is never overwritten",
    ):
        if expected not in contract:
            errors.append(f"Suite contract missing boundary: {expected}")

    scope_files = [
        "README.md",
        "README-zh.md",
        ".codex-plugin/plugin.json",
        *(f"skills/{name}/SKILL.md" for name in SKILL_NAMES),
        *(f"skills/{name}/agents/openai.yaml" for name in SKILL_NAMES),
    ]
    for rel in scope_files:
        text = read(rel)
        if not any(token in text for token in ("student academic", "学生学术", "student-owned academic")):
            errors.append(f"Scope file must state the student academic boundary: {rel}")

    if "standalone scripts/Q&A" not in read("skills/student-presentation/SKILL.md"):
        errors.append("Planning skill must reject standalone scripts/Q&A")
    if "edit files only when explicitly authorized" not in read(
        "skills/student-presentation-review/SKILL.md"
    ):
        errors.append("Review skill must require explicit file-edit authorization")


def check_markdown_references(errors: list[str]) -> None:
    pattern = re.compile(r"`([^`\n]+\.(?:md|json|py|yaml|yml))`")
    for path in ROOT.rglob("*.md"):
        for ref in pattern.findall(path.read_text(encoding="utf-8")):
            ref = ref.strip()
            if (
                "<" in ref
                or ">" in ref
                or " " in ref
                or ref.startswith(("http://", "https://", "outputs/", "path/to/"))
            ):
                continue
            if not ((path.parent / ref).exists() or (ROOT / ref).exists()):
                errors.append(f"Broken Markdown reference in {path.relative_to(ROOT)}: {ref}")


def check_runtime_boundaries(errors: list[str]) -> None:
    forbidden_tokens = (
        ".claude-plugin",
        "document-skills",
        "pptxgenjs",
        "check_claude_pptx_env.py",
        "slide_spec_to_pptx_brief.py",
    )
    for root in ACTIVE_RUNTIME_PATHS:
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
                        "Active Codex runtime file contains forbidden Claude production token: "
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
    check_agent_metadata(errors)
    check_skill_size(errors)
    check_behavior(errors)
    check_scope_consistency(errors)
    check_markdown_references(errors)
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
