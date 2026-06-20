# Student Presentation Suite for Codex

中文 | [English](README.md)

仅适配 Codex 的学生汇报插件，覆盖汇报规划、可编辑 PPTX 生成/改进和 deck 审查。

## Skills

- `student-presentation`：选题、提纲、讲稿、转场、小组衔接和 Q&A。
- `student-presentation-ppt`：生成或改进可编辑 PPTX，包含讲稿、视觉风格、Slide Spec 交接、变更摘要、预览和交付 QA。
- `student-presentation-review`：审查 PPTX/PDF/截图/Slide Spec 的逻辑、可读性、评分适配、AI 写作风险、讲稿和 PPTX 静态问题。

## 运行时

本目录仅服务 Codex：

- Manifest：`.codex-plugin/plugin.json`
- PPTX 生产：Codex `Presentations`；artifact-tool 仅是该标准 workflow 的内部实现细节
- 可选视觉生成：`imagegen`，只在确有价值且用户允许时使用
- Skill UI metadata：`skills/*/agents/openai.yaml`

本目录不再包含 `.claude-plugin`、`document-skills` 依赖、Claude 环境检查脚本或 Claude 生产 brief。

`student-presentation-ppt` 在生产前必须确认 `Presentations` 可用。若缺失，应报告前提并停止，不能用 Markdown 大纲冒充已生成 PPTX。恢复或安装 Codex presentations 插件后，应在新线程重试。

## 工作流

1. `student-presentation` 生成提纲或 Slide Spec。
2. `student-presentation-ppt` 通过 Codex presentation workflow 创建或改进 deck。
3. `student-presentation-review` 审查 deck，并可把问题交回 PPT skill 修改。
4. 不覆盖原始 deck；改进版使用新文件名并生成 `outputs/<topic>-change-summary.md`。

预期输出：

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

## 验证

在本插件目录运行：

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/check_plugin_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

生成文件和依赖目录由 `.gitignore` 忽略。

可直接校验的 Slide Spec 示例位于 `examples/ai-learning-report.yaml`。
