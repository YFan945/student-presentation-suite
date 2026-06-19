# Repository Guidelines

This directory is the Claude Code-only plugin marketplace.

GitHub publishing for this marketplace must use the `claude-code` branch of
`YFan945/student-presentation-suite`. Do not publish Claude Code plugin changes
to `main`.

- `.claude-plugin/marketplace.json`: Claude Code marketplace manifest.
- `plugins/student-presentation-suite/`: complete Claude Code plugin package.
- `scripts/check_marketplace_release.py`: repository-level release check.

Do not add Codex `.codex-plugin` manifests, `agents/openai.yaml`, `artifact-tool`, or Codex runtime dependencies here.

Run validation from this directory:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
claude plugin validate .\plugins\student-presentation-suite
```
