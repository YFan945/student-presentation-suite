# Codex Plugins

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[中文](README-zh.md) | English

This directory is a Codex-only repository marketplace. It is registered explicitly with Codex and is not the default auto-discovered personal marketplace layout.

It publishes `student-presentation-suite` from `plugins/student-presentation-suite`. The package uses `.codex-plugin/plugin.json` and the Codex `Presentations` workflow, with optional `imagegen` visuals. It contains no Claude Code manifest or `document-skills` dependency.

```text
.
├── .agents/plugins/marketplace.json
├── plugins/
│   └── student-presentation-suite/
│       ├── .codex-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── shared/
│       ├── references/
│       └── tests/
└── .github/workflows/validate.yml
```

## Installation

```powershell
Set-Location "$env:USERPROFILE\.agents\plugins"
codex plugin marketplace add (Get-Location).Path
codex plugin add student-presentation-suite@personal
```

Read the marketplace name during updates with the explicit repository manifest:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json
```

## Runtime prerequisites

- `student-presentation-ppt` requires the Codex `Presentations` capability.
- PPTX creation stays inside the standard Codex presentation workflow; the plugin does not ship a second PPTX engine.
- `imagegen` is optional and is used only when a generated visual is useful and the user permits it.
- If `Presentations` is unavailable, the PPT skill must report the missing prerequisite and stop before claiming a PPTX was generated. Re-enable or install the Codex presentations plugin, then start a new thread.

## Validation

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
```

The independent Claude Code marketplace is maintained in the sibling directory `%USERPROFILE%\.agents\claude-plugins`.

## License

MIT. See [LICENSE](LICENSE).
