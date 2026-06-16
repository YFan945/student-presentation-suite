---
name: student-presentation-ppt
description: Generate editable university PPTX decks, speaker notes, previews, and production QA from topics, outlines, or Slide Spec YAML.
---

# Student Presentation PPT

## Role

Produce actual editable PowerPoint decks for university presentations. This skill handles PPTX generation, visual system, assets, export, preview, and QA.

Platform-specific PPTX generation:
- **Codex 环境**：使用内置的 `Presentations` skill 和 artifact-tool presentation JSX workflow
- **Claude Code 环境**：依赖 `document-skills` 插件，并使用其中的 `pptx` skill（本机参考路径：`C:\Users\28603\.claude\plugins\marketplaces\anthropic-agent-skills\skills\pptx`）

Do not stop at a text outline when the user asks for PPT, PPTX, PowerPoint, editable slides, rendered slides, or a ready presentation file.

## Clarification Gate

Before planning or building, decide whether the user's request is specific enough to produce a deck responsibly. If the prompt is vague, incomplete, or only says to make a PPT from a broad topic, stop and ask concise follow-up questions. Do not start outlining, selecting a style, collecting images, generating files, or making assumptions until the production target is clear.

Ask for the missing items that materially affect the deck, including whether the user needs an outline first, expected slide count, language, duration, course/rubric, audience, individual/group format, source material, visual style, template/logo requirements, and image-source preference. Prefer 3-6 grouped questions in one reply. If the user is unsure about visual style, offer 3-5 topic-fit choices from `references/visual-style-menu.md` instead of asking an open-ended style question. Include at least one conservative classroom-safe option and one more expressive option when the grading context is unknown.

Proceed without another question only when the conversation or Slide Spec already confirms the core constraints, or when the user explicitly asks Codex to decide. In that case, write a short assumption block before production, covering at least language, duration, slide count, audience, source basis, visual style, image/source policy, and whether the deck is conceptual or evidence-backed. Do not hide defaults in the final response only.

## Workflow

1. Enforce the Clarification Gate. Check confirmed constraints from the conversation or Slide Spec meta, then ask for missing production-critical items before any production work: type, language, duration, slide count, course/rubric, group setup, source material, whether an outline is needed first, template/logo, visual style, and image-source preference.
2. Load `../../references/shared-standards.md` first. Load only the needed task references:
   - `references/pptx-production.md` for the full build sequence, creativity rules, content quality, anti-AI review, deliverable QA, and final response contract
   - `references/visual-style-menu.md` for the style selection menu, choice guide, general visual principles, structural visual layer, and template inheritance
	   - After choosing a style, also load `references/visual-styles/<style>.md` for that style's detailed guardrails
   - `../../references/slide-spec.md` when input includes Slide Spec YAML
   - `../../references/image-strategy.md` for image/source choices and fallback visuals
   - Platform-specific references:
     - **Codex 环境**：`references/pptx-production.md` 中的 Artifact-Tool Pitfalls 章节
     - **Claude Code 环境**：先遵循 `document-skills` 插件提供的 `pptx` skill；从零生成读 `pptxgenjs.md`，套模板/编辑读 `editing.md`
   - Run `scripts/pptx_delivery_check.py` after generation to verify the deliverable package when a PPTX path is available
3. Choose one creative direction before building. If the style is missing and materially affects the result, ask the user to choose from 3-5 viable directions adapted to the topic. Only select the best fit without another question when the prompt is already specific enough or the user explicitly asks Codex to decide; state the reason briefly.
4. Build or adapt the slide plan using student-presentation principles: one message per slide, claim-style titles, concise text, natural notes, B1-B2 English when relevant, and balanced group ownership.
5. Design and build the deck:
   - use 16:9 unless a template requires otherwise
   - use shapes, panels, dividers, timeline blocks, process nodes, comparison cards, callouts, and background layers as functional structures, not repeated decoration
   - use simulated glassmorphism/translucent panels only when readability remains strong
   - follow shared typography: Chinese body >= 22pt, English body >= 20pt, titles/subtitles/section headers/card headers/chart titles/panel labels >= 24pt
6. Build the deck using the platform-appropriate tool:
   - **Codex 环境**：使用 artifact-tool presentation JSX workflow。先运行单页 toolchain smoke test，确认坐标、填充、文字、讲稿、PPTX 导出和 PNG 预览都正确。shape position 使用 `left`/`top`/`width`/`height`，勿用 `x`/`y`。
   - **Claude Code 环境**：使用 `document-skills` 插件里的 `pptx` skill 生产 PPTX。先运行 `python scripts/check_claude_pptx_env.py --json` 检查 `pptx` skill 需要的工具；如果输入包含 Slide Spec，先运行 `python scripts/slide_spec_to_pptx_brief.py <spec.yaml> --output outputs/<topic>-claude-pptx-brief.md`，用生成的 brief 作为 `pptx` skill 的生产输入。然后读取该 skill 的 `SKILL.md`；从零生成时参考 `pptxgenjs.md`，编辑已有模板时参考 `editing.md`。保留本 skill 的课堂汇报约束、Slide Spec、风格选择、讲稿和 QA contract 作为上层要求。
7. Export and validate through the presentation workflow. Do not claim ready-to-present unless the `.pptx` exists and has been verified. In Codex 环境下同时检查预览图；在 Claude Code 环境下按 `pptx` skill 要求使用 `python -m markitdown`、LibreOffice/Poppler 渲染图片，并运行 `pptx_delivery_check.py` 验证文件完整性。
8. Before the final response, run `scripts/pptx_delivery_check.py` when possible. Report whether the PPTX, notes, and preview/contact sheet files actually exist, the detected slide count, static XML risk count, risk breakdown when available, and any validation limitations. If static risks are mostly expected small footer/kicker/caption text, say that explicitly and still confirm rendered visual QA. If the script cannot run, state that limitation instead of implying the package was checked.

## Output Contract

Use topic-specific filenames under `outputs/`:
- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or contact sheet

If Slide Spec meta includes `output_prefix`, use it as `<topic>`; otherwise derive a short ASCII-safe slug from the topic.

Final response must follow the contract in `references/pptx-production.md`: `Generated Files`, `Deck Summary`, `Creative Direction`, and `QA`. Always explicitly say whether each expected file exists.
