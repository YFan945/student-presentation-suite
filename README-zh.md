# Claude Code Plugins

中文 | [English](README.md)

本目录是 `%USERPROFILE%\.agents\claude-plugins` 下仅适配 Claude Code 的插件 marketplace。

当前发布 `plugins/student-presentation-suite`。插件使用 `.claude-plugin/plugin.json`，依赖 `document-skills@anthropic-agent-skills`，并包含 Claude PPTX 环境检查和 Slide Spec 生产桥接脚本。

```text
.
├── .claude-plugin/marketplace.json
├── plugins/
│   └── student-presentation-suite/
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── shared/
│       ├── references/
│       └── tests/
├── scripts/check_marketplace_release.py
└── .github/workflows/validate.yml
```

## 安装

```powershell
claude plugin marketplace add "$env:USERPROFILE\.agents\claude-plugins"
claude plugin install student-presentation-suite@personal
```

## 依赖

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
python -m pip install -r plugins/student-presentation-suite/requirements-claude-pptx.txt
npm --prefix plugins/student-presentation-suite install
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json
```

LibreOffice 和 Poppler 是 PPTX 渲染 QA 使用的系统依赖。

## 验证

```powershell
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
claude plugin validate .\plugins\student-presentation-suite
```

独立 Codex marketplace 保留在同级目录 `%USERPROFILE%\.agents\plugins`。

## License

MIT。见 [LICENSE](LICENSE)。
