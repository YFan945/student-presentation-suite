# Visual Style Presets

Load `../../../references/shared-standards.md` for typography, readability, and anti-AI consistency. Load `../../../references/image-strategy.md` before choosing photo, generated image, diagram, or fallback visual treatments.

Use these presets as creative directions when the user does not provide a school template or visual direction. Ask the user to choose when visual style materially matters.

Each direction defines intent and guardrails, not a fixed template. The deck may vary layout, cover treatment, section rhythm, chart style, and visual metaphors as long as readability, density, contrast, source safety, and delivery QA remain intact.

## Structural Visual Layer

Every produced PPTX should use visible structural elements to organize information, unless the user explicitly asks for a plain text deck.

Use:
- background shape layers to divide sections
- translucent panels or frosted-glass cards behind text
- rounded or sharp rectangles as comparison cards, process nodes, and quote blocks
- thin divider lines, numbering blocks, tabs, ribbons, and section markers
- shape callouts for key findings, limitations, Q&A risks, and conclusions
- subtle shadows or blur-like glassmorphism effects only when contrast remains strong

Avoid:
- placing text directly on busy images without a readable panel
- decorative shapes that do not support hierarchy
- low-contrast glass effects
- too many floating cards on one slide
- heavy shadows or effects that make the deck look like a marketing template

Good use of glassmorphism:
- a semi-transparent white or dark panel behind text over a photo or textured background
- one or two frosted cards to separate key points
- enough opacity and contrast for classroom projection

PPTX limitation:
- PowerPoint cannot reliably reproduce CSS-style `backdrop-filter` blur across all apps.
- Treat glassmorphism as simulated layered translucent shapes, soft shadows, and muted background overlays.
- If the effect reduces readability or fails in WPS/older PowerPoint, replace it with an opaque panel, section band, or clean shape card.

Bad use of glassmorphism:
- transparent text containers over complex images
- multiple overlapping panels that make the slide noisy
- using blur/shadow effects as decoration when a simple block would be clearer

## Academic Rigorous

Best for defenses, research reports, reading reports, and teacher-facing coursework.

- Visual character: calm, evidence-first, teacher-facing, precise.
- Use when: defense, research report, reading report, course design, technical or rubric-heavy presentation.
- Creative freedom: section bands, annotated screenshots, argument chains, process diagrams, method/result pairing, restrained data emphasis.
- Guardrails: dark navy or charcoal with neutral background, one restrained accent, large conservative typography, high contrast.
- Do not sacrifice: source clarity, method/result structure, readable tables/charts, limitation/reflection slides.
- Avoid: playful colors, oversized decorative icons, flashy gradients, vague research slogans.

## Modern Minimal

Best for general classroom reports and English presentations.

- Visual character: clean, direct, spacious, easy to present.
- Use when: general classroom report, English presentation, topic introduction, conceptual explanation.
- Creative freedom: large claim titles, asymmetrical two-column pages, sparse callouts, simple icons, one strong image per section, restrained translucent panels.
- Guardrails: neutral base, black/gray text, one bright accent, simple sans-serif typography, generous spacing.
- Do not sacrifice: B1-B2 speakability, short slide text, projection contrast, natural speaker notes.
- Avoid: dense tables, visual clutter, repeated cards on every slide, decorative minimalism that leaves slides empty.

## Data Driven

Best for surveys, market analysis, experiments, and comparison-heavy decks.

- Visual character: evidence-led, comparative, quantitative, conclusion-forward.
- Use when: survey, market analysis, experiment, evaluation, performance comparison, data-backed argument.
- Creative freedom: chart-first pages, KPI strips, highlighted evidence panels, before/after comparisons, visual annotations, data-story section openers.
- Guardrails: neutral base with blue/green/orange chart accents, large labels, one chart/table per slide, one conclusion sentence.
- Do not sacrifice: data interpretation, source/date/scope notes, readable axes, clear relationship between evidence and claim.
- Avoid: raw tables without interpretation, decorative chart junk, unqualified causal claims.

## Creative Student

Best for innovation projects, design topics, campus-life topics, and light classroom showcases.

- Visual character: vivid, personal, scenario-based, student-like but still classroom-readable.
- Use when: innovation project, design topic, campus-life topic, product idea, light showcase, reflection report.
- Creative freedom: story slides, user journeys, scene images, before/after sections, concept diagrams, playful section markers, expressive but readable titles.
- Guardrails: warm accent plus neutral base, not over-saturated, strong text panels over images, meaningful visuals only.
- Do not sacrifice: topic evidence, student-specific detail, speaking clarity, image/source appropriateness.
- Avoid: decorative stock images, overdesigned covers, crowded stickers/icons, entertainment style that weakens the argument.

## Template Inheritance

If the user provides a school template:
- preserve logo, footer, school color, and required cover format
- use the template's placeholder structure when it improves consistency
- avoid fighting the template with unrelated palettes
- if placeholders are unclear, keep the school header/footer and rebuild the content area cleanly
