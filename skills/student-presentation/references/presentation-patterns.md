# Student Presentation Patterns

This file provides reusable templates, examples, and phrase banks. Core rules are defined in `../SKILL.md` and shared standards are defined in `../../../references/shared-standards.md`.

## Requirement Questions

Check confirmed constraints from the conversation or Slide Spec meta first, then ask only for missing items that affect the plan. When choices are still needed, confirm:
- type: defense, coursework report, English presentation, group presentation, innovation/project pitch, reading report, final summary, or other
- language: Chinese, English, bilingual, or course-required format
- duration and target slide count
- individual or group; if group, member count/names and speaking order preferences
- teacher/rubric requirements, required sections, source material, and whether a full script is needed

Do not silently choose the presentation type when the user has not made it clear. If the user asks Codex to decide, state the chosen type and assumptions briefly.

Load `../../../references/shared-standards.md` for shared readability, anti-AI wording, AI-writing pattern risk, English, Chinese, and group standards. Load `../../../references/image-strategy.md` for image and visual source choices.

## Topic Narrowing

When the topic is too broad, offer 2-3 narrowed angles. Each angle should include:
- why it is suitable for the course or audience
- what evidence can realistically support it
- what the main conclusion could be
- whether it fits the time limit

Example:
- Broad topic: "AI and education"
- Better angle: "How students use AI for first drafts, not final answers"
- Why: easy to connect with class experience, surveys, examples, and a clear balanced conclusion

## General University Presentation

Use 8-12 slides for a common 5-10 minute classroom presentation:

1. Title and team/member
2. Why this topic matters
3. Core question or problem
4. Key background or concept
5. Analysis point 1
6. Analysis point 2 or example
7. Solution, insight, or result
8. Limitation or reflection
9. Conclusion
10. Q&A

## Defense Presentation

Use this for course design, graduation defense, project defense, or research report:

1. Title, student, advisor/course
2. Research/project background
3. Objective and key question
4. Method, design, or workflow
5. Main result 1
6. Main result 2
7. Problems encountered and fixes
8. Innovation or value
9. Limitations and future work
10. Thank you / Q&A

Defense wording should be confident but not exaggerated. Prefer "This project focuses on..." over "This project completely solves...".

## Coursework Report

Use this for common class reports:

1. Topic and main claim
2. Course context or why the issue matters
3. Key concept or background
4. Problem or question
5. Analysis point 1
6. Analysis point 2
7. Case/example/data
8. Insight or solution
9. Limitation or reflection
10. Conclusion / Q&A

## English Presentation

Use B1-B2 level English by default:
- keep each slide to 2-4 short sentences or phrase groups
- avoid complex long sentences, passive-heavy academic wording, and abstract slogans
- use simple connectors in notes: "First...", "This example shows...", "So the main point is...", "Now I will hand over to..."
- include optional pronunciation help or a short glossary for difficult keywords when useful
- make notes speakable rather than essay-like

Suggested structure:

1. Opening hook
2. Topic and main idea
3. Point 1
4. Point 2
5. Example or short story
6. Implication or suggestion
7. Summary
8. Thank you / questions

## Innovation Or Project Pitch

Use this for innovation, entrepreneurship, product, or practical project presentations:

1. User/problem
2. Current pain point
3. Proposed solution
4. Core feature or workflow
5. Feasibility
6. Value and difference
7. Risks or limitations
8. Next step

## Subject Presets

### Engineering

Structure: problem -> requirement -> design/implementation -> test/result -> limitation -> Q&A.

Visuals:
- architecture diagram
- process flow
- test result chart
- before/after comparison

Style:
- practical and evidence-based
- explain tradeoffs instead of claiming perfection
- highlight implementation constraints

Common scoring risks:
- no test evidence
- vague "system optimization" wording
- architecture diagram too crowded
- result not connected to the original problem

### Business

Structure: opportunity/problem -> market/user insight -> analysis -> strategy/solution -> feasibility -> risk -> conclusion.

Visuals:
- SWOT or 2x2 matrix
- market size chart
- customer journey
- simple financial or KPI table

Style:
- confident but data-supported
- avoid empty "huge market potential" claims
- make assumptions explicit

Common scoring risks:
- unsupported market claims
- unclear target users
- strategy not connected to analysis
- financial numbers without assumptions

