# Visual Style Presets

Load `../../../references/shared-standards.md` for typography, readability, and anti-AI consistency. Load `../../../references/image-strategy.md` before choosing photo, generated image, diagram, or fallback visual treatments.

Use these presets when the user does not provide a school template or visual direction. Ask the user to choose when visual style materially matters.

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

- Palette: dark navy or charcoal, white background, one restrained accent
- Layout: clear title, structured blocks, diagrams, data tables, restrained section bands
- Typography: large, conservative, high contrast
- Visuals: process diagrams, charts, annotated screenshots, shape-framed evidence blocks
- Avoid: playful colors, oversized decorative icons, flashy gradients

## Modern Minimal

Best for general classroom reports and English presentations.

- Palette: neutral background, black/gray text, one bright accent
- Layout: large claim title, two-column explanation, sparse callouts, translucent content panels
- Typography: simple sans-serif, generous spacing
- Visuals: clean diagrams, one strong image per key section, glass-style text panels when needed
- Avoid: dense tables and visual clutter

## Data Driven

Best for surveys, market analysis, experiments, and comparison-heavy decks.

- Palette: neutral base, blue/green/orange chart accents
- Layout: chart-first slide, conclusion sentence, supporting note, KPI strips and shape-based annotations
- Typography: large labels and short annotations
- Visuals: bar charts, line charts, comparison cards, KPI strips, highlighted evidence panels
- Avoid: raw tables without interpretation

## Creative Student

Best for innovation projects, design topics, campus-life topics, and light classroom showcases.

- Palette: warm accent plus neutral base, not over-saturated
- Layout: case/story slides, process snapshots, before/after sections, layered cards or soft panels
- Typography: readable but more expressive titles
- Visuals: user journey, scene images, concept diagrams, image-backed panels with readable overlays
- Avoid: decorative stock images that do not explain the message

## Template Inheritance

If the user provides a school template:
- preserve logo, footer, school color, and required cover format
- use the template's placeholder structure when it improves consistency
- avoid fighting the template with unrelated palettes
- if placeholders are unclear, keep the school header/footer and rebuild the content area cleanly
