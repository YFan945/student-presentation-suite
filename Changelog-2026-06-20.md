# 修改日志 - 2026-06-20

| 字段 | 内容 |
| --- | --- |
| 时间范围 | UTC+8，2026-06-20 |
| 提交者 | yfan945 |
| 提交 Hash | `03e3751`、本次发布提交 |

## 今日概述

当天完成两阶段收敛：首先将仓库从共享运行时结构迁移为 Codex-only marketplace，删除 Claude 生产桥接和第二套依赖；随后全面规范化三个 Skill，建立统一 suite contract、强制 PPTX Decision Gate、Skill 长度预算、引用链检查和跨层一致性测试。根级文档、版本日志和每日工程日志同步补齐。

## 变更内容

### refactor · Codex-only Marketplace

- 使用 `.agents/plugins/marketplace.json` 作为显式注册的仓库 marketplace。
- 删除仓库及插件包中的 Claude manifests、Claude 环境检查、production bridge、Node/PPTXGenJS 依赖。
- 保留 Codex `Presentations` 作为唯一 PPTX 生产工作流，`imagegen` 仅作为可选视觉能力。
- 新增 Codex plugin 图标、真实 Slide Spec fixture，并强化 CI。

### feat · Suite Contract

- 新增 `references/suite-contract.md`，集中定义严格学生学术 PPT 范围、非目标、三 Skill 路由、授权和运行时边界。
- 明确讲稿、转场、Q&A 和小组衔接只能作为合格 PPT 任务的配套输出。
- review 默认只给建议；只有明确要求修改文件时，才交接给 PPT Skill，且不得覆盖原始 deck。

### feat · Mandatory Decision Gate

- 制作目标缺少高影响决策时，每轮只提出 1–3 个问题。
- 每题提供 2–4 个互斥、主题相关的选项，推荐项优先并说明影响。
- 用户选择前禁止创建 slide plan 或 PPTX。
- 用户明确授权 Codex 决策时，允许采用推荐方案，但必须先列出 production assumptions。
- 增加时长已知、页数未知时的精简/标准/详细密度选项。

### refactor · Skill 与引用结构

- 三个 `SKILL.md` 压缩到 38–41 行，全部低于 65 行预算。
- `shared-standards.md` 只负责内容和表达标准，范围与路由交给 suite contract。
- 保留视觉风格 menu → 单个 style 文件的选择性加载。

### docs · 全局文档

- 完整重写根级 `README.md`、`README-zh.md` 和 `AGENTS.md`。
- README 覆盖范围、路由、Decision Gate、目录、安装、更新、验证、输出和故障处理。
- AGENTS 明确 source of truth、开发规范、测试、发布和 direct-main 校验要求。
- 新增根级 `CHANGELOG.md`，补齐 6 月 18、19、20 日日志。

### test · 发布契约

- release checker 新增 Skill 行数预算、Markdown 引用可达性、跨层范围一致性和 Decision Gate 检查。
- 路由 fixture 覆盖模糊 PPTX、完整约束、用户授权决定、商业培训和教师培训拒绝场景。
- 行为测试从关键词存在升级为 suite contract、授权和 option-based gate 契约。

## 文件更改概览

| 区域 | 主要变化 |
| --- | --- |
| 根目录 | README、AGENTS、版本日志、每日工程日志 |
| Marketplace | Codex-only 显式 marketplace |
| Plugin metadata | cachebuster、能力和 UI 文案统一 |
| Skills | 入口压缩、职责边界、Decision Gate |
| References | suite contract、shared standards ownership |
| Tests/scripts | 长度、引用、范围、路由和 gate 自动检查 |

## 验证记录

已运行并通过：

```text
python -m unittest discover -s plugins/student-presentation-suite/tests
python plugins/student-presentation-suite/scripts/check_plugin_release.py
python scripts/check_marketplace_release.py
quick_validate.py × 3 skills
validate_plugin.py
python -m py_compile ...
git diff --check
```

## 已知问题

- 当前 PowerShell 调用 WindowsApps 中的 `codex.exe` 返回 `Access is denied`，因此尚未完成本轮 cachebuster 对应的实际重新安装。
- 重新安装后仍需在新线程验证真实运行时触发和 Decision Gate 交互。

## 后续

- CLI 权限恢复后执行 `codex plugin add student-presentation-suite@personal`。
- 在新线程使用模糊、已授权和完整需求三类提示进行真实行为验证。

## 备注

- 本日志同时记录提交 `03e3751` 和其后的全面规范化工作。
- marketplace entry 未被修改。
