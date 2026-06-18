# 修改日志 - 2026-06-17

| 字段 | 内容 |
| --- | --- |
| 时间范围 | UTC+8，2026-06-17 00:00 至生成时 |
| 提交者 | yfan945 |
| 提交 Hash | `5bd40ca`、`296eaf5`、`b89620a`、`d911a68`、`8cdaa68`、`3e5150f`、`0ea44d9`、`8c5fd11`、`af864fc`、`b0bd8cc`、`85fd816`、`c8ee2ef`、`1b1588f`、`1dd173e` |

## 今日概述

今天主要围绕 `student-presentation-suite` 插件从单插件目录演进为 Codex 与 Claude Code 都能直接添加的本地共享 marketplace，同时保留可被 OpenCode 等工具复用的 skill 源文件。最终结构只保留根 `.claude-plugin/marketplace.json` 作为共享市场文件；插件内部继续保留兼容元数据、Slide Spec bridge、PPTX QA 环境检查和 skill 行为边界。

## 变更内容

### feat · Codex/Claude marketplace 与 skill 复用

- **marketplace 根结构**：删除根级 `marketplace.json`，保留 `.claude-plugin/marketplace.json` 作为 Codex 和 Claude Code 共享的 marketplace；该文件指向 `plugins/student-presentation-suite/`。（`.claude-plugin/marketplace.json`）
- **Claude/OpenCode 复用路线**：Claude Code 可直接从本目录添加插件市场；OpenCode 等工具仍可直接消费 `skills/` 源文件或插件本体内兼容元数据。（`.claude-plugin/marketplace.json`、`plugins/student-presentation-suite/skills/`、`plugins/student-presentation-suite/.claude-plugin/plugin.json`）
- **Claude Code PPTX bridge**：插件内仍保留 `.claude-plugin/plugin.json` 和 `document-skills` 相关 bridge，用于需要直接读取插件本体的场景。（`plugins/student-presentation-suite/.claude-plugin/plugin.json`、`plugins/student-presentation-suite/scripts/slide_spec_to_pptx_brief.py`）
- **已有 deck 改进交接**：扩展 Slide Spec schema 和文档，支持 `source_deck`、`edit_intent`、`review_findings`、`preserve`、`change_summary_required`，让 review 结果可稳定交给 PPTX 生成流程。（`plugins/student-presentation-suite/references/slide-spec.schema.json`、`plugins/student-presentation-suite/references/slide-spec.md`）

### fix · 安装与发布可用性

- **安装文档闭环**：根 README 说明 Codex 和 Claude Code 都通过同一个 `.claude-plugin/marketplace.json` 添加本目录 marketplace。（`README.md`、`README-zh.md`）
- **发布元数据**：将 manifest 中的 `Local developer` 替换为 `YFan945`，补充 Codex homepage/repository 作者信息，并刷新 Codex cachebuster 版本。（`plugins/student-presentation-suite/.codex-plugin/plugin.json`、`plugins/student-presentation-suite/.claude-plugin/plugin.json`）
- **CI 导入路径**：修复 GitHub Actions 中测试导入路径问题，确保 `shared` 等插件内模块能在 CI 中正常导入。（`.github/workflows/validate.yml`）

### refactor · Skill 行为与提示词边界

- **规划/PPT/审阅职责分离**：收紧 `student-presentation`、`student-presentation-ppt`、`student-presentation-review` 的路由规则，避免用户要 PPTX 时停在大纲，也避免只要求审阅时直接改文件。（`plugins/student-presentation-suite/skills/student-presentation/SKILL.md`、`plugins/student-presentation-suite/skills/student-presentation-ppt/SKILL.md`）
- **PPTX 生产约束**：强化澄清门、fast default、视觉风格选择、Artifact Tool 坐标注意事项、Claude `pptx` skill 读取顺序、交付 QA 和最终回复契约。（`plugins/student-presentation-suite/skills/student-presentation-ppt/references/pptx-production.md`）
- **审阅输出交接**：增加 `Edit Plan` 和 `Change Summary Handoff` 输出要求，支持从审阅自然进入改进版 PPTX 生产。（`plugins/student-presentation-suite/skills/student-presentation-review/references/review-output-format.md`）

