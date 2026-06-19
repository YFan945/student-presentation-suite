# Claude Code Plugins

[中文](README-zh.md) | English

Claude Code-only marketplace published from the
[`claude-code`](https://github.com/YFan945/student-presentation-suite/tree/claude-code)
branch. The marketplace name is `claude-personal`.

## Install or migrate

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install_claude_plugin.ps1 -Migrate
```

The script:

- keeps the Codex workspace untouched
- removes the obsolete Claude `personal` registration and plugin cache
- installs dependencies
- registers this directory as `claude-personal`
- installs `document-skills@anthropic-agent-skills`
- installs and validates `student-presentation-suite@claude-personal`

Restart Claude Code after installation.

## Manual development setup

```powershell
git clone --branch claude-code --single-branch `
  git@github.com:YFan945/student-presentation-suite.git `
  "$env:USERPROFILE\.agents\claude-plugins"
python -m pip install -r plugins/student-presentation-suite/requirements.txt
python -m pip install -r plugins/student-presentation-suite/requirements-claude-pptx.txt
npm --prefix plugins/student-presentation-suite ci
claude plugin marketplace add --scope user "$env:USERPROFILE\.agents\claude-plugins"
claude plugin install -s user student-presentation-suite@claude-personal
```

## Validation

```powershell
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json --strict
claude plugin validate --strict .\plugins\student-presentation-suite
claude plugin validate --strict .
```

Claude-specific changes are published only to `claude-code`; `main` remains the
separate Codex line.

## License

MIT. See [LICENSE](LICENSE).
