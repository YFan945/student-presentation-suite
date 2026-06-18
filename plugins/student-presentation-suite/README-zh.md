# Student Presentation Suite 插件

[![Plugin](https://img.shields.io/badge/plugin-student--presentation--suite-111827)](.codex-plugin/plugin.json)
[![Python](https://img.shields.io/badge/python-3.x-3776AB)](scripts/validate_slide_spec.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

中文 | [English](README.md)

`student-presentation-suite` 是一个面向大学生课堂汇报的插件。它帮助 agent 完成汇报规划、可编辑 PPTX 生成/改进和已有成品审阅，并统一使用课堂可读性、讲稿、素材来源、反 AI 套话和小组汇报标准。

本插件采用聚焦的触发边界：请求需要形成明确的学生学业场景，并要求 PPT/幻灯片大纲、制作或改进 PPT/PPTX，或者审查已有 PPT 成品。单独出现 `course`、`competition` 等歧义词并不足以触发，应结合大学、作业、答辩、教师评分等上下文判断，必要时只问一个路由问题。通用演示、单独讲稿/Q&A、非学生场景的 deck 不应触发本插件。

本文只说明插件本体。仓库安装、marketplace 和 GitHub 项目说明见根目录 [README-zh.md](../../README-zh.md)。

## Skills

### `student-presentation`

当用户需要规划，而不是直接生成 PPTX 文件时使用。

它负责：

- 选题聚焦
- 大纲和页面顺序
- 逐页讲稿和转场
- 小组成员衔接
- Q&A 准备
- 可选 Slide Spec YAML，供后续生成 PPTX

### `student-presentation-ppt`

当用户要求 editable slides、PowerPoint、PPT、PPTX、渲染预览、可直接汇报的文件，或基于已有 deck 输出改进版时使用。

它负责：

- 生成可编辑 `.pptx`
- 基于审查结果输出已有 deck 的改进副本
- 生成 speaker notes
- 选择视觉风格
- 处理图片和素材来源策略
- 把 Slide Spec 转成 PPTX 生产输入
- 预览图/缩略图总览 QA
- 检查 PPTX、讲稿、页数和静态 XML 风险

Codex 路线仍使用默认 `Presentations` skill/plugin、`artifact-tool` 和 `imagegen`。Claude Code 路线使用 `document-skills` 中的 `pptx` skill，并通过 `scripts/` 下的桥接脚本适配 Slide Spec。

正式生成 PPTX 前：
- 在 Codex 中，确认 runtime 提供 `Presentations`、`artifact-tool` 和 `imagegen`。
- 在 Claude Code 中，先安装 `document-skills@anthropic-agent-skills`，再安装可选 Python/Node QA 依赖，并在插件目录运行 `python scripts/check_claude_pptx_env.py --json`。

### `student-presentation-review`

当用户提供已有 PPTX、PDF 导出、截图、讲稿、Slide Spec，或需要对比两个版本时使用。

它检查：

- 页面逻辑和叙事顺序
- 课堂投影可读性
- AI 写作模式风险
- 评分标准适配
- 讲稿质量
- 前后版本变化
- PPTX 静态 XML 风险信号

## 共享标准

三个 skill 共享以下标准：

- 已确认约束处理
- 课堂投影可读性
- 中文/英文汇报表达
- 需要英语时使用 B1-B2 难度
- 反 AI 套话改写
- 小组汇报衔接
- 图片和素材来源安全

共享规则采用明确的唯一来源：`references/shared-standards.md` 负责全套件路由、字号、密度、语言难度默认值、反 AI 表达和小组规则；`references/slide-spec.md` 负责结构化交接；`references/image-strategy.md` 负责素材来源和视觉策略。各 skill 的本地 reference 只增加任务专属规则，不另立一套通用标准。

默认字号要求：

- 中文正文：22pt 或更大
- 英文正文：20pt 或更大
- 标题、副标题、章节标题、卡片标题、图表标题、面板标签：24pt 或更大

## 输入

插件可以处理：

- 宽泛主题，但同一请求或既有上下文仍需明确这是学生学业 PPT 任务
- 课程/评分标准说明
- 大纲
- 资料笔记或研究材料
- Slide Spec YAML
- 已有 PPTX/PDF/截图
- 讲稿
- 前后两个版本的 deck

如果 PPTX 生成请求过于模糊，PPT skill 应追问关键生产约束，或提供“快速默认生成 / 先确认大纲 / 用户补充约束”的选择；不能静默编造网页来源、时事事实或评分要求。

需要用户确认视觉风格时，PPT skill 会列出完整风格菜单，把最适合当前主题的选项排在前面并说明理由，同时保留其余全部风格供选择。

选中的风格不是宽泛的氛围标签，而是可执行的生成控制。每个风格文件都规定颜色角色、版式几何、页面类型配方、图片处理、密度限制、图表/图解方式、fallback 布局和渲染验收点。

Slide Spec YAML 也可以承载已有 deck 改进交接字段：`source_deck`、`edit_intent`、`review_findings`、`preserve`、`change_summary_required`。

Slide Spec 校验同时检查 JSON Schema 和跨字段逻辑，包括页码与页数、总讲解时间、小组成员/owner，以及已有 deck 改进字段组合。

## 输出

PPTX 生成的典型输出：

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

`change-summary.md` 用于已有 deck 改进场景。

Claude Code 使用 Slide Spec 输入时，桥接脚本还可以生成：

```text
outputs/<topic>-claude-pptx-brief.md
```

## 运行路线

| 运行环境 | Manifest | PPTX 生产 |
| --- | --- | --- |
| Codex | `.codex-plugin/plugin.json` | 默认 `Presentations` skill/plugin + `artifact-tool` + `imagegen` |
| Claude Code | `.claude-plugin/plugin.json` | `document-skills` 插件中的 `pptx` skill |

Codex 依赖提示位于：

```text
skills/student-presentation-ppt/agents/openai.yaml
```

Claude Code 插件依赖声明位于：

```text
.claude-plugin/plugin.json
```

Claude Code 用户可以在仓库根目录按以下流程安装依赖插件和本地 marketplace：

```powershell
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin marketplace add <path-to-this-repository>
/plugin install student-presentation-suite@personal
```

然后在本插件目录安装 PPTX QA 依赖：

```powershell
python -m pip install -r requirements-claude-pptx.txt
npm install
python scripts/check_claude_pptx_env.py --json
```

## 辅助脚本

校验 Slide Spec：

```powershell
python scripts/validate_slide_spec.py path/to/slide-spec.yaml --json
```

从 Slide Spec 生成 Claude Code `pptx` 生产 brief。如果 spec 包含审查问题或原始 deck，生成的 brief 会转入 `pptx` editing workflow，并要求变更摘要：

```powershell
python scripts/slide_spec_to_pptx_brief.py path/to/slide-spec.yaml `
  --output outputs/<topic>-claude-pptx-brief.md
```

检查 Claude Code PPTX 环境：

```powershell
python scripts/check_claude_pptx_env.py --json
```

检查生成后的 PPTX 交付包：

```powershell
python skills/student-presentation-ppt/scripts/pptx_delivery_check.py `
  --pptx outputs/<topic>-presentation.pptx `
  --notes outputs/<topic>-speaker-notes.md `
  --preview outputs/<topic>-preview.png `
  --strict `
  --json
```

讲稿和预览默认是必需交付物；省略参数时脚本会根据 PPTX 文件名推导预期路径。只有明确不需要时才能使用 `--allow-missing-notes` 或 `--allow-missing-preview`，缺少预览意味着视觉 QA 未完成。

运行 PPTX 静态审阅：

```powershell
python skills/student-presentation-review/scripts/pptx_static_check.py path/to/deck.pptx --json
```

## 验证

在当前插件目录运行：

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python scripts/check_plugin_release.py
python scripts/check_claude_pptx_env.py --json
```

如果要在 Claude Code 中生成 PPTX 并做渲染 QA：

```powershell
python -m pip install -r requirements-claude-pptx.txt
npm install
```

LibreOffice 和 Poppler 是系统工具，仍需要单独安装。安装后运行 `python scripts/check_claude_pptx_env.py --json` 检查环境。

在仓库根目录运行：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
```

## 示例

参见 [examples/ai-learning-report.md](examples/ai-learning-report.md)，里面包含完整主题、大纲、Slide Spec YAML、讲稿样本和预期输出命名。

## License

MIT。见 [LICENSE](LICENSE)。
