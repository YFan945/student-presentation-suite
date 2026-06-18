# Local Agent Skills Marketplace

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Marketplace](https://img.shields.io/badge/Agent-marketplace-111827)](.claude-plugin/marketplace.json)

[中文](README-zh.md) | English

This repository is the local shared marketplace at `%USERPROFILE%\.agents\plugins` for Codex and Claude Code. Both runtimes use the same marketplace file: `.claude-plugin/marketplace.json`. It also keeps reusable skill source files for tools such as OpenCode.

The parent `.agents` directory keeps obsolete marketplace experiments under `archive/`; this `plugins/` directory is the only active marketplace root.

It currently publishes one plugin, `student-presentation-suite`, with three skills:

- `student-presentation`: plan topics, outlines, scripts, transitions, handoffs, and Q&A.
- `student-presentation-ppt`: generate or improve editable PPTX decks with speaker notes, visual styles, Slide Spec handoff, change summaries, and delivery QA.
- `student-presentation-review`: review PPTX/PDF/screenshots/specs for logic, readability, rubric fit, AI-writing risk, and static PPTX issues.

## Repository Layout

```text
.
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

`.claude-plugin/marketplace.json` is the shared marketplace manifest for Codex and Claude Code. It points to the plugin package at `plugins/student-presentation-suite`.

## Installation

Codex uses the same marketplace file:

```powershell
codex plugin marketplace add "$env:USERPROFILE\.agents\plugins"
codex plugin add student-presentation-suite@personal
```

Claude Code uses the same marketplace file:

```powershell
claude plugin marketplace add "$env:USERPROFILE\.agents\plugins"
claude plugin install student-presentation-suite@personal
```

Inside Claude Code chat, the equivalent slash commands are:

```text
/plugin marketplace add <path-to-this-repository>
/plugin install student-presentation-suite@personal
```

The shared marketplace entry points to `plugins/student-presentation-suite` through:

```json
"source": "./plugins/student-presentation-suite"
```

Codex PPTX generation expects the built-in `Presentations` skill/plugin, `artifact-tool`, and `imagegen` to be available in the Codex runtime. Claude Code PPTX generation expects the plugin-local Claude metadata and `document-skills` route documented in the plugin README.

## Other Agent Tools

OpenCode or similar tools should consume the skill source directly from `plugins/student-presentation-suite/skills/` or from the plugin-local metadata they support.

## Development

Install validation dependencies:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
```

Run tests and release checks from the repository root:

```powershell
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
```

Validate the runtime manifests:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
claude plugin validate .
claude plugin validate .\plugins\student-presentation-suite
```

## Notes

- Generated PPTX, PNG, PDF, dependency, and cache files are ignored by default.
- `plugins/student-presentation-suite/README.md` documents the plugin behavior.
- The root README documents the shared Codex and Claude Code marketplace structure and installation.

## License

MIT. See [LICENSE](LICENSE).
