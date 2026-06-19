# Student Presentation Suite for Claude Code

Claude Code-only plugin providing three skills:

- `student-presentation`: outline and speaking plan
- `student-presentation-ppt`: editable PPTX creation and improvement
- `student-presentation-review`: existing-deck diagnosis and edit handoff

Install as `student-presentation-suite@claude-personal`. PPTX production uses
`document-skills@anthropic-agent-skills`; this package adds the student routing,
Slide Spec bridge, visual styles, runtime resolver, and delivery checks.

Runtime dependencies are not automatically installed by Claude Code. Use the
repository-level `scripts/install_claude_plugin.ps1` or install
`requirements-claude-pptx.txt` and run `npm ci`.

All user deliverables go to the active project `outputs/` directory. Plugin
resources are addressed through `${CLAUDE_PLUGIN_ROOT}` and must not receive
generated decks.

```powershell
python scripts/check_claude_pptx_env.py --json --strict
python scripts/slide_spec_to_pptx_brief.py <spec.yaml> --output-dir <project>\outputs
node scripts/run_with_pptxgenjs.js --probe
```

This package intentionally contains no `.codex-plugin`, `agents/openai.yaml`,
`artifact-tool`, or other Codex runtime declarations.
