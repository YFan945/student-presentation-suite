#!/usr/bin/env python3
"""Validate the Codex-only marketplace layout."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Codex marketplace release structure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()

def load_utf8_json(path: Path, label: str, errors: list[str]) -> dict | None:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        errors.append(f"Cannot read {label}: {exc}")
        return None
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{label} must be UTF-8 without BOM")
        return None
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label} must contain valid UTF-8 JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label} must contain a JSON object")
        return None
    return payload


def main() -> None:
    args = parse_args()
    errors: list[str] = []
    required = [
        ".agents/plugins/marketplace.json",
        "plugins/student-presentation-suite/.codex-plugin/plugin.json",
        "README.md",
        "README-zh.md",
        ".github/workflows/validate.yml",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required file: {rel}")
    if (ROOT / ".claude-plugin").exists():
        errors.append("Codex marketplace root must not contain .claude-plugin")
    if (ROOT / "claude-plugins").exists():
        errors.append("Claude plugins must live outside the Codex marketplace root")
    marketplace = load_utf8_json(MARKETPLACE_PATH, "marketplace.json", errors)
    if marketplace is not None:
        if marketplace.get("name") != "personal":
            errors.append("Codex marketplace name must be personal")
        if marketplace.get("interface", {}).get("displayName") != "Personal":
            errors.append("Codex marketplace interface.displayName must be Personal")
        entries = marketplace.get("plugins")
        if not isinstance(entries, list) or not entries:
            errors.append("Codex marketplace must publish at least one plugin")
            entries = []
        names = [
            entry.get("name")
            for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("name"), str)
        ]
        duplicate_names = sorted({name for name in names if names.count(name) > 1})
        if duplicate_names:
            errors.append(
                "Codex marketplace contains duplicate plugin names: "
                + ", ".join(duplicate_names)
            )
        for index, entry in enumerate(entries):
            label = f"plugins[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{label} must be an object")
                continue
            name = entry.get("name")
            source = entry.get("source", {})
            if not isinstance(name, str) or not name:
                errors.append(f"{label}.name must be a non-empty string")
                continue
            if not isinstance(source, dict) or source.get("source") != "local":
                errors.append(f"{label}.source.source must be local")
                continue
            source_path = source.get("path")
            if not isinstance(source_path, str) or not source_path.startswith("./plugins/"):
                errors.append(f"{label}.source.path must use ./plugins/<name>")
                continue
            plugin_root = (ROOT / source_path).resolve()
            if not plugin_root.is_relative_to(ROOT.resolve()) or not plugin_root.is_dir():
                errors.append(f"{label}.source.path does not resolve to a plugin directory")
                continue
            manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
            manifest = load_utf8_json(
                manifest_path,
                f"{name} plugin.json",
                errors,
            )
            if manifest is not None and manifest.get("name") != name:
                errors.append(f"{label}.name must match plugin.json name")
            if entry.get("policy") != {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            }:
                errors.append(f"{label}.policy must use AVAILABLE/ON_INSTALL")
            if not isinstance(entry.get("category"), str) or not entry["category"]:
                errors.append(f"{label}.category must be a non-empty string")

    for rel in ("README.md", "README-zh.md", "AGENTS.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        for required_text in (
            ".agents/plugins/marketplace.json",
            "--marketplace-path .agents/plugins/marketplace.json",
        ):
            if required_text not in text:
                errors.append(f"{rel} missing repository marketplace instruction: {required_text}")
    for rel in ("README.md", "README-zh.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "codex plugin marketplace add" not in text:
            errors.append(f"{rel} missing explicit marketplace registration command")
    result = {"ok": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Codex marketplace release check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print("Codex marketplace release check passed.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
