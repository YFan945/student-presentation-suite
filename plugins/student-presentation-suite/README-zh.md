# Student Presentation Suite for Claude Code

仅适配 Claude Code，包含三个 skill：

- `student-presentation`：大纲和口播规划
- `student-presentation-ppt`：可编辑 PPTX 新建与改进
- `student-presentation-review`：已有 deck 审查和编辑交接

安装 ID 为 `student-presentation-suite@claude-personal`。PPTX 底层生产使用
`document-skills@anthropic-agent-skills`；本插件负责学生场景路由、Slide Spec、
视觉风格、runtime resolver 和交付检查。

Claude Code 不会自动安装本包的 Python/Node runtime 依赖。请使用仓库根目录的
`scripts/install_claude_plugin.ps1`，或手动安装
`requirements-claude-pptx.txt` 并执行 `npm ci`。

所有用户交付物写入当前项目的 `outputs/`。插件资源通过
`${CLAUDE_PLUGIN_ROOT}` 定位，不得把生成的 deck 写入插件目录。

```powershell
python scripts/check_claude_pptx_env.py --json --strict
python scripts/slide_spec_to_pptx_brief.py <spec.yaml> --output-dir <project>\outputs
node scripts/run_with_pptxgenjs.js --probe
```

本包不包含 `.codex-plugin`、`agents/openai.yaml`、`artifact-tool` 或其他
Codex runtime 声明。
