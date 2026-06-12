# PPTX Build Workflow

Use this workflow to generate creative but reliable student presentation decks.

## Build Sequence

1. Confirm production-critical constraints from the conversation or Slide Spec meta: presentation type, language, duration, slide count, format, course/rubric, source material, image-source limits, template/logo, and output prefix.
2. Choose a creative direction from `visual-styles.md`. If the user has not specified one, pick the direction that best serves the topic and evidence type. If multiple directions are genuinely strong and the user has time to choose, offer 2-3 options.
3. Generate or absorb Slide Spec structure. Preserve slide order, ownership, timing, visual purpose, and handoff intent unless changing them prevents crowding or improves clarity.
4. Design the PPTX with variation inside guardrails. Layouts should express a function, not force a repeated template. Use topic-specific examples, visuals, chart forms, section rhythm, and opening/closing treatment.
5. Run delivery checks. Confirm PPTX, notes, preview/contact sheet, slide count, and static XML risk summary where possible.
6. Confirm visual QA. Preview/contact sheet review is required before calling a deck ready-to-present; otherwise say the file is generated but visual QA is incomplete.

## Creativity Rules

- Do not make every slide a card grid. Vary structure based on meaning: process, contrast, evidence, story, risk, recommendation, or Q&A.
- Do not use visual effects as decoration. Each image, shape, panel, timeline, chart, or callout must clarify the slide's main claim.
- Keep the deck subject-specific. Use course context, project details, survey/result evidence, examples, or scenario language from the user instead of generic filler.
- Style freedom is allowed in composition, section pacing, cover treatment, diagrams, color accents, and visual metaphors, but not in readability, source safety, or delivery verification.

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
```
