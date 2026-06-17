#!/usr/bin/env python3
"""Check local tools expected by Claude document-skills/pptx production."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


COMMON_SOFFICE_PATHS = [
    Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
    Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
]
ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Claude document-skills/pptx environment")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when required tools are missing",
    )
    return parser.parse_args()


def command_path(name: str, extra_paths: list[Path] | None = None) -> str | None:
    if os.name == "nt" and not Path(name).suffix:
        for suffix in (".cmd", ".exe", ".bat"):
            found_with_suffix = shutil.which(name + suffix)
            if found_with_suffix:
                return found_with_suffix
    found = shutil.which(name)
    if found:
        return found
    for path in extra_paths or []:
        if path.is_file():
            return str(path)
    return None


def python_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def run_probe(command: list[str]) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    output = (proc.stdout or proc.stderr or "").strip()
    return proc.returncode == 0, output


def check_pptxgenjs() -> dict[str, Any]:
    node = command_path("node")
    npm = command_path("npm")
    if not node:
        return {
            "ok": False,
            "method": "node",
            "detail": "node is not available; cannot load pptxgenjs",
        }
    resolve_script = (
        "console.log(require.resolve('pptxgenjs', "
        f"{{ paths: [{json.dumps(str(ROOT))}] }}))"
    )
    ok, output = run_probe([node, "-e", resolve_script])
    if ok:
        return {
            "ok": True,
            "method": "node require.resolve with plugin root",
            "detail": output,
        }
    result: dict[str, Any] = {
        "ok": False,
        "method": "node require.resolve with plugin root",
        "detail": output,
        "warning": (
            "pptxgenjs must be resolvable from the plugin root by the Node process "
            "that builds the deck. Run `npm install --prefix plugins/student-presentation-suite` "
            "from the repository root. A global npm install alone is not treated as sufficient."
        ),
    }
    if npm:
        ok_global, global_output = run_probe([npm, "list", "-g", "pptxgenjs", "--depth=0"])
        result["global_installed"] = ok_global
        result["global_detail"] = global_output
        if not output:
            result["detail"] = global_output
        return result
    result["detail"] = output or "npm is not available for a global package check"
    return result


def inspect_environment() -> dict[str, Any]:
    checks = {
        "node": {"ok": command_path("node") is not None, "path": command_path("node")},
        "npm": {"ok": command_path("npm") is not None, "path": command_path("npm")},
        "pptxgenjs": check_pptxgenjs(),
        "markitdown": {"ok": python_module("markitdown"), "module": "markitdown"},
        "Pillow": {"ok": python_module("PIL"), "module": "PIL"},
        "LibreOffice": {
            "ok": command_path("soffice", COMMON_SOFFICE_PATHS) is not None,
            "path": command_path("soffice", COMMON_SOFFICE_PATHS),
        },
        "Poppler pdftoppm": {
            "ok": command_path("pdftoppm") is not None,
            "path": command_path("pdftoppm"),
        },
        "jsonschema": {"ok": python_module("jsonschema"), "module": "jsonschema"},
        "PyYAML": {"ok": python_module("yaml"), "module": "yaml"},
    }
    required = ["node", "pptxgenjs", "markitdown", "Pillow", "LibreOffice", "Poppler pdftoppm"]
    missing_required = [name for name in required if not checks[name]["ok"]]
    return {
        "ok": not missing_required,
        "missing_required": missing_required,
        "checks": checks,
        "note": (
            "Missing required tools do not break the student planning/review skills, "
            "but Claude document-skills/pptx generation or rendered QA will degrade."
        ),
    }


def print_text(result: dict[str, Any]) -> None:
    print(result["note"])
    for name, check in result["checks"].items():
        status = "ok" if check["ok"] else "missing"
        detail = check.get("path") or check.get("module") or check.get("detail") or ""
        print(f"{name}: {status} {detail}".rstrip())
    if result["missing_required"]:
        print("Missing required: " + ", ".join(result["missing_required"]))


def main() -> None:
    args = parse_args()
    result = inspect_environment()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    if args.strict and result["missing_required"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
