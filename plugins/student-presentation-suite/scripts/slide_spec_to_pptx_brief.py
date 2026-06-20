#!/usr/bin/env python3
"""Convert a validated Student Presentation Slide Spec into a Claude pptx brief."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.slide_spec_validation import semantic_errors
from shared.runtime_paths import output_root


def load_optional_dependencies():
    try:
        import jsonschema
        import yaml
    except ImportError as exc:
        print(
            "Missing dependency. Install Slide Spec dependencies with: "
            "python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(3) from exc
    return jsonschema, yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Slide Spec YAML/JSON and emit a Claude document-skills/pptx production brief"
    )
    parser.add_argument("spec", type=Path, help="Slide Spec YAML or JSON file")
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "references" / "slide-spec.schema.json",
        help="JSON Schema path",
    )
    parser.add_argument("--output", type=Path, help="Markdown brief output path")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Deliverable directory; defaults to CLAUDE_PROJECT_DIR/outputs or cwd/outputs",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON metadata instead of Markdown")
    return parser.parse_args()


def load_spec(path: Path, yaml_module: Any) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml_module.safe_load(text)


def validate_spec(data: Any, schema_path: Path, jsonschema_module: Any) -> list[dict[str, str]]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema_module.Draft202012Validator.check_schema(schema)
    validator = jsonschema_module.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    errors = [
        {
            "path": "." + ".".join(str(part) for part in error.path),
            "message": error.message,
        }
        for error in errors
    ]
    if not errors:
        errors.extend(semantic_errors(data))
    return errors


def text_block(value: Any, indent: str = "") -> str:
    if isinstance(value, str):
        return indent + value
    if isinstance(value, list):
        return "\n".join(f"{indent}- {text_block(item).strip()}" for item in value)
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{indent}- {key}:")
                lines.append(text_block(item, indent + "  "))
            else:
                lines.append(f"{indent}- {key}: {item}")
        return "\n".join(lines)
    return indent + str(value)


def meta_value(meta: dict[str, Any], key: str, default: str = "not specified") -> Any:
    value = meta.get(key)
    if value in (None, "", []):
        return default
    return value


def build_brief(
    data: dict[str, Any],
    source: Path,
    deliverable_dir: Path | None = None,
) -> str:
    meta = data.get("meta") or {}
    slides = data["slides"]
    output_prefix = meta.get("output_prefix") or source.stem
    resolved_output_dir = output_root(deliverable_dir)
    pptx_path = resolved_output_dir / f"{output_prefix}-presentation.pptx"
    notes_path = resolved_output_dir / f"{output_prefix}-speaker-notes.md"
    preview_path = resolved_output_dir / f"{output_prefix}-preview.png"
    change_summary_path = resolved_output_dir / f"{output_prefix}-change-summary.md"
    total_timing = sum(int(slide.get("timing_sec", 0)) for slide in slides)
    members = meta.get("members") or []
    member_text = ", ".join(members) if members else "not specified"
    review_findings = data.get("review_findings") or []
    preserve = data.get("preserve") or []
    is_improvement = bool(
        data.get("source_deck")
        or data.get("edit_intent")
        or review_findings
        or data.get("change_summary_required")
    )

    lines = [
        "# Claude PPTX Production Brief",
        "",
        "Use the `pptx` skill from the `document-skills` plugin to create the editable PPTX.",
        "This brief is generated from a validated Student Presentation Slide Spec.",
        "",
        "## Required Skill Route",
        "- Dependency plugin: `document-skills`",
        "- Target skill: `pptx`",
        "- New deck from scratch: follow `pptxgenjs.md`",
        "- Existing template/editing: follow `editing.md`",
        "- Keep all student-presentation constraints in this brief while using the pptx skill for PPTX generation.",
        "",
        "## Output Contract",
        f"- Project output directory: `{resolved_output_dir}`",
        f"- PPTX: `{pptx_path}`",
        f"- Notes: `{notes_path}`",
        f"- Preview/contact sheet: `{preview_path}` or a contact sheet in the same directory",
    ]
    if is_improvement or data.get("change_summary_required"):
        lines.append(f"- Change summary: `{change_summary_path}`")
    lines.extend(
        [
            "",
            "## Deck Constraints",
            f"- Topic: {meta_value(meta, 'topic')}",
            f"- Presentation type: {meta_value(meta, 'presentation_type')}",
            f"- Audience: {meta_value(meta, 'audience')}",
            f"- Language: {meta_value(meta, 'language')}",
            f"- Duration minutes: {meta_value(meta, 'duration_min')}",
            f"- Slide count: {meta.get('slide_count') or len(slides)}",
            f"- Total scripted timing seconds: {total_timing}",
            f"- Format: {meta_value(meta, 'format')}",
            f"- Members: {member_text}",
            f"- Course: {meta_value(meta, 'course')}",
            f"- Rubric: {meta_value(meta, 'rubric')}",
            "- Source material:",
            text_block(meta.get("source_material") or ["not specified"], "  "),
            f"- Template: {meta_value(meta, 'template')}",
            f"- Logo: {meta_value(meta, 'logo')}",
            f"- Image source policy: {meta_value(meta, 'image_source')}",
            f"- Visual style: {meta_value(meta, 'visual_style')}",
            "- Required deliverables:",
            text_block(
                meta.get("deliverables")
                or ["pptx", "speaker-notes", "preview"],
                "  ",
            ),
        ]
    )
    if is_improvement:
        lines.extend(
            [
                "",
                "## Existing Deck Improvement Contract",
                f"- Source deck/artifact: {data.get('source_deck') or 'not specified'}",
                f"- Edit intent: {data.get('edit_intent') or 'review-fix'}",
                "- Use `editing.md` from the `pptx` skill unless rebuilding from scratch is explicitly safer.",
                "- Do not overwrite the source deck; write a separate improved PPTX.",
                "- Preserve:",
                text_block(preserve or ["template/logo/footer/source citations unless the spec says otherwise"], "  "),
                "- Review findings to apply:",
            ]
        )
        for finding in review_findings:
            lines.append(
                f"  - {finding.get('severity', 'Major')}, {finding.get('target', 'deck')}: "
                f"{finding.get('problem', 'problem not specified')} "
                f"Fix: {finding.get('fix', 'fix not specified')}"
            )
        if not review_findings:
            lines.append(
                "  - No structured findings supplied; infer fixes from the conversation and source deck evidence."
            )
    lines.extend(
        [
            "",
            "## Student Presentation Requirements",
            "- Keep one clear message per content slide; use claim-style titles for argumentative and evidence slides.",
            "- Chinese normal body text must be >= 22pt; English normal body text must be >= 20pt.",
            "- Primary slide titles should normally be >= 24pt; visually verify smaller secondary labels.",
            "- Use functional visual structures when they clarify content; do not force decoration onto covers, dividers, references, appendix, or Q&A slides.",
            "- Avoid generic AI-sounding filler; prefer course/project-specific examples and modest claims.",
            "- Include speaker notes or a separate notes file with note goals and transitions.",
            "",
            "## Slide Plan",
        ]
    )
    for slide in slides:
        visual = slide.get("visual") or {}
        lines.extend(
            [
                "",
                f"### Slide {slide['id']}: {slide['title']}",
                f"- Layout intent: {slide['layout']}",
                f"- Owner: {slide['owner']}",
                f"- Timing seconds: {slide['timing_sec']}",
                f"- Slide kind: {slide.get('kind', 'content')}",
                f"- Visual type: {visual.get('type', 'not required')}",
                f"- Visual purpose: {visual.get('purpose', 'not required')}",
                "- Content:",
                text_block(slide["content"], "  "),
                f"- Speaker note goal: {slide.get('note_goal', 'not required')}",
                f"- Transition: {slide.get('transition', 'not required')}",
            ]
        )

    lines.extend(
        [
            "",
            "## Required QA",
            "- Run `python -m markitdown output.pptx` and inspect extracted text.",
            "- Render with LibreOffice, then convert PDF pages to images with Poppler.",
            "- Inspect rendered images or a contact sheet and complete at least one fix-and-verify loop.",
            "- Run `python \"${CLAUDE_PLUGIN_ROOT}/skills/student-presentation-ppt/scripts/pptx_delivery_check.py\" --pptx <pptx> --notes <notes> --preview <preview> --strict --json`.",
            f"- For existing deck improvements, verify `{change_summary_path}` lists kept content, changed slides, unresolved risks, and QA results.",
            "- Final response must report file existence, slide count, static XML risks, visual QA status, and limitations.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    jsonschema, yaml = load_optional_dependencies()
    try:
        data = load_spec(args.spec, yaml)
        errors = validate_spec(data, args.schema, jsonschema)
    except (OSError, json.JSONDecodeError, yaml.YAMLError, jsonschema.SchemaError) as exc:
        result = {"valid": False, "error": str(exc), "errors": []}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Slide Spec conversion failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    if errors:
        result = {"valid": False, "error_count": len(errors), "errors": errors}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("Slide Spec is invalid:", file=sys.stderr)
            for error in errors:
                print(f"- {error['path']}: {error['message']}", file=sys.stderr)
        raise SystemExit(1)

    deliverable_dir = output_root(args.output_dir)
    brief = build_brief(data, args.spec, deliverable_dir)
    result = {
        "valid": True,
        "slide_count": len(data["slides"]),
        "output_dir": str(deliverable_dir),
        "output": str(args.output) if args.output else None,
        "brief": brief,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(brief, encoding="utf-8")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not args.output:
        print(brief)
    else:
        print(f"Wrote Claude pptx brief: {args.output}")


if __name__ == "__main__":
    main()
