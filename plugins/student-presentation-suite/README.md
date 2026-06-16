# Student Presentation Suite Plugin

[![Plugin](https://img.shields.io/badge/plugin-student--presentation--suite-111827)](.codex-plugin/plugin.json)
[![Python](https://img.shields.io/badge/python-3.x-3776AB)](scripts/validate_slide_spec.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[中文版](README-zh.md)

`student-presentation-suite` is a plugin for university presentation work. It helps an agent plan a classroom presentation, generate an editable PPTX deck, and review an existing deck with student-focused standards.

This file describes the plugin package itself. Repository-level installation and marketplace setup are documented in the root [README](../../README.md).

## Skills

### `student-presentation`

Use this when the user needs planning rather than a PPTX file.

It handles:

- topic narrowing
- outline and slide order
- speaker script and transitions
- group handoffs
- Q&A preparation
- optional Slide Spec YAML for later PPTX generation

### `student-presentation-ppt`

Use this when the user asks for editable slides, PowerPoint, PPT, PPTX, rendered slides, or a ready presentation file.

It handles:

- editable `.pptx` generation
- speaker notes
- visual style selection
- image/source strategy
- Slide Spec to PPTX handoff
- preview/contact-sheet QA
- delivery checks for PPTX, notes, slide count, and static XML risks

Codex keeps using the default `Presentations` skill/plugin with `artifact-tool` and `imagegen`. Claude Code uses `document-skills` and its `pptx` skill, with bridge scripts in `scripts/`.

### `student-presentation-review`

Use this when the user provides an existing deck, PDF export, screenshot, notes, Slide Spec, or two versions for comparison.

It checks:

- slide logic and narrative flow
- classroom readability
- AI-like wording risk
- rubric fit
- speaker notes
- before/after changes
- PPTX static XML risk signals

## Shared Standards

All three skills share standards for:

- confirmed constraint handling
- classroom readability
- Chinese and English presentation style
- B1-B2 English when requested
- anti-AI wording cleanup
- group presentation handoffs
- image/source safety

Typography defaults:

- Chinese normal body text: 22pt or larger
- English normal body text: 20pt or larger
- titles, subtitles, section headers, card headers, chart titles, and panel labels: 24pt or larger

## Inputs

The plugin can work from:

- a broad topic
- a course/rubric brief
- an outline
- source notes or research material
- Slide Spec YAML
- an existing PPTX/PDF/screenshot
- speaker notes
- before/after deck versions

For vague PPTX requests, the PPT skill should ask for missing production-critical constraints before generating files.

## Outputs

Typical PPTX generation outputs:

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
```

When using Claude Code with Slide Spec input, the bridge script can also create:

```text
outputs/<topic>-claude-pptx-brief.md
```

## Runtime Routes

| Runtime | Manifest | PPTX production |
| --- | --- | --- |
| Codex | `.codex-plugin/plugin.json` | Default `Presentations` skill/plugin + `artifact-tool` + `imagegen` |
| Claude Code | `.claude-plugin/plugin.json` | `document-skills` plugin and its `pptx` skill |

Codex dependency hints are in:

```text
skills/student-presentation-ppt/agents/openai.yaml
```

Claude Code dependency is declared in:

```text
.claude-plugin/plugin.json
```

## Helper Scripts

Validate Slide Spec:

```powershell
python scripts/validate_slide_spec.py path/to/slide-spec.yaml --json
```

Create a Claude Code `pptx` production brief from Slide Spec:

```powershell
python scripts/slide_spec_to_pptx_brief.py path/to/slide-spec.yaml `
  --output outputs/<topic>-claude-pptx-brief.md
```

Check Claude Code PPTX environment:

```powershell
python scripts/check_claude_pptx_env.py --json
```

Check a generated PPTX delivery package:

```powershell
python skills/student-presentation-ppt/scripts/pptx_delivery_check.py `
  --pptx outputs/<topic>-presentation.pptx `
  --notes outputs/<topic>-speaker-notes.md `
  --preview outputs/<topic>-preview.png `
  --json
```

Run a static PPTX review:

```powershell
python skills/student-presentation-review/scripts/pptx_static_check.py path/to/deck.pptx --json
```

## Validation

From this plugin directory:

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python scripts/check_plugin_release.py
python scripts/check_claude_pptx_env.py --json
```

From the repository root:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
```

## Example

See [examples/ai-learning-report.md](examples/ai-learning-report.md) for a complete topic, outline, Slide Spec YAML, notes sample, and expected output naming.

## License

MIT. See [LICENSE](LICENSE).
