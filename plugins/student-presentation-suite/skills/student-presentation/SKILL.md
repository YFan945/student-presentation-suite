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
2. Load `../../references/presentation-brief.md`; classify scenario, audience depth, structure mode, interaction mode, quality level, and content controls. Confirm only constraints that materially change story, timing, evidence, or ownership.
3. Load only the references needed:
   - `references/slide-structures.md` for structure and topic narrowing
   - `references/transition-phrases.md` for transitions
   - `references/group-handoff.md` for group ownership
   - `references/qa-prediction.md` for defense/report Q&A
   - `../../references/content-workflow.md` for directory → slide points → PPT copy → speaker version
   - `../../references/evidence-and-citations.md` when claims need sources
   - `../../references/revision-training-export.md` for training cards or quality reports
   - `../../references/slide-spec.md` only when a structured PPTX handoff is useful
   - `../../references/image-strategy.md` only when visual sourcing matters
4. For a broad topic, choose or offer 2-3 viable angles based on duration and evidence.
5. Build one presentation spine, then generate the requested layers in order: directory, per-slide claim/points, PPT copy, speaker version, and optional Slide Spec.
6. For each content slide, provide its story role, claim, concise copy, optional visual, evidence refs, notes, timing, owner, and transition.
7. In beginner mode, explain why major structure/layout choices fit the audience. Run `analyze_presentation_spec.py` for structured/high-score output. Add training cards, Q&A, glossary, scoring risks, Evidence Ledger, or revision metadata only when requested or useful.
8. If file production becomes the requested outcome, hand off to `student-presentation-ppt`; its full intake gate still applies.

## Output Contract

Use `outputs/<topic>-outline.md`, `outputs/<topic>-speaker-notes.md`, or `outputs/<topic>-handoff-plan.md` under the active user project. If `CLAUDE_PROJECT_DIR` is unavailable, use the current project directory. Never write deliverables into `${CLAUDE_PLUGIN_ROOT}`.
