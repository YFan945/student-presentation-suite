"""Shared static PPTX XML risk checks.

The checks are intentionally conservative: they flag likely readability and
layout risks from PPTX XML, but rendered previews remain the source of truth.
"""

from __future__ import annotations

import re
import posixpath
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

EMU_PER_CM = 360_000
SMALL_TEXT_BOX_WIDTH_EMU = 900_000
SMALL_TEXT_BOX_HEIGHT_EMU = 250_000
TEXT_CHARS_PER_CM_LIMIT = 18
CHINESE_PARAGRAPH_LIMIT = 160
LATIN_PARAGRAPH_LIMIT = 220
HEADING_PLACEHOLDER_TYPES = {"title", "ctrTitle", "subTitle"}
BODY_PLACEHOLDER_TYPES = {"body", "dt", "ftr", "sldNum"}
HEADING_NAME_HINTS = ("title", "subtitle", "heading", "header", "标题", "副标题")
DEFAULT_MAX_PPTX_BYTES = 80 * 1024 * 1024


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


def rels_path(part_name: str) -> str:
    directory, filename = posixpath.split(part_name)
    return posixpath.join(directory, "_rels", f"{filename}.rels")


def resolve_relationship_target(source_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(source_part), target))


def relationship_target(zf: zipfile.ZipFile, source_part: str, type_suffix: str) -> str | None:
    rels_name = rels_path(source_part)
    if rels_name not in zf.namelist():
        return None
    root = ET.fromstring(zf.read(rels_name))
    for rel in root.findall("./rel:Relationship", NS):
        rel_type = rel.attrib.get("Type", "")
        target = rel.attrib.get("Target")
        if target and rel_type.endswith(type_suffix):
            return resolve_relationship_target(source_part, target)
    return None


def read_xml(zf: zipfile.ZipFile, part_name: str | None) -> ET.Element | None:
    if not part_name or part_name not in zf.namelist():
        return None
    return ET.fromstring(zf.read(part_name))


def first_style_size(root: ET.Element | None, style_name: str) -> float | None:
    if root is None:
        return None
    paths = [
        f".//p:txStyles/a:{style_name}/a:lvl1pPr/a:defRPr",
        f".//p:txStyles/a:{style_name}/a:defRPr",
        ".//p:defaultTextStyle/a:lvl1pPr/a:defRPr",
    ]
    for path in paths:
        node = root.find(path, NS)
        if node is not None:
            size = pptx_size_to_pt(node.attrib.get("sz"))
            if size is not None:
                return size
    return None


def placeholder_type(el: ET.Element) -> str | None:
    ph = el.find("./p:nvSpPr/p:nvPr/p:ph", NS)
    if ph is None:
        return None
    return ph.attrib.get("type") or "body"


def placeholder_font_sizes(root: ET.Element | None) -> dict[str, float]:
    if root is None:
        return {}
    sizes: dict[str, float] = {}
    for shape in root.findall(".//p:sp", NS):
        ph_type = placeholder_type(shape)
        if not ph_type:
            continue
        shape_sizes = font_sizes(shape)
        if shape_sizes:
            sizes.setdefault(ph_type, min(shape_sizes))
    return sizes


def inherited_font_context_for_layout(
    zf: zipfile.ZipFile, layout_name: str | None
) -> dict[str, dict[str, float] | dict[str, str]]:
    master_name = relationship_target(zf, layout_name, "/slideMaster") if layout_name else None
    layout_root = read_xml(zf, layout_name)
    master_root = read_xml(zf, master_name)

    styles: dict[str, float] = {}
    style_sources: dict[str, str] = {}
    for key, style_name in (("title", "titleStyle"), ("body", "bodyStyle"), ("other", "otherStyle")):
        for source, root in (("layout-style", layout_root), ("master-style", master_root)):
            size = first_style_size(root, style_name)
            if size is not None:
                styles[key] = size
                style_sources[key] = source
                break

    placeholders = placeholder_font_sizes(master_root)
    placeholder_sources = {key: "master-placeholder" for key in placeholders}
    layout_placeholders = placeholder_font_sizes(layout_root)
    placeholders.update(layout_placeholders)
    placeholder_sources.update({key: "layout-placeholder" for key in layout_placeholders})
    return {
        "styles": styles,
        "style_sources": style_sources,
        "placeholders": placeholders,
        "placeholder_sources": placeholder_sources,
    }


