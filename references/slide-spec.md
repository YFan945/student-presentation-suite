# Slide Spec YAML

Use Slide Spec YAML as an optional handoff format when:
- the user says the outline will later become a PPTX
- the deck is complex or group-based
- the user asks for structured output
- the review should compare plan vs actual slides

Do not force YAML for simple outline-only requests.

## Required Fields

Each slide entry should include:
- `id`: slide number
- `title`: claim-style slide title
- `layout`: intended layout or slide type
- `content`: short on-slide text or structured objects
- `visual`: visual type and purpose
- `note_goal`: what the speaker note should accomplish
- `transition`: transition or handoff sentence
- `timing_sec`: planned speaking time as an integer number of seconds
- `owner`: speaker/member, or `Individual`

Optional deck-level `meta` may carry confirmed constraints across planning, PPTX production, and review:

Meta field rules:
- Recommended required fields: `presentation_type`, `language`, `duration_min`, and `format`
- Optional fields: `slide_count`, `members`, `course`, `rubric`, `template`, `logo`, `image_source`, and `output_prefix`
- `language`: `"Chinese" | "English" | "bilingual"`
- `format`: `"individual" | "group"`
- `duration_min`: number of minutes
- `slide_count`: integer target slide count
- `image_source`: `"user-assets" | "web-search" | "generated" | "diagram-only" | "text-only" | "ask-before-web-search"`
- Use short ASCII-safe `output_prefix` when a later PPTX output filename needs a stable slug.

```yaml
meta:
  presentation_type: "coursework report"
  language: "Chinese"
  duration_min: 8
  slide_count: 10
  format: "group"
  members: ["A", "B", "C", "D"]
  course: "Introduction to AI"
  image_source: "ask-before-web-search"
```

## Example

```yaml
slides:
  - id: 3
    title: "Convenience is the main reason students choose short videos for news"
    layout: "comparison"
    content:
      bullets:
        - "Fast updates"
        - "Low reading effort"
        - "Easy sharing"
    visual:
      type: "bar-chart"
      purpose: "Compare the top three survey reasons"
    note_goal: "Explain the survey result without reading every number"
    transition: "But convenience also creates a reliability problem."
    timing_sec: 50
    owner: "Member B"
```

## PPTX Handoff Rules

When `student-presentation-ppt` receives Slide Spec YAML:
- preserve slide order and ownership
- treat `visual.purpose` as required design intent
- use integer `timing_sec` values to balance speaker notes
- keep `layout` unless a better layout is needed to prevent crowding
- report any spec item that cannot be implemented

## Review Rules

When `student-presentation-review` receives Slide Spec YAML plus a deck:
- compare planned title, layout, visual, timing, and owner against the actual deck
- flag missing visuals, changed claims, lost handoff lines, or timing drift
- treat mismatches as risks, not automatic errors, when the final deck improves clarity
