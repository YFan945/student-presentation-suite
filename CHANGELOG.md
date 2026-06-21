# CHANGELOG

## Unreleased — 2026-06-20

### 新增

- 五类学生汇报场景、受众深度、新手/熟手和基础/高分模式。
- 分层内容生成、证据状态、字段锁定和指定页面局部修改契约。
- Slide Spec 确定性质量分析、逐页评审卡和答辩演练检查。

### 兼容性

- 保持三个 Skill 名称、职责边界及原有 Slide Spec 字段兼容。
- 仍使用 Codex `Presentations` 作为唯一 PPTX 生产能力。

## 0.1.1 — 2026-06-20

| 字段 | 内容 |
| --- | --- |
| 版本 | `0.1.1` |
| 时间范围 | 2026-06-17 ~ 2026-06-20 |
| Git 范围 | `5bd40ca..HEAD` |
| 主要贡献者 | yfan945 |

### 版本概述

本版本将仓库从多运行时共享实验收敛为明确的 Codex-only marketplace，并完成学生学术 PPT 三 Skill 的职责分离、结构化 review → edit 交接、视觉生成控制、PPTX QA 和强制 Decision Gate。插件现在以统一 contract、精简 Skill 入口和可执行发布检查保证范围、路由、引用链及用户授权不会漂移。

### 重大功能

- **严格学生学术 PPT 范围**：仅处理 PPT 大纲、实际 PPTX 制作/改进和已有 deck 审查；通用演示、商业汇报、教师培训及独立讲稿/Q&A 明确排除。
- **PPTX Decision Gate**：目标不明确时，每轮提出 1–3 个高影响问题，每题给出 2–4 个互斥、主题相关、带推荐项和影响说明的选项，用户选择前不进入制作。
- **结构化已有 deck 改进**：Slide Spec 支持 `source_deck`、`edit_intent`、`review_findings`、`preserve` 和 `change_summary_required`，审查结果可稳定交接给 PPTX 生产。
- **可执行视觉风格系统**：14 个风格文件具有 color roles、geometry、slide recipes、image treatment、density control 和 acceptance checks，并通过菜单按需加载。
- **PPTX 交付 QA**：加强预览/contact sheet、静态 XML 风险、讲稿和必要交付文件检查，区分真实 blocker 与页码、脚注等合理小字号内容。

### 重要调整

- marketplace 迁移为 `.agents/plugins/marketplace.json`，仓库和插件包均只保留 Codex manifest。
- 三个 `SKILL.md` 均限制在 65 行以内，详细规则下沉到 references。
- 新增 `suite-contract.md`，集中管理范围、路由、决策授权、运行时边界和跨 Skill 交接。
- manifest、agent metadata、中英文 README、Skill 文案和发布检查统一使用相同的学生学术范围。
- CI 增加官方 plugin/Skill validator、真实 Slide Spec fixture、Python 编译和 patch hygiene。

### 验证记录

- `python -m unittest discover -s plugins/student-presentation-suite/tests`
- `python plugins/student-presentation-suite/scripts/check_plugin_release.py`
- `python scripts/check_marketplace_release.py`
- 三个 Skill 的 `quick_validate.py`
- 官方 `validate_plugin.py`
- Python entrypoint 编译
- `git diff --check`

### 已知问题

- 当前 WindowsApps 环境中直接调用 `codex.exe` 可能返回 `Access is denied`，因此插件重新安装需要在 CLI 权限恢复或重启 Codex/PowerShell 后执行。
- 修改插件后仍需在新线程验证真实运行时触发和 Decision Gate 交互。

### 参考来源

- `Changelog-2026-06-17.md`
- `Changelog-2026-06-18.md`
- `Changelog-2026-06-19.md`
- `Changelog-2026-06-20.md`
