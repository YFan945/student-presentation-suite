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

Schema and validation:
- JSON Schema: `references/slide-spec.schema.json`
- Validator: `scripts/validate_slide_spec.py`
- The validator requires `jsonschema` and `PyYAML` from `requirements.txt`.

```powershell
python scripts/validate_slide_spec.py path/to/slide-spec.yaml --json
```

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
- implement `layout` as a functional intent, not a fixed visual template
- split slides or move details into speaker notes when content is dense; do not shrink normal body text below shared typography thresholds to make content fit
- report any spec item that cannot be implemented

## Layout Functional Mapping

Use these mappings as intent rules. The final visual form may vary by creative direction.

- `timeline`: must show sequence, phases, or change over time. May use a horizontal timeline, vertical timeline, stepped path, roadmap, process ribbon, or milestone cards.
- `comparison`, `comparison-cards`, `before-after`: must make differences easy to scan. May use side-by-side panels, 2x2 matrix, before/after cards, annotated examples, or contrast bands.
- `process`, `three-step-process`, `loop-diagram`: must show flow, order, or feedback. May use numbered nodes, cycle diagram, path diagram, swimlane, or staged panels.
- `risk-callout`, `limitations`: must identify the risk or boundary and explain why it matters. May use warning callouts, evidence cards, redline annotations, or limitation panels.
- `data`, `chart`, `survey`: must put the conclusion near the chart/table and avoid unexplained raw data. Use one main chart/table per slide.
- `team-workflow`, `handoff`: must show member ownership and speaking flow. May use role lanes, member cards, sequence markers, or workflow arrows.
- `summary-qa`, `closing`: must leave one memorable takeaway and a clear Q&A/closing cue. May use a summary card, final claim, key-number recap, or question prompt.

## Review Rules

When `student-presentation-review` receives Slide Spec YAML plus a deck:
- compare planned title, layout, visual, timing, and owner against the actual deck
- flag missing visuals, changed claims, lost handoff lines, or timing drift
- treat mismatches as risks, not automatic errors, when the final deck improves clarity
