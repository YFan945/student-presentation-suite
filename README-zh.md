# Student Presentation Suite — Codex 学生学术 PPT 插件

[![Validate](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/YFan945/student-presentation-suite/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/runtime-Codex-111827)](plugins/student-presentation-suite/.codex-plugin/plugin.json)

中文 | [English](README.md)

> 本仓库 `main` 分支适配 **Codex**。如果你使用 **Claude Code**，请查看 [`claude-code` 分支](https://github.com/YFan945/student-presentation-suite/tree/claude-code)，不要使用 `main` 分支的安装步骤。

`student-presentation-suite` 用于学生主导的学术 PPT 工作，包括：

- 规划课程汇报、答辩、竞赛或研究展示的 PPT 大纲；
- 创建、重建或明确修改可编辑的 PPTX；
- 审查、评分和诊断已有学生 PPT。

它不适用于公司汇报、销售提案、教师培训、通用职业演示，也不会因单独的演讲稿、Q&A 或一个未说明用途的附件而触发。完整边界见 [`references/suite-contract.md`](plugins/student-presentation-suite/references/suite-contract.md)。

## 下载与安装

### 方式一：使用 Git 克隆

在 PowerShell 中运行：

```powershell
git clone --branch main https://github.com/YFan945/student-presentation-suite.git
Set-Location .\student-presentation-suite
```

如果同名目录已经存在，请换一个空目录名；后续命令必须在下载后的仓库根目录运行。

### 方式二：下载 ZIP

1. 打开 [GitHub 仓库主页](https://github.com/YFan945/student-presentation-suite)。
2. 选择 **Code → Download ZIP**。
3. 解压到固定目录，并在 PowerShell 中进入包含 `.agents`、`plugins`、`README-zh.md` 的仓库根目录。

### 注册 marketplace 并安装插件

本仓库不是 Codex 默认自动发现的 marketplace，必须显式注册当前仓库根目录：

```powershell
codex plugin marketplace add (Get-Location).Path

python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json

codex plugin add student-presentation-suite@personal
codex plugin list
```

`codex plugin list` 应显示 `student-presentation-suite@personal` 已安装并启用。安装后新建一个 Codex 线程，使三个 Skill 被重新加载。

实际生成 PPTX 还要求当前 Codex 环境提供 `Presentations` 能力；`imagegen` 是可选能力。

## 如何使用

安装完成后，直接在新 Codex 线程中用自然语言描述任务。Codex 会按目标自动选择 Skill：

| 你要做什么 | 使用的 Skill | 主要结果 |
| --- | --- | --- |
| 只要 PPT 大纲或 Slide Spec | `student-presentation` | 逐页大纲、可选讲稿、转场和 Q&A |
| 创建、重建或明确编辑 PPTX | `student-presentation-ppt` | 可编辑 PPTX、讲稿、预览和 QA |
| 审查、评分或比较已有 PPT | `student-presentation-review` | 分级问题、逐页建议和评分 |
| 先审查，再明确要求改文件 | review → PPT skill | 独立保存的改进版 PPTX 和变更摘要 |

为了获得更稳定的结果，建议在请求中提供：

- 课程或比赛名称、汇报主题；
- 听众和评分标准；
- 时长或页数；
- 语言、个人/小组形式；
- 资料、数据、参考文献或已有 PPT；
- 期望风格，以及哪些内容必须保留。

## 使用案例

### 1. 生成课程汇报大纲

```text
帮我规划一个大学软件工程课程汇报的 PPT 大纲。
主题是“AI 辅助软件测试”，面向老师和同学，8 分钟，中文，控制在 10 页。
请给出每页标题、核心内容、建议配图和逐页讲稿。
```

### 2. 创建可编辑 PPTX

```text
帮我制作一个大学生创新项目答辩 PPTX。
项目材料在附件中，答辩 6 分钟，评委重点关注创新性、实现过程和结果验证。
请生成可编辑文件、逐页讲稿和预览图。
```

制作开始前，如果目标、评分重点、内容范围或风格等高影响决策仍不明确，PPT Skill 会执行强制 **Decision Gate**：每轮只问 1–3 个关键问题，给出互斥选项，并等待你选择后再创建 slide plan 或 PPTX。你也可以明确说“按推荐方案，你决定”，授权它采用推荐选项。

### 3. 审查已有学生 PPT

```text
请审查我上传的大学课程 PPT。
重点检查叙事逻辑、每页信息密度、图文关系、讲述难度和 AI 套话，
按 Critical、Major、Minor 分级，并给出逐页修改建议和评分。
```

### 4. 审查后修改文件

```text
先审查这个毕业答辩 PPT，再根据审查结果修改文件。
保留封面、学校模板和第 4 页实验数据，其他页面可以调整。
不要覆盖原文件，请输出改进版 PPTX 和变更摘要。
```

### 不会触发本插件的请求

```text
帮公司做季度业务汇报 PPT。
写一篇三分钟演讲稿。
我上传了一个 PPT。
```

这些请求缺少学生学术 PPT 场景、目标类型或明确的审查/编辑动作，应使用其他能力或补充上下文。

## 输出文件

根据任务类型，结果通常保存到：

```text
outputs/<topic>-outline.md
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

插件不会覆盖原始 deck。修改已有 PPT 时，会另存改进版文件。

## 更新插件

进入仓库根目录后运行：

```powershell
git pull origin main

python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py" `
  .\plugins\student-presentation-suite

python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\read_marketplace_name.py" `
  --marketplace-path .agents/plugins/marketplace.json

codex plugin add student-presentation-suite@personal
```

重新安装后请新建 Codex 线程。不要手动修改 marketplace 配置。

## 常见问题

- **找不到插件**：确认当前目录是仓库根目录，再运行 `codex plugin marketplace add (Get-Location).Path`。
- **安装后仍使用旧规则**：更新 cachebuster、重新安装，然后新建线程。
- **无法生成 PPTX**：确认 Codex `Presentations` 能力可用；插件不会用 Markdown 大纲冒充 PPTX。
- **`Access denied` 或 `os error 5`**：关闭可能占用 Codex 插件缓存的进程，重启 Codex 和 PowerShell 后重试。
- **请求没有触发插件**：明确说明学生学术场景，并写清目标是“大纲”“生成/修改 PPTX”还是“审查已有 PPT”。

## 开发与验证

开发者请参阅 [AGENTS.md](AGENTS.md)。主要验证入口：

```powershell
python -m pip install -r plugins/student-presentation-suite/requirements.txt
$env:PYTHONPATH=(Resolve-Path "plugins/student-presentation-suite").Path
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" `
  .\plugins\student-presentation-suite
git diff --check
```

版本记录见 [CHANGELOG.md](CHANGELOG.md)，每日工程日志使用 `Changelog-YYYY-MM-DD.md`。

## License

MIT，见 [LICENSE](LICENSE)。
