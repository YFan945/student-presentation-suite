---
name: student-presentation
description: Use only when an explicit student academic context asks for a PPT/slide outline or Slide Spec. Supporting scripts and Q&A are allowed only within that eligible PPT planning task. Do not create PPTX files.
---

# Student Presentation

## Contract

Plan an eligible student PPT: topic angle, story, slide-by-slide outline, Slide Spec, and supporting speaker notes, transitions, Q&A, timing, or group handoffs.

Load `../../references/suite-contract.md` first. Do not use this skill for standalone scripts/Q&A, generic presentations, non-student work, or actual PPTX production. Route PPTX requests to `student-presentation-ppt`.

## Workflow

1. Confirm the request passes the suite scope and routes to outline planning.
2. Check known constraints before asking: presentation type, language, duration, slide count, audience/course, rubric, individual/group format, members, script needs, and later PPTX intent.
3. Ask only for missing constraints that materially change the outline. If the user delegates low-risk choices, state assumptions and continue.
4. Load `../../references/shared-standards.md` and only the references needed:
   - `references/slide-structures.md` for structures, topic narrowing, and subject patterns
   - `references/transition-phrases.md` for transitions and defense phrases
   - `references/group-handoff.md` for group work
   - `references/qa-prediction.md` for Q&A attached to the eligible PPT
   - `../../references/slide-spec.md` for structured handoff
   - `../../references/image-strategy.md` for visual source planning
5. If the topic is broad, offer 2–3 concrete angles or choose one when authorized.
6. Build the main claim, story arc, timing, slide purposes, and ownership.
7. Match detail to the request: concise outline by default; include notes, visuals, transitions, Q&A, and Slide Spec only when useful or requested.
8. If PPTX production follows, list unresolved production constraints and hand off to `student-presentation-ppt`.

## Output

Use claim-style titles for argumentative or evidence slides; descriptive titles are allowed for covers, dividers, references, appendix, Q&A, and closing.

When saving deliverables:

- `outputs/<topic>-outline.md`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-handoff-plan.md` for group presentations

Follow `../../references/slide-spec.md` when emitting Slide Spec YAML.
