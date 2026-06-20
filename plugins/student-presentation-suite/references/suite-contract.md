# Student Presentation Suite Contract

This is the canonical contract for suite scope, routing, decision authority, runtime boundaries, and cross-skill handoff. Skill entrypoints and README files must link to this contract instead of redefining it.

## Supported Scope

Use this suite only when both conditions are established:

1. The work has explicit student-owned academic context, such as a university assignment, classroom report, course or thesis defense, teacher rubric, or student competition.
2. The requested outcome is a PPT/slide outline, an actual PPTX, or review of an existing presentation artifact.

Supporting outputs such as speaker notes, scripts, transitions, Q&A preparation, pronunciation help, and group handoffs are available only as part of an eligible PPT task. They do not independently trigger this suite.

## Out of Scope

- generic presentation planning without explicit student academic context
- business, sales, company, teacher-training, or general professional decks
- standalone speech, script, Q&A, research, document, or image requests
- an attached deck without a request to review or edit it
- non-Codex manifests, external production bridges, or an alternate PPTX engine

Use a general-purpose capability when the request is outside this scope. If only the requested outcome is ambiguous, ask one routing question: outline, editable PPTX, or review.

## Skill Routing

| Requested outcome | Skill | Boundary |
| --- | --- | --- |
| PPT/slide outline or Slide Spec | `student-presentation` | May include supporting notes and Q&A; never creates PPTX |
| Create, rebuild, or explicitly edit a PPTX | `student-presentation-ppt` | Owns planning needed for production and all delivery QA |
| Review, score, compare, or diagnose an existing deck/export | `student-presentation-review` | Advice only unless file editing is explicitly requested |
| Review plus explicit file modification | review, then `student-presentation-ppt` | Preserve the source and write a separate improved copy |

Route by requested outcome, not merely by attachment type. “做 PPT”, “生成 slides”, or equivalent means PPTX production. “PPT 大纲” means planning. “优化这个 PPT” requires review first; edit the file only when the user authorizes file changes.

## Decision Authority

- Check the conversation, attachments, source deck, rubric, and Slide Spec before asking questions.
- Ask only about missing decisions that materially change the result.
- `student-presentation-ppt` must follow the mandatory Decision Gate in its production reference.
- Defaults cannot replace unresolved high-impact decisions unless the user explicitly delegates them.
- When the user says “你决定”, “按推荐方案”, or equivalent, state the selected assumptions before production.

## Runtime and Handoff

- Actual PPTX work requires the Codex `Presentations` capability.
- `imagegen` is optional and may be used only when generated imagery is useful and permitted.
- The original deck is never overwritten.
- Slide Spec is the structured planning and review-to-edit handoff.
- Existing-deck improvement produces a separate PPTX and a change summary when required.

## Ownership

- `suite-contract.md`: scope, routing, authority, runtime boundary, cross-skill handoff
- `shared-standards.md`: readability, density, language, anti-AI wording, group presentation standards
- `slide-spec.md` and schema: structured handoff format
- `image-strategy.md`: image source and fallback policy
- skill-local references: task-specific execution rules only
