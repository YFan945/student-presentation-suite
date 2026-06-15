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
├── .github/workflows/
├── examples/
├── references/
├── scripts/
├── shared/
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

PPTX 生成依赖已安装的 `Presentations` skill/plugin 和 artifact-tool presentation 导出运行时。PPTX 静态检查只使用 Python 3 标准库。Slide Spec 校验需要 `requirements.txt` 中的依赖：

```powershell
python -m pip install -r requirements.txt
```

各 skill 的 `agents/openai.yaml` 使用 `dependencies.tools` 表示当前 Codex 插件校验器支持的依赖提示。这些条目描述运行时能力，例如 `Presentations`、`artifact-tool`、`imagegen` 或 `python`；它们不是 Python 包依赖。

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

如果需求还比较模糊，PPT skill 应先追问清楚再产出文件。关键问题包括是否需要先出大纲、PPT 页数、语言、汇报时长、课程/评分标准、听众、小组分工、资料来源、视觉风格、模板/logo 要求，以及图片/素材来源偏好。

提供主题、大纲、资料或 Slide Spec YAML。PPT skill 默认产出：

- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` 或联系页

最终回复应包含绝对路径、页数、时间安排、小组顺序，以及无法完成的验证项。

PPT 生成遵循“创意方向 + 质量护栏”模式：先选择适合主题的 creative direction，再根据 slide function 设计版式。`timeline`、`comparison-cards`、`process`、`risk-callout`、`summary-qa` 等 layout 表示要完成的表达功能，不代表固定模板。字号、密度、对比度、素材来源和交付检查仍是硬性底线。

内置风格库包括 `Academic Rigorous`（学术严谨）、`Modern Minimal`（现代简洁）、`Data Driven`（数据驱动）、`Creative Student`（学生创意）、`Midnight Business`（深蓝商务）、`Forest Moss`（森林苔藓）、`Coral Energy`（珊瑚活力）、`Warm Terracotta`（暖陶人文）、`Ocean Tech`（海洋科技）、`Charcoal Editorial`（炭黑杂志）、`Teal Trust`（青绿可信）、`Berry Cream`（莓果奶油）、`Sage Calm`（鼠尾草平静）和 `Cherry Bold`（樱桃醒目）。用户不确定风格时，PPT skill 应根据主题给出 3-5 个候选，而不是直接默认一种风格。

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

静态检测逻辑集中在共享模块 `shared/pptx_static_core.py`，由审阅脚本和交付检查脚本复用。它只提供风险信号，可解析常见的 Slide Layout / Slide Master 继承字号，但仍可能漏掉复杂主题行为、图表、SmartArt、图片内文字和真实渲染溢出。重要问题应尽量结合预览图或联系页确认。

## Slide Spec 校验

用共享 Schema 校验 Slide Spec YAML：

```powershell
python scripts/validate_slide_spec.py path/to/slide-spec.yaml --json
```

Schema 文件：`references/slide-spec.schema.json`。

## PPTX 交付检查

生成 PPTX 后，可以检查交付文件是否真实存在、PPTX 页数和静态 XML 风险摘要：

```powershell
python skills/student-presentation-ppt/scripts/pptx_delivery_check.py `
  --pptx outputs/ai-learning-report-presentation.pptx `
  --notes outputs/ai-learning-report-speaker-notes.md `
  --preview outputs/ai-learning-report-preview.png `
  --json
```

该检查不会渲染幻灯片，不能替代预览图或联系页的视觉 QA。它会输出风险类型 breakdown，并把页脚、页码、caption、kicker 等可能可接受的小字号提示，与更需要人工复核的 blocker-like 风险区分开。

### PPTX 生成排错

通过 artifact-tool 生成可编辑 PPTX 时，先跑一页 smoke test，再批量生成整套 deck。确认坐标、填充、文字、讲稿、PPTX 导出和 PNG 预览都正确。当前 artifact-tool 的 shape position API 使用 `left`、`top`、`width`、`height`；误用 `x`/`y` 可能导出有效文件，但渲染版式会坏。Windows 下如果 helper 脚本找不到 bundled runtime，先把 `HOME` 设为 `$env:USERPROFILE`；生成 contact sheet 需要 Python 时，把 `PYTHON` 指到 bundled Python。

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
- `README.md` 作为英文镜像，面向仓库访客。行为变化时先更新 `README-zh.md`，再把操作性内容同步到 `README.md`。
- 除非是刻意保留的示例，不要把生成的 PPTX、PNG 和其他输出文件提交到 git。

## License

MIT。见 [LICENSE](LICENSE)。