def inherited_font_sizes(
    el: ET.Element, context: dict[str, dict[str, float] | dict[str, str]], heading: bool
) -> tuple[list[float], str | None]:
    ph_type = placeholder_type(el)
    placeholders = context.get("placeholders", {})
    placeholder_sources = context.get("placeholder_sources", {})
    styles = context.get("styles", {})
    style_sources = context.get("style_sources", {})
    if ph_type and ph_type in placeholders:
        return [placeholders[ph_type]], placeholder_sources.get(ph_type, "placeholder")
    if ph_type in HEADING_PLACEHOLDER_TYPES or heading:
        style_key = "title" if styles.get("title") is not None else "other"
    elif ph_type in BODY_PLACEHOLDER_TYPES:
        style_key = "body" if styles.get("body") is not None else "other"
    else:
        style_key = "other" if styles.get("other") is not None else "body"
    size = styles.get(style_key)
    source = style_sources.get(style_key)
    return ([size], source) if size is not None else ([], None)


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
            colors.append(f"srgb:{val.upper()}")
    for scheme in el.findall(".//a:schemeClr", NS):
        val = scheme.attrib.get("val")
        if val:
            colors.append(f"scheme:{val}")
    for sys_color in el.findall(".//a:sysClr", NS):
        val = sys_color.attrib.get("val") or sys_color.attrib.get("lastClr")
        if val:
            colors.append(f"sys:{val.upper()}")
    return colors


def has_cjk(text: str) -> bool:
    for ch in text:
        cp = ord(ch)
        if (
            0x4E00 <= cp <= 0x9FFF
            or 0x3400 <= cp <= 0x4DBF
            or 0x3000 <= cp <= 0x303F
            or 0xFF00 <= cp <= 0xFFEF
        ):
            return True
    return False


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def iter_text_containers(root: ET.Element) -> list[tuple[str, ET.Element]]:
    containers: list[tuple[str, ET.Element]] = []
    for shape in root.findall(".//p:sp", NS):
        containers.append(("shape", shape))
    for table_or_chart in root.findall(".//p:graphicFrame", NS):
        if text_of(table_or_chart):
            containers.append(("graphicFrame", table_or_chart))
    return containers


def inspect_pptx(path: Path, max_bytes: int = DEFAULT_MAX_PPTX_BYTES) -> dict:
    findings = []
    try:
        size = path.stat().st_size
        if size > max_bytes:
            return {
                "file": str(path),
                "error": f"PPTX is too large for static scan: {size} bytes > {max_bytes} bytes",
                "note": "Static XML risk scan skipped; use rendered previews and a sampled manual review.",
                "findings": [],
            }
        with zipfile.ZipFile(path) as zf:
            slide_names = sorted(
                [n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")],
                key=slide_number,
            )
            layout_cache: dict[str, dict[str, dict[str, float] | dict[str, str]]] = {}
            for slide_name in slide_names:
                slide_id = slide_number(slide_name)
                root = ET.fromstring(zf.read(slide_name))
                layout_name = relationship_target(zf, slide_name, "/slideLayout")
                layout_cache_key = layout_name or ""
                if layout_cache_key not in layout_cache:
                    layout_cache[layout_cache_key] = inherited_font_context_for_layout(zf, layout_name)
                inherited_context = layout_cache[layout_cache_key]
                for idx, (container_type, container) in enumerate(iter_text_containers(root), start=1):
                    txt = text_of(container)
                    if not txt:
                        continue
                    heading = container_type == "shape" and is_heading_shape(container)
                    sizes = font_sizes(container)
                    font_size_source = "explicit" if sizes else None
                    if not sizes and container_type == "shape":
                        sizes, font_size_source = inherited_font_sizes(container, inherited_context, heading)
                    min_size = min(sizes) if sizes else None
                    bounds = shape_bounds(container)
                    chars = len(txt)
                    is_cjk = has_cjk(txt)
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
                        if chars / width_cm > TEXT_CHARS_PER_CM_LIMIT:
                            risk.append("high-text-density-overflow-risk")
                        if bounds["cx"] < SMALL_TEXT_BOX_WIDTH_EMU or bounds["cy"] < SMALL_TEXT_BOX_HEIGHT_EMU:
                            risk.append("small-text-box-risk")
                    paragraph_limit = CHINESE_PARAGRAPH_LIMIT if is_cjk else LATIN_PARAGRAPH_LIMIT
                    if chars > paragraph_limit:
                        risk.append("paragraph-heavy-slide-text")
                    colors = fill_colors(container)
                    if len(set(colors)) >= 6:
                        risk.append("many-colors-in-shape")
                    if risk:
                        findings.append(
                            {
                                "slide": slide_id,
                                "shape": idx,
                                "container_type": container_type,
                                "text_preview": txt[:80],
                                "min_font_pt": min_size,
                                "font_size_source": font_size_source or "unknown",
                                "char_count": chars,
                                "detected_cjk": is_cjk,
                                "heading_shape": heading,
                                "bounds": bounds,
                                "risk": risk,
                            }
                        )
    except (FileNotFoundError, PermissionError, OSError, zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
        return {
            "file": str(path),
            "error": str(exc),
            "note": "Static XML risk scan failed; verify the file format and use rendered previews when possible.",
            "findings": [],
        }
    return {
        "file": str(path),
        "note": (
            "Static XML risk scan only; verify with rendered previews when possible. "
            "Common layout/master inherited font sizes are resolved, but PowerPoint rendering may still differ."
        ),
        "findings": findings,
    }
