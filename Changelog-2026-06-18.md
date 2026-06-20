# 修改日志 - 2026-06-18

| 字段 | 内容 |
| --- | --- |
| 时间范围 | UTC+8，2026-06-18 |
| 提交者 | yfan945 |
| 提交 Hash | `690aa95` |

## 今日概述

当天重点是统一 marketplace 结构并收紧插件触发边界。仓库明确区分 marketplace 根、插件包和运行时职责，三个 Skill 统一要求明确学生学术场景和 PPT 目标，减少通用演示或仅上传文件时的误触发。

## 变更内容

### refactor · Marketplace 与运行时边界

- 统一 marketplace 配置和相对 source 路径，减少重复入口与错误注册。
- 更新 README、AGENTS 和发布检查，使 marketplace 根与 plugin package 边界一致。

### fix · Skill 路由

- 收紧 `student-presentation`、`student-presentation-ppt`、`student-presentation-review` 的学生场景和输出目标判断。
- “PPT 大纲”“实际 PPTX”“已有 deck 审查”分别路由到对应 Skill。
- 附件存在但未要求审查、非学生商业汇报和独立讲稿/Q&A 不再作为插件触发条件。

### test · 行为契约

- 增加中英文路由案例及非目标场景。
- 发布检查同步验证 marketplace、manifest、README 和 Skill 边界。

## 验证记录

- 插件行为契约测试通过。
- marketplace 和 plugin release checks 通过。

## 后续

- 继续完善视觉风格控制和 Slide Spec/PPTX QA。
- 进一步确认 Skill references 是否真正按需拆分。
