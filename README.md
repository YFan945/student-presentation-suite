# Claude Code Plugins

[中文](README-zh.md) | English

This directory is the Claude Code-only plugin marketplace at `%USERPROFILE%\.agents\claude-plugins`.

It publishes `student-presentation-suite` from `plugins/student-presentation-suite`. The package uses `.claude-plugin/plugin.json`, depends on `document-skills@anthropic-agent-skills`, and contains the Claude PPTX environment checker and Slide Spec production bridge.

```text
.
├── .claude-plugin/marketplace.json
├── plugins/
│   └── student-presentation-suite/
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── shared/
│       ├── references/
│       └── tests/
├── scripts/check_marketplace_release.py
└── .github/workflows/validate.yml
```

## Installation

```powershell
claude plugin marketplace add "$env:USERPROFILE\.agents\claude-plugins"
claude plugin install student-presentation-suite@personal
```

## Dependencies

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
python -m pip install -r plugins/student-presentation-suite/requirements-claude-pptx.txt
npm --prefix plugins/student-presentation-suite install
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json
```

LibreOffice and Poppler are system dependencies for rendered PPTX QA.

## Validation

```powershell
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
claude plugin validate .\plugins\student-presentation-suite
```

The independent Codex marketplace remains in the sibling directory `%USERPROFILE%\.agents\plugins`.

## License

MIT. See [LICENSE](LICENSE).
