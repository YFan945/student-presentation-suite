# Deck Production Checklist

Load `../../../references/shared-standards.md` for shared readability, anti-AI wording, AI-writing pattern risk, English, Chinese, and group standards. Load `../../../references/image-strategy.md` for image/source choices. Load `visual-styles.md` when choosing a visual direction.

## Before Building

Check confirmed constraints first, then ask the user to choose or confirm only missing production items:
- topic and course
- presentation type
- audience and language
- duration and slide count
- individual or group format
- required sections or rubric
- source material, data, images, and template constraints
- image source preference: user assets, web search, generated visuals, diagram-only, or text-only

If duration is known but slide count is not, suggest choices rather than silently deciding:
- 3 minutes: 5-7 slides
- 5 minutes: 7-9 slides
- 8 minutes: 9-12 slides
- 10 minutes: 10-14 slides
- 15 minutes: 14-18 slides

## Creative Direction

Before building, choose one direction from `visual-styles.md` or ask the user to choose when the difference materially affects the result. The choice must be based on presentation type, audience, evidence, and topic tone.

Do:
- state the chosen direction and why it fits
- vary layouts by slide function instead of repeating the same card grid
- use topic-specific visuals, examples, and section rhythm
- keep creative freedom inside readability and source-safety guardrails

Do not:
- treat a preset as a fixed template
- add decorative visuals that do not support the claim
- make the deck look creative by shrinking text, lowering contrast, or using unsupported image sources

## Output Naming

Use topic-specific filenames under `outputs/`:
- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or a generated contact sheet

If Slide Spec meta includes `output_prefix`, use it as the `<topic>` slug; otherwise derive a short ASCII-safe slug from the topic.

Use a short ASCII-safe slug for `<topic>` when the tooling or filesystem path may have trouble with long Chinese names. Keep the final response paths absolute.

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

Every slide should have:
- one message
- one visual or structural focus
- a speaker note or script point
- a transition to the next slide

Slides should feel content-rich but not crowded:
- use concrete examples, data, diagrams, process steps, comparisons, or case details
- use shape-based structure such as panels, cards, dividers, process nodes, timeline blocks, callouts, or section bands
- use translucent panels or simulated glassmorphism only when they make text easier to read and hierarchy clearer; fall back to opaque panels if PPTX/WPS rendering is weak
- move explanation into speaker notes instead of shrinking slide text
- avoid pages that look empty because they only contain a title and one vague sentence

For data slides:
- one chart/table only
- one conclusion sentence
- no unexplained raw data

For defense decks:
- include objective, method/work, result, reflection, and Q&A

For group decks:
- include member assignment and handoff lines

For English decks:
- use B1-B2 level language
- keep slide text to 2-4 short sentences or phrase groups
- avoid complex long sentences
- include natural connector lines in notes
- add pronunciation or glossary help for difficult keywords when useful

## Image Handling

Follow `../../../references/image-strategy.md`. Images or meaningful visuals are expected unless the user explicitly asks for text-only, diagram-only, no network, or no generated assets. Avoid unrelated stock-like decoration. Record source URLs for web images when appropriate.

## Anti-AI Review

Remove or rewrite:
- generic openings
- exaggerated claims
- textbook paragraphs
- motivational filler
- repeated sentence patterns
- vague words such as "various", "many aspects", "very important" without specifics

Prefer:
- concrete class/project context
- simple direct claims
- examples from student life, data, case, or source material
- modest but clear conclusions

## Final Deliverable QA

Before final response:
- confirm `.pptx` exists
- confirm filename is topic-specific
- run `../scripts/pptx_delivery_check.py` when possible to verify PPTX existence, slide count, notes file, preview/contact sheet file, and static XML risk summary
- render or preview slides when possible
- check at least the contact sheet or preview images
- verify Chinese normal body text is at least 22pt
- verify English normal body text is at least 20pt
- verify slide titles, subtitles, section headers, card headers, chart titles, panel labels, and other subheadings are at least 24pt
- verify important keywords are visually emphasized
- verify no text is out of frame, clipped, overflowing, or too close to box edges
- verify layouts are neither too empty nor too crowded
- verify images support the argument and are not decorative filler
- verify each normal slide has a clear structural layer, such as shapes, panels, dividers, cards, callouts, or diagram nodes
- verify background shapes, translucent panels, or glassmorphism effects improve hierarchy without reducing readability
- verify text is not placed directly over busy images unless a sufficiently opaque panel or glass layer protects readability
- create a separate script/notes file if speaker notes are not embedded
- report any missing expected file and validation limitations honestly
- include the final response sections from `pptx-build-workflow.md`: `Generated Files`, `Deck Summary`, `Creative Direction`, and `QA`
