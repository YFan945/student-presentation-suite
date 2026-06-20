# Presentation Intake

This is the canonical intake contract for student presentation work. Reuse facts
already supplied by the user, attached materials, an existing deck, or Slide
Spec meta. Never ask for a confirmed item again.

## Intake Modes

- PPTX creation or existing-deck editing: full intake is a hard gate.
- Outline-only planning: ask only for missing items that materially change the
  story, timing, evidence, or ownership; low-risk preferences may be stated as
  assumptions.
- Review-only work: proceed when the artifact is readable; ask only for missing
  duration, presentation type, group format, or rubric when it materially
  changes the review.

## Full PPTX Intake

Confirm every item before production:

| Item | Recommended value when missing | Why it matters |
| --- | --- | --- |
| Topic | Restate the user's topic as one focused sentence | Defines the story and slide claims |
| Course/context | General undergraduate classroom report | Controls terminology and academic framing |
| Presentation type | Coursework report | Determines required sections |
| Audience | Teacher and classmates | Controls explanation depth |
| Language | Follow the user's language | Controls slide and note language |
| Duration | 5 minutes | Controls scope and timing |
| Slide count | 7-9 slides for 5 minutes | Controls density |
| Format | Individual unless members are named | Controls ownership and handoffs |
| Rubric/required sections | No supplied rubric; use standard academic structure | Controls scoring priorities |
| Source material | User material plus stable general background | Controls evidence boundaries |
| Template/branding | No required template, logo, or brand | Controls layout constraints |
| Image strategy | Diagram-only or generated abstract visuals; no web images | Controls sourcing and production |
| Visual style | Recommend three topic-fit styles; choose one only after confirmation | Controls visual direction |
| Deliverables | PPTX, speaker notes, preview/contact sheet; add change summary for edits | Controls completion criteria |

If duration is known but slide count is not, recommend:

- 3 minutes: 5-7 slides
- 5 minutes: 7-9 slides
- 8 minutes: 9-12 slides
- 10 minutes: 10-14 slides
- 15 minutes: 14-18 slides

## Required Interaction

For an incomplete PPTX request:

1. Extract and display `Confirmed`.
2. Display only unresolved fields under `Please confirm`.
3. For every unresolved field, include a recommended value and one short impact
   statement.
4. Ask for one consolidated reply.
5. Do not run environment checks, generation scripts, rendering, or delivery
   checks while the state is `intake_pending`.

Use this response shape:

```markdown
## Confirmed
- Topic: ...
- Language: ...

## Please confirm
1. Duration — Recommended: 5 minutes. Impact: determines scope and slide count.
2. Visual style — Recommended: Modern Minimal. Impact: determines layout and palette.

Reply with changes, or say "use the recommendations".
```

If the user says “你决定”, “按推荐来”, “use the recommendations”, or otherwise
delegates the choices, fill every missing item with the recommended value. Then
show a complete `Production Summary` and ask for explicit confirmation.
Delegation does not itself move the state to `intake_confirmed`; approval of the
summary does.

If all fields were already supplied, show the complete `Production Summary` and
ask for confirmation without repeating questions.

## Production Summary

The confirmation summary must list all full-intake fields plus the planned output
directory or filename prefix when known. Only an affirmative reply to this
summary moves the workflow to `intake_confirmed`.

After confirmation, map supported values into Slide Spec `meta`:

- `topic`, `presentation_type`, `audience`, `language`, `duration_min`, `slide_count`
- `format`, `members`, `course`, `rubric`
- `source_material`, `template`, `logo`, `image_source`, `visual_style`
- `deliverables`, `output_prefix`

Use existing-deck top-level fields for editing: `source_deck`, `edit_intent`,
`review_findings`, `preserve`, and `change_summary_required`.

## Workflow States

`intake_pending → intake_confirmed → planned → producing → qa → complete`

- `intake_pending`: full intake is incomplete or its summary is unconfirmed.
- `intake_confirmed`: user approved the complete Production Summary.
- `planned`: slide spine or Slide Spec is ready.
- `producing`: editable files are being generated or edited.
- `qa`: static checks, rendering, inspection, and correction are running.
- `complete`: all required deliverables and gates passed.
- `incomplete`: a usable artifact exists but a required deliverable or QA gate failed.
- `blocked`: production cannot proceed because a required input, artifact, or runtime dependency is unavailable.

Never claim production has started before `intake_confirmed`. `incomplete` and
`blocked` may be entered from any later state when their conditions are met.
