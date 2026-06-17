# 修改日志 - 2026-06-17

| 字段 | 内容 |
| --- | --- |
| 时间范围 | UTC+8，2026-06-17 00:00 至生成时 |
| 提交者 | yfan945 |
| 提交 Hash | `5bd40ca`、`296eaf5`、`b89620a`、`d911a68`、`8cdaa68`、`3e5150f`、`0ea44d9`、`8c5fd11`、`af864fc`、`b0bd8cc`、`85fd816`、`c8ee2ef`、`1b1588f`、`1dd173e` |

## 今日概述

今天主要围绕 `student-presentation-suite` 插件从单插件目录演进为同时适配 Codex 和 Claude Code 的本地 marketplace 仓库，并持续补齐安装、校验、运行时依赖和 skill 行为边界。整体成果包括 marketplace 根结构、Claude Code `document-skills` 路线、Codex `Presentations` 路线、已有 deck 改进交接、PPTX QA 环境检查、发布检查脚本和中英文 README。

## 变更内容

### feat · 插件市场与双运行时适配

- **marketplace 根结构**：新增根级 `marketplace.json`、`.claude-plugin/marketplace.json`，把插件本体移动到 `plugins/student-presentation-suite/`，保留 Codex 与 Claude Code 两条入口路线。（`marketplace.json`、`.claude-plugin/marketplace.json`）
- **Claude Code PPTX 路线**：为 Claude Code 增加 `.claude-plugin/plugin.json`，声明 `document-skills` 依赖，并通过 Slide Spec bridge 把本插件的课堂汇报约束传给 `pptx` skill。（`plugins/student-presentation-suite/.claude-plugin/plugin.json`、`plugins/student-presentation-suite/scripts/slide_spec_to_pptx_brief.py`）
- **已有 deck 改进交接**：扩展 Slide Spec schema 和文档，支持 `source_deck`、`edit_intent`、`review_findings`、`preserve`、`change_summary_required`，让 review 结果可稳定交给 PPTX 生成流程。（`plugins/student-presentation-suite/references/slide-spec.schema.json`、`plugins/student-presentation-suite/references/slide-spec.md`）

### fix · 安装与发布可用性

- **安装文档闭环**：根 README 补齐 Codex 非默认 marketplace 安装命令、默认个人 marketplace 合并说明、Claude Code marketplace/install 命令，以及 PPTX 运行依赖检查步骤。（`README.md`、`README-zh.md`）
- **发布元数据**：将 manifest 中的 `Local developer` 替换为 `YFan945`，补充 Codex homepage/repository 作者信息，并刷新 Codex cachebuster 版本。（`plugins/student-presentation-suite/.codex-plugin/plugin.json`、`plugins/student-presentation-suite/.claude-plugin/plugin.json`）
- **CI 导入路径**：修复 GitHub Actions 中测试导入路径问题，确保 `shared` 等插件内模块能在 CI 中正常导入。（`.github/workflows/validate.yml`）

### refactor · Skill 行为与提示词边界

- **规划/PPT/审阅职责分离**：收紧 `student-presentation`、`student-presentation-ppt`、`student-presentation-review` 的路由规则，避免用户要 PPTX 时停在大纲，也避免只要求审阅时直接改文件。（`plugins/student-presentation-suite/skills/student-presentation/SKILL.md`、`plugins/student-presentation-suite/skills/student-presentation-ppt/SKILL.md`）
- **PPTX 生产约束**：强化澄清门、fast default、视觉风格选择、Artifact Tool 坐标注意事项、Claude `pptx` skill 读取顺序、交付 QA 和最终回复契约。（`plugins/student-presentation-suite/skills/student-presentation-ppt/references/pptx-production.md`）
- **审阅输出交接**：增加 `Edit Plan` 和 `Change Summary Handoff` 输出要求，支持从审阅自然进入改进版 PPTX 生产。（`plugins/student-presentation-suite/skills/student-presentation-review/references/review-output-format.md`）

### docs · README 与贡献说明

