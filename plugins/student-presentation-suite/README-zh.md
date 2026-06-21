# Student Presentation Suite for Codex

中文 | [English](README.md)

> 此插件包适配 **Codex**。Claude Code 用户请查看仓库的 [`claude-code` 分支](https://github.com/YFan945/student-presentation-suite/tree/claude-code)。

该插件严格用于学生学术 PPT：规划大纲、创建或修改可编辑 PPTX，以及审查已有学生 deck。公司汇报、教师培训、通用职业演示和独立演讲稿/Q&A 不在范围内。规范边界见 [`references/suite-contract.md`](references/suite-contract.md)。

## 安装

建议从仓库根目录安装，而不是单独复制本目录：

```powershell
git clone --branch main https://github.com/YFan945/student-presentation-suite.git
Set-Location .\student-presentation-suite
codex plugin marketplace add (Get-Location).Path
codex plugin add student-presentation-suite@personal
codex plugin list
```

安装后新建 Codex 线程。插件 Manifest 为 [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json)。制作 PPTX 需要 Codex `Presentations`；artifact-tool 仅是内部实现细节。

## 使用方式

| 请求 | Skill | 输出 |
| --- | --- | --- |
| 学生 PPT 大纲或 Slide Spec | `student-presentation` | 逐页大纲及可选讲稿、转场、Q&A |
| 创建、重建或明确编辑 PPTX | `student-presentation-ppt` | 可编辑 PPTX、讲稿、预览和 QA |
| 审查、评分或比较已有 PPT | `student-presentation-review` | 分级问题、逐页建议和评分 |
| 审查后明确修改文件 | review → PPT skill | 独立改进版 PPTX 和变更摘要 |

直接在新线程中描述任务即可，例如：

```text
帮我制作一个大学生创新项目答辩 PPTX。
材料在附件中，答辩 6 分钟，评委重点关注创新性、实现过程和结果验证。
请生成可编辑文件、逐页讲稿和预览图。
```

```text
请审查我上传的大学课程 PPT，按 Critical、Major、Minor 分级，
检查叙事、信息密度、视觉层级、讲述难度和 AI 套话，并给出逐页建议。
```

PPTX 制作存在未解决的目标、评分重点、内容范围或风格选择时，Skill 会执行强制 **Decision Gate**，询问 1–3 个关键问题并等待选择后再开始制作。

## 输出

```text
outputs/<topic>-outline.md
outputs/<topic>-presentation.pptx
outputs/<topic>-speaker-notes.md
outputs/<topic>-preview.png
outputs/<topic>-change-summary.md
```

原始 deck 永不覆盖。完整下载、更新、故障排查和开发说明见仓库根目录 [README-zh.md](../../README-zh.md)。
