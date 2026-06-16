---
name: student-presentation
description: Plan university presentation outlines, scripts, Q&A, timing, and handoffs; do not create PPTX files.
---

# Student Presentation

## Role

Plan what a student should present and say: topic narrowing, outline, slide-by-slide content, speaker notes, transitions, Q&A prep, timing, and member handoffs.

Do not create actual `.pptx`, editable PowerPoint, rendered slides, or production-ready decks. If the user asks for those, use `student-presentation-ppt`.

## Clarification Gate

Before drafting an outline or script, decide whether the user's request is specific enough to plan responsibly. If the prompt is vague, incomplete, or only names a broad topic, stop and ask concise follow-up questions instead of immediately writing slides.

Ask for missing items that affect the plan, including presentation type, language, duration, expected slide count, audience/course, rubric, individual/group format, members, whether a full script is needed, and whether later PPTX generation is expected. Prefer 3-6 grouped questions in one reply and wait for confirmation when the answer changes the structure.

## Workflow

1. Enforce the Clarification Gate. Check confirmed constraints from the conversation or Slide Spec meta, then ask for missing items that affect the plan before drafting: type, language, duration, slide count, audience/course, rubric, individual/group format, members, script needs, and whether later PPTX generation is expected.
2. Load `../../references/shared-standards.md` first. Load only the needed task references:
   - `references/slide-structures.md` for templates, topic narrowing, subject presets, density examples, and quality checklist
   - `references/transition-phrases.md` for transition and defense phrase banks
   - When the presentation is a group format, also load `references/group-handoff.md`
   - `references/qa-prediction.md` for defense/report Q&A preparation
   - `../../references/slide-spec.md` for optional structured handoff
   - `../../references/image-strategy.md` for visual source planning
3. If the topic is broad, offer 2-3 concrete angles that fit the duration, evidence, and likely conclusion.
4. Build the presentation spine: main claim, story arc, timing, and member ownership.
5. Draft each slide with a claim-style title, concise on-slide content, visual idea, speaker note goal, and transition/handoff sentence.
6. Add Q&A, scoring-risk warnings, pronunciation/glossary support, or Slide Spec YAML when useful.

## Output

For outline requests:

```markdown
## Slide 1: Title
- Main content:
- Visual suggestion:
- Speaker note:
- Transition:
```

When saving deliverables, use:
- `outputs/<topic>-outline.md`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-handoff-plan.md` for group presentations

If later PPTX production is expected, append optional Slide Spec YAML following `../../references/slide-spec.md`.
