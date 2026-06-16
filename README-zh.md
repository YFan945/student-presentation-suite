# Student Presentation Suite

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/Codex-plugin-111827)](marketplace.json)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-5B35D5)](.claude-plugin/marketplace.json)

中文 | [English](README.md)

Student Presentation Suite 是一个同时适配 Codex 和 Claude Code 的本地插件 marketplace，用于大学生课堂汇报的规划、PPTX 生成和成品审阅。

当前包含一个插件：`student-presentation-suite`，内部有三个 skill：

- `student-presentation`：选题、提纲、讲稿、转场、小组衔接和 Q&A 准备。
- `student-presentation-ppt`：根据主题、大纲或 Slide Spec 生成可编辑 PPTX、讲稿和预览/交付 QA。
- `student-presentation-review`：审阅 PPTX/PDF/截图/Slide Spec，检查逻辑、可读性、评分适配、AI 写作风险和 PPTX 静态问题。

## 项目定位

课堂汇报不只是“生成几页 PPT”。这个插件把规划、PPTX 生产和审阅拆开，同时共享课堂投影可读性、素材来源、反 AI 套话、时间控制和小组分工标准。

本仓库以 marketplace 根目录组织，方便别人 clone 后直接安装使用。

## 目录结构

```text
.
├── marketplace.json
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── student-presentation-suite/
│       ├── .codex-plugin/plugin.json
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── shared/
│       ├── references/
│       └── tests/
└── .github/workflows/validate.yml
```

## 兼容性

| 运行环境 | 入口文件 | PPTX 路线 |
| --- | --- | --- |
| Codex | `marketplace.json` | 默认 `Presentations` skill/plugin + `artifact-tool` + `imagegen` |
| Claude Code | `.claude-plugin/marketplace.json` | `document-skills` 插件中的 `pptx` skill |

Claude Code 生成 PPTX 前，需要先安装 `document-skills@anthropic-agent-skills`。

## 安装

### Codex

把仓库克隆到本地插件 marketplace 目录：

```powershell
git clone https://github.com/YFan945/student-presentation-suite.git `
  "$env:USERPROFILE\.agents\plugins"
```

Codex marketplace manifest 位于：

```text
marketplace.json
```

插件路径是：

```json
"./plugins/student-presentation-suite"
```

### Claude Code

克隆同一个仓库后，按你的 Claude Code 本地插件流程添加/安装 marketplace。Claude Code marketplace manifest 位于：

```text
.claude-plugin/marketplace.json
```

使用 PPTX 生成功能前，先安装 Anthropic document skills：

```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

## 使用方式

可以直接围绕三个工作流使用：

- 从主题规划课堂汇报。
- 根据大纲或 Slide Spec 生成可编辑 PPTX。
- 审阅已有 PPTX、PDF 导出、截图或 Slide Spec。

更多插件本体说明见：

- [插件中文文档](plugins/student-presentation-suite/README-zh.md)
- [Plugin README](plugins/student-presentation-suite/README.md)
- [示例汇报 brief](plugins/student-presentation-suite/examples/ai-learning-report.md)

## 开发与验证

安装校验依赖：

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
```

从仓库根目录运行测试和发布检查：

```powershell
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json
```

校验插件 manifest：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
claude plugin validate .
```

## 说明

- 生成的 PPTX、PNG、PDF 和缓存文件默认不会提交。
- 根 `marketplace.json` 给 Codex 使用。
- 根 `.claude-plugin/marketplace.json` 给 Claude Code 使用。
- 插件本体在 `plugins/student-presentation-suite`。

## License

MIT。见 [LICENSE](LICENSE)。
