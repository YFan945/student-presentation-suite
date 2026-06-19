---
name: student-presentation-ppt
description: Use only when the request explicitly identifies a student, university, course, classroom, defense, or other student context and explicitly asks to create or improve a PPT, PPTX, PowerPoint, or slide deck. Do not trigger for generic or non-student presentation work.
---

# Student Presentation PPT

## Role

Produce actual editable PowerPoint decks for university presentations. This skill handles PPTX generation, existing deck improvement, visual system, assets, export, preview, and QA.

## Trigger Gate

Use this skill only when both conditions are explicit in the user's request or established conversation context:

1. The deck has a clearly student-owned academic context, such as an identified student, university assignment, classroom report, thesis/course defense, teacher rubric, or student competition. A single ambiguous word such as "course" or "competition" is not enough without supporting context.
2. The user explicitly asks to create, generate, edit, improve, or rebuild a PPT, PPTX, PowerPoint, slide deck, or editable slides.

Do not trigger for generic presentation requests, non-student business decks, topic research, standalone outlines, scripts, or Q&A. If either condition is missing, use a general-purpose presentation skill or ask one routing question instead.

PPTX generation depends on `document-skills@anthropic-agent-skills` and uses its `pptx` skill.

Do not stop at a text outline when the user asks for PPT, PPTX, PowerPoint, editable slides, rendered slides, or a ready presentation file.

If an eligible student-context request provides only a broad topic but explicitly asks for PPT/PPTX/slides, this skill owns the request. Do not route back to outline-only planning. First create or confirm a concise slide plan/Slide Spec inside the PPTX workflow, then build the deck once production-critical constraints are handled. If an eligible request asks only for "PPT 大纲" or "slide outline" without a file, use `student-presentation` instead.

If the request comes from `student-presentation-review` or includes an existing deck plus review findings, treat it as an improvement/editing workflow. Preserve the original deck as input evidence, write a separate improved PPTX file, and create `outputs/<topic>-change-summary.md` describing kept content, changed slides, unresolved risks, and QA results. If Slide Spec includes `source_deck`, `edit_intent`, `review_findings`, `preserve`, or `change_summary_required`, use those fields as the authoritative edit handoff.

## Clarification Gate

Before planning or building, decide whether the user's request is specific enough to produce a deck responsibly. If the prompt is vague, incomplete, or only says to make a PPT from a broad topic, ask concise follow-up questions for constraints that would materially change the deck. Avoid blocking on minor preferences that can be handled with explicit assumptions.

Ask for the missing items that materially affect the deck, including expected slide count, language, duration, course/rubric, audience, individual/group format, source material, visual style, template/logo requirements, and image-source preference. Prefer 3-6 grouped questions in one reply. If the user is unsure about visual style, show the complete style menu from `references/visual-style-menu.md`, rank the most suitable choices first, and briefly explain the top recommendations. Do not ask whether an outline is needed first after the user has already requested a PPTX; create a compact internal slide plan as part of production.

Proceed without another question when the conversation or Slide Spec already confirms the core constraints, when the user explicitly asks the agent to decide, or when the missing items are low-risk defaults for a general classroom deck. In that case, write a short assumption block before production, covering at least language, duration, slide count, audience, source basis, visual style, image/source policy, and whether the deck is conceptual or evidence-backed. Do not hide defaults in the final response only. Stable general knowledge may be used for basic explanation when clearly labeled as general background, but source-sensitive, disputed, statistical, or current claims require supplied sources or permission to research. Never use web images without permission.

If the request is too vague to build responsibly but clearly asks for PPTX, do not only ask open-ended questions. Give the user a short production choice:
- "fast default": agent chooses a general classroom deck plan and proceeds with stated assumptions
- "confirm first": agent drafts a slide plan/Slide Spec for approval before file generation
- "provide constraints": user supplies duration, slide count, source material, and style

Fast default assumptions:
- language follows the user's request language
- duration: 5 minutes
- slide count: 7-9 slides
- format: individual unless group members are mentioned
- source basis: user-provided facts plus clearly identified stable general background; omit or qualify unsupported statistics, current claims, and source-sensitive details
- image policy: diagram-only or generated abstract visuals; no web images
- style: choose one conservative classroom-safe direction from `references/visual-style-menu.md`

## Workflow

