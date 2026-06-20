# Student Presentation Suite for Codex

中文 | [English](README.md)

仅适配 Codex、严格限定于学生学术 PPT。通用演示、商业汇报、教师培训、独立演讲稿或独立 Q&A 不属于插件范围。

## 路由

| 用户目标 | Skill | 结果 |
| --- | --- | --- |
| 学生 PPT 大纲或 Slide Spec | `student-presentation` | 大纲及可选的配套讲稿、转场、Q&A 和交接 |
| 创建、重建或明确修改学生 PPTX | `student-presentation-ppt` | 可编辑 PPTX、讲稿、预览和 QA |
| 审查或评分已有学生 deck/export | `student-presentation-review` | 基于证据的问题与具体修改建议 |
| 审查并明确要求修改文件 | review → PPT skill | 单独保存的改进版 deck 和变更摘要 |

讲稿、Q&A 和小组衔接只能作为合格 PPT 任务的配套输出，不能单独触发插件。规范边界以 `references/suite-contract.md` 为准。

## PPTX Decision Gate

开始制作前，PPT skill 必须读取已有对话、附件和 Slide Spec，并识别尚未确定的高影响决策。每轮只问 1–3 个问题；每个问题提供 2–4 个结合主题的互斥选项，将推荐项放在最前，并说明选择影响，然后等待用户决定。

当目标、受众或评分重点、内容范围等关键决策仍未解决时，不得开始制作。只有低风险细节或用户明确说“你决定”“按推荐方案”时才能采用默认值，并须先列出最终假设。

## 运行时与输出

- Manifest：`.codex-plugin/plugin.json`
- PPTX 生产：Codex `Presentations`；artifact-tool 只是内部实现细节
- 可选视觉：`imagegen`，只在有价值且获得允许时使用
- 结构化交接：Slide Spec
- 永不覆盖原始 deck

PPTX 预期输出：

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

如果 `Presentations` 不可用，PPT skill 必须停止并报告缺失前提，不能用文本大纲冒充 PPTX。

## 验证

在插件目录运行：

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/check_plugin_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

本插件明确不包含 `.claude-plugin`、`document-skills`、Claude production bridge 或第二套 PPTX 引擎。
