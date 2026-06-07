#!/usr/bin/env python3
"""Static PPTX checks for student presentation review.

This script inspects PPTX XML and reports risk signals. It cannot prove true
rendered overflow or classroom readability; use its findings as review evidence.

Windows usage:
    python skills/student-presentation-review/scripts/pptx_static_check.py deck.pptx --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}

# Office Open XML uses EMU for shape sizes.
# 1 inch = 914400 EMU, 1 cm ~= 360000 EMU.
EMU_PER_CM = 360_000
SMALL_TEXT_BOX_WIDTH_EMU = 900_000  # about 2.5 cm
SMALL_TEXT_BOX_HEIGHT_EMU = 250_000  # about 0.7 cm
TEXT_CHARS_PER_CM_LIMIT = 18  # rough visible characters per cm of text-box width
CHINESE_PARAGRAPH_LIMIT = 160
LATIN_PARAGRAPH_LIMIT = 220
HEADING_PLACEHOLDER_TYPES = {"title", "ctrTitle", "subTitle"}
HEADING_NAME_HINTS = ("title", "subtitle", "heading", "header", "标题", "副标题")


def text_of(el: ET.Element) -> str:
    parts = []
    for t in el.findall(".//a:t", NS):
        if t.text:
            parts.append(t.text)
    return "".join(parts).strip()


def pptx_size_to_pt(sz: str | None) -> float | None:
    if sz and sz.isdigit():
        return int(sz) / 100
    return None


def font_sizes(el: ET.Element) -> list[float]:
    """Return effective run font sizes.

    For each a:r text run, use explicit a:rPr/@sz first. Fall back to the
    paragraph a:defRPr/@sz only when that run has no explicit size.
    """
    sizes: list[float] = []
    for paragraph in el.findall(".//a:p", NS):
        default_size = None
        def_rpr = paragraph.find("./a:pPr/a:defRPr", NS)
        if def_rpr is not None:
            default_size = pptx_size_to_pt(def_rpr.attrib.get("sz"))
        for run in paragraph.findall("./a:r", NS):
            run_size = None
            rpr = run.find("./a:rPr", NS)
            if rpr is not None:
                run_size = pptx_size_to_pt(rpr.attrib.get("sz"))
            effective_size = run_size if run_size is not None else default_size
            if effective_size is not None:
                sizes.append(effective_size)
    return sizes


def shape_bounds(el: ET.Element) -> dict[str, int] | None:
    off = el.find(".//a:xfrm/a:off", NS)
    ext = el.find(".//a:xfrm/a:ext", NS)
    if off is None or ext is None:
        return None
    try:
        return {
            "x": int(off.attrib.get("x", "0")),
            "y": int(off.attrib.get("y", "0")),
            "cx": int(ext.attrib.get("cx", "0")),
            "cy": int(ext.attrib.get("cy", "0")),
        }
    except ValueError:
        return None


def is_heading_shape(el: ET.Element) -> bool:
    ph = el.find("./p:nvSpPr/p:nvPr/p:ph", NS)
    if ph is not None and ph.attrib.get("type") in HEADING_PLACEHOLDER_TYPES:
        return True
    c_nv_pr = el.find("./p:nvSpPr/p:cNvPr", NS)
    name = (c_nv_pr.attrib.get("name", "") if c_nv_pr is not None else "").lower()
    return any(hint.lower() in name for hint in HEADING_NAME_HINTS)


def fill_colors(el: ET.Element) -> list[str]:
    colors = []
    for srgb in el.findall(".//a:srgbClr", NS):
        val = srgb.attrib.get("val")
        if val:
            colors.append(val.upper())
    return colors


def has_cjk(text: str) -> bool:
    for ch in text:
        cp = ord(ch)
        if (
            0x4E00 <= cp <= 0x9FFF  # CJK Unified
            or 0x3400 <= cp <= 0x4DBF  # CJK Ext-A
            or 0x3000 <= cp <= 0x303F  # CJK punctuation
            or 0xFF00 <= cp <= 0xFFEF  # Fullwidth forms
        ):
            return True
    return False


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def inspect_pptx(path: Path) -> dict:
    findings = []
    try:
        with zipfile.ZipFile(path) as zf:
            slide_names = sorted(
                [n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")],
                key=slide_number,
            )
            for slide_name in slide_names:
                slide_id = slide_number(slide_name)
                root = ET.fromstring(zf.read(slide_name))
                for idx, shape in enumerate(root.findall(".//p:sp", NS), start=1):
                    txt = text_of(shape)
                    if not txt:
                        continue
                    sizes = font_sizes(shape)
                    min_size = min(sizes) if sizes else None
                    bounds = shape_bounds(shape)
                    chars = len(txt)
                    is_cjk = has_cjk(txt)
                    heading = is_heading_shape(shape)
                    risk = []
                    if min_size is None:
                        risk.append("font-size-not-explicit")
                    elif min_size < 20:
                        risk.append("font-size-below-20pt")
                    elif is_cjk and min_size < 22:
                        risk.append("chinese-font-size-below-22pt")
                    if heading and min_size is not None and min_size < 24:
                        risk.append("heading-font-size-below-24pt")
                    if bounds:
                        width_cm = max(bounds["cx"] / EMU_PER_CM, 0.1)
                        chars_per_cm = chars / width_cm
                        if chars_per_cm > TEXT_CHARS_PER_CM_LIMIT:
                            risk.append("high-text-density-overflow-risk")
                        if bounds["cx"] < SMALL_TEXT_BOX_WIDTH_EMU or bounds["cy"] < SMALL_TEXT_BOX_HEIGHT_EMU:
                            risk.append("small-text-box-risk")
                    paragraph_limit = CHINESE_PARAGRAPH_LIMIT if is_cjk else LATIN_PARAGRAPH_LIMIT
                    if chars > paragraph_limit:
                        risk.append("paragraph-heavy-slide-text")
                    colors = fill_colors(shape)
                    if len(set(colors)) >= 6:
                        risk.append("many-colors-in-shape")
                    if risk:
                        findings.append(
                            {
                                "slide": slide_id,
                                "shape": idx,
                                "text_preview": txt[:80],
                                "min_font_pt": min_size,
                                "char_count": chars,
                                "detected_cjk": is_cjk,
                                "heading_shape": heading,
                                "bounds": bounds,
                                "risk": risk,
                            }
                        )
    except (FileNotFoundError, zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
        return {
            "file": str(path),
            "error": str(exc),
            "note": "Static XML risk scan failed; verify the file format and use rendered previews when possible.",
            "findings": [],
        }
    return {
        "file": str(path),
        "note": "Static XML risk scan only; verify with rendered previews when possible.",
        "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Static PPTX risk checker")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when the PPTX cannot be scanned",
    )
    args = parser.parse_args()

    result = inspect_pptx(args.pptx)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.strict and "error" in result:
            sys.exit(2)
    else:
        if "error" in result:
            print(result["note"])
            print(f"Error: {result['error']}")
            if args.strict:
                sys.exit(2)
            return
        print(result["note"])
        if not result["findings"]:
            print("No static risks found.")
            return
        for item in result["findings"]:
            print(
                f"Slide {item['slide']} shape {item['shape']}: "
                f"{', '.join(item['risk'])}; "
                f"min_font={item['min_font_pt']}; text={item['text_preview']!r}"
            )


if __name__ == "__main__":
    main()
