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
   - `references/deck-production-checklist.md` for production QA and output naming
   - `references/visual-styles.md` for visual presets, structural layers, and PPTX glass-effect limits
   - `../../references/slide-spec.md` when input includes Slide Spec YAML
   - `../../references/image-strategy.md` for image/source choices and fallback visuals
3. Build or adapt the slide plan using student-presentation principles: one message per slide, claim-style titles, concise text, natural notes, B1-B2 English when relevant, and balanced group ownership.
4. Design and build the deck:
   - use 16:9 unless a template requires otherwise
   - use shapes, panels, dividers, timeline blocks, process nodes, comparison cards, callouts, and background layers
   - use simulated glassmorphism/translucent panels only when readability remains strong
   - follow shared typography: Chinese body >= 22pt, English body >= 20pt, titles/subtitles/section headers/card headers/chart titles/panel labels >= 24pt
5. Export and validate through the presentation workflow. Do not claim ready-to-present unless the `.pptx` exists and preview/contact sheet QA has checked text overflow, clipping, unreadable text, broken images, weak titles, and crowding.

## Output Contract

Use topic-specific filenames under `outputs/`:
- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or contact sheet

If Slide Spec meta includes `output_prefix`, use it as `<topic>`; otherwise derive a short ASCII-safe slug from the topic.

Final response should include absolute paths to the PPTX, notes if separate, preview/contact sheet if available, plus slide count/timing/group order and any validation limitations.
