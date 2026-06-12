#!/usr/bin/env python3
"""Check expected PPTX delivery files for student presentation generation.

This script verifies file existence, counts slides from PPTX XML, and can include
static XML risk findings from the review checker. It does not render slides, so
preview/contact-sheet review is still required for visual QA.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check PPTX delivery package")
    parser.add_argument("--pptx", type=Path, required=True, help="Generated PPTX path")
    parser.add_argument("--notes", type=Path, help="Speaker notes Markdown path")
    parser.add_argument(
        "--preview",
        type=Path,
        action="append",
        default=[],
        help="Preview image, contact sheet, or exported PDF path; repeatable",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when required PPTX, notes, or preview files are missing",
    )
    return parser.parse_args()


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def count_slides(path: Path) -> tuple[int | None, str | None]:
    try:
        with zipfile.ZipFile(path) as zf:
            slide_names = [
                n
                for n in zf.namelist()
                if n.startswith("ppt/slides/slide") and n.endswith(".xml")
            ]
            return len(sorted(slide_names, key=slide_number)), None
    except (FileNotFoundError, zipfile.BadZipFile, KeyError) as exc:
        return None, str(exc)


def load_static_checker() -> Any | None:
    script = Path(__file__).resolve().parents[2] / "student-presentation-review"
    script = script / "scripts" / "pptx_static_check.py"
    if not script.is_file():
        return None
    spec = importlib.util.spec_from_file_location("pptx_static_check", script)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_info(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    exists = path.is_file()
    return {
        "path": str(path),
        "exists": exists,
        "size_bytes": path.stat().st_size if exists else None,
    }


def inspect_delivery(pptx: Path, notes: Path | None, previews: list[Path]) -> dict[str, Any]:
    pptx_info = file_info(pptx)
    slide_count, slide_error = count_slides(pptx)
    preview_infos = [file_info(path) for path in previews]
    missing = []
    if not pptx_info or not pptx_info["exists"]:
        missing.append("pptx")
    if notes is not None and not notes.is_file():
        missing.append("notes")
    if previews and any(info and not info["exists"] for info in preview_infos):
        missing.append("preview")

    static_summary: dict[str, Any] = {
        "available": False,
        "finding_count": None,
        "error": None,
    }
    checker = load_static_checker()
    if checker is not None and pptx.is_file():
        static_result = checker.inspect_pptx(pptx)
        static_summary = {
            "available": True,
            "finding_count": len(static_result.get("findings", [])),
            "error": static_result.get("error"),
            "note": static_result.get("note"),
        }

    return {
        "pptx": pptx_info,
        "notes": file_info(notes),
        "previews": preview_infos,
        "slide_count": slide_count,
        "slide_count_error": slide_error,
        "static_xml_risk_summary": static_summary,
        "missing_expected_files": missing,
        "note": (
            "Delivery check verifies files and PPTX XML only. Rendered preview or "
            "contact-sheet review is still required for visual QA."
        ),
    }


def print_text(result: dict[str, Any]) -> None:
    pptx = result["pptx"]
    print(result["note"])
    print(f"PPTX: {pptx['path']} exists={pptx['exists']} size={pptx['size_bytes']}")
    notes = result.get("notes")
    if notes is not None:
        print(f"Notes: {notes['path']} exists={notes['exists']} size={notes['size_bytes']}")
    for idx, preview in enumerate(result.get("previews", []), start=1):
        print(
            f"Preview {idx}: {preview['path']} exists={preview['exists']} "
            f"size={preview['size_bytes']}"
        )
    print(f"Slide count: {result['slide_count']}")
    if result["slide_count_error"]:
        print(f"Slide count error: {result['slide_count_error']}")
    static = result["static_xml_risk_summary"]
    print(
        "Static XML risks: "
        f"available={static['available']} count={static['finding_count']} error={static['error']}"
    )
    if result["missing_expected_files"]:
        print("Missing expected files: " + ", ".join(result["missing_expected_files"]))


def main() -> None:
    args = parse_args()
    result = inspect_delivery(args.pptx, args.notes, args.preview)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    if args.strict and result["missing_expected_files"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
