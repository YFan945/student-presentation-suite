# PPTX Production

Load `../../../references/suite-contract.md` for scope and decision authority. Load `../../../references/shared-standards.md` for readability, anti-AI wording, language, and group standards. Load `../../../references/image-strategy.md` for image/source choices. Load `visual-style-menu.md` for the style menu; after selection, load only the matching file from `visual-styles/<style>.md`.

## Runtime Contract

- Require the Codex `Presentations` capability before production.
- If it is unavailable, report the missing prerequisite and stop. Do not fall back to a Markdown outline or claim a PPTX was generated.
- Use the standard Presentations workflow only. Artifact-tool is an internal implementation detail, not a separate public dependency or alternate engine.
- Use `imagegen` only when generated imagery materially helps and the user permits it. Diagram-only and shape-based decks must remain valid without it.

## Mandatory Decision Gate

Before creating a slide plan, Slide Spec, or PPTX, inspect the conversation, attachments, source deck, rubric, and supplied constraints. Identify unresolved decisions that materially change the deck:

- presentation type, purpose, and expected conclusion
- audience, course, rubric, and grading emphasis
- duration or target slide count
- content scope and required sections
- individual/group format and ownership
- visual direction or school template
- source material, data, image assets, and permitted image sources

If any high-impact decision is unresolved:

1. Ask only the 1–3 highest-impact questions in the current turn.
2. Give 2–4 mutually exclusive, topic-specific options for each question.
3. Put the recommended option first and label it `(Recommended)`.
4. Add one concise sentence explaining the impact or tradeoff of each option.
5. Wait for the user's choices. Do not create the slide plan, invoke production, or claim work has started.
6. Continue the gate in another round only when additional high-impact decisions remain.

Do not use abstract labels such as “方案 A/B” without describing the actual direction. Low-risk details may use visible defaults, but defaults must not bypass unresolved purpose, audience, grading emphasis, content scope, or other decisions that would substantially change the result.

If the user explicitly says “你决定”, “按推荐方案”, or equivalent, choose the recommended options and show a short `Production assumptions` block before building. Do not ask again. A direct request to “马上制作” does not waive the gate when the goal remains materially unclear.

When duration is known but slide count is not, offer density choices rather than one silent default. For 5 minutes, use:

- `Standard 8–9 slides (Recommended)` — balanced explanation and speaking pace
- `Concise 6–7 slides` — stronger focus with less supporting detail
- `Detailed 10–11 slides` — more evidence but faster delivery and higher crowding risk

Scale equivalent choices for other durations. When visual direction is unresolved and materially important, show 3–5 topic-fit recommendations with reasons and provide the complete style menu as an additional reference.

The gate is resolved only when every high-impact decision is either confirmed by the user, supplied by an artifact/Slide Spec, or explicitly delegated. Record the resolved choices before production.

## Build Sequence

1. Complete the Mandatory Decision Gate and record confirmed or delegated production choices.
2. Choose a creative direction from `visual-style-menu.md`. If the user has not specified one and style choice needs confirmation, show the complete menu with the best topic-fit options first and concise reasons for the top recommendations. If the user delegates the choice, pick the direction that best serves the topic and evidence type.
3. Generate or absorb Slide Spec structure. Preserve slide order, ownership, timing, visual purpose, and handoff intent unless changing them prevents crowding or improves clarity. Apply `generation_controls`, preserve every `locked_fields` entry, and enforce `revision_contract`; in partial mode, untargeted slides must remain unchanged. If the Slide Spec includes `source_deck`, `edit_intent`, `review_findings`, `preserve`, or `change_summary_required`, treat those fields as the programmatic handoff from review to PPTX production.
4. For existing deck improvement, convert review findings into a brief edit plan first. Preserve useful content and required template elements, decide which slides are rewritten vs redesigned, and write the improved deck to a new filename instead of overwriting the source. When `change_summary_required` is true, do not finish without `outputs/<topic>-change-summary.md` or an explicit limitation.
5. Design the PPTX with variation inside guardrails. Layouts should express a function, not force a repeated template. Use topic-specific examples, visuals, chart forms, section rhythm, and opening/closing treatment. Keep a mismatch ledger while building: record any difference between requested constraints and the working assumptions, any missing source material, and any tool/API behavior discovered during production.
6. Run delivery checks. Confirm PPTX, notes, preview/contact sheet, slide count, static XML risk summary, and risk breakdown where possible. Static XML risk counts are not enough on their own: distinguish true production blockers from expected small footer, page marker, caption, source, or kicker text.
7. Confirm visual QA. Preview/contact sheet review is required before calling a deck ready-to-present; otherwise say the file is generated but visual QA is incomplete. If the first render shows geometry mismatch, blank slides, text collapsed into the corner, overlap, or clipped callouts, fix the slide code and rerender before delivery.

## Creativity Rules

- Do not make every slide a card grid. Vary structure based on meaning: process, contrast, evidence, story, risk, recommendation, or Q&A.
- Do not use visual effects as decoration. Each image, shape, panel, timeline, chart, or callout must clarify the slide's main claim.
- Keep the deck subject-specific. Use course context, project details, survey/result evidence, examples, or scenario language from the user instead of generic filler.
- Style freedom is allowed in composition, section pacing, cover treatment, diagrams, color accents, and visual metaphors, but not in readability, source safety, or delivery verification.
- State the chosen direction and why it fits. Do not treat a preset as a fixed template.

## Output Naming

