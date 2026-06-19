#!/usr/bin/env python3
"""Validate the Claude Code-only marketplace layout."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "student-presentation-suite"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Claude Code marketplace structure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    errors: list[str] = []
    required = [
        ".claude-plugin/marketplace.json",
        "plugins/student-presentation-suite/.claude-plugin/plugin.json",
        "README.md",
        "README-zh.md",
        ".github/workflows/validate.yml",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")
    if (ROOT / ".agents").exists():
        errors.append("Claude marketplace root must not contain Codex .agents metadata")
    try:
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
        )
        entry = marketplace["plugins"][0]
        if marketplace.get("name") != "personal":
            errors.append("Claude marketplace name must be personal")
        if entry.get("name") != manifest.get("name"):
            errors.append("Claude marketplace and manifest names must match")
        if entry.get("source") != "./plugins/student-presentation-suite":
            errors.append("Claude marketplace source path is incorrect")
        if entry.get("version") != manifest.get("version"):
            errors.append("Claude marketplace and manifest versions must match")
        if (PLUGIN_ROOT / ".codex-plugin").exists():
            errors.append("Claude plugin must not contain .codex-plugin")
    except (OSError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        errors.append(f"Cannot validate Claude marketplace JSON: {exc}")
    result = {"ok": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Claude marketplace release check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Claude marketplace release check passed.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
