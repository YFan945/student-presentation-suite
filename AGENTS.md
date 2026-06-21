# Repository Guidelines

## Repository Scope

This repository tracks the `student-presentation-suite` marketplace. The `claude-code` branch carries the Claude Code-adapted plugin package; `main` keeps the repository packaging and documentation aligned. It publishes one plugin: `plugins/student-presentation-suite`.

The plugin is strictly limited to student-owned academic PPT outlines, editable PPTX production/improvement, and review of existing student presentation artifacts.

Do not add or advertise:

- On `main`, Claude Code `.claude-plugin` manifests;
- `document-skills`, Claude environment checks, or Claude production bridges;
- `pptxgenjs` or a second PPTX engine;
- generic business, company, teacher-training, or professional presentation support;
- standalone script/Q&A behavior as a plugin trigger.

The Claude Code-adapted package is maintained on the `claude-code` branch.

## Source of Truth

- `.agents/plugins/marketplace.json`: repository marketplace manifest.
- `plugins/student-presentation-suite/.codex-plugin/plugin.json`: plugin metadata and cachebuster version.
- `plugins/student-presentation-suite/references/suite-contract.md`: canonical scope, routing, decision authority, runtime boundary, and cross-skill handoff.
- `plugins/student-presentation-suite/references/shared-standards.md`: readability, density, language, anti-AI wording, and group standards.
- `plugins/student-presentation-suite/references/slide-spec.md` and schema: structured planning and review-to-edit handoff.
- `plugins/student-presentation-suite/references/image-strategy.md`: image source and fallback policy.
- Skill-local references: task-specific execution rules only.

Do not duplicate canonical rules across multiple Skill entrypoints. Update the owner document and link to it.

## Skill Boundaries

- `student-presentation`: PPT/slide outline or Slide Spec only. Speaker notes, transitions, Q&A, and handoffs are supporting outputs; no PPTX creation.
- `student-presentation-ppt`: actual PPTX creation, rebuild, or explicitly authorized edit. Owns production planning, visual direction, rendering, and QA.
- `student-presentation-review`: review, scoring, comparison, and diagnosis. Advice by default; file editing requires explicit authorization and handoff to the PPT skill.

Keep all three Skill names backward-compatible.

Each `SKILL.md` must remain at or below 65 lines. Move detailed rules into selectively loaded references instead of growing entrypoints.

## Mandatory Decision Gate

When PPTX production has unresolved high-impact decisions:

1. inspect the conversation, attachments, source deck, rubric, and Slide Spec first;
2. ask only 1–3 highest-impact questions in the current round;
3. provide 2–4 mutually exclusive, topic-specific options per question;
4. put the recommended option first and explain each impact;
5. wait for the user’s choice before creating a slide plan or PPTX.

Defaults may cover low-risk details only. They must not bypass purpose, audience/grading emphasis, content scope, or similarly material decisions. Explicit delegation such as “你决定” permits recommended defaults, but assumptions must be stated before production.

## Project Layout

```text
.agents/plugins/marketplace.json
.github/workflows/validate.yml
plugins/student-presentation-suite/
  .codex-plugin/plugin.json
  assets/
  examples/
  references/
  scripts/
  shared/
  skills/
  tests/
scripts/check_marketplace_release.py
```

Generated PPTX/PNG files, output contents, dependency folders, and caches are ignored. Preserve `outputs/.gitkeep`.

## Coding and Documentation Style

- Use Python 3.11-compatible code, 4-space indentation, type hints where practical, and small single-purpose functions.
- Keep CLI scripts deterministic, with `argparse`, useful `--json` output, and non-zero exit codes on validation failure.
- Use kebab-case for plugin/Skill names and snake_case for Python modules/functions.
- Never hardcode user-specific absolute paths in repository files.
- Keep English and Chinese README files semantically aligned.
- Update root README files and plugin README files after material behavior, installation, output, or validation changes.
- Add or update `Changelog-YYYY-MM-DD.md` for substantial daily work and maintain newest-first `CHANGELOG.md` for version-level releases.

## Marketplace and Update Rules

This repository is not the default auto-discovered personal marketplace. Register the repository root explicitly.

Always read the marketplace name with:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json
```

Do not hand-edit marketplace configuration during routine plugin updates. Preserve the existing marketplace entry unless the release intentionally changes marketplace metadata.

For local plugin updates:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py" `
  .\plugins\student-presentation-suite
codex plugin add student-presentation-suite@personal
```

Open a new thread after reinstalling.

## Validation

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
python -m py_compile `
  plugins/student-presentation-suite/scripts/check_plugin_release.py `
  plugins/student-presentation-suite/scripts/validate_slide_spec.py `
  plugins/student-presentation-suite/skills/student-presentation-ppt/scripts/pptx_delivery_check.py `
  plugins/student-presentation-suite/skills/student-presentation-review/scripts/pptx_static_check.py `
  scripts/check_marketplace_release.py
git diff --check
```

Do not claim completion from documentation or validator text alone. Report the commands actually run and their results.

## Tests

- Tests use `unittest`; name files `test_*.py`.
- Add behavior-contract tests when changing trigger gates, routing, authorization, Decision Gate, runtime prerequisites, or outputs.
- Add release-check assertions for structural invariants that must not regress.
- Preserve tests for Slide Spec validation, static PPTX inspection, delivery QA, existing-deck handoff, and all visual style controls.

## Commit and Release Guidance

- Use concise Chinese imperative commit messages consistent with recent history.
- Keep generated artifacts and unrelated local changes out of commits.
- Before pushing, fetch the target branch and inspect `origin/main..HEAD` and `HEAD..origin/main`.
- For a direct `main` release, require a clean validation pass and verify the remote SHA after pushing.
- Do not create tags or GitHub releases unless explicitly requested.
