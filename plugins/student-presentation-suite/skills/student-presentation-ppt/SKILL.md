---
name: student-presentation-ppt
description: Use only for a clearly student-owned academic context when the user explicitly asks to create, edit, improve, or rebuild an editable PPT, PPTX, PowerPoint, or slide deck.
---

# Student Presentation PPT

Create or improve an actual editable student presentation.

## Routing and ownership

Load `../../references/shared-standards.md` first.

- A broad academic topic plus an explicit PPTX request belongs here; create a compact internal slide plan and continue.
- An outline-only request belongs to `student-presentation`.
- An existing deck plus “直接改好” starts with review diagnosis, then continues here in the same task.
- An existing deck plus “看看问题” belongs to `student-presentation-review` and must not modify files.
- Do not overwrite an existing source deck. Produce a separate improved deck and change summary.

PPTX production depends on `document-skills@anthropic-agent-skills`. This skill is the upper-level contract. Its classroom readability, Slide Spec, output, notes, change-summary, and QA requirements override conflicting generic advice from the upstream `pptx` skill.

## Decision policy

Ask only when missing information changes structure, evidence, output format, or required branding. Otherwise state assumptions and continue.

Fast defaults:

- language follows the user
- duration: 5 minutes
- slide count: 7-9
- individual unless group members are named
- conceptual classroom explanation unless reliable source material is supplied
- diagrams or generated abstract visuals; no unapproved web images
- choose the best classroom-safe style and state why

When asking about style, recommend the three best matches. Show all 14 styles only when the user asks for every option.

## Workflow

1. Load only the required references:
   - `references/pptx-production.md`
   - `references/visual-style-menu.md`, then exactly one matching `references/visual-styles/<style>.md`
   - `../../references/slide-spec.md` for Slide Spec input
   - `../../references/image-strategy.md` for source and visual policy
2. Run:

   ```text
   python "${CLAUDE_PLUGIN_ROOT}/scripts/check_claude_pptx_env.py" --json --strict
   ```

   If it fails, production status is `blocked`; report the exact dependency and do not claim the deck is ready.
3. For Slide Spec input, run:

   ```text
   python "${CLAUDE_PLUGIN_ROOT}/scripts/slide_spec_to_pptx_brief.py" <spec> --output-dir "${CLAUDE_PROJECT_DIR}/outputs" --output "${CLAUDE_PROJECT_DIR}/outputs/<topic>-claude-pptx-brief.md"
   ```

   If `CLAUDE_PROJECT_DIR` is unavailable, use the current project directory.
4. Follow the installed `document-skills` `pptx` skill:
   - new deck → `pptxgenjs.md`
   - existing deck/template → `editing.md`
5. Run generated Node deck scripts through:

   ```text
   node "${CLAUDE_PLUGIN_ROOT}/scripts/run_with_pptxgenjs.js" <deck-script.js>
   ```

6. Apply this suite’s overrides:
   - Chinese body normally >= 22pt; English body normally >= 20pt
   - primary titles normally >= 24pt
   - one core message per content slide
   - visuals are functional, not mandatory decoration
   - do not force every slide into a card grid
   - write notes and preserve source/template constraints
7. Run text extraction, LibreOffice/Poppler rendering, visual inspection, and at least one fix-and-verify loop.
8. Run the delivery gate:

   ```text
   python "${CLAUDE_PLUGIN_ROOT}/skills/student-presentation-ppt/scripts/pptx_delivery_check.py" --pptx <pptx> --notes <notes> --preview <preview> --strict --json
   ```

   A failed gate is `incomplete`. Do not say ready-to-present until it passes.

## Deliverables

Write only to `${CLAUDE_PROJECT_DIR}/outputs` or the current project’s `outputs/` fallback:

- `<topic>-presentation.pptx`
- `<topic>-speaker-notes.md`
- `<topic>-preview.png` or contact sheet
- `<topic>-change-summary.md` for existing-deck improvements

The final response must report each file’s absolute path and existence, slide count, static risk summary, rendered QA status, and whether status is `complete`, `incomplete`, or `blocked`.