1. Enforce the Clarification Gate. Check confirmed constraints from the conversation or Slide Spec meta. If missing items would materially change the deck, ask for them or offer the fast default / confirm-first / provide-constraints choice before file generation. Do not block on low-risk preferences that can be covered by the assumption block.
2. Load `../../references/shared-standards.md` first. Load only the needed task references:
   - `references/pptx-production.md` for the full build sequence, creativity rules, content quality, anti-AI review, deliverable QA, and final response contract
   - `references/visual-style-menu.md` for the style selection menu, choice guide, general visual principles, structural visual layer, and template inheritance
   - After choosing a style, also load `references/visual-styles/<style>.md` for that style's detailed guardrails
   - `../../references/slide-spec.md` when input includes Slide Spec YAML
   - `../../references/image-strategy.md` for image/source choices and fallback visuals
   - Follow the `document-skills` `pptx` skill; read `pptxgenjs.md` for new decks and `editing.md` for templates or existing decks
   - Run `python skills/student-presentation-ppt/scripts/pptx_delivery_check.py --pptx <pptx> --notes <notes> --preview <preview> --strict` from the plugin package root after generation. The script derives expected notes/preview names when omitted; use `--allow-missing-notes` or `--allow-missing-preview` only for an explicit exception and report the limitation.
3. Choose one creative direction before building. If the style is missing and materially affects the result, show every available direction from `references/visual-style-menu.md`, with the topic-fit recommendations listed first. Only select the best fit without another question when the prompt is already specific enough or the user explicitly asks the agent to decide; state the reason briefly.
4. Build or adapt the slide plan using student-presentation principles: one message per content slide, claim-style titles for argumentative or evidence slides, concise text, natural notes, audience-appropriate English, and balanced group ownership. Covers, section dividers, references, appendix, and Q&A slides may use descriptive titles and omit unnecessary transitions or visuals. When no approved outline exists, create a compact internal slide plan first and use it as the source of truth for PPTX generation.
5. For existing deck improvement, convert review findings into an edit plan before building: keep useful content, identify slides to rewrite, identify slides to redesign, preserve required template/logo/footer elements, and choose whether to edit the original structure or rebuild a cleaner copy. Do not overwrite the source PPTX.
6. Design and build the deck:
   - use 16:9 unless a template requires otherwise
   - use shapes, panels, dividers, timeline blocks, process nodes, comparison cards, callouts, and background layers only when they clarify hierarchy or meaning, not as a mandatory layer on every slide
   - use simulated glassmorphism/translucent panels only when readability remains strong
   - follow shared typography: Chinese normal body >= 22pt, English normal body >= 20pt, and primary slide titles normally >= 24pt; allow smaller secondary labels when necessary and visually verified
7. Build the deck with the `document-skills` `pptx` skill. From the plugin root, run `python scripts/check_claude_pptx_env.py --json`. For Slide Spec input, run `python scripts/slide_spec_to_pptx_brief.py <spec.yaml> --output outputs/<topic>-claude-pptx-brief.md` and use that brief as the production input. Read the `pptx` skill's `SKILL.md`; use `pptxgenjs.md` for new decks and `editing.md` for existing decks or templates.
8. Export and validate as required by the `pptx` skill: run `python -m markitdown`, render through LibreOffice/Poppler, inspect the rendered images, and run `python skills/student-presentation-ppt/scripts/pptx_delivery_check.py` from the plugin root.
9. Before the final response, run `python skills/student-presentation-ppt/scripts/pptx_delivery_check.py --pptx <pptx> --notes <notes> --preview <preview> --strict` from the plugin package root when possible. Report whether the PPTX, notes, and preview/contact sheet files actually exist, the detected slide count, static XML risk count, risk breakdown when available, and any validation limitations. If static risks are mostly expected small footer/kicker/caption text, say that explicitly and still confirm rendered visual QA. Treat `font-size-not-explicit` as unresolved style inheritance evidence, not a blocker by itself. If the script cannot run, state that limitation instead of implying the package was checked.

## Output Contract

Use topic-specific filenames under `outputs/`:
- `outputs/<topic>-presentation.pptx`
- `outputs/<topic>-speaker-notes.md`
- `outputs/<topic>-preview.png` or contact sheet
- `outputs/<topic>-change-summary.md` for improved existing decks

If Slide Spec meta includes `output_prefix`, use it as `<topic>`; otherwise derive a short ASCII-safe slug from the topic.

Final response must follow the contract in `references/pptx-production.md`: `Generated Files`, `Deck Summary`, `Creative Direction`, and `QA`. Always explicitly say whether each expected file exists.
