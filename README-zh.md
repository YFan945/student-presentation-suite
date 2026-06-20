# Codex Plugins

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

中文 | [English](README.md)

本目录是仅适配 Codex、需要显式注册的仓库型 marketplace，不是 Codex 默认自动发现的 personal marketplace 布局。

当前发布 `plugins/student-presentation-suite`。插件使用 `.codex-plugin/plugin.json` 和 Codex `Presentations` workflow，并可按需使用 `imagegen`，不包含 Claude Code manifest 或 `document-skills` 依赖。

```text
.
├── .agents/plugins/marketplace.json
├── plugins/
│   └── student-presentation-suite/
│       ├── .codex-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── shared/
│       ├── references/
│       └── tests/
└── .github/workflows/validate.yml
```

## 安装

```powershell
Set-Location "$env:USERPROFILE\.agents\plugins"
codex plugin marketplace add (Get-Location).Path
codex plugin add student-presentation-suite@personal
```

更新时必须从仓库 manifest 显式读取 marketplace 名称：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json
```

## 运行前提

- `student-presentation-ppt` 依赖 Codex `Presentations` 能力。
- PPTX 生产只使用 Codex 标准 presentation workflow，插件不内置第二套 PPTX 引擎。
- `imagegen` 是可选能力，只在视觉确有价值且用户允许时使用。
- 若 `Presentations` 不可用，PPT skill 必须明确报告缺失前提并停止，不能退化为大纲后宣称已生成 PPTX。恢复或安装 presentations 插件后，应在新线程重试。

## 验证

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
```

独立 Claude Code marketplace 位于同级目录 `%USERPROFILE%\.agents\claude-plugins`。

## License

MIT。见 [LICENSE](LICENSE)。
