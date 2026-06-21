# Controlled Content Workflow

Use this workflow for complete outlines, stronger content, speaker notes, high-score treatment, or iterative revision.

## Goal Confirmation

Before drafting, summarize the confirmed goal in five short fields:

- scenario and required outcome
- main audience and knowledge level
- expected conclusion or judging emphasis
- duration/slide target
- available evidence and missing evidence

Do not repeat questions already answered by the conversation, rubric, source material, or Slide Spec.

## Layered Generation

Generate in this order:

1. **Story directory:** section names and one-sentence narrative arc.
2. **Slide purposes:** one audience takeaway per slide.
3. **Slide points:** two to four evidence-linked points.
4. **PPT text:** concise projection-readable wording.
5. **Speaker notes:** natural explanation, examples, transitions, and boundaries.

Do not write final slide prose before the directory and slide purposes are coherent. Keep PPT text and speaker notes separate.

## Scenario And Audience

| Scenario | Default structure | Main emphasis |
| --- | --- | --- |
| Course report | context → question → analysis → example/evidence → insight | course understanding and clear explanation |
| Defense | background → objective → method/work → result → limitation → Q&A | traceable work and defensible evidence |
| Competition | problem → user/evidence → solution → feasibility → value → risk | differentiation, feasibility, measurable value |
| Club showcase | identity → activity story → outcomes → member experience → next step | participation, authenticity, visual storytelling |
| Research presentation | question → literature/context → method → results → discussion → limits | method, evidence, interpretation, citations |

Adapt depth by audience:

- teacher: connect claims to rubric, course concepts, method, and limitations
- classmates: explain unfamiliar terms and use relatable examples
- judges: lead with differentiation, evidence, feasibility, and risk
- non-specialists: minimize jargon and explain why each result matters
- mixed: use plain-language main slides with technical detail in notes or appendix

## Argument Strengthening

For every important claim, seek evidence, interpretation, and a boundary. Use data, sources, cases, experiments, comparisons, feedback, or project artifacts.

Never invent statistics, papers, survey results, user feedback, or citations. Mark missing support as `to-verify`. Mark hypothetical examples as `illustrative`.

Rewrite content that is generic, repetitive, exaggerated, or detached from the student's actual course/project. Add one concrete context, observation, process detail, evidence item, or limitation.

## Controlled Revision

- Respect every `locked_fields` entry.
- In partial mode, modify only `revision_contract.targets`.
- Report requested changes that conflict with locked content instead of silently overriding it.
- After revision, summarize changed slides, preserved slides, locked fields, and unresolved evidence.

## Training Outputs

When requested or when `quality_tier: high-score` and useful, add:

- one keyword card per section
- likely teacher/judge questions tied to weak evidence or limitations
- concise answer points with an honest boundary
- cumulative timing and slides likely to overrun
- one sentence explaining why the selected structure and key layouts fit
