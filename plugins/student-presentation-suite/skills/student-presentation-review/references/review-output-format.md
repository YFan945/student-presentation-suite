# Review Output Format

Use this structure by default. Omit sections that do not apply. Keep the review direct and actionable.

```markdown
## Overall Verdict

## What Works Well

## Five-Dimension Score

## Critical Issues

## Slide-by-Slide Suggestions

## Speaking And Notes

## Evidence And Citations

## Rehearsal And Timing

## Per-Slide Scores

## Group Handoffs

## Quick Fix Priority

## Edit Plan

## Change Summary Handoff

## Before/After Diff
```

When requested, add a Training Card for each slide:

```markdown
### Slide N Training Card
- Speaking goal:
- Keywords:
- Planned seconds:
- Likely question:
- Answer points:
- Avoid overstating:
```

For each issue, include:
- severity (Critical / Major / Minor)
- slide/page number when known
- problem
- why it matters
- concrete fix

Example:

```markdown
- Major, Slide 4: The title "Analysis" does not tell the audience the conclusion.
  Fix: Rename it to "Convenience is the main reason students choose short videos for news".
```

Use `Edit Plan` only when the user asks to optimize, modify, regenerate, or directly improve a deck. Include:
- what to keep
- what to rewrite
- what to redesign
- whether to preserve the original structure or rebuild a cleaner copy
- whether file editing is requested or only advice is requested

Use `Change Summary Handoff` when file editing is requested. It must be concise enough to pass into `student-presentation-ppt` and should include the expected improved PPTX filename plus `outputs/<topic>-change-summary.md`.
