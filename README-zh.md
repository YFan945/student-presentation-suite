# 本地 Agent Skills Marketplace

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Marketplace](https://img.shields.io/badge/Agent-marketplace-111827)](.claude-plugin/marketplace.json)

中文 | [English](README.md)

这个仓库是 Codex 和 Claude Code 共享的本地 marketplace，位置是 `%USERPROFILE%\.agents\plugins`。两个运行时共用同一个市场文件：`.claude-plugin/marketplace.json`。它也保存给 OpenCode 等工具复用的 skill 源文件。

父级 `.agents` 目录会把旧的 marketplace 实验放在 `archive/`；当前这个 `plugins/` 目录是唯一活跃的 marketplace 根目录。

当前发布一个插件：`student-presentation-suite`，内部有三个 skill：

- `student-presentation`：选题、提纲、讲稿、转场、小组衔接和 Q&A 准备。
- `student-presentation-ppt`：根据主题、大纲、Slide Spec 或已有 deck 审查结果生成/改进可编辑 PPTX、讲稿、变更摘要和交付 QA。
- `student-presentation-review`：审阅 PPTX/PDF/截图/Slide Spec，检查逻辑、可读性、评分适配、AI 写作风险和 PPTX 静态问题。

## 目录结构

```text
.
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

`.claude-plugin/marketplace.json` 是 Codex 和 Claude Code 共享的 marketplace manifest，指向插件本体：`plugins/student-presentation-suite`。

## 安装

Codex 使用同一个市场文件：

```powershell
codex plugin marketplace add "$env:USERPROFILE\.agents\plugins"
codex plugin add student-presentation-suite@personal
```

Claude Code 使用同一个市场文件：

```powershell
claude plugin marketplace add "$env:USERPROFILE\.agents\plugins"
claude plugin install student-presentation-suite@personal
```

在 Claude Code chat 里，等价 slash 命令是：

```text
/plugin marketplace add <path-to-this-repository>
/plugin install student-presentation-suite@personal
```

共享 marketplace 条目通过下面的相对路径指向插件本体：

```json
"source": "./plugins/student-presentation-suite"
```

Codex 生成 PPTX 需要 Codex runtime 中已有默认 `Presentations` skill/plugin、`artifact-tool` 和 `imagegen`。Claude Code 生成 PPTX 使用插件 README 中记录的插件内 Claude 元数据和 `document-skills` 路线。

## 其他 Agent 工具

OpenCode 或类似工具应直接消费 `plugins/student-presentation-suite/skills/` 下的 skill 源文件，或读取它们支持的插件本体元数据。

## 开发与验证

安装校验依赖：

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
```

从仓库根目录运行测试和发布检查：

```powershell
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
```

校验运行时 manifest：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
claude plugin validate .
claude plugin validate .\plugins\student-presentation-suite
```

## 说明

- 生成的 PPTX、PNG、PDF、依赖目录和缓存文件默认不会提交。
- `plugins/student-presentation-suite/README-zh.md` 说明插件行为。
- 根 README 说明 Codex 和 Claude Code 共享 marketplace 的结构与安装方式。

## License

MIT。见 [LICENSE](LICENSE)。
