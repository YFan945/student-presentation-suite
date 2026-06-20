# Student Presentation Suite — Codex Marketplace

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/runtime-Codex-111827)](plugins/student-presentation-suite/.codex-plugin/plugin.json)

[中文](README-zh.md) | English

This repository is a Codex-only, explicitly registered local marketplace for `student-presentation-suite`. The plugin is strictly scoped to student-owned academic PPT work:

- planning a PPT outline or Slide Spec;
- creating or improving an editable PPTX;
- reviewing, scoring, or diagnosing an existing student deck.

It does not handle generic presentations, company decks, teacher training, standalone speeches/Q&A, or Claude Code production. The independent Claude Code package is maintained in the sibling repository directory `..\claude-plugins`.

## Plugin behavior

| User outcome | Skill | Deliverable |
| --- | --- | --- |
| Student PPT outline or Slide Spec | `student-presentation` | Outline plus optional supporting notes, transitions, Q&A, and group handoff |
| Create, rebuild, or explicitly edit a student PPTX | `student-presentation-ppt` | Editable PPTX, speaker notes, preview/contact sheet, and QA |
| Review or score an existing student deck/export | `student-presentation-review` | Prioritized findings, slide-level fixes, and optional scoring |
| Review plus explicit file modification | review → PPT skill | Separate improved deck and change summary |

Speaker notes, scripts, Q&A, and handoffs are supporting outputs only. They do not independently trigger the plugin.

### Mandatory PPTX Decision Gate

Before production, `student-presentation-ppt` reads the conversation, attachments, source deck, rubric, and Slide Spec. If a high-impact decision is missing, it must:

1. ask only the 1–3 most important questions in the current round;
2. provide 2–4 mutually exclusive, topic-specific options for each question;
3. place the recommended option first and explain each tradeoff;
4. wait for the user’s choices before creating a slide plan or PPTX.

Defaults cannot bypass unresolved purpose, audience/grading emphasis, content scope, or other material decisions. If the user explicitly delegates the choices, the skill records its production assumptions before building.

## Repository layout

```text
.
├── .agents/plugins/marketplace.json
├── .github/workflows/validate.yml
├── plugins/
│   └── student-presentation-suite/
│       ├── .codex-plugin/plugin.json
│       ├── assets/
│       ├── examples/
│       ├── references/
│       ├── scripts/
│       ├── shared/
│       ├── skills/
│       └── tests/
├── scripts/check_marketplace_release.py
├── AGENTS.md
├── CHANGELOG.md
└── Changelog-YYYY-MM-DD.md
```

Important ownership:

- `.agents/plugins/marketplace.json`: repository marketplace registration.
- `.codex-plugin/plugin.json`: plugin metadata, version, UI prompts, and capabilities.
- `references/suite-contract.md`: canonical scope, routing, decision authority, and runtime boundary.
- `references/shared-standards.md`: readability, density, language, anti-AI wording, and group standards.
- `skills/*/SKILL.md`: concise skill entrypoints; detailed rules live in selectively loaded references.
- `scripts/check_plugin_release.py`: package-level release contract.
- `scripts/check_marketplace_release.py`: repository-level marketplace contract.

## Requirements

- Windows, macOS, or Linux with Python 3.11+.
- Codex with the `Presentations` capability for actual PPTX production.
- `imagegen` is optional and used only when generated imagery is useful and permitted.
- Python dependencies from `plugins/student-presentation-suite/requirements.txt`.

The plugin intentionally contains no `.claude-plugin`, `document-skills`, Claude environment checker, Claude production bridge, `pptxgenjs`, or alternate PPTX engine.

## Installation

This repository is not the default auto-discovered personal marketplace layout. Register the repository root explicitly:

```powershell
Set-Location "$env:USERPROFILE\.agents\plugins"
codex plugin marketplace add (Get-Location).Path
codex plugin add student-presentation-suite@personal
```

Read the marketplace name from the repository manifest when updating:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json
```

After changing plugin skills or metadata, update the cachebuster and reinstall:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py" `
  .\plugins\student-presentation-suite
codex plugin add student-presentation-suite@personal
```

Start a new Codex thread after reinstalling so the updated skills are loaded.

## Development and validation

Run from the repository root:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path

python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py

python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  .\plugins\student-presentation-suite\skills\student-presentation
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  .\plugins\student-presentation-suite\skills\student-presentation-ppt
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  .\plugins\student-presentation-suite\skills\student-presentation-review
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite

git diff --check
```

The release checker enforces:

- a maximum of 65 lines for each `SKILL.md`;
- valid Markdown reference paths;
- consistent student-academic scope across manifest, README, agent metadata, and skills;
- mandatory Decision Gate wording and behavior;
- Codex-only runtime boundaries;
- Slide Spec improvement fields and review-to-edit handoff.

GitHub Actions runs the same core validation on every push and pull request.

## Generated files

PPTX production normally writes:

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

Generated PPTX/PNG files, caches, dependencies, and output contents are ignored. Keep only `outputs/.gitkeep`.

## Troubleshooting

- **`Presentations` unavailable:** restore the Codex presentations capability and retry in a new thread. The plugin must not substitute a Markdown outline for a requested PPTX.
- **Updated skill is not visible:** update the cachebuster, reinstall `student-presentation-suite@personal`, and open a new thread.
- **Marketplace name mismatch:** read `.agents/plugins/marketplace.json` with the command above; the current name is `personal`.
- **CLI reports access denied:** close processes that may hold the plugin cache or Codex executable, restart Codex/PowerShell, and retry the install command.
- **Release check fails:** use its exact file/path error as the source of truth; do not bypass the checker by removing required contracts.

## Release history

- Version-level notes: [CHANGELOG.md](CHANGELOG.md)
- Daily engineering logs: `Changelog-YYYY-MM-DD.md`

## License

MIT. See [LICENSE](LICENSE).
