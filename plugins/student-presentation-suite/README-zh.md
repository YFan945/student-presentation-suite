# Student Presentation Suite for Claude Code

中文 | [English](README.md)

仅适配 Claude Code 的学生汇报插件，覆盖汇报规划、可编辑 PPTX 生成/改进和 deck 审查。

## Skills

- `student-presentation`：选题、提纲、讲稿、转场、小组衔接和 Q&A。
- `student-presentation-ppt`：通过 `document-skills` 生成或改进可编辑 PPTX，包含视觉风格、Slide Spec 交接、变更摘要和渲染 QA。
- `student-presentation-review`：审查 PPTX/PDF/截图/Slide Spec 的逻辑、可读性、评分适配、AI 写作风险、讲稿和 PPTX 静态问题。

## 运行时

本目录仅服务 Claude Code：

- Manifest：`.claude-plugin/plugin.json`
- 必需插件：`document-skills@anthropic-agent-skills`
- PPTX 生产：`document-skills` 提供的 `pptx` skill
- 本地 QA 依赖：`requirements-claude-pptx.txt` 和 `package.json`

本目录不包含 `.codex-plugin`、Codex `agents/openai.yaml`、`artifact-tool` 或 Codex runtime 依赖声明。

## 安装

在仓库根目录运行：

```powershell
claude plugin marketplace add "<仓库路径>"
claude plugin install student-presentation-suite@personal
```

安装可选本地 QA 依赖：

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-claude-pptx.txt
npm install
python scripts/check_claude_pptx_env.py --json
```

LibreOffice 和 Poppler 是渲染 QA 使用的系统依赖。

## Slide Spec 桥接

```powershell
python scripts/slide_spec_to_pptx_brief.py <spec.yaml> `
  --output outputs/<topic>-claude-pptx-brief.md
```

生成的 brief 会把新 deck 路由到 `pptxgenjs.md`，把已有 deck 改进路由到 `editing.md`。不覆盖原始 deck，并生成 `outputs/<topic>-change-summary.md`。

## 验证

```powershell
python -m unittest discover -s tests
python scripts/check_plugin_release.py
claude plugin validate .
```
