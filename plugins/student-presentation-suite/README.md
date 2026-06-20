# Student Presentation Suite for Codex

[中文](README-zh.md) | English

Codex-only plugin for student presentation planning, editable PPTX generation/improvement, and deck review.

## Skills

- `student-presentation`: topic narrowing, outlines, scripts, transitions, handoffs, and Q&A.
- `student-presentation-ppt`: create or improve editable PPTX decks with speaker notes, visual styles, Slide Spec handoff, change summaries, preview, and delivery QA.
- `student-presentation-review`: review PPTX/PDF/screenshots/specs for logic, readability, rubric fit, AI-writing risk, notes, and static PPTX issues.

## Runtime

This package is exclusively for Codex:

- Manifest: `.codex-plugin/plugin.json`
- PPTX production: Codex `Presentations`; artifact-tool is an internal implementation detail of that workflow
- Optional visual generation: `imagegen`, only when useful and permitted
- Skill UI metadata: `skills/*/agents/openai.yaml`

It intentionally contains no `.claude-plugin`, `document-skills` dependency, Claude environment checker, or Claude production brief.

`student-presentation-ppt` must verify that `Presentations` is available before production. If it is missing, the skill reports the prerequisite and stops; it must not return a Markdown outline as if it were a generated PPTX. Re-enable or install the Codex presentations plugin and retry in a new thread.

## Workflow

1. `student-presentation` creates an outline or Slide Spec.
2. `student-presentation-ppt` builds or improves the deck through the Codex presentation workflow.
3. `student-presentation-review` checks the deck and can hand findings back to the PPT skill.
4. Existing decks are never overwritten; improved decks use a new filename and include `outputs/<topic>-change-summary.md`.

Expected outputs:

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

## Validation

From this plugin directory:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/check_plugin_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

Generated files and dependencies are ignored by `.gitignore`.

The validated Slide Spec example is available at `examples/ai-learning-report.yaml`.
