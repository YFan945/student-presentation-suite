---
name: student-presentation-ppt
description: Use only when the request explicitly identifies a student, university, course, classroom, defense, or other student context and explicitly asks to create or improve a PPT, PPTX, PowerPoint, or slide deck. Do not trigger for generic or non-student presentation work.
---

# Student Presentation PPT

## Role

Produce actual editable PowerPoint decks for university presentations. This skill handles PPTX generation, existing deck improvement, visual system, assets, export, preview, and QA.

## Trigger Gate

Use this skill only when both conditions are explicit in the user's request or established conversation context:

1. The deck has a clearly student-owned academic context, such as an identified student, university assignment, classroom report, thesis/course defense, teacher rubric, or student competition. A single ambiguous word such as "course" or "competition" is not enough without supporting context.
2. The user explicitly asks to create, generate, edit, improve, or rebuild a PPT, PPTX, PowerPoint, slide deck, or editable slides.

Do not trigger for generic presentation requests, non-student business decks, topic research, standalone outlines, scripts, or Q&A. If either condition is missing, use a general-purpose presentation skill or ask one routing question instead.

PPTX generation requires the Codex `Presentations` capability. At the start of production, verify that it is available in the current tool/skill context. If unavailable, report the missing prerequisite and stop. The skill must not fall back to a text outline or imply that a PPTX was generated.

Do not stop at a text outline when the user asks for PPT, PPTX, PowerPoint, editable slides, rendered slides, or a ready presentation file.

If an eligible student-context request provides only a broad topic but explicitly asks for PPT/PPTX/slides, this skill owns the request. Do not route back to outline-only planning. First create or confirm a concise slide plan/Slide Spec inside the PPTX workflow, then build the deck once production-critical constraints are handled. If an eligible request asks only for "PPT 大纲" or "slide outline" without a file, use `student-presentation` instead.

If the request comes from `student-presentation-review` or includes an existing deck plus review findings, treat it as an improvement/editing workflow. Preserve the original deck as input evidence, write a separate improved PPTX file, and create `outputs/<topic>-change-summary.md` describing kept content, changed slides, unresolved risks, and QA results. If Slide Spec includes `source_deck`, `edit_intent`, `review_findings`, `preserve`, or `change_summary_required`, use those fields as the authoritative edit handoff.

## Workflow

1. Verify the Codex `Presentations` prerequisite before planning or building. If missing, report how to restore the presentations plugin and stop without producing a substitute outline.
2. Load `../../references/shared-standards.md` first. Load only the needed task references:
   - `references/pptx-production.md` for clarification defaults, the full build sequence, runtime contract, creativity rules, content quality, deliverable QA, and final response contract
   - `references/visual-style-menu.md` for the style selection menu, choice guide, general visual principles, structural visual layer, and template inheritance
   - After choosing a style, also load `references/visual-styles/<style>.md` for that style's detailed guardrails
   - `../../references/slide-spec.md` when input includes Slide Spec YAML
   - `../../references/image-strategy.md` for image/source choices and fallback visuals
3. Apply the clarification/default policy in `pptx-production.md`; do not ask whether an outline is needed after the user has already requested a PPTX.
4. Choose one style, load only its matching style file, and create or absorb a compact slide plan/Slide Spec.
5. For existing deck improvement, preserve the source, convert findings into an edit plan, write a new PPTX, and create the required change summary.
6. Build through the standard `Presentations` workflow. Treat artifact-tool as an internal implementation detail; do not create a second PPTX engine. Use `imagegen` only when a generated visual is useful and permitted.
7. Render every slide, inspect the preview/contact sheet, fix visible defects, and run `pptx_delivery_check.py`. Use `--fail-on-blockers` for release-grade validation.

## Output Contract

Use topic-specific filenames under `outputs/`:
- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or contact sheet
- `outputs/<topic>-change-summary.md` for improved existing decks

If Slide Spec meta includes `output_prefix`, use it as `<topic>`; otherwise derive a short ASCII-safe slug from the topic.

Follow the final response contract in `references/pptx-production.md` and explicitly report whether each expected file exists.
