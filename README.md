# Student Presentation Suite — Academic PPT Plugin for Codex

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/runtime-Codex-111827)](plugins/student-presentation-suite/.codex-plugin/plugin.json)

[中文](README-zh.md) | English

> The `main` branch is built for **Codex**. If you use **Claude Code**, see the [`claude-code` branch](https://github.com/YFan945/student-presentation-suite/tree/claude-code) and do not follow the `main` installation steps.

`student-presentation-suite` supports student-owned academic presentation work:

- planning course reports, defenses, competitions, or research presentation outlines;
- creating, rebuilding, or explicitly editing editable PPTX files;
- reviewing, scoring, and diagnosing existing student decks.

It does not support company reports, sales decks, teacher training, generic professional presentations, standalone speeches/Q&A, or unexplained attachments. See the canonical [`references/suite-contract.md`](plugins/student-presentation-suite/references/suite-contract.md) for the full boundary.

## Download and install

### Option 1: clone with Git

Run in PowerShell:

```powershell
git clone --branch main https://github.com/YFan945/student-presentation-suite.git
Set-Location .\student-presentation-suite
```

If the directory already exists, use another empty directory name. Run the following commands from the downloaded repository root.

### Option 2: download ZIP

1. Open the [GitHub repository](https://github.com/YFan945/student-presentation-suite).
2. Choose **Code → Download ZIP**.
3. Extract it to a stable directory and open PowerShell in the repository root containing `.agents`, `plugins`, and `README.md`.

### Register the marketplace and install

This is not an auto-discovered Codex marketplace. Register the current repository root explicitly:

```powershell
codex plugin marketplace add (Get-Location).Path

python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json

codex plugin add student-presentation-suite@personal
codex plugin list
```

`codex plugin list` should show `student-presentation-suite@personal` as installed and enabled. Open a new Codex thread after installation so the three skills are loaded.

Actual PPTX production also requires the Codex `Presentations` capability. `imagegen` is optional.

## Usage

Describe the task naturally in a new Codex thread. Codex routes by requested outcome:

| Goal | Skill | Main result |
| --- | --- | --- |
| PPT outline or Slide Spec only | `student-presentation` | Slide-by-slide outline, optional notes, transitions, and Q&A |
| Create, rebuild, or explicitly edit a PPTX | `student-presentation-ppt` | Editable PPTX, notes, preview, and QA |
| Review, score, or compare an existing deck | `student-presentation-review` | Prioritized findings, slide-level fixes, and scoring |
| Review, then explicitly modify the file | review → PPT skill | Separate improved PPTX and change summary |

For reliable results, provide the course or competition, topic, audience, rubric, duration or slide count, language, individual/group format, source material, desired style, and content that must be preserved.

## Examples

### 1. Plan a course presentation

```text
Plan a university software engineering presentation about AI-assisted software testing.
It is for the instructor and classmates, in English, 8 minutes, and no more than 10 slides.
Include each slide title, key point, suggested visual, and speaker notes.
```

### 2. Create an editable PPTX

```text
Create an editable PPTX for a university innovation-project defense.
Use the attached project material. The defense is 6 minutes, and judges focus on novelty,
implementation, and result validation. Include speaker notes and a preview.
```

If purpose, grading emphasis, content scope, style, or another high-impact choice remains unresolved, the PPT skill enforces a mandatory **Decision Gate**. It asks only 1–3 key questions per round, provides mutually exclusive options, and waits for your choice before creating a slide plan or PPTX. You may explicitly delegate with “use the recommended options.”

### 3. Review an existing student deck

```text
Review my uploaded university course presentation.
Check story logic, slide density, visual hierarchy, speaking difficulty, and AI-like wording.
Prioritize findings as Critical, Major, or Minor and provide slide-level fixes and scores.
```

### 4. Review and edit the file

```text
Review this thesis-defense PPT and then edit the file based on the findings.
Preserve the cover, university template, and the experiment data on slide 4.
Do not overwrite the original. Return an improved PPTX and a change summary.
```

### Requests that do not trigger this plugin

```text
Create a quarterly company report deck.
Write a three-minute speech.
I uploaded a PPT.
```

These requests lack an eligible student academic PPT context, a clear outcome, or an explicit review/edit action.

## Output files

Depending on the task, files are normally written as:

```text
outputs/<topic>-outline.md
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

The original deck is never overwritten.

## Update

From the repository root:

```powershell
git pull origin main

python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py" `
  .\plugins\student-presentation-suite

python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json

codex plugin add student-presentation-suite@personal
```

Open a new Codex thread after reinstalling. Do not manually edit marketplace configuration.

## Troubleshooting

- **Plugin not found:** confirm PowerShell is at the repository root, then run `codex plugin marketplace add (Get-Location).Path`.
- **Old behavior after reinstall:** update the cachebuster, reinstall, and open a new thread.
- **PPTX cannot be generated:** confirm Codex `Presentations` is available. The plugin will not substitute a Markdown outline.
- **`Access denied` or `os error 5`:** close processes holding the Codex plugin cache, restart Codex and PowerShell, and retry.
- **Request does not trigger:** state the student academic context and specify outline, PPTX creation/editing, or deck review.

## Development

See [AGENTS.md](AGENTS.md). Main validation commands:

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
git diff --check
```

See [CHANGELOG.md](CHANGELOG.md) for version notes. Daily engineering logs use `Changelog-YYYY-MM-DD.md`.

## License

MIT. See [LICENSE](LICENSE).
