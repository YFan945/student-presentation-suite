# Repository Guidelines

## Project Structure & Module Organization

This repository is a plugin marketplace root for Codex and Claude Code.

- `marketplace.json`: Codex marketplace manifest.
- `.claude-plugin/marketplace.json`: Claude Code marketplace manifest.
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
- `check_marketplace_release.py` validates root marketplace manifests and paths.

Validate runtime manifests:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
claude plugin validate .
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
- affected runtime: Codex, Claude Code, or both
- validation commands run
- screenshots or generated file notes when PPTX output changes

## Agent-Specific Instructions

Preserve both runtime routes:

- Codex uses default `Presentations` + `artifact-tool` + `imagegen`.
- Claude Code uses `document-skills` and its `pptx` skill.

Do not move marketplace files into the plugin package. Root README covers repository installation; plugin README covers plugin behavior.
