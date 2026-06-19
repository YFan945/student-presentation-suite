# Student Presentation Suite for Claude Code

[中文](README-zh.md) | English

Claude Code-only plugin for student presentation planning, editable PPTX generation/improvement, and deck review.

## Skills

- `student-presentation`: topic narrowing, outlines, scripts, transitions, handoffs, and Q&A.
- `student-presentation-ppt`: create or improve editable PPTX decks with `document-skills`, visual styles, Slide Spec handoff, change summaries, and rendered QA.
- `student-presentation-review`: review PPTX/PDF/screenshots/specs for logic, readability, rubric fit, AI-writing risk, notes, and static PPTX issues.

## Runtime

This package is exclusively for Claude Code:

- Manifest: `.claude-plugin/plugin.json`
- Required plugin: `document-skills@anthropic-agent-skills`
- PPTX production: the `pptx` skill supplied by `document-skills`
- Local QA dependencies: `requirements-claude-pptx.txt` and `package.json`

It intentionally contains no `.codex-plugin`, Codex `agents/openai.yaml`, `artifact-tool`, or Codex runtime dependency declarations.

## Installation

From the repository root:

```powershell
claude plugin marketplace add "<path-to-this-repository>"
claude plugin install student-presentation-suite@personal
```

Install optional local QA dependencies:

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-claude-pptx.txt
npm install
python scripts/check_claude_pptx_env.py --json
```

LibreOffice and Poppler are system dependencies used for rendered QA.

## Slide Spec Bridge

```powershell
python scripts/slide_spec_to_pptx_brief.py <spec.yaml> `
  --output outputs/<topic>-claude-pptx-brief.md
```

The generated brief routes new decks to `pptxgenjs.md` and existing-deck improvements to `editing.md`. Existing decks are not overwritten and use `outputs/<topic>-change-summary.md`.

## Validation

```powershell
python -m unittest discover -s tests
python scripts/check_plugin_release.py
claude plugin validate .
```
