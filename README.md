# Personal Plugins Marketplace

This repository is a local plugin marketplace for both Codex and Claude Code.

## Structure

```text
.
├── marketplace.json                 # Codex marketplace manifest
├── .claude-plugin/marketplace.json   # Claude Code marketplace manifest
├── .github/workflows/                # GitHub CI
├── plugins/
│   └── student-presentation-suite/   # Plugin package
└── README.md / README-zh.md
```

## Included Plugin

- `student-presentation-suite`: university presentation planning, PPTX generation, and deck review.

Plugin documentation:

- [中文文档](plugins/student-presentation-suite/README-zh.md)
- [English README](plugins/student-presentation-suite/README.md)

## Codex

Codex uses the root `marketplace.json`. Plugin paths are relative to this repository root:

```json
"path": "./plugins/student-presentation-suite"
```

In Codex, `student-presentation-suite` keeps using the default `Presentations` skill/plugin, `artifact-tool`, and `imagegen`. Those dependencies are declared in:

```text
plugins/student-presentation-suite/skills/student-presentation-ppt/agents/openai.yaml
```

## Claude Code

Claude Code uses:

```text
.claude-plugin/marketplace.json
```

The plugin manifest is:

```text
plugins/student-presentation-suite/.claude-plugin/plugin.json
```

Claude Code PPTX generation depends on `document-skills`:

```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

## Validation

Run from the repository root:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json
```

Codex / Claude Code manifest validation:

```powershell
python C:\Users\28603\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py `
  C:\Users\28603\.agents\plugins\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
claude plugin validate .
```

