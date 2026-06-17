# Student Presentation Suite

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/Codex-plugin-111827)](marketplace.json)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-5B35D5)](.claude-plugin/marketplace.json)

[中文](README-zh.md) | English

Student Presentation Suite is a local plugin marketplace for building university presentation workflows in both Codex and Claude Code.

It ships one plugin, `student-presentation-suite`, with three skills:

- `student-presentation`: plan topics, outlines, scripts, transitions, handoffs, and Q&A.
- `student-presentation-ppt`: generate or improve editable PPTX decks with speaker notes, visual styles, Slide Spec handoff, change summaries, and delivery QA.
- `student-presentation-review`: review PPTX/PDF/screenshots/specs for logic, readability, rubric fit, AI-writing risk, and static PPTX issues.

## Why This Exists

University presentation work usually needs more than slide generation. This plugin keeps planning, PPTX production, and review as separate skills while sharing classroom readability, source-use, anti-AI wording, timing, and group-presentation standards.

The repository is structured as a marketplace root so others can clone it and install the plugin directly.

## Repository Layout

```text
.
├── marketplace.json
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── student-presentation-suite/
│       ├── .codex-plugin/plugin.json
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── shared/
│       ├── references/
│       └── tests/
└── .github/workflows/validate.yml
```

## Compatibility

| Runtime | Entry point | PPTX route |
| --- | --- | --- |
| Codex | `marketplace.json` | Default `Presentations` skill/plugin + `artifact-tool` + `imagegen` |
| Claude Code | `.claude-plugin/marketplace.json` | `document-skills` plugin, using its `pptx` skill |

Claude Code PPTX generation expects `document-skills@anthropic-agent-skills` to be installed.

## Installation

### Codex

Clone this repository into a dedicated local directory. Avoid cloning directly over an existing `%USERPROFILE%\.agents\plugins` directory unless you intentionally want this repository to be your whole local marketplace root.

```powershell
git clone https://github.com/YFan945/student-presentation-suite.git `
  "$env:USERPROFILE\student-presentation-suite-marketplace"
```

Register this repository as a non-default local Codex marketplace, then install the plugin from the marketplace name declared in `marketplace.json`:

```powershell
codex plugin marketplace add "$env:USERPROFILE\student-presentation-suite-marketplace"
codex plugin add student-presentation-suite@student-presentation-marketplace
```

If you instead merge this into Codex's default personal marketplace at `%USERPROFILE%\.agents\plugins\marketplace.json`, do not run `codex plugin marketplace add`. Copy the plugin package into `%USERPROFILE%\.agents\plugins\plugins\student-presentation-suite`, merge the `plugins[]` entry from this repository's `marketplace.json`, then run `codex plugin add student-presentation-suite@<your-personal-marketplace-name>`.

Codex PPTX generation also expects the built-in `Presentations` skill/plugin, `artifact-tool`, and `imagegen` to be available in the Codex runtime.

### Claude Code

Clone the same repository, install the Anthropic document skills dependency, then add this repository as a Claude Code marketplace and install the plugin:

```powershell
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin marketplace add <path-to-cloned-repository>
/plugin install student-presentation-suite@student-presentation-suite
```

The equivalent Claude CLI commands are:

```powershell
claude plugin marketplace add anthropics/skills
claude plugin marketplace add "$env:USERPROFILE\student-presentation-suite-marketplace"
claude plugin install document-skills@anthropic-agent-skills
claude plugin install student-presentation-suite@student-presentation-suite
```

For Claude Code PPTX generation and rendered QA, install the optional runtime dependencies after cloning:

```powershell
python -m pip install -r "$env:USERPROFILE\student-presentation-suite-marketplace\plugins\student-presentation-suite\requirements-claude-pptx.txt"
npm install --prefix "$env:USERPROFILE\student-presentation-suite-marketplace\plugins\student-presentation-suite"
python "$env:USERPROFILE\student-presentation-suite-marketplace\plugins\student-presentation-suite\scripts\check_claude_pptx_env.py" --json
```

LibreOffice and Poppler are system tools and must still be installed separately.

## Usage

Use the plugin by asking for one of the three workflows:

- Plan a class presentation from a topic.
- Generate or improve an editable PPTX from an outline, Slide Spec, or review findings.
- Review an existing deck, PDF export, screenshot, or Slide Spec.

For full plugin-level details, see:

- [Plugin README](plugins/student-presentation-suite/README.md)
- [中文文档](plugins/student-presentation-suite/README-zh.md)
- [Example presentation brief](plugins/student-presentation-suite/examples/ai-learning-report.md)

## Development

Install validation dependencies:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
```

For Claude Code PPTX generation and rendered QA, install the optional runtime dependencies:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements-claude-pptx.txt
npm install --prefix plugins/student-presentation-suite
```

LibreOffice and Poppler are system tools and must still be installed separately. Run `python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json` after installing them.

Run tests and release checks from the repository root:

```powershell
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json
```

Validate plugin manifests:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
claude plugin validate .
```

## Notes

- Generated PPTX, PNG, PDF, and cache files are ignored by default.
- The root `marketplace.json` is for Codex.
- The root `.claude-plugin/marketplace.json` is for Claude Code.
- The plugin package lives under `plugins/student-presentation-suite`.

## License

MIT. See [LICENSE](LICENSE).
