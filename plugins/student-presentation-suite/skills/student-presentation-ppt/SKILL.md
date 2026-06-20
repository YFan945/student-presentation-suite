---
name: student-presentation-ppt
description: Use only for a clearly student-owned academic context when the user explicitly asks to create, edit, improve, or rebuild an editable PPT, PPTX, PowerPoint, or slide deck.
---

# Student Presentation PPT

Create or improve an actual editable student presentation.

## Responsibility

Load `../../references/shared-standards.md` first.

- A broad academic topic plus an explicit PPTX request belongs here; create a compact internal slide plan and continue.
- An outline-only request belongs to `student-presentation`.
- An existing deck plus “直接改好” starts with review diagnosis, then continues here in the same task.
- An existing deck plus “看看问题” belongs to `student-presentation-review` and must not modify files.
- Do not overwrite an existing source deck. Produce a separate improved deck and change summary.

PPTX production depends on `document-skills@anthropic-agent-skills`. This skill is the upper-level contract. Its classroom readability, Slide Spec, output, notes, change-summary, and QA requirements override conflicting generic advice from the upstream `pptx` skill.

## State Gate

Load `../../references/presentation-intake.md`. Use the full PPTX intake and the
canonical state sequence:

`intake_pending → intake_confirmed → planned → producing → qa → complete`

While `intake_pending`, only inspect supplied inputs and ask for confirmation.
Do not run environment checks or generation commands and do not claim production
has started. User delegation fills recommendations but still requires approval
of the complete Production Summary.

## Workflow

1. Complete intake and receive explicit confirmation.
2. Load only the required references:
   - `references/pptx-production.md`
   - `references/visual-style-menu.md`, then exactly one matching `references/visual-styles/<style>.md`
   - `../../references/slide-spec.md` for Slide Spec input
   - `../../references/image-strategy.md` for source and visual policy
3. Create the internal slide plan or validated Slide Spec; state becomes `planned`.
4. Run `python "${CLAUDE_PLUGIN_ROOT}/scripts/check_claude_pptx_env.py" --json --strict`. A failure is `blocked`.
5. For Slide Spec input, run `slide_spec_to_pptx_brief.py` as specified in `pptx-production.md`; use the current project when `CLAUDE_PROJECT_DIR` is unavailable.
6. Enter `producing` and follow the installed `document-skills` `pptx` skill:
   - new deck → `pptxgenjs.md`
   - existing deck/template → `editing.md`
7. Run generated Node scripts through `run_with_pptxgenjs.js`.
8. Enter `qa`; run text extraction, rendering, visual inspection, at least one fix-and-verify loop, and `pptx_delivery_check.py --strict --json`. A failed gate is `incomplete`.

## Output Contract

Write only to `${CLAUDE_PROJECT_DIR}/outputs` or the current project’s `outputs/` fallback:

- `<topic>-presentation.pptx`
- `<topic>-speaker-notes.md`
- `<topic>-preview.png` or contact sheet
- `<topic>-change-summary.md` for existing-deck improvements

The final response must report each file’s absolute path and existence, slide count, static risk summary, rendered QA status, and whether status is `complete`, `incomplete`, or `blocked`.
