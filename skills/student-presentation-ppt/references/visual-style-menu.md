# Visual Style Menu

Load `../../../references/shared-standards.md` for typography, readability, and anti-AI consistency. Load `../../../references/image-strategy.md` before choosing photo, generated image, diagram, or fallback visual treatments.

Use these presets as creative directions when the user does not provide a school template or visual direction. Ask the user to choose when visual style materially matters.

Each direction defines intent and guardrails, not a fixed template. The deck may vary layout, cover treatment, section rhythm, chart style, and visual metaphors as long as readability, density, contrast, source safety, and delivery QA remain intact.

When the user is unsure about style, offer 3-5 suitable options from the style menu below. Keep the options tied to the topic and presentation situation, not a generic list. Each option should include a short reason, for example: "Academic Rigorous — safest for defense and teacher-facing evaluation" or "Creative Student — better for campus life and product showcase topics."

## Style Selection Menu

| Style | 中文别名 | Best for | Visual signal | Palette direction |
| --- | --- | --- | --- | --- |
| Academic Rigorous | 学术严谨 | defense, research report, reading report, course design | restrained, evidence-first, formal | navy/charcoal + neutral + one accent |
| Modern Minimal | 现代简洁 | general classroom report, English presentation, concept explanation | clean, spacious, direct | white/gray + bright accent |
| Data Driven | 数据驱动 | survey, experiment, market analysis, comparison | chart-first, KPI-led, evidence-heavy | neutral + blue/green/orange data accents |
| Creative Student | 学生创意 | innovation, campus life, design topic, product idea | vivid, scenario-based, student-like | warm accent + neutral base |
| Midnight Business | 深蓝商务 | business case, entrepreneurship, strategy, management | dark cover, polished corporate rhythm | `1E2761` navy + `CADCFC` ice blue + white |
| Forest Moss | 森林苔藓 | sustainability, agriculture, ecology, health, social good | organic, grounded, calm | `2C5F2D` forest + `97BC62` moss + cream |
| Coral Energy | 珊瑚活力 | marketing, youth topic, campaign, creative proposal | energetic, optimistic, attention-grabbing | `F96167` coral + `F9E795` gold + navy |
| Warm Terracotta | 暖陶人文 | culture, humanities, community, education reflection | warm, documentary, human-centered | `B85042` terracotta + `E7E8D1` sand + `A7BEAE` sage |
| Ocean Tech | 海洋科技 | software, AI, engineering, systems, future topic | technical, fluid, high-trust | `065A82` deep blue + `1C7293` cyan + `21295C` midnight |
| Charcoal Editorial | 炭黑杂志 | literature, critique, portfolio, serious analysis | magazine-like, monochrome, typographic | `36454F` charcoal + `F2F2F2` off-white + black |
| Teal Trust | 青绿可信 | healthcare, public service, education technology, UX | reliable, clear, friendly | `028090` teal + `00A896` seafoam + `02C39A` mint |
| Berry Cream | 莓果奶油 | psychology, social research, gender/culture, reflective topics | soft, thoughtful, distinctive | `6D2E46` berry + `A26769` dusty rose + `ECE2D0` cream |
| Sage Calm | 鼠尾草平静 | wellness, counseling, learning habits, low-stress reports | quiet, balanced, natural | `84B59F` sage + `69A297` eucalyptus + `50808E` slate |
| Cherry Bold | 樱桃醒目 | debate, persuasive pitch, warning/risk, strong conclusion | bold, high-contrast, memorable | `990011` cherry + `FCF6F5` off-white + navy |

## Choosing For An Unsure User

When the user says they are unsure, gives only a topic, or asks "你来定", offer or choose styles this way:
- Defense/research/teacher-scored work: offer `Academic Rigorous`, `Data Driven`, and topic-specific `Ocean Tech` or `Charcoal Editorial`.
- Business/entrepreneurship/project pitch: offer `Midnight Business`, `Data Driven`, and `Coral Energy`.
- AI/software/engineering/system design: offer `Ocean Tech`, `Academic Rigorous`, and `Modern Minimal`.
- Sustainability/health/social good: offer `Forest Moss`, `Teal Trust`, and `Academic Rigorous`.
- Humanities/culture/education reflection: offer `Warm Terracotta`, `Charcoal Editorial`, and `Berry Cream`.
- Campus life/creative/product concept: offer `Creative Student`, `Coral Energy`, and `Modern Minimal`.
- If the grading context is unknown, include at least one conservative option and one expressive option.

When asking a Chinese user to choose, show the English style name and 中文别名, for example `Ocean Tech（海洋科技）`. Do not overwhelm the user with all styles. Offer the top choices, unless the user explicitly asks Codex to decide.

## General Visual Principles

- choose a palette that feels specific to the topic instead of defaulting to blue
- use 60-70% dominant color weight, 1-2 supporting colors, and one accent
- create clear hierarchy through size, color, spacing, and section rhythm
- use a consistent visual motif across the whole deck: rounded image frames, numbered tabs, side bars, circular icons, thick edge bands, or chart callout pills
- vary layouts across slides instead of repeating the same card grid
- use dark cover/conclusion with lighter content slides when appropriate
- every slide should include a meaningful visual element: photo, chart, icon, diagram, structural shape, timeline, process, or comparison block
- never use decorative underline strokes under titles; use spacing, bands, background blocks, or typography instead

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

PPTX limitation on glassmorphism: PowerPoint cannot reliably reproduce CSS-style `backdrop-filter` blur across all apps. Treat glassmorphism as simulated layered translucent shapes, soft shadows, and muted background overlays. If the effect reduces readability or fails in WPS/older PowerPoint, replace it with an opaque panel, section band, or clean shape card.

## Template Inheritance

If the user provides a school template:
- preserve logo, footer, school color, and required cover format
- use the template's placeholder structure when it improves consistency
- avoid fighting the template with unrelated palettes
- if placeholders are unclear, keep the school header/footer and rebuild the content area cleanly