- **根 README 重写**：把仓库定位、目录结构、兼容性、安装、使用、开发验证拆清楚，并维护中英文互链。（`README.md`、`README-zh.md`）
- **插件 README 重写**：将插件包 README 从安装混合说明调整为插件能力说明，覆盖三个 skill、输入输出、运行路线、辅助脚本和验证方式。（`plugins/student-presentation-suite/README.md`、`plugins/student-presentation-suite/README-zh.md`）
- **贡献指南**：新增 AGENTS.md，明确 marketplace 根结构、测试命令、命名规范、Codex/Claude 双路线和 README 更新要求。（`AGENTS.md`）

### test · 发布检查与行为契约

- **marketplace 发布检查**：新增根级 `scripts/check_marketplace_release.py`，校验根 marketplace、Claude marketplace、README 中英互链、路径和安装说明。（`scripts/check_marketplace_release.py`）
- **插件发布检查**：扩展 `check_plugin_release.py`，校验双 manifest、运行时依赖、已有 deck 改进字段、README 运行说明、禁止提交 `node_modules`/缓存目录等。（`plugins/student-presentation-suite/scripts/check_plugin_release.py`）
- **行为契约测试**：新增/扩展测试，覆盖 vague PPTX 请求、review 到 edit 的交接、Slide Spec bridge、schema 字段和 README/skill 行为一致性。（`plugins/student-presentation-suite/tests/test_skill_behavior_contracts.py`、`plugins/student-presentation-suite/tests/test_slide_spec_bridge.py`）

### chore · 运行时依赖和忽略规则

- **Claude PPTX 环境检查**：新增 `requirements-claude-pptx.txt`、`package.json`、`package-lock.json`，并完善 `check_claude_pptx_env.py` 对 Node、npm、pptxgenjs、markitdown、Pillow、LibreOffice、Poppler 的检查。（`plugins/student-presentation-suite/requirements-claude-pptx.txt`、`plugins/student-presentation-suite/scripts/check_claude_pptx_env.py`）
- **忽略规则**：补充生成文件、输出目录、PPTX/PNG/PDF、缓存和 `node_modules` 的忽略规则，避免本地产物污染发布包。（`.gitignore`、`plugins/student-presentation-suite/.gitignore`）

## 文件更改概览

| 区域 | 主要变化 |
| --- | --- |
| 根目录 | marketplace manifest、README、AGENTS、CI、发布检查脚本 |
| 插件 manifest | Codex/Claude 插件元数据、依赖和版本 cachebuster |
| Skill 文件 | 三个 skill 的职责、路由、澄清门、QA 和输出契约 |
| references | Slide Spec、PPTX production、review output、shared standards |
| scripts | 发布检查、Claude PPTX 环境检查、Slide Spec bridge |
| tests | 行为契约、Slide Spec bridge、PPTX 静态检查相关测试 |

## 验证记录

今日最终验证已通过：

```text
python scripts/check_marketplace_release.py --json
python plugins/student-presentation-suite/scripts/check_plugin_release.py --json
python -m pytest -q plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_claude_pptx_env.py --json
python %USERPROFILE%\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
claude plugin validate .
```

## 未完成事项

- Codex CLI 在当前 shell 中执行 `codex plugin --help` 返回 `Access is denied`，因此 Codex 安装命令按 `plugin-creator` 规范写入文档并通过 Codex plugin validator 验证 manifest，但没有在当前 shell 实跑安装。
- 尚未做一次从干净 clone 开始的真实用户安装演练，尤其是 Claude Code marketplace add/install 与 PPTX 生成端到端流程。

## 明日计划

- 在干净目录执行一次 clone 后的 Codex/Claude Code 安装路径演练，确认 README 命令可直接复现。
- 准备一个最小 Slide Spec 示例，跑通 Claude Code `document-skills` PPTX 生成、渲染和 `pptx_delivery_check.py`。
- 继续检查 marketplace 元数据是否需要补充图标、截图、隐私/条款链接或更正式的发布说明。

## 备注

- 本日志按 UTC+8 的 2026-06-17 自然日统计，包含提交 `5bd40ca` 到 `1dd173e`。
- 日志本身是在提交 `1dd173e` 之后生成，用于记录今天已完成的仓库改动。
