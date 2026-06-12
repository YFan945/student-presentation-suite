# Student Presentation Suite

[![Plugin](https://img.shields.io/badge/Codex-plugin-111827)](#)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](.codex-plugin/plugin.json)
[![Python](https://img.shields.io/badge/python-3.x-3776AB)](skills/student-presentation-review/scripts/pptx_static_check.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](README.md)

Student Presentation Suite 是一个面向大学生课堂汇报的 Codex 插件。它把工作流拆成规划、可编辑 PPTX 生成和成品审阅三个阶段，让 Codex 根据任务自动使用合适的 skill。

## 功能

- `student-presentation`：选题聚焦、大纲规划、逐页内容、讲稿、转场、小组衔接、Q&A 答辩准备和可选 Slide Spec YAML。
- `student-presentation-ppt`：生成可编辑 `.pptx`，包含讲稿文件、视觉风格预设、有效视觉素材、主题化输出命名和预览/联系页 QA。
- `student-presentation-review`：审阅已有 PPTX/PDF/截图/Slide Spec，覆盖逻辑、可读性、AI 写作模式风险、评分标准、讲稿、版本对比和 PPTX XML 静态检查。

## 仓库结构

```text
.
├── .codex-plugin/plugin.json
├── examples/
├── references/
├── skills/
│   ├── student-presentation/
│   ├── student-presentation-ppt/
│   └── student-presentation-review/
└── outputs/
```

## 安装

把仓库复制或克隆到本地 Codex 插件目录，然后重启或刷新 Codex 插件发现。

```powershell
git clone https://github.com/YFan945/student-presentation-suite.git `
  "$env:USERPROFILE\.agents\plugins\plugins\student-presentation-suite"
```

PPTX 生成依赖已安装的 `Presentations` skill/plugin。静态审阅脚本需要 Python 3。

如果按上面的命令克隆到 `$env:USERPROFILE\.agents\plugins\plugins\student-presentation-suite`，个人 marketplace 入口 `$env:USERPROFILE\.agents\plugins\marketplace.json` 中该插件的 `source.path` 应指向这个真实目录：

```json
"./.agents/plugins/plugins/student-presentation-suite"
```

## 典型工作流

### 先出大纲，再做 PPTX

1. 使用 `student-presentation` 聚焦选题并生成大纲。
2. 如果后续要生成 PPTX，要求输出 Slide Spec YAML。
3. 使用 `student-presentation-ppt` 根据大纲或 Slide Spec 生成可编辑 PPTX。

### 生成 PPTX

提供主题、大纲、资料或 Slide Spec YAML。PPT skill 默认产出：

- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` 或联系页

最终回复应包含绝对路径、页数、时间安排、小组顺序，以及无法完成的验证项。

PPT 生成遵循“创意方向 + 质量护栏”模式：先选择适合主题的 creative direction，再根据 slide function 设计版式。`timeline`、`comparison-cards`、`process`、`risk-callout`、`summary-qa` 等 layout 表示要完成的表达功能，不代表固定模板。字号、密度、对比度、素材来源和交付检查仍是硬性底线。

### 审阅已有 PPT

提供 PPTX、导出的 PDF、截图、联系页、讲稿、Slide Spec YAML，或两个版本用于对比。审阅 skill 会优先指出影响理解、评分和现场表达的问题。

## 共享标准

三个 skill 共享以下规范：

- 已确认约束的传递与处理
- 课堂投影可读性
- 反 AI 套话和 AI 写作模式风险
- B1-B2 英语汇报风格
- 中文汇报表达规范
- 小组汇报成员衔接
- 图片和素材来源策略

默认排版要求：

- 中文正文：22pt 或更大
- 英文正文：20pt 或更大
- 标题、副标题、章节标题、卡片标题、图表标题、面板标签等：24pt 或更大

## PPTX 静态检查

运行 XML 风险检查：

```powershell
python skills/student-presentation-review/scripts/pptx_static_check.py path/to/deck.pptx --json
```

自动化检查中，如果希望文件格式错误或 XML 扫描失败时返回非 0 退出码，可以加 `--strict`：

```powershell
python skills/student-presentation-review/scripts/pptx_static_check.py path/to/deck.pptx --json --strict
```

静态检测只提供风险信号。它不能完整解析从母版或主题继承的字号，也可能漏掉表格、图表、SmartArt、图片内文字和真实渲染溢出。重要问题应尽量结合预览图或联系页确认。

## PPTX 交付检查

生成 PPTX 后，可以检查交付文件是否真实存在、PPTX 页数和静态 XML 风险摘要：

```powershell
python skills/student-presentation-ppt/scripts/pptx_delivery_check.py `
  --pptx outputs/ai-learning-report-presentation.pptx `
  --notes outputs/ai-learning-report-speaker-notes.md `
  --preview outputs/ai-learning-report-preview.png `
  --json
```

该检查不会渲染幻灯片，不能替代预览图或联系页的视觉 QA。

## 本地维护与验证

修改插件后先运行 manifest 校验：

```powershell
python C:\Users\28603\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py `
  C:\Users\28603\.agents\plugins\plugins\student-presentation-suite
```

需要让 Codex 重新加载本地插件时，使用 cachebuster helper 更新版本：

```powershell
python C:\Users\28603\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py `
  C:\Users\28603\.agents\plugins\plugins\student-presentation-suite
codex plugin add student-presentation-suite@personal
```

重新安装后开新线程测试 3 个 skills：`student-presentation`、`student-presentation-ppt`、`student-presentation-review`。

## 示例

参见 [examples/ai-learning-report.md](examples/ai-learning-report.md)，里面包含端到端示例：选题、大纲、Slide Spec YAML、讲稿样本和预期 PPTX 输出命名。

## 维护

- 以 `README-zh.md` 作为主要用户文档。
- 工作流或行为有较大改动时，同步更新中英文 README。
- 除非是刻意保留的示例，不要把生成的 PPTX、PNG 和其他输出文件提交到 git。

## License

MIT。见 [LICENSE](LICENSE)。
