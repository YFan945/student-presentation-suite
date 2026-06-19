# Claude Code Plugins

中文 | [English](README.md)

这是仅适配 Claude Code 的插件 marketplace，只从
[`claude-code`](https://github.com/YFan945/student-presentation-suite/tree/claude-code)
分支发布。marketplace 名称为 `claude-personal`。

## 安装或迁移

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install_claude_plugin.ps1 -Migrate
```

脚本会：

- 不触碰 Codex 工作区
- 删除旧 Claude `personal` 注册项及对应插件缓存
- 安装 Python 和 Node 依赖
- 注册 `claude-personal`
- 安装 `document-skills@anthropic-agent-skills`
- 安装并验证 `student-presentation-suite@claude-personal`

安装后重启 Claude Code。

## 手动开发安装

```powershell
git clone --branch claude-code --single-branch `
  git@github.com:YFan945/student-presentation-suite.git `
  "$env:USERPROFILE\.agents\claude-plugins"
python -m pip install -r plugins/student-presentation-suite/requirements.txt
python -m pip install -r plugins/student-presentation-suite/requirements-claude-pptx.txt
npm --prefix plugins/student-presentation-suite ci
claude plugin marketplace add --scope user "$env:USERPROFILE\.agents\claude-plugins"
claude plugin install -s user student-presentation-suite@claude-personal
```

## 验证

```powershell
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json --strict
claude plugin validate --strict .\plugins\student-presentation-suite
claude plugin validate --strict .
```

Claude 专用修改只上传到 `claude-code`；`main` 保留为独立 Codex 路线。

## License

MIT。见 [LICENSE](LICENSE)。