### docs · README 与贡献说明

- **根 README 重写**：把仓库定位为 Codex/Claude Code 共享 marketplace 和通用 skill 源目录，维护中英文互链。（`README.md`、`README-zh.md`）
- **插件 README 重写**：将插件包 README 从安装混合说明调整为插件能力说明，覆盖三个 skill、输入输出、运行路线、辅助脚本和验证方式。（`plugins/student-presentation-suite/README.md`、`plugins/student-presentation-suite/README-zh.md`）
- **贡献指南**：更新 AGENTS.md，明确需要保留单一共享 marketplace 路线，不再恢复单独的根 `marketplace.json`。（`AGENTS.md`）

### test · 发布检查与行为契约

- **marketplace 发布检查**：根级 `scripts/check_marketplace_release.py` 校验共享 marketplace、README 中英互链、路径和安装说明。（`scripts/check_marketplace_release.py`）
- **插件发布检查**：扩展 `check_plugin_release.py`，校验双 manifest、运行时依赖、已有 deck 改进字段、README 运行说明、禁止提交 `node_modules`/缓存目录等。（`plugins/student-presentation-suite/scripts/check_plugin_release.py`）
- **行为契约测试**：新增/扩展测试，覆盖 vague PPTX 请求、review 到 edit 的交接、Slide Spec bridge、schema 字段和 README/skill 行为一致性。（`plugins/student-presentation-suite/tests/test_skill_behavior_contracts.py`、`plugins/student-presentation-suite/tests/test_slide_spec_bridge.py`）

### chore · 运行时依赖和忽略规则

- **Claude PPTX 环境检查**：新增 `requirements-claude-pptx.txt`、`package.json`、`package-lock.json`，并完善 `check_claude_pptx_env.py` 对 Node、npm、pptxgenjs、markitdown、Pillow、LibreOffice、Poppler 的检查。（`plugins/student-presentation-suite/requirements-claude-pptx.txt`、`plugins/student-presentation-suite/scripts/check_claude_pptx_env.py`）
- **忽略规则**：补充生成文件、输出目录、PPTX/PNG/PDF、缓存和 `node_modules` 的忽略规则，避免本地产物污染发布包。（`.gitignore`、`plugins/student-presentation-suite/.gitignore`）

## 文件更改概览

| 区域 | 主要变化 |
| --- | --- |
| 根目录 | 共享 marketplace manifest、README、AGENTS、CI、发布检查脚本 |
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
python %USERPROFILE%\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .\plugins\student-presentation-suite
claude plugin validate .\plugins\student-presentation-suite
claude plugin validate .
```

## 未完成事项

- Codex CLI 在当前 shell 中执行 `codex plugin --help` 返回 `Access is denied`，因此 Codex 安装命令按 `plugin-creator` 规范写入文档并通过 Codex plugin validator 验证 manifest，但没有在当前 shell 实跑安装。
- 尚未做一次从干净 clone、新 Codex 线程或 Claude Code 实例开始的真实用户安装演练。

## 明日计划

- 在干净目录、新 Codex 线程或 Claude Code 实例执行一次安装路径演练，确认 README 命令可直接复现。
- 准备一个最小 Slide Spec 示例，跑通 Codex PPTX 生成、渲染和 `pptx_delivery_check.py`。
- 继续检查 marketplace 元数据是否需要补充图标、截图、隐私/条款链接或更正式的发布说明。

## 备注

- 本日志按 UTC+8 的 2026-06-17 自然日统计，包含提交 `5bd40ca` 到 `1dd173e`。
- 日志本身是在提交 `1dd173e` 之后生成，用于记录今天已完成的仓库改动。
