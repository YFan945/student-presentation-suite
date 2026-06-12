# Student Presentation Suite

[![Plugin](https://img.shields.io/badge/Codex-plugin-111827)](#)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](.codex-plugin/plugin.json)
[![Python](https://img.shields.io/badge/python-3.x-3776AB)](skills/student-presentation-review/scripts/pptx_static_check.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[中文版](README-zh.md)

Student Presentation Suite is a Codex plugin for university presentation work. It separates the workflow into planning, editable PowerPoint generation, and review so Codex can use the right skill for each task.

## What It Provides

- `student-presentation`: topic narrowing, outline planning, slide-by-slide content, scripts, transitions, group handoffs, Q&A preparation, and optional Slide Spec YAML.
- `student-presentation-ppt`: editable `.pptx` generation with speaker notes, visual style presets, meaningful visuals, topic-specific output names, and preview/contact-sheet QA.
- `student-presentation-review`: review of existing PPTX/PDF/screenshots/specs, including logic, readability, AI-writing pattern risk, rubric fit, speaker notes, version comparison, and static PPTX XML checks.

## Repository Structure

```text
.
├── .codex-plugin/plugin.json
├── examples/
├── references/
├── skills/
│   ├── student-presentation/
│   ├── student-presentation-ppt/
│   └── student-presentation-review/
└── outputs/
```

## Install

Copy or clone this repository into your local Codex plugin directory, then restart or refresh Codex plugin discovery.

```powershell
git clone https://github.com/YFan945/student-presentation-suite.git `
  "$env:USERPROFILE\.agents\plugins\plugins\student-presentation-suite"
```

PPTX production depends on the installed `Presentations` skill/plugin. The static review checker requires Python 3.

If cloned with the command above into `$env:USERPROFILE\.agents\plugins\plugins\student-presentation-suite`, the personal marketplace entry at `$env:USERPROFILE\.agents\plugins\marketplace.json` should point to that real directory:

```json
"./.agents/plugins/plugins/student-presentation-suite"
```

## Typical Workflows

### Outline First, PPTX Later

1. Ask `student-presentation` to narrow the topic and create an outline.
2. Request Slide Spec YAML if the deck will be generated later.
3. Ask `student-presentation-ppt` to generate the editable PPTX from the outline or Slide Spec.

### Generate A PPTX

Provide a topic, outline, source material, or Slide Spec YAML. The PPT skill should produce:

- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or a contact sheet

The final response should include absolute paths, slide count, timing, group order when relevant, and any validation limitations.

PPTX generation now follows a creative-direction plus quality-guardrail model. The skill chooses a direction that fits the topic, then designs layouts by slide function. Layout names such as `timeline`, `comparison-cards`, `process`, `risk-callout`, and `summary-qa` describe what the slide must express, not a fixed visual template. Typography, density, contrast, source safety, and delivery checks remain hard requirements.

### Review An Existing Deck

Provide a PPTX, exported PDF, screenshot, contact sheet, speaker notes, Slide Spec YAML, or two versions for comparison. The review skill prioritizes issues that affect comprehension, grading, and delivery.

## Shared Standards

The three skills share standards for:

- confirmed constraint handling
- classroom readability
- anti-AI wording and AI-writing pattern risk
- B1-B2 English presentation style
- Chinese presentation norms
- group presentation handoffs
- image/source strategy

Typography defaults:

- Chinese normal body text: 22pt or larger
- English normal body text: 20pt or larger
- titles, subtitles, section headers, card headers, chart titles, panel labels, and other subheadings: 24pt or larger

## Static PPTX Check

Run the XML risk checker with:

```powershell
python skills/student-presentation-review/scripts/pptx_static_check.py path/to/deck.pptx --json
```

For automation, add `--strict` when a file-format or XML-scan failure should return a non-zero exit code:

```powershell
python skills/student-presentation-review/scripts/pptx_static_check.py path/to/deck.pptx --json --strict
```

Static checks are only risk signals. They cannot fully resolve font sizes inherited from slide masters or themes, and they may miss tables, charts, SmartArt, image text, and true rendered overflow. Confirm important issues with rendered previews or contact sheets when possible.

## PPTX Delivery Check

After generating a PPTX, verify the deliverable package exists, count slides, and summarize static XML risk signals:

```powershell
python skills/student-presentation-ppt/scripts/pptx_delivery_check.py `
  --pptx outputs/ai-learning-report-presentation.pptx `
  --notes outputs/ai-learning-report-speaker-notes.md `
  --preview outputs/ai-learning-report-preview.png `
  --json
```

This check does not render slides and does not replace preview/contact-sheet visual QA.

## Local Maintenance

Validate the plugin manifest after edits:

```powershell
python C:\Users\28603\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py `
  C:\Users\28603\.agents\plugins\plugins\student-presentation-suite
```

When Codex needs to pick up local plugin updates, update the cachebuster version and reinstall from the personal marketplace:

```powershell
python C:\Users\28603\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py `
  C:\Users\28603\.agents\plugins\plugins\student-presentation-suite
codex plugin add student-presentation-suite@personal
```

Open a new thread after reinstalling to test `student-presentation`, `student-presentation-ppt`, and `student-presentation-review`.

## Example

See [examples/ai-learning-report.md](examples/ai-learning-report.md) for an end-to-end example with topic, outline, Slide Spec YAML, speaker notes sample, and expected PPTX output naming.

## Maintenance

- Keep `README-zh.md` as the primary user-facing documentation.
- Update both README files after major workflow or behavior changes.
- Keep generated PPTX, PNG, and other output files out of git unless they are intentional examples.

## License

MIT. See [LICENSE](LICENSE).
