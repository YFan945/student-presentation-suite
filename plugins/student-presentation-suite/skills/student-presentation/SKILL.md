---
name: student-presentation
description: Use only when the request explicitly identifies a student, university, course, classroom, defense, or other student context and explicitly asks for a PPT/slide outline. Do not trigger for generic presentation planning, scripts, Q&A, or non-student work; do not create PPTX files.
---

# Student Presentation

## Role

Plan what a student should present and say: topic narrowing, outline, slide-by-slide content, speaker notes, transitions, Q&A prep, timing, and member handoffs.

## Trigger Gate

Use this skill only when both conditions are explicit in the user's request or established conversation context:

1. The work is for a student, university course, classroom report, thesis defense, competition, or another clearly student-owned scenario.
2. The requested output is a PPT/slide outline or an outline intended for a student PPT.

Do not trigger for a generic topic, generic presentation planning, standalone scripts, Q&A preparation, speeches, meeting decks, business decks, or other non-student work. If either condition is missing, use a general-purpose skill or ask one routing question instead.

Do not create actual `.pptx`, editable PowerPoint, rendered slides, or production-ready decks. If the user asks for those, use `student-presentation-ppt`.

If an eligible student-context request says "做 PPT", "生成 slides", or asks for a ready presentation file, do not handle it as outline-only planning. Route to `student-presentation-ppt`. Use this skill only when the eligible request asks for "PPT 大纲", "slide outline", or an equivalent PPT structure without requesting the actual file.

## Clarification Gate

Before drafting an outline or script, decide whether the user's request is specific enough to plan responsibly. If the prompt is vague, incomplete, or only names a broad topic, ask concise follow-up questions for missing constraints that would materially change the plan. Avoid blocking on minor preferences that can be handled with explicit assumptions.

Ask for missing items that affect the plan, including presentation type, language, duration, expected slide count, audience/course, rubric, individual/group format, members, whether a full script is needed, and whether later PPTX generation is expected. Prefer 3-6 grouped questions in one reply and wait for confirmation when the answer changes the structure. If the user asks the agent to decide, or if the missing items are low-risk defaults for a general classroom outline, state assumptions and continue.

## Workflow

1. Enforce the Clarification Gate. Check confirmed constraints from the conversation or Slide Spec meta. Ask for missing items only when they would materially change the plan: type, language, duration, slide count, audience/course, rubric, individual/group format, members, script needs, and whether later PPTX generation is expected. For a general classroom outline, state low-risk assumptions and continue.
2. Load `../../references/shared-standards.md` first. Load only the needed task references:
   - `references/slide-structures.md` for templates, topic narrowing, subject presets, density examples, and quality checklist
   - `references/transition-phrases.md` for transition and defense phrase banks
   - When the presentation is a group format, also load `references/group-handoff.md`
   - `references/qa-prediction.md` for defense/report Q&A preparation
   - `../../references/slide-spec.md` for optional structured handoff
   - `../../references/image-strategy.md` for visual source planning
3. If the topic is broad, offer 2-3 concrete angles that fit the duration, evidence, and likely conclusion. If the user asked the agent to decide, choose one angle and state why.
4. Build the presentation spine: main claim, story arc, timing, and member ownership.
5. Draft each slide with a claim-style title, concise on-slide content, visual idea, speaker note goal, and transition/handoff sentence.
6. Add Q&A, scoring-risk warnings, pronunciation/glossary support, or Slide Spec YAML when useful.
7. If later PPTX generation is likely, include a handoff note that the outline is ready for `student-presentation-ppt` and list any unresolved constraints that would affect visual production.

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
