# Personal Plugins Marketplace

这是一个同时适配 Codex 和 Claude Code 的本地插件 marketplace 仓库。

## 目录结构

```text
.
├── marketplace.json                 # Codex marketplace manifest
├── .claude-plugin/marketplace.json   # Claude Code marketplace manifest
├── .github/workflows/                # GitHub CI
├── plugins/
│   └── student-presentation-suite/   # 插件本体
└── README.md / README-zh.md
```

## 插件

- `student-presentation-suite`：大学生课堂汇报规划、PPTX 生成和成品审阅。

插件本体文档见：

- [中文文档](plugins/student-presentation-suite/README-zh.md)
- [English README](plugins/student-presentation-suite/README.md)

## Codex 使用

Codex marketplace 文件是根目录的 `marketplace.json`。插件路径应相对本仓库根目录：

```json
"path": "./plugins/student-presentation-suite"
```

`student-presentation-suite` 在 Codex 下仍依赖默认 `Presentations` skill/plugin、`artifact-tool` 和 `imagegen`。这些依赖保留在：

```text
plugins/student-presentation-suite/skills/student-presentation-ppt/agents/openai.yaml
```

## Claude Code 使用

Claude Code marketplace 文件是：

```text
.claude-plugin/marketplace.json
```

`student-presentation-suite` 的 Claude 插件 manifest 位于：

```text
plugins/student-presentation-suite/.claude-plugin/plugin.json
```

Claude Code 的 PPTX 生成依赖 `document-skills`，通常先安装：

```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

## 验证

从仓库根目录运行：

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json
```

Codex / Claude Code manifest 校验：

```powershell
python C:\Users\28603\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py `
  C:\Users\28603\.agents\plugins\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
claude plugin validate .
```

