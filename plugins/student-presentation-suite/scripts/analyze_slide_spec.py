#!/usr/bin/env python3
"""Analyze a Slide Spec for structure, evidence, density, and rehearsal risks."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


GENERIC_TITLES = {
    "background",
    "analysis",
    "results",
    "conclusion",
    "introduction",
    "背景",
    "分析",
    "结果",
    "结论",
    "总结",
}
EVIDENCE_LAYOUT_HINTS = {"data", "chart", "survey", "comparison", "results", "experiment"}
EXEMPT_KINDS = {"cover", "section-divider", "quotation", "references", "appendix", "qa", "closing"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze Student Presentation Slide Spec")
    parser.add_argument("spec", type=Path, help="Slide Spec YAML path")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def normalize(text: str) -> str:
    return re.sub(r"[\W_]+", "", text.casefold())


def content_text(slide: dict[str, Any]) -> str:
    value = slide.get("ppt_text", slide.get("content", ""))
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def finding(
    severity: str,
    code: str,
    message: str,
    slide: int | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if slide is not None:
        result["slide"] = slide
    return result


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    slides = [slide for slide in data.get("slides", []) if isinstance(slide, dict)]
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    controls = (
        data.get("generation_controls")
        if isinstance(data.get("generation_controls"), dict)
        else {}
    )
    findings: list[dict[str, Any]] = []
    title_groups: dict[str, list[int]] = defaultdict(list)

    for slide in slides:
        slide_id = slide.get("id")
        title = str(slide.get("title", "")).strip()
        normalized = normalize(title)
        if normalized:
            title_groups[normalized].append(slide_id)
        if title.casefold() in GENERIC_TITLES and slide.get("kind", "content") == "content":
            findings.append(
                finding(
                    "Major",
                    "generic-title",
                    "标题只描述页面类别，没有表达本页结论。",
                    slide_id,
                )
            )

        kind = slide.get("kind", "content")
        layout = str(slide.get("layout", "")).casefold()
        evidence = slide.get("evidence", [])
        requires_evidence = (
            kind not in EXEMPT_KINDS
            and (
                meta.get("quality_tier") == "high-score"
                or any(hint in layout for hint in EVIDENCE_LAYOUT_HINTS)
            )
        )
        if requires_evidence and not evidence:
            findings.append(
                finding(
                    "Major",
                    "missing-evidence",
                    "高分或证据型页面没有声明支持主张的证据。",
                    slide_id,
                )
            )
        for item in evidence if isinstance(evidence, list) else []:
            if isinstance(item, dict) and item.get("status") == "to-verify":
                findings.append(
                    finding(
                        "Major",
                        "evidence-to-verify",
                        f"证据仍待核验：{item.get('claim', '未命名主张')}",
                        slide_id,
                    )
                )

        max_words = controls.get("max_words_per_slide")
        if isinstance(max_words, int):
            words = re.findall(r"\b[\w'-]+\b", content_text(slide))
            if len(words) > max_words:
                findings.append(
                    finding(
                        "Major",
                        "word-limit",
                        f"页面约 {len(words)} 个词，超过上限 {max_words}。",
                        slide_id,
                    )
                )

    for ids in title_groups.values():
        if len(ids) > 1:
            findings.append(
                finding(
                    "Major",
                    "duplicate-title",
                    f"页面标题重复或高度相似：{ids}",
                )
            )

    for index, slide in enumerate(slides[:-1]):
        if slide.get("kind", "content") not in EXEMPT_KINDS and not slide.get("transition"):
            findings.append(
                finding(
                    "Minor",
                    "missing-transition",
                    "内容页缺少通向下一页的衔接意图。",
                    slide.get("id"),
                )
            )

    kinds = {slide.get("kind", "content") for slide in slides}
    titles = " ".join(str(slide.get("title", "")).casefold() for slide in slides)
    if not ({"closing", "qa"} & kinds) and not any(
        token in titles for token in ("conclusion", "summary", "结论", "总结", "答疑", "q&a")
    ):
        findings.append(
            finding("Major", "missing-close", "缺少明确的总结、结论或答疑收束页面。")
        )

    duration = meta.get("duration_min")
    timings = [slide.get("timing_sec") for slide in slides]
    if isinstance(duration, (int, float)) and all(isinstance(value, int) for value in timings):
        total = sum(timings)
        target = round(float(duration) * 60)
        if total > target:
            findings.append(
                finding(
                    "Major",
                    "timing-overrun",
                    f"计划讲述 {total} 秒，超过目标 {target} 秒。",
                )
            )

    severity_order = {"Critical": 0, "Major": 1, "Minor": 2}
    findings.sort(key=lambda item: (severity_order[item["severity"]], item.get("slide", 0)))
    return {
        "slide_count": len(slides),
        "finding_count": len(findings),
        "findings": findings,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Slide Spec Quality Report",
        "",
        f"- Slides: {result['slide_count']}",
        f"- Findings: {result['finding_count']}",
        "",
    ]
    if not result["findings"]:
        lines.append("No deterministic structure, evidence, density, or timing risks found.")
        return "\n".join(lines)
    for item in result["findings"]:
        location = f", Slide {item['slide']}" if "slide" in item else ""
        lines.append(
            f"- {item['severity']}{location} [{item['code']}]: {item['message']}"
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    data = yaml.safe_load(args.spec.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Slide Spec root must be an object")
    result = analyze(data)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))


if __name__ == "__main__":
    main()
