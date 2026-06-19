---
name: student-presentation
description: Use only for a clearly student-owned academic context when the user explicitly requests a PPT or slide outline, not an editable deck. Do not use for generic presentations, standalone scripts, Q&A-only work, or non-student tasks.
---

# Student Presentation

Plan a student presentation without creating a `.pptx`.

## Routing

Load `../../references/shared-standards.md` first and apply its student-context and intent gate.

- Outline, slide structure, or outline plus notes → stay in this skill.
- Editable PPTX, PowerPoint, ready slides, or an existing deck to modify → `student-presentation-ppt`.
- Review, audit, score, or “看看问题” for an existing artifact → `student-presentation-review`.
- Never create or claim to create a presentation file from this skill.

## Decision policy

Ask only when a missing answer changes the story, evidence basis, duration, group ownership, or required deliverable. For a normal classroom outline, state low-risk assumptions and continue. Do not block on style, exact slide count, or other preferences that can be adjusted later.

## Workflow

1. Confirm the academic context and outline intent.
2. Load only the references needed:
   - `references/slide-structures.md` for structure and topic narrowing
   - `references/transition-phrases.md` for transitions
   - `references/group-handoff.md` for group ownership
   - `references/qa-prediction.md` for defense/report Q&A
   - `../../references/slide-spec.md` only when a structured PPTX handoff is useful
   - `../../references/image-strategy.md` only when visual sourcing matters
3. For a broad topic, choose or offer 2-3 viable angles based on duration and evidence.
4. Build one presentation spine: main claim, sequence, timing, and ownership.
5. For each content slide, provide its purpose, concise content, optional visual idea, note goal, and meaningful transition. Do not invent visuals or transitions for covers, references, appendix, or Q&A.
6. Add Q&A, glossary, scoring risks, or a Slide Spec only when useful.
7. If file production is the next step, hand off unresolved production constraints to `student-presentation-ppt`.

## Output

Use `outputs/<topic>-outline.md`, `outputs/<topic>-speaker-notes.md`, or `outputs/<topic>-handoff-plan.md` under the active user project. If `CLAUDE_PROJECT_DIR` is unavailable, use the current project directory. Never write deliverables into `${CLAUDE_PLUGIN_ROOT}`.
