# Student Presentation Suite — Codex Marketplace

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/runtime-Codex-111827)](plugins/student-presentation-suite/.codex-plugin/plugin.json)

中文 | [English](README.md)

本仓库是仅适配 Codex、需要显式注册的本地 marketplace，发布 `student-presentation-suite`。插件严格限定于学生主导的学术 PPT：

- 规划 PPT 大纲或 Slide Spec；
- 创建或改进可编辑 PPTX；
- 审查、评分或诊断已有学生 deck。

通用演示、公司汇报、教师培训、独立演讲稿/Q&A 和 Claude Code 生产不属于本仓库范围。独立 Claude Code 版本位于同级目录 `..\claude-plugins`。

## 插件行为

| 用户目标 | Skill | 交付物 |
| --- | --- | --- |
| 学生 PPT 大纲或 Slide Spec | `student-presentation` | 大纲及可选配套讲稿、转场、Q&A 和小组交接 |
| 创建、重建或明确修改学生 PPTX | `student-presentation-ppt` | 可编辑 PPTX、讲稿、预览/contact sheet 和 QA |
| 审查或评分已有学生 deck/export | `student-presentation-review` | 分级问题、逐页修改建议和可选评分 |
| 审查并明确要求修改文件 | review → PPT skill | 单独保存的改进版 deck 和变更摘要 |

讲稿、Q&A 和小组衔接只能作为合格 PPT 任务的配套输出，不能单独触发插件。

### 强制 PPTX Decision Gate

开始制作前，`student-presentation-ppt` 必须读取已有对话、附件、源 deck、评分标准和 Slide Spec。若仍缺少高影响决策，必须：

1. 当前轮次只提出最重要的 1–3 个问题；
2. 每个问题提供 2–4 个结合主题的互斥选项；
3. 将推荐项放在最前，并说明每个选项的影响；
4. 等待用户选择后，才能创建 slide plan 或 PPTX。

默认值不能绕过目标、受众/评分重点、内容范围等关键决策。用户明确说“你决定”或“按推荐方案”时，skill 可以代为选择，但必须在制作前列出最终假设。

## 仓库结构

```text
.
├── .agents/plugins/marketplace.json
├── .github/workflows/validate.yml
├── plugins/
│   └── student-presentation-suite/
│       ├── .codex-plugin/plugin.json
│       ├── assets/
│       ├── examples/
│       ├── references/
│       ├── scripts/
│       ├── shared/
│       ├── skills/
│       └── tests/
├── scripts/check_marketplace_release.py
├── AGENTS.md
├── CHANGELOG.md
└── Changelog-YYYY-MM-DD.md
```

关键职责：

- `.agents/plugins/marketplace.json`：仓库 marketplace 注册清单。
- `.codex-plugin/plugin.json`：插件版本、UI 提示和能力元数据。
- `references/suite-contract.md`：插件范围、路由、决策授权和运行时边界的唯一规范。
- `references/shared-standards.md`：可读性、信息密度、语言、反 AI 套话和小组汇报规范。
- `skills/*/SKILL.md`：精简 Skill 入口；详细规则通过 references 按需加载。
- `scripts/check_plugin_release.py`：插件包发布契约。
- `scripts/check_marketplace_release.py`：仓库 marketplace 发布契约。

## 环境要求

- Python 3.11+。
- 实际制作 PPTX 时需要 Codex `Presentations` 能力。
- `imagegen` 为可选能力，只在生成视觉确有价值且用户允许时使用。
- Python 依赖见 `plugins/student-presentation-suite/requirements.txt`。

本插件明确不包含 `.claude-plugin`、`document-skills`、Claude 环境检查、Claude production bridge、`pptxgenjs` 或第二套 PPTX 引擎。

## 安装

本仓库不是 Codex 默认自动发现的 personal marketplace 布局，必须显式注册仓库根目录：

```powershell
Set-Location "$env:USERPROFILE\.agents\plugins"
codex plugin marketplace add (Get-Location).Path
codex plugin add student-presentation-suite@personal
```

更新时必须从仓库 manifest 读取 marketplace 名称：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json
```

修改 Skill 或插件元数据后，更新 cachebuster 并重新安装：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py" `
  .\plugins\student-presentation-suite
codex plugin add student-presentation-suite@personal
```

重新安装后请开启新 Codex 线程，确保加载最新 Skill。

## 开发与验证

从仓库根目录运行：

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path

python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py

python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  .\plugins\student-presentation-suite\skills\student-presentation
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  .\plugins\student-presentation-suite\skills\student-presentation-ppt
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  .\plugins\student-presentation-suite\skills\student-presentation-review
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite

git diff --check
```

发布检查会强制验证：

- 每个 `SKILL.md` 不超过 65 行；
- Markdown 相对引用真实存在；
- manifest、README、agent metadata 和 Skill 的学生学术范围一致；
- Decision Gate 为强制行为，不能退化为直接套默认值；
- Codex-only 运行时边界；
- Slide Spec 改进字段和 review → edit 交接。

GitHub Actions 会在每次 push 和 pull request 中运行同类验证。

## 生成文件

PPTX 生产通常生成：

```text
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

生成的 PPTX/PNG、缓存、依赖目录和输出内容默认忽略，只保留 `outputs/.gitkeep`。

## 常见问题

- **`Presentations` 不可用**：恢复 Codex presentations 能力并在新线程重试；不能用 Markdown 大纲冒充 PPTX。
- **修改后 Skill 没更新**：更新 cachebuster、重新安装 `student-presentation-suite@personal`，然后新建线程。
- **marketplace 名称不一致**：使用上面的命令读取 `.agents/plugins/marketplace.json`；当前名称是 `personal`。
- **CLI 返回拒绝访问**：关闭可能占用插件缓存或 Codex 可执行文件的进程，重启 Codex/PowerShell 后重试。
- **发布检查失败**：以检查器给出的文件和路径错误为准，不要通过删除规范来绕过检查。

## 发布记录

- 版本级日志：[CHANGELOG.md](CHANGELOG.md)
- 每日工程日志：`Changelog-YYYY-MM-DD.md`

## License

MIT，见 [LICENSE](LICENSE)。
