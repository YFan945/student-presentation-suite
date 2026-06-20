---
name: student-presentation-ppt
description: Use only when an explicit student academic context asks to create, rebuild, or explicitly edit an actual PPT/PPTX/PowerPoint deck. Enforce the Decision Gate before production when high-impact goals are unresolved.
---

# Student Presentation PPT

## Contract

Create or improve an editable student PPTX with planning, visuals, speaker notes, preview, QA, and change summary when applicable.

Load `../../references/suite-contract.md` first. Do not use this skill for generic/non-student presentations, outline-only requests, standalone scripts/Q&A, or review-only requests.

Actual production requires Codex `Presentations`. Verify it before planning or building. If unavailable, report the missing prerequisite and stop; never substitute a Markdown outline or imply that a PPTX exists.

## Workflow

1. Confirm the request passes suite scope and routes to actual PPTX production.
2. Load `references/pptx-production.md` and enforce its mandatory Decision Gate before creating a slide plan or PPTX.
3. Load `../../references/shared-standards.md` plus only the needed references:
   - `references/visual-style-menu.md`; after selection, load only `references/visual-styles/<style>.md`
   - `../../references/slide-spec.md` when Slide Spec is supplied or useful
   - `../../references/image-strategy.md` for source and fallback choices
4. After the gate is resolved, create or absorb a compact slide plan/Slide Spec.
5. For an existing deck, preserve the source, convert findings into an edit plan, write a separate improved PPTX, and create `outputs/<topic>-change-summary.md`. Treat `source_deck`, `edit_intent`, `review_findings`, `preserve`, and `change_summary_required` as authoritative.
6. Build through the standard `Presentations` workflow. Artifact-tool is internal; do not create a second PPTX engine. Use `imagegen` only when useful and permitted.
7. Render every slide, inspect the preview/contact sheet, fix visible defects, and run `scripts/pptx_delivery_check.py --fail-on-blockers` for release-grade validation.

## Output

Use `meta.output_prefix` when supplied; otherwise derive a short ASCII-safe topic slug.

- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or contact sheet
- `outputs/<topic>-change-summary.md` for improved decks

Follow the final response contract in `references/pptx-production.md` and report whether each expected file exists.
