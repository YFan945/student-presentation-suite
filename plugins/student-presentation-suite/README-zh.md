# Student Presentation Suite 插件

[![Plugin](https://img.shields.io/badge/plugin-student--presentation--suite-111827)](.codex-plugin/plugin.json)
[![Python](https://img.shields.io/badge/python-3.x-3776AB)](scripts/validate_slide_spec.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

中文 | [English](README.md)

`student-presentation-suite` 是一个面向大学生课堂汇报的插件。它帮助 agent 完成汇报规划、可编辑 PPTX 生成和已有成品审阅，并统一使用课堂可读性、讲稿、素材来源、反 AI 套话和小组汇报标准。

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

当用户要求 editable slides、PowerPoint、PPT、PPTX、渲染预览或可直接汇报的文件时使用。

它负责：

- 生成可编辑 `.pptx`
- 生成 speaker notes
- 选择视觉风格
- 处理图片和素材来源策略
- 把 Slide Spec 转成 PPTX 生产输入
- 预览图/缩略图总览 QA
- 检查 PPTX、讲稿、页数和静态 XML 风险

Codex 路线仍使用默认 `Presentations` skill/plugin、`artifact-tool` 和 `imagegen`。Claude Code 路线使用 `document-skills` 中的 `pptx` skill，并通过 `scripts/` 下的桥接脚本适配 Slide Spec。

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

默认字号要求：

- 中文正文：22pt 或更大
- 英文正文：20pt 或更大
- 标题、副标题、章节标题、卡片标题、图表标题、面板标签：24pt 或更大

## 输入

插件可以处理：

- 宽泛主题
- 课程/评分标准说明
- 大纲
- 资料笔记或研究材料
- Slide Spec YAML
- 已有 PPTX/PDF/截图
- 讲稿
- 前后两个版本的 deck

如果 PPTX 生成请求过于模糊，PPT skill 应追问关键生产约束，或提供“快速默认生成 / 先确认大纲 / 用户补充约束”的选择；不能静默编造网页来源、时事事实或评分要求。

## 输出

PPTX 生成的典型输出：

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
```

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

## 辅助脚本

校验 Slide Spec：

```powershell
python scripts/validate_slide_spec.py path/to/slide-spec.yaml --json
```

从 Slide Spec 生成 Claude Code `pptx` 生产 brief：

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
  --json
```

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

LibreOffice 和 Poppler 是系统工具，仍需要单独安装。

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
