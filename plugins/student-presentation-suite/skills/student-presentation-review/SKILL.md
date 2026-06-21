---
name: student-presentation-review
description: Use only when an explicit student academic context asks to review, audit, score, compare, or critique an existing PPT/PPTX deck or export. Review by default; edit files only when explicitly authorized.
---

# Student Presentation Review

## Contract

Review eligible student presentation artifacts for story, readability, rubric fit, speaking readiness, AI-writing risk, visuals, notes, and static PPTX risks.

Load `../../references/suite-contract.md` first. An attached file alone does not trigger review. Do not use this skill for new-deck generation, generic file review, or non-student decks.

Review and advice are the default. If the user explicitly requests file modification, diagnose first and then hand the edit plan to `student-presentation-ppt`. Never overwrite the source; require a separate improved deck and change summary.

## Workflow

1. Confirm the request passes suite scope and routes to review.
2. Check known constraints and ask only for missing information that materially affects judgment. If the artifact is reviewable, proceed with stated assumptions rather than blocking.
3. Load `../../references/shared-standards.md` and only the needed references:
   - `references/review-checklist.md` for standards, scoring, AI-writing risk, and diff review
   - `references/review-output-format.md` for output structure and edit handoff
   - `../../references/slide-spec.md` for planned-versus-actual comparison
   - `../../references/image-strategy.md` for source and visual judgment
4. For `.pptx`, run `python skills/student-presentation-review/scripts/pptx_static_check.py` from the plugin root. Treat XML findings as risk evidence, not rendering proof.
5. Prefer rendered previews, PDFs, screenshots, or contact sheets for readability, clipping, crowding, and image judgments.
6. Prioritize findings as Critical, Major, or Minor and provide slide-specific fixes.
7. Include strengths, deck scoring, page scorecards, rubric alignment, notes/timing, rehearsal risks, group balance, and before/after comparison when applicable.
8. For authorized edits, separate diagnosis, preserve list, and edit plan, then hand off to `student-presentation-ppt`.

## Rules

- Do not claim to predict AI-detector results.
- Use B1–B2 as the default reference for general undergraduate English, while preserving necessary terminology.
- Confirm static risks visually when possible.
- For large decks, lead with critical issues and highest-priority slide examples.

Follow `references/review-output-format.md` and omit sections that do not apply.
