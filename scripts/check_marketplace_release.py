#!/usr/bin/env python3
"""Check the repository-level shared marketplace structure before publishing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check marketplace repository release structure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Cannot read JSON {path.relative_to(ROOT)}: {exc}")
        return None


def check_required_paths(errors: list[str]) -> None:
    required = [
        "README.md",
        "README-zh.md",
        "LICENSE",
        ".gitignore",
        ".claude-plugin/marketplace.json",
        ".github/workflows/validate.yml",
        "plugins/student-presentation-suite/.codex-plugin/plugin.json",
        "plugins/student-presentation-suite/.claude-plugin/plugin.json",
        "plugins/student-presentation-suite/README.md",
        "plugins/student-presentation-suite/README-zh.md",
        "plugins/student-presentation-suite/requirements-claude-pptx.txt",
        "plugins/student-presentation-suite/package.json",
        "plugins/student-presentation-suite/package-lock.json",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required repository file: {rel}")


def check_shared_marketplace(errors: list[str]) -> None:
    path = ROOT / ".claude-plugin" / "marketplace.json"
    data = load_json(path, errors)
    if data is None:
        return
    if data.get("name") != "personal":
        errors.append("Shared marketplace name must be lowercase personal")
    owner = data.get("owner", {})
    if owner.get("name") in {None, "", "Local developer"}:
        errors.append("Shared marketplace owner.name must be a publishable owner name")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("Shared marketplace must include a non-empty plugins array")
        return
    names = {item.get("name") for item in plugins if isinstance(item, dict)}
    if names != {"student-presentation-suite"}:
        errors.append(f"Shared marketplace should publish only student-presentation-suite, got {sorted(names)}")
    for item in plugins:
        if not isinstance(item, dict):
            errors.append("Shared marketplace plugin entry must be an object")
            continue
        source = item.get("source")
        if source != "./plugins/student-presentation-suite":
            errors.append(f"Shared marketplace source should be ./plugins/student-presentation-suite, got {source}")
        elif not (ROOT / source).is_dir():
            errors.append(f"Shared marketplace source path does not exist: {source}")


def check_readmes(errors: list[str]) -> None:
    root_en = (ROOT / "README.md").read_text(encoding="utf-8")
    root_zh = (ROOT / "README-zh.md").read_text(encoding="utf-8")
    plugin_en = (ROOT / "plugins/student-presentation-suite/README.md").read_text(encoding="utf-8")
    plugin_zh = (ROOT / "plugins/student-presentation-suite/README-zh.md").read_text(encoding="utf-8")
    for label, text in (
        ("README.md", root_en),
        ("README-zh.md", root_zh),
        ("plugins/student-presentation-suite/README.md", plugin_en),
        ("plugins/student-presentation-suite/README-zh.md", plugin_zh),
    ):
        if "C:\\Users\\28603" in text:
            errors.append(f"{label} contains a machine-specific absolute path")
    if "[中文](README-zh.md) | English" not in root_en:
        errors.append("Root README.md missing zh/en switch")
    if "中文 | [English](README.md)" not in root_zh:
        errors.append("Root README-zh.md missing zh/en switch")
    if "[中文](README-zh.md) | English" not in plugin_en:
        errors.append("Plugin README.md missing zh/en switch")
    if "中文 | [English](README.md)" not in plugin_zh:
        errors.append("Plugin README-zh.md missing zh/en switch")
    for label, text in (("README.md", root_en), ("README-zh.md", root_zh)):
        for expected in (
            ".claude-plugin/marketplace.json",
            "plugins/student-presentation-suite",
            "codex plugin marketplace add",
            "codex plugin add student-presentation-suite@personal",
            "claude plugin marketplace add",
            "claude plugin install student-presentation-suite@personal",
            "Claude Code",
            "OpenCode",
        ):
            if expected not in text:
                errors.append(f"{label} missing repository usage detail: {expected}")
    for label, text in (
        ("plugins/student-presentation-suite/README.md", plugin_en),
        ("plugins/student-presentation-suite/README-zh.md", plugin_zh),
    ):
        for expected in (
            "document-skills@anthropic-agent-skills",
            "student-presentation-suite@student-presentation-suite",
            "check_claude_pptx_env.py --json",
        ):
            if expected not in text:
                errors.append(f"{label} missing plugin runtime detail: {expected}")


def main() -> None:
    args = parse_args()
    errors: list[str] = []
    check_required_paths(errors)
    check_shared_marketplace(errors)
    check_readmes(errors)
    result = {"ok": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Marketplace release check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Marketplace release check passed.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
