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
import struct
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))


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
        "--allow-missing-notes",
        action="store_true",
        help="Do not require a notes file; use only when notes are embedded or explicitly out of scope",
    )
    parser.add_argument(
        "--allow-missing-preview",
        action="store_true",
        help="Do not require a preview/contact sheet; visual QA must then be reported as incomplete",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 2 when required files are missing or delivery artifacts are invalid",
    )
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit 3 when blocker-like static risks remain",
    )
    return parser.parse_args()


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def inspect_pptx_package(path: Path) -> dict[str, Any]:
    required_parts = {
        "[Content_Types].xml",
        "_rels/.rels",
        "ppt/presentation.xml",
        "ppt/_rels/presentation.xml.rels",
    }
    try:
        with zipfile.ZipFile(path) as zf:
            corrupt_member = zf.testzip()
            names = set(zf.namelist())
            slide_names = [
                n
                for n in names
                if n.startswith("ppt/slides/slide") and n.endswith(".xml")
            ]
            notes_names = [
                n
                for n in names
                if n.startswith("ppt/notesSlides/notesSlide") and n.endswith(".xml")
            ]
            missing_parts = sorted(required_parts - names)
            errors = []
            if corrupt_member:
                errors.append(f"corrupt ZIP member: {corrupt_member}")
            if missing_parts:
                errors.append("missing package parts: " + ", ".join(missing_parts))
            if not slide_names:
                errors.append("presentation contains no slide XML parts")
            return {
                "valid": not errors,
                "errors": errors,
                "slide_count": len(sorted(slide_names, key=slide_number)),
                "embedded_notes_count": len(notes_names),
            }
    except (FileNotFoundError, PermissionError, OSError, zipfile.BadZipFile) as exc:
        return {
            "valid": False,
            "errors": [str(exc)],
            "slide_count": None,
            "embedded_notes_count": 0,
        }



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

def preview_info(path: Path) -> dict[str, Any]:
    info = file_info(path) or {"path": str(path), "exists": False, "size_bytes": None}
    info.update({"valid": False, "format": None, "width": None, "height": None})
    if not info["exists"]:
        return info
    try:
        data = path.read_bytes()
        if len(data) < 8:
            info["error"] = "preview file is empty or truncated"
            return info
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            if len(data) < 24 or data[12:16] != b"IHDR":
                info["error"] = "invalid PNG header"
                return info
            width, height = struct.unpack(">II", data[16:24])
            info.update(
                {"valid": width > 0 and height > 0, "format": "png", "width": width, "height": height}
            )
            return info
        if data.startswith(b"%PDF-"):
            info.update({"valid": len(data) > 16, "format": "pdf"})
            if not info["valid"]:
                info["error"] = "invalid PDF preview"
            return info
        if data.startswith(b"\xff\xd8"):
            index = 2
            while index + 9 < len(data):
                if data[index] != 0xFF:
                    index += 1
                    continue
                marker = data[index + 1]
                index += 2
                if marker in {0xD8, 0xD9}:
                    continue
                if index + 2 > len(data):
                    break
                segment_length = int.from_bytes(data[index : index + 2], "big")
                if marker in range(0xC0, 0xC4) and index + 7 < len(data):
                    height = int.from_bytes(data[index + 3 : index + 5], "big")
                    width = int.from_bytes(data[index + 5 : index + 7], "big")
                    info.update(
                        {
                            "valid": width > 0 and height > 0,
                            "format": "jpeg",
                            "width": width,
                            "height": height,
                        }
                    )
                    return info
                index += max(segment_length, 2)
            info["error"] = "invalid JPEG preview"
            return info
        info["error"] = "unsupported or invalid preview format"
    except (OSError, struct.error) as exc:
        info["error"] = str(exc)
    return info


def expected_notes_path(pptx: Path) -> Path:
    stem = pptx.stem
    prefix = stem[: -len("-presentation")] if stem.endswith("-presentation") else stem
    return pptx.with_name(f"{prefix}-speaker-notes.md")


def expected_preview_paths(pptx: Path) -> list[Path]:
    stem = pptx.stem
    prefix = stem[: -len("-presentation")] if stem.endswith("-presentation") else stem
    parent = pptx.parent
    discovered = sorted(
        {
            *parent.glob(f"{prefix}*preview*.png"),
            *parent.glob(f"{prefix}*contact*.png"),
            *parent.glob(f"{prefix}*preview*.pdf"),
            *parent.glob(f"{prefix}*contact*.pdf"),
        }
    )
    return discovered or [parent / f"{prefix}-preview.png"]



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


def inspect_delivery(
    pptx: Path,
    notes: Path | None,
    previews: list[Path],
    *,
    require_notes: bool = True,
    require_preview: bool = True,
) -> dict[str, Any]:
    if require_notes and notes is None:
        notes = expected_notes_path(pptx)
    if require_preview and not previews:
        previews = expected_preview_paths(pptx)
    pptx_info = file_info(pptx)
    package = inspect_pptx_package(pptx)
    preview_infos = [preview_info(path) for path in previews]
    missing = []
    fatal_issues = []
    if not pptx_info or not pptx_info["exists"]:
        missing.append("pptx")
    elif not package["valid"]:
        fatal_issues.append("pptx-invalid")
    embedded_notes_count = package["embedded_notes_count"]
    if require_notes and embedded_notes_count == 0 and (notes is None or not notes.is_file()):
        missing.append("notes")
    if require_preview and not any(info and info["valid"] for info in preview_infos):
        missing.append("preview")
        if any(info and info["exists"] for info in preview_infos):
            fatal_issues.append("preview-invalid")

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
        if static_result.get("error"):
            fatal_issues.append("pptx-scan-failed")

    return {
        "pptx": pptx_info,
        "notes": file_info(notes),
        "previews": preview_infos,
        "package_integrity": package,
        "slide_count": package["slide_count"],
        "embedded_notes_count": embedded_notes_count,
        "static_xml_risk_summary": static_summary,
        "missing_expected_files": missing,
        "fatal_issues": sorted(set(fatal_issues)),
        "requirements": {
            "notes_required": require_notes,
            "preview_required": require_preview,
        },
        "note": (
            "Delivery check verifies package integrity, files, preview headers, and PPTX XML. "
            "Human or visual-model inspection of rendered slides is still required for visual QA."
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
    package = result["package_integrity"]
    print(
        f"PPTX package: valid={package['valid']} "
        f"errors={json.dumps(package['errors'], ensure_ascii=False)}"
    )
    print(f"Slide count: {result['slide_count']}")
    print(f"Embedded notes: {result['embedded_notes_count']}")
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
    if result["fatal_issues"]:
        print("Fatal delivery issues: " + ", ".join(result["fatal_issues"]))


def determine_exit_code(
    result: dict[str, Any],
    *,
    strict: bool,
    fail_on_blockers: bool,
) -> int:
    if strict and (result["missing_expected_files"] or result["fatal_issues"]):
        return 2
    blocker_count = result["static_xml_risk_summary"].get("blocker_like_count") or 0
    if fail_on_blockers and blocker_count:
        return 3
    return 0


def main() -> None:
    args = parse_args()
    result = inspect_delivery(
        args.pptx,
        args.notes,
        args.preview,
        require_notes=not args.allow_missing_notes,
        require_preview=not args.allow_missing_preview,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    exit_code = determine_exit_code(
        result,
        strict=args.strict,
        fail_on_blockers=args.fail_on_blockers,
    )
    if exit_code:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
