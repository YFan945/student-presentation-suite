# Review Output Format

Use this structure by default. Omit sections that do not apply. Keep the review direct and actionable.

```markdown
## Overall Verdict

## What Works Well

## Five-Dimension Score

## Page Scorecard

## Critical Issues

## Slide-by-Slide Suggestions

## Speaking And Notes

## Group Handoffs

## Quick Fix Priority

## Edit Plan

## Change Summary Handoff

## Before/After Diff
```

For each issue, include:
- severity (Critical / Major / Minor)
- slide/page number when known
- problem
- why it matters
- concrete fix

For `Page Scorecard`, rate each applicable slide from 1–5 on logic, content clarity, visual readability, speakability, and evidence. Add one main problem and one concrete fix. Use `n/a` for evidence on covers, dividers, Q&A, or other slides where evidence is not expected. Scores support diagnosis; they do not replace it.

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
