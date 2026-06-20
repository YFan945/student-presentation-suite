---
name: student-presentation
description: Use only for a clearly student-owned academic context when the user explicitly requests a PPT or slide outline, not an editable deck. Do not use for generic presentations, standalone scripts, Q&A-only work, or non-student tasks.
---

# Student Presentation

Plan a student presentation without creating a `.pptx`.

## Responsibility

Load `../../references/shared-standards.md` first and apply its student-context and intent gate.

- Outline, slide structure, or outline plus notes → stay in this skill.
- Editable PPTX, PowerPoint, ready slides, or an existing deck to modify → `student-presentation-ppt`.
- Review, audit, score, or “看看问题” for an existing artifact → `student-presentation-review`.
- Never create or claim to create a presentation file from this skill.

## Workflow

1. Load `../../references/presentation-intake.md` and use its outline-only intake mode.
2. Confirm the academic context, requested outline deliverable, and any constraints that change story, timing, evidence, or ownership. State low-risk assumptions instead of blocking.
3. Load only the references needed:
   - `references/slide-structures.md` for structure and topic narrowing
   - `references/transition-phrases.md` for transitions
   - `references/group-handoff.md` for group ownership
   - `references/qa-prediction.md` for defense/report Q&A
   - `../../references/slide-spec.md` only when a structured PPTX handoff is useful
   - `../../references/image-strategy.md` only when visual sourcing matters
4. For a broad topic, choose or offer 2-3 viable angles based on duration and evidence.
5. Build one presentation spine: main claim, sequence, timing, and ownership.
6. For each content slide, provide its purpose, concise content, optional visual idea, note goal, and meaningful transition.
7. Add Q&A, glossary, scoring risks, or a Slide Spec only when useful.
8. If file production becomes the requested outcome, hand off to `student-presentation-ppt`; its full intake gate still applies.

## Output Contract

Use `outputs/<topic>-outline.md`, `outputs/<topic>-speaker-notes.md`, or `outputs/<topic>-handoff-plan.md` under the active user project. If `CLAUDE_PROJECT_DIR` is unavailable, use the current project directory. Never write deliverables into `${CLAUDE_PLUGIN_ROOT}`.
