# Student Presentation Suite for Codex

[中文](README-zh.md) | English

Codex-only plugin strictly scoped to student-owned academic PPT work. It does not handle generic, business, teacher-training, or standalone speech/Q&A requests.

## Routing

| Request | Skill | Result |
| --- | --- | --- |
| Student PPT outline or Slide Spec | `student-presentation` | Outline with optional supporting notes, transitions, Q&A, and handoff |
| Create, rebuild, or explicitly edit a student PPTX | `student-presentation-ppt` | Editable PPTX, notes, preview, and QA |
| Review or score an existing student deck/export | `student-presentation-review` | Evidence-based findings and concrete fixes |
| Review plus explicit file modification | review → PPT skill | Separate improved deck and change summary |

Speaker notes, scripts, Q&A, and handoffs are supporting outputs only; they do not independently trigger this plugin. The canonical boundary is `references/suite-contract.md`.

## PPTX Decision Gate

Before production, the PPT skill reads existing context and identifies unresolved high-impact decisions. It asks only 1–3 questions per round, provides 2–4 mutually exclusive topic-specific options with the recommended option first, explains the tradeoff, and waits for the user's choice.

Production does not start while purpose, audience/grading emphasis, content scope, or another material decision remains unresolved. Defaults are allowed only for low-risk details or when the user explicitly delegates the decision.

## Runtime and outputs

- Manifest: `.codex-plugin/plugin.json`
- PPTX production: Codex `Presentations`; artifact-tool is an internal implementation detail
- Optional visuals: `imagegen`, only when useful and permitted
- Structured handoff: Slide Spec
- Original decks are never overwritten

Expected production outputs:

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

If `Presentations` is unavailable, the PPT skill stops and reports the prerequisite. It must not return a text outline as if a PPTX was generated.

## Validation

From this plugin directory:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/check_plugin_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

This package intentionally contains no `.claude-plugin`, `document-skills`, Claude production bridge, or alternate PPTX engine.
