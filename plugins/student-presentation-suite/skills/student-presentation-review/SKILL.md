---
name: student-presentation-review
description: Use only for a clearly student-owned academic context when the user explicitly asks to review, audit, score, critique, compare, or diagnose an existing PPT/PPTX/PowerPoint deck or rendered export.
---

# Student Presentation Review

Review an existing student presentation. By default, diagnose and recommend; do not edit files.

## Responsibility

Load `../../references/shared-standards.md` first.

- “看看问题”, review, audit, score, or critique → review only.
- Review-only requests must not modify files.
- “直接改好”, modify, rebuild, or produce an improved file → diagnose first, then hand off to `student-presentation-ppt` in the same task.
- New deck without an existing artifact → planning or PPTX skill according to requested output.
- Never overwrite the original deck.

## Workflow

1. Load `../../references/presentation-intake.md` and use its review-only intake mode. If the artifact is reviewable, state low-risk assumptions and proceed.
2. Load only what is needed:
   - `references/review-checklist.md`
   - `references/review-output-format.md`
   - `../../references/content-workflow.md` for story-order checks
   - `../../references/evidence-and-citations.md` for source gaps
   - `../../references/revision-training-export.md` for per-slide scoring and rehearsal
   - `../../references/slide-spec.md` for planned-vs-actual comparison
   - `../../references/image-strategy.md` for visual/source review
3. For PPTX input, run:

   ```text
   python "${CLAUDE_PLUGIN_ROOT}/skills/student-presentation-review/scripts/pptx_static_check.py" <deck.pptx> --json
   ```

4. Inspect rendered previews, PDF pages, screenshots, or contact sheets when available. Rendered evidence determines clipping and readability; XML findings are risk signals only.
5. Classify every actionable finding:
   - Critical: blocks understanding, grading, or delivery
   - Major: should be fixed before presenting
   - Minor: polish
6. For each finding, identify target slide/page, problem, impact, concrete fix, and—when requested—logic/evidence/readability/speakability/defense score.
7. Check source gaps, story order, repeated pages, conclusion support, timing, transitions, opening/closing, and likely teacher/judge questions. Use `analyze_presentation_spec.py` when a Slide Spec is available.
8. For edit requests, produce a structured handoff using `source_deck`, `edit_intent`, `review_findings`, `preserve`, locked slides, and `change_summary_required`, then enter `student-presentation-ppt`. Require a separate improved deck, change summary, and revision manifest. Its full intake and Production Summary confirmation remain mandatory before editing.

## Status rules

- Static scan plus rendered inspection completed → `complete`.
- Review is useful but rendered evidence is unavailable → `incomplete`; state that visual conclusions remain unverified.
- Required artifact cannot be read → `blocked`.

Never present static XML output as proof of rendered overflow or readability. Never claim to predict an AI detector result.

Write review reports to `${CLAUDE_PROJECT_DIR}/outputs` or the current project’s `outputs/` fallback, never `${CLAUDE_PLUGIN_ROOT}`.
