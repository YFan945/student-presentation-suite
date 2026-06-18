# Student Presentation Suite Plugin

[![Plugin](https://img.shields.io/badge/plugin-student--presentation--suite-111827)](.codex-plugin/plugin.json)
[![Python](https://img.shields.io/badge/python-3.x-3776AB)](scripts/validate_slide_spec.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[中文](README-zh.md) | English

`student-presentation-suite` is a plugin for university presentation work. It helps an agent plan a classroom presentation, generate or improve an editable PPTX deck, and review an existing deck with student-focused standards.

The suite uses a strict trigger boundary: the request must clearly establish a student-owned context and explicitly ask for a PPT/slide outline, PPT/PPTX creation or improvement, or review of an existing PPT artifact. Generic presentation work, standalone scripts/Q&A, and non-student decks should use other skills.

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

Use this when the user asks for editable slides, PowerPoint, PPT, PPTX, rendered slides, a ready presentation file, or an improved copy of an existing deck.

It handles:

- editable `.pptx` generation
- improved copies of existing decks based on review findings
- speaker notes
- visual style selection
- image/source strategy
- Slide Spec to PPTX handoff
- preview/contact-sheet QA
- delivery checks for PPTX, notes, slide count, and static XML risks

Codex keeps using the default `Presentations` skill/plugin with `artifact-tool` and `imagegen`. Claude Code uses `document-skills` and its `pptx` skill, with bridge scripts in `scripts/`.

Before using this skill for real PPTX generation:
- In Codex, confirm the runtime provides `Presentations`, `artifact-tool`, and `imagegen`.
- In Claude Code, install `document-skills@anthropic-agent-skills`, then install the optional Python/Node QA dependencies and run `python scripts/check_claude_pptx_env.py --json` from this plugin directory.

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

For vague PPTX requests, the PPT skill should either ask for production-critical constraints or offer a fast default / confirm-first path. It should not silently invent web sources, current facts, or grading-specific requirements.

Slide Spec YAML can also carry an existing-deck improvement handoff with `source_deck`, `edit_intent`, `review_findings`, `preserve`, and `change_summary_required`.

## Outputs

Typical PPTX generation outputs:

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

`change-summary.md` is used when improving an existing deck.

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

Claude Code users should install the dependency plugin and this local marketplace from the repository root:

```powershell
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin marketplace add <path-to-this-repository>
/plugin install student-presentation-suite@student-presentation-suite
```

Then install local PPTX QA dependencies from this plugin directory:

```powershell
python -m pip install -r requirements-claude-pptx.txt
npm install
python scripts/check_claude_pptx_env.py --json
```

## Helper Scripts

Validate Slide Spec:

```powershell
python scripts/validate_slide_spec.py path/to/slide-spec.yaml --json
```

Create a Claude Code `pptx` production brief from Slide Spec. If the spec includes review findings or a source deck, the generated brief routes to the `pptx` editing workflow and requires a change summary:

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

For Claude Code PPTX generation and rendered QA:

```powershell
python -m pip install -r requirements-claude-pptx.txt
npm install
```

LibreOffice and Poppler are system tools and must be installed separately. Run `python scripts/check_claude_pptx_env.py --json` after installing them.

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
