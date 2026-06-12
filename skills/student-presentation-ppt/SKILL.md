---
name: student-presentation-ppt
description: Generate editable university PPTX decks, speaker notes, previews, and production QA from topics, outlines, or Slide Spec YAML.
---

# Student Presentation PPT

## Role

Produce actual editable PowerPoint decks for university presentations. This skill handles PPTX generation, visual system, assets, export, preview, and QA.

Use the installed `Presentations` skill and its artifact-tool presentation JSX workflow. Do not stop at a text outline when the user asks for PPT, PPTX, PowerPoint, editable slides, rendered slides, or a ready presentation file.

## Workflow

1. Check confirmed constraints from the conversation or Slide Spec meta, then ask only for missing production-critical items: type, language, duration, slide count, course/rubric, group setup, source material, template/logo, visual style, and image-source preference.
2. Load `../../references/shared-standards.md` first. Load only the needed task references:
   - `references/pptx-build-workflow.md` for the creative-guardrail build sequence and final response contract
   - `references/deck-production-checklist.md` for production QA and output naming
   - `references/visual-styles.md` for creative directions, visual guardrails, structural layers, and PPTX glass-effect limits
   - `../../references/slide-spec.md` when input includes Slide Spec YAML
   - `../../references/image-strategy.md` for image/source choices and fallback visuals
   - `scripts/pptx_delivery_check.py` after generation to verify the deliverable package when a PPTX path is available
3. Choose one creative direction before building. If the user did not choose a style, select the best fit from `visual-styles.md` based on topic, presentation type, audience, and evidence type, then state the reason briefly. When style materially affects the result and time allows, offer 2-3 viable directions instead of defaulting silently.
4. Build or adapt the slide plan using student-presentation principles: one message per slide, claim-style titles, concise text, natural notes, B1-B2 English when relevant, and balanced group ownership.
5. Design and build the deck:
   - use 16:9 unless a template requires otherwise
   - use shapes, panels, dividers, timeline blocks, process nodes, comparison cards, callouts, and background layers as functional structures, not repeated decoration
   - use simulated glassmorphism/translucent panels only when readability remains strong
   - follow shared typography: Chinese body >= 22pt, English body >= 20pt, titles/subtitles/section headers/card headers/chart titles/panel labels >= 24pt
6. Export and validate through the presentation workflow. Do not claim ready-to-present unless the `.pptx` exists and preview/contact sheet QA has checked text overflow, clipping, unreadable text, broken images, weak titles, and crowding.
7. Before the final response, run `scripts/pptx_delivery_check.py` when possible. Report whether the PPTX, notes, and preview/contact sheet files actually exist, the detected slide count, static XML risk count, and any validation limitations. If the script cannot run, state that limitation instead of implying the package was checked.

## Output Contract

Use topic-specific filenames under `outputs/`:
- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or contact sheet

If Slide Spec meta includes `output_prefix`, use it as `<topic>`; otherwise derive a short ASCII-safe slug from the topic.

Final response must follow the contract in `references/pptx-build-workflow.md`: `Generated Files`, `Deck Summary`, `Creative Direction`, and `QA`. Always explicitly say whether each expected file exists.
