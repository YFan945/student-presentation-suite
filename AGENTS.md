# Repository Guidelines

## Project Structure & Module Organization

This repository is a local shared plugin marketplace root for Codex and Claude Code, plus a source
tree for agent skills that can also be reused by tools such as OpenCode.

- `.claude-plugin/marketplace.json`: shared marketplace manifest for Codex and Claude Code.
- `plugins/student-presentation-suite/`: plugin package.
- `plugins/student-presentation-suite/skills/`: agent skills.
- `plugins/student-presentation-suite/scripts/`: validation and bridge scripts.
- `plugins/student-presentation-suite/shared/`: reusable PPTX inspection code.
- `plugins/student-presentation-suite/tests/`: Python unit tests.
- `scripts/check_marketplace_release.py`: repository-level release check.

Generated PPTX, PNG, PDF, cache files, and `outputs/*` are ignored. Keep only `outputs/.gitkeep`.

## Build, Test, and Development Commands

Run commands from the repository root unless noted.

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
```

- `pytest` runs plugin unit tests.
- `check_plugin_release.py` validates plugin package structure.
- `check_marketplace_release.py` validates the shared marketplace manifest and paths.

Validate runtime manifests:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .\plugins\student-presentation-suite
```

## Coding Style & Naming Conventions

Use Python 3 with 4-space indentation, type hints where practical, and small single-purpose functions. Keep scripts CLI-friendly with `argparse`, `--json` output when useful, and deterministic exit codes. Use kebab-case for plugin and skill names, for example `student-presentation-ppt`; use snake_case for Python files and functions.

Do not hardcode machine-specific paths such as `C:\Users\...`; use relative paths or environment variables.

## Testing Guidelines

Tests use `unittest` and are run by both `pytest` locally and `unittest discover` in CI. Name test files `test_*.py`. When adding scripts, add focused tests for parsing, validation, and generated output. If a test imports plugin-local packages such as `shared`, ensure it works with `PYTHONPATH=plugins/student-presentation-suite`.

## Commit & Pull Request Guidelines

Recent commits use concise Chinese imperative messages, for example `修复 CI 测试导入路径` and `完善 marketplace 发布检查`. Keep commits scoped and descriptive.

Pull requests should include:

- summary of changed plugin behavior
- affected runtime or skill consumer: Codex, Claude Code, OpenCode, or shared files
- validation commands run
- screenshots or generated file notes when PPTX output changes

## Agent-Specific Instructions

Preserve the shared marketplace route:

- Codex uses default `Presentations` + `artifact-tool` + `imagegen`.
- Codex and Claude Code both install from `.claude-plugin/marketplace.json`.
- Claude Code also uses the plugin-local `.claude-plugin/plugin.json`.
- Do not reintroduce a separate root `marketplace.json` unless the shared marketplace design changes.

Root README covers repository installation; plugin README covers plugin behavior.