### Humanities

Structure: text/context -> question -> interpretation -> evidence -> comparison -> significance -> reflection.

Visuals:
- quote block with annotation
- concept map
- timeline
- argument chain

Style:
- analytical and careful
- avoid absolute conclusions
- explain why an interpretation matters

Common scoring risks:
- long quoted text without analysis
- conclusion repeats background
- no clear argument chain
- missing source context

## Group Presentation Division

For 4 members and 10 slides:

- Member A: opening, background, transition to problem
- Member B: problem and analysis
- Member C: case/example and visual explanation
- Member D: solution, conclusion, Q&A lead

For 5 members and 12 slides:

- Member A: opening and topic framing
- Member B: background and key concept
- Member C: analysis 1 and data/example
- Member D: analysis 2 and solution/insight
- Member E: conclusion, reflection, Q&A lead

Rotate difficulty if there are many technical slides. Give each member at least one slide with a clear argument.

## Transition Templates

Use transitions based on the logical relationship between slides.

| Logic | Chinese transition | English transition |
| --- | --- | --- |
| Add | "更重要的是..." | "What is more important is..." |
| Contrast | "但数据告诉我们另一个事实。" | "But the data tells a different story." |
| Example | "我们班/项目里有一个很典型的例子。" | "Here is a concrete example from our class/project." |
| Cause | "造成这个现象的一个关键原因是..." | "One key reason behind this is..." |
| Summary | "回到最初的问题，我们可以看到..." | "So coming back to our original question..." |
| Handoff | "下面这部分由 X 同学继续说明..." | "Now I will hand over to X for the next part." |
| Q&A bridge | "这个问题也可能成为老师追问的重点。" | "This point may also lead to a question in the Q&A." |

## Chinese Defense Phrases

Use natural polite phrases:
- "各位老师好，我们今天汇报的题目是..."
- "我们选择这个题目，是因为它在本课程/项目中有一个很具体的问题..."
- "感谢老师的提问。这个问题主要涉及..."
- "这个地方确实是我们目前考虑不够充分的地方。"
- "基于现有数据，我们只能说明...，还不能直接证明..."
- "以上是我的分享，请老师批评指正。"

Avoid stiff or empty phrasing:
- "在当今社会快速发展的背景下"
- "本研究具有十分重要的理论和现实意义"
- "由于本人水平有限，不足之处请批评指正" when it sounds like a copied template

## Scoring Risk Warnings

Warn the user when the plan has:
- data, images, or quotes without source notes
- conclusion not supported by earlier analysis
- group member roles described only as "all members participated"
- reference formats mixed across slides
- English technical terms likely to be mispronounced
- no limitation/reflection in a defense deck
- too much background and too little result or insight

## Shared Writing And Visual Rules

Use `../../../references/shared-standards.md` for anti-AI wording, classroom readability, typography, English level, Chinese presentation norms, and group standards. Use `../../../references/image-strategy.md` for image and visual source decisions.

## Slide Density Examples

Good normal slide:

Title: "Most students use AI for first drafts, not final answers"

Main content:
- Quick idea generation
- Outline support
- Grammar polishing
- Less trust in final accuracy

Speaker note:
"This slide shows that students are not simply asking AI to finish everything. In our discussion, most people used it at the beginning of the task, especially for ideas and outlines. But when it came to final answers, they still checked or rewrote the content."

Bad normal slide:

Title: "Survey Results"

Main content:
"According to our survey, many students use artificial intelligence tools in different learning scenarios, including writing, translation, coding, searching, organizing notes, and preparing presentations. This indicates that artificial intelligence has become an important part of university learning..."

Problem: too much text, weak point, no speaking space.

## Quality Checklist

Before finalizing a plan, verify:
- each slide has one clear message
- slide body text is not a script
- normal slide text stays within the density guidance in `../../../references/shared-standards.md`
- visual suggestions explain the message
- typography can realistically follow `../../../references/shared-standards.md`
- key terms are marked for bold/color/size emphasis
- teacher-facing logic is clear
- speaker notes are natural and speakable
- transitions connect the story
- group roles are balanced when applicable
- English slides use B1-B2 level and short sentences
- the result does not sound like generic AI filler
