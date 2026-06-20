# Repository Guidelines

This directory is a Codex-only, explicitly registered repository marketplace.

- `.agents/plugins/marketplace.json`: repository marketplace manifest.
- `plugins/student-presentation-suite/`: complete Codex plugin package.
- `scripts/check_marketplace_release.py`: repository-level release check.

Do not add Claude Code `.claude-plugin` manifests, `document-skills`, Claude PPTX environment checks, or Claude production bridges here. The independent Claude Code marketplace lives at sibling path `..\claude-plugins`.

This is not the default auto-discovered personal marketplace layout. Register the repository root explicitly. When reading the marketplace name, always pass:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json
```

Run validation from this directory:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .\plugins\student-presentation-suite
```
