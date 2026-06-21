# Student Presentation Suite for Codex

[中文](README-zh.md) | English

> This plugin package is built for **Codex**. Claude Code users should use the repository's [`claude-code` branch](https://github.com/YFan945/student-presentation-suite/tree/claude-code).

The plugin is strictly scoped to student academic PPT work: planning outlines, creating or editing editable PPTX files, and reviewing existing student decks. Company reports, teacher training, generic professional presentations, and standalone speeches/Q&A are out of scope. See [`references/suite-contract.md`](references/suite-contract.md).

## Install

Install from the repository root instead of copying this directory alone:

```powershell
git clone --branch main https://github.com/YFan945/student-presentation-suite.git
Set-Location .\student-presentation-suite
codex plugin marketplace add (Get-Location).Path
codex plugin add student-presentation-suite@personal
codex plugin list
```

Open a new Codex thread after installation. The manifest is [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json). PPTX production requires Codex `Presentations`; artifact-tool is an internal implementation detail.

## Usage

| Request | Skill | Output |
| --- | --- | --- |
| Student PPT outline or Slide Spec | `student-presentation` | Slide-by-slide outline and optional notes, transitions, and Q&A |
| Create, rebuild, or explicitly edit a PPTX | `student-presentation-ppt` | Editable PPTX, notes, preview, and QA |
| Review, score, or compare an existing deck | `student-presentation-review` | Prioritized findings, slide-level fixes, and scoring |
| Review, then explicitly modify the file | review → PPT skill | Separate improved PPTX and change summary |

Describe the task in a new thread, for example:

```text
Create an editable PPTX for a university innovation-project defense.
Use the attached material. The defense is 6 minutes, and judges focus on novelty,
implementation, and result validation. Include speaker notes and a preview.
```

```text
Review my uploaded university course presentation.
Prioritize findings as Critical, Major, or Minor and check story, density,
visual hierarchy, speaking difficulty, and AI-like wording.
```

If purpose, grading emphasis, content scope, style, or another high-impact choice remains unresolved, the PPT skill enforces a mandatory **Decision Gate** and waits for answers to 1–3 key questions before production.

## Output

```text
outputs/<topic>-outline.md
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

The original deck is never overwritten. See the repository-level [README.md](../../README.md) for full download, update, troubleshooting, and development instructions.
