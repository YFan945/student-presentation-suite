#!/usr/bin/env python3
"""Validate the standalone Claude Code plugin release package."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
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
    "scripts/run_with_pptxgenjs.js",
    "scripts/smoke_pptx.py",
    "scripts/slide_spec_to_pptx_brief.py",
    "scripts/validate_slide_spec.py",
    "tests/test_runtime_paths.py",
]
FORBIDDEN_PATH_PARTS = {".codex-plugin", "agents", "__pycache__", ".pytest_cache", "node_modules"}
FORBIDDEN_SUFFIXES = {".pyc", ".pptx", ".png"}
REQUIRED_METADATA = ("homepage", "repository", "license", "keywords")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check standalone Claude Code plugin structure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def run_git(*args: str) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "git failed").strip())
    return proc.stdout.splitlines()


def tracked_files(errors: list[str]) -> list[str]:
    try:
        return run_git("ls-files")
    except RuntimeError as exc:
        errors.append(f"Cannot inspect tracked files: {exc}")
        return []


def check_structure(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")


def check_manifest(errors: list[str]) -> None:
    try:
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Manifest/package JSON parse failed: {exc}")
        return
    if manifest.get("name") != "student-presentation-suite":
        errors.append("Claude manifest name must be student-presentation-suite")
    if manifest.get("version") != "0.2.0" or package.get("version") != manifest.get("version"):
        errors.append("Claude manifest and package.json versions must both be 0.2.0")
    if manifest.get("author", {}).get("name") in {None, "", "Local developer"}:
        errors.append("Claude manifest author.name must be publishable")
    if "document-skills@anthropic-agent-skills" not in manifest.get("dependencies", []):
        errors.append("Claude manifest must depend on document-skills@anthropic-agent-skills")
    for field in REQUIRED_METADATA:
        if not manifest.get(field):
            errors.append(f"Claude manifest missing metadata: {field}")
    if len(manifest.get("keywords", [])) < 5:
        errors.append("Claude manifest should provide at least five keywords")


def check_runtime_contract(errors: list[str]) -> None:
    combined = "\n".join(
        (ROOT / rel).read_text(encoding="utf-8")
        for rel in (
            "skills/student-presentation-ppt/SKILL.md",
            "skills/student-presentation-review/SKILL.md",
            "skills/student-presentation-ppt/references/pptx-production.md",
        )
    )
    for expected in (
        "${CLAUDE_PLUGIN_ROOT}",
        "${CLAUDE_PROJECT_DIR}",
        "document-skills@anthropic-agent-skills",
        "run_with_pptxgenjs.js",
        "blocked",
        "incomplete",
    ):
        if expected not in combined:
            errors.append(f"Claude runtime contract missing: {expected}")
    for forbidden in ("artifact-tool", "Presentations` skill", "agents/openai.yaml"):
        if forbidden in combined:
            errors.append(f"Claude runtime instructions contain Codex-only text: {forbidden}")


def check_tracked_files(errors: list[str]) -> None:
    files = tracked_files(errors)
    folded: dict[str, str] = {}
    for rel in files:
        path = Path(rel)
        if not rel.startswith("plugins/student-presentation-suite/"):
            continue
        local = rel.removeprefix("plugins/student-presentation-suite/")
        local_path = Path(local)
        if any(part in FORBIDDEN_PATH_PARTS for part in local_path.parts):
            errors.append(f"Forbidden generated or Codex path is tracked: {local}")
        if local_path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"Generated artifact is tracked: {local}")
        key = local.casefold()
        if key in folded and folded[key] != local:
            errors.append(f"Case-colliding tracked paths: {folded[key]} and {local}")
        folded[key] = local
        disk_path = ROOT / local
        if disk_path.is_file() and disk_path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"UTF-8 BOM is not allowed: {local}")


def main() -> None:
    args = parse_args()
    errors: list[str] = []
    check_structure(errors)
    check_manifest(errors)
    check_runtime_contract(errors)
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