Use topic-specific filenames under `outputs/`:
- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or a generated contact sheet
- `outputs/<topic>-change-summary.md` when improving an existing deck

If Slide Spec meta includes `output_prefix`, use it as the `<topic>` slug; otherwise derive a short ASCII-safe slug from the topic. Keep the final response paths absolute.

## Classroom Readability

Check:
- title is readable from the back of a classroom
- Chinese normal body text is 22pt or larger
- English normal body text is 20pt or larger
- smaller text appears only in minor explanations, captions, citations, footnotes, or chart axes when unavoidable
- slide titles, subtitles, section headers, card headers, chart titles, panel labels, and other subheadings are 24pt or larger
- key terms are visually emphasized with bold, accent color, larger type, or callouts
- contrast is high
- slide is understandable in 3 seconds
- no dense paragraph blocks
- no decorative objects fighting the main message
- no text overflow, clipping, or text touching the edge of its box

## Content Quality

Every content slide should have one message and a clear visual or structural focus when that helps explain the message. Argumentative and evidence slides should normally use claim-style titles. Covers, section dividers, quotation slides, references, appendix, and Q&A slides may use descriptive titles and may omit speaker-note goals, transitions, or additional visuals when those elements would be artificial. Move explanation into speaker notes instead of shrinking slide text. Avoid pages that look empty because they only contain a title and one vague sentence.

Use concrete examples, data, diagrams, process steps, comparisons, or case details. Use shape-based structure such as panels, cards, dividers, process nodes, timeline blocks, callouts, or section bands. Use translucent panels or simulated glassmorphism only when they make text easier to read; fall back to opaque panels if PPTX/WPS rendering is weak.

For data slides: one chart/table only, one conclusion sentence, no unexplained raw data.
For evidence: distinguish `verified`, `user-provided`, `to-verify`, and `illustrative`; do not present the latter two as verified facts.
For defense decks: include objective, method/work, result, reflection, and Q&A.
For group decks: include member assignment and handoff lines.
For general undergraduate English decks: use B1-B2 as the default reference point, 2-4 short sentences per content slide, natural connectors in notes, and pronunciation/glossary help when useful. Adjust language level for advanced courses, disciplinary terminology, audience, and speaker ability.

## Image Handling

Follow `../../../references/image-strategy.md`. Use images or meaningful visuals on content slides when they explain, evidence, compare, or organize the message. Do not force imagery onto covers, dividers, references, appendix, Q&A, or content that is clearer as text. Respect requests for text-only, diagram-only, no network, or no generated assets. Avoid unrelated stock-like decoration. Record source URLs for web images when appropriate.

## Anti-AI Review

Remove or rewrite: generic openings, exaggerated claims, textbook paragraphs, motivational filler, repeated sentence patterns, vague words such as "various", "many aspects", "very important" without specifics.

Prefer: concrete class/project context, simple direct claims, examples from student life or source material, modest but clear conclusions.

## Presentations Workflow Pitfalls

When the Presentations workflow uses artifact-tool presentation primitives:
- run a one-slide smoke test before generating many slides
- verify shape positions use `left`, `top`, `width`, and `height` (not `x`/`y`)
- verify text is written through the shape text API when required by the runtime
- if helper scripts locate the runtime through `HOME`, set `HOME` explicitly on Windows when PowerShell points it at the workspace rather than the user profile
- if the contact-sheet helper needs Python, set `PYTHON` to the bundled runtime Python when available
- treat a nonblank PPTX file as insufficient evidence; the rendered PNG/contact sheet must show the intended layout

## Final Deliverable QA

Before final response:
- confirm `.pptx` exists and filename is topic-specific
- from the plugin package root, run `python skills/student-presentation-ppt/scripts/pptx_delivery_check.py --pptx <pptx> --notes <notes> --preview <preview> --strict --fail-on-blockers` when possible to verify PPTX integrity, slide count, notes, preview/contact sheet, static XML risk summary, and blocker-like findings
- render or preview slides when possible; check at least the contact sheet or preview images
- verify Chinese normal body text >= 22pt, English normal body text >= 20pt, and primary slide titles normally >= 24pt; visually verify any smaller secondary labels
- verify important keywords are visually emphasized
- verify no text is out of frame, clipped, overflowing, or too close to box edges
- verify layouts are neither too empty nor too crowded
- verify images support the argument and are not decorative filler
- verify content slides have enough hierarchy to communicate clearly; do not add shapes, panels, cards, or diagrams solely to satisfy a structural-layer rule
- verify background shapes or translucent panels improve hierarchy without reducing readability
- verify text is not placed directly over busy images unless a sufficiently opaque panel protects readability
- create a separate script/notes file if speaker notes are not embedded
- for improved existing decks, create a change summary that lists kept content, changed slides, unresolved issues, and QA results
- report any missing expected file and validation limitations honestly
- list `Known Issues to Fix` and `Before Presenting` when any validation, source, timing, or visual issue remains

## Final Response Contract

```markdown
## Generated Files
- PPTX: <absolute path> exists=<true|false>
- Notes: <absolute path or not created> exists=<true|false|n/a>
- Preview/Contact Sheet: <absolute path or not created> exists=<true|false|n/a>

## Deck Summary
- Slides:
- Duration:
- Language:
- Group order:

## Creative Direction
- Direction:
- Why it fits:
- Main visual choices:

## QA
- Delivery check:
- Static XML risks:
- Visual QA:
- Limitations:
- Known Issues to Fix:
- Before Presenting:
```
