#!/usr/bin/env python3
"""Check expected PPTX delivery files for student presentation generation.

This script verifies file existence, counts slides from PPTX XML, and can include
static XML risk findings from the review checker. It does not render slides, so
preview/contact-sheet review is still required for visual QA.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
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
    except (FileNotFoundError, PermissionError, OSError, zipfile.BadZipFile, KeyError) as exc:
        return None, str(exc)



def _load_inspect_pptx():
    from shared._import_helpers import load_inspect_pptx  # noqa: PLC0415
    return load_inspect_pptx(__file__)


def file_info(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    try:
        exists = path.is_file()
        size = path.stat().st_size if exists else None
        error = None
    except (PermissionError, OSError) as exc:
        exists = False
        size = None
        error = str(exc)
    return {
        "path": str(path),
        "exists": exists,
        "size_bytes": size,
        "error": error,
    }



def summarize_static_risks(static_result: dict[str, Any]) -> dict[str, Any]:
    findings = static_result.get("findings", []) if isinstance(static_result, dict) else []
    risk_counter: Counter[str] = Counter()
    acceptable_minor_counter: Counter[str] = Counter()
    blocker_like: list[dict[str, Any]] = []
    minor_markers = (
        "footer",
        "page",
        "slide",
        "source",
        "caption",
        "kicker",
        "eyebrow",
        "页码",
        "来源",
        "注释",
    )
    blocker_risks = {
        "high-text-density-overflow-risk",
        "paragraph-heavy-slide-text",
        "heading-font-size-below-24pt",
        "font-size-not-explicit",
    }
    for item in findings:
        risks = item.get("risk", []) or []
        text_preview = str(item.get("text_preview", ""))
        lower_preview = text_preview.lower()
        min_font = item.get("min_font_pt")
        char_count = item.get("char_count") or 0
        looks_minor = (
            char_count <= 24
            and min_font is not None
            and min_font >= 10
            and any(marker in lower_preview or marker in text_preview for marker in minor_markers)
        )
        for risk in risks:
            risk_counter[risk] += 1
            if looks_minor and risk in {"font-size-below-20pt", "chinese-font-size-below-22pt", "small-text-box-risk"}:
                acceptable_minor_counter[risk] += 1
        if any(risk in blocker_risks for risk in risks) and not looks_minor:
            blocker_like.append(
                {
                    "slide": item.get("slide"),
                    "shape": item.get("shape"),
                    "text_preview": text_preview[:80],
                    "risk": risks,
                    "min_font_pt": min_font,
                }
            )
    return {
        "risk_breakdown": dict(sorted(risk_counter.items())),
        "acceptable_minor_risk_breakdown": dict(sorted(acceptable_minor_counter.items())),
        "blocker_like_count": len(blocker_like),
        "blocker_like_examples": blocker_like[:10],
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
    if pptx_info and pptx_info["exists"]:
        static_result = _load_inspect_pptx()(pptx)
        static_summary = {
            "available": True,
            "finding_count": len(static_result.get("findings", [])),
            "error": static_result.get("error"),
            "note": static_result.get("note"),
            **summarize_static_risks(static_result),
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
    if static.get("risk_breakdown"):
        print("Risk breakdown: " + json.dumps(static["risk_breakdown"], ensure_ascii=False, sort_keys=True))
    if static.get("acceptable_minor_risk_breakdown"):
        print(
            "Acceptable minor risk breakdown: "
            + json.dumps(static["acceptable_minor_risk_breakdown"], ensure_ascii=False, sort_keys=True)
        )
    if static.get("blocker_like_count") is not None:
        print(f"Blocker-like static risks: {static['blocker_like_count']}")
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
