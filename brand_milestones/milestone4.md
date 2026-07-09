# Prisent Corporate Brand Guidelines & Production Manual v1.0

**Document Reference:** Corporate Identity Manual & Brand System

**Milestone:** 4 — Final Production Baseline

**Status:** Released for Production Use

**Target Audience:** Internal Design Teams, Frontend Engineers, Product Managers, Global Operations

**Classification:** Corporate Source of Truth

---

## 1. Brand Introduction & Operational Philosophy

Prisent represents a fundamental paradigm shift in enterprise computing: the transition from reactive, human-prompted software to autonomous, proactive execution networks. The Prisent identity is built on the philosophy of **Structural Functionalism**. We purposefully reject the temporary visual trends of early artificial intelligence software—such as neon gradients, robotic characters, and abstract glowing blobs—in favor of a disciplined, premium, and industrial-grade system. This manual acts as the absolute strategic and technical source of truth for all corporate touchpoints, ensuring absolute consistency across software interfaces, physical assets, and global communications.

---

## 2. Strategic Core: Mission, Vision, & Values

Every asset created for Prisent must reflect our strategic foundations. If a marketing piece, UI component, or corporate document violates these definitions, it must be rejected during review.

### Brand Mission

To build AI-native systems that proactively transform ideas into execution through intelligent agents, automation, and autonomous workflows.

### Brand Vision

Become one of the world's leading AI-native companies building proactive AI systems that think, collaborate, and execute work for individuals and businesses.

### Core Corporate Values

- **Execution over Intention:** We value finished, verified results over promises, descriptions, or open-ended configurations.
- **Precision:** Every line of code, text layout, and visual border must match exact mathematical metrics.
- **Simplicity:** We remove unnecessary friction, decorative elements, and choices from every workflow.
- **Trust:** We maintain long-term confidence through transparent system logs and predictable security compliance.
- **Innovation:** We continually push the boundaries of orchestration speed, agent logic, and infrastructure performance.
- **Human-Centered AI:** We ensure that users always retain clear oversight, verification capabilities, and final decision-making power.

---

## 3. Brand Personality Attributes

The corporate personality defines how Prisent presents itself to the world. It is a unified framework composed of eight distinct characteristics:

```
 Professional ─── Premium ─── Technical ─── Minimal
    Modern    ─── Trustworthy ─── Intelligent ─── Timeless
```

These attributes require a highly disciplined visual and verbal style. All public assets must remain calm, objective, and authoritative, avoiding casual humor, decorative flourishes, or temporary design trends.

---

## 4. The Logo System & Construction Architecture

### Logo Construction Grid

The Prisent logo icon is a geometric character constructed on a strict $16 \times 16$ unit power-of-two grid layer. The unit variable $X$ represents the baseline width of the primary vertical stroke.

```
       |<─── 4X ───>|
    ───┌────────────┐───
    ▲  │ ┌────────┐ │ ▲
    │  │ │        │ │ │
    4X │ └────────┘ │ 2X
    │  │ ┌────────┐ │ │
    ▼  │ └────────┘ │ ▼
    ───└─┐          └───
         │
         │ <── 1X (Stroke Width)
         │
```

- **Vertical Stem:** Occupies a fixed 2-unit width on the left boundary.
- **Parallel Pathways:** Made of three horizontal loops, each exactly 2 units in height, separated by 2-unit negative space channels.
- **Concentric Corner Radii:** External curves use matching radii (outer curve = 4 units, middle curve = 2 units, internal corner = 0 units) to keep the pathway lines perfectly parallel through the turn.

### Logo Clear Space Rules

To protect the visual clarity of the mark, maintain a strict clear space around the asset on all sides. This boundary is defined as $2X$, equal to twice the width of the primary stroke. No text, borders, or secondary elements may enter this area.

```
┌────────────────────────────────────────┐
│               Clear Space (2X)         │
│     ┌────────────────────────────┐     │
│     │                            │     │
│ 2X  │         [ LOGO ]           │  2X │
│     │                            │     │
│     └────────────────────────────┘     │
│               Clear Space (2X)         │
└────────────────────────────────────────┘
```

### Sizing Limits

- **Digital Canvas:** Icon Only minimum resolution is $16\text{px} \times 16\text{px}$. Full Lockup minimum height is $24\text{px}$.
- **Physical Print:** Icon Only minimum footprint is $6\text{mm} \times 6\text{mm}$. Full Lockup minimum height is $8\text{mm}$.

---

## 5. Approved System Configurations

The logo system is configured into four approved layouts. Never create alternative arrangements of these components.

### 1. Horizontal Lockup (Primary configuration)

Used on the main website navigation bar, primary app headings, and formal corporate letterheads. The icon is placed on the left, separated from the wordmark by an exact clear gap of $2X$.

```
 [ICON]  (2X Gap)  PRISENT
```

### 2. Vertical Lockup (Secondary configuration)

Reserved for centered landing pages, presentation slide covers, product packaging, and corporate merchandise labels. The icon is centered directly above the wordmark, separated by a vertical gap of $1.5X$.

```
 [ICON]
(1.5X Gap)
PRISENT
```

### 3. Icon-Only (Utility layer)

Used exclusively inside constrained environments like browser favicons, system application shortcuts, in-app notification windows, and social media profile icons.

```
 [ICON]
```

### 4. Wordmark-Only (Technical layer)

Reserved for plain-text terminal headers, API code documentation titles, legal contracts, and back-page copyright lines where graphic symbols are not required.

```
 PRISENT
```

---

## 6. Prohibited Variations & Distortion Controls

To protect the integrity of our visual identity, the following adjustments are strictly banned across all internal and external layouts:

```
[ BANNED: Rotations or Angled Placements ] ──► Breaks the grid structure
[ BANNED: Outlining the Parallel Lines   ] ──► Confuses the stroke weights
[ BANNED: Adding Decorative AI Sparkles  ] ──► Violates minimal design rules
```

- **No Geometric Distortion:** Never stretch, squeeze, flatten, angle, or skew the logo paths.
- **No Multi-Color Gradients:** Never apply gradients, drop shadows, or background glows to the mark. The logo must remain flat and single-colored.
- **No Custom Enclosures:** Never place the logo inside decorative non-functional shapes like badges or circles unless deploying standard operating system app icons.
- **No Element Separation:** Never rearrange or adjust individual lines within the parallel loop paths independently of the official vector files.

---

## 7. The Visual Identity Matrix: Color, Type, & Space

### Corporate Color Tokens

The color architecture uses a high-contrast monochrome base to keep interfaces focused and clean, with a single functional accent color to highlight active processes.

| Token Type | Variable Name | Hex Code | Purpose & Core Application |
| --- | --- | --- | --- |
| **Canvas Base** | `color-deep-carbon` | `#09090B` | Default dark mode background; absolute text color in light mode. |
| **Surface Bed** | `color-core-slate` | `#18181B` | Secondary interface cards, container panels, and sidebars. |
| **Text Muted** | `color-mid-grey` | `#71717A` | Placeholder inputs, disabled statuses, and secondary descriptions. |
| **Grid Boundary** | `color-steel-muted` | `#27272A` | Subdued 1px layout lines, grid borders, and panel dividers. |
| **System Accent** | `color-precision-amber` | `#D97706` | Active tracking indicators, success updates, and code alerts. |
| **Light Canvas** | `color-pure-light` | `#FAFAFA` | Light mode workspace background; primary text color in dark mode. |

### Typographic Specifications

We use clean, legible fonts across all interfaces, reserving our monospaced face exclusively for technical system metrics and code updates.

- **Display & Heading Font:** *Geist Sans*. A modern neo-grotesque sans-serif featuring tight character tracking, designed for structural headlines.
- **Body Interface Font:** *Inter*. A clean sans-serif optimized for readability across dense informational paragraphs and text fields.
- **Technical Log Font:** *Geist Mono*. A geometric monospaced font used for all source code examples, active terminal logs, status values, and numerical readouts.

### Layout Type Scale Matrix

| Scale Token | Font Family | Size (px) | Line Height | Letter Spacing | Operational Application |
| --- | --- | --- | --- | --- | --- |
| `type-display-xl` | Geist Sans | 48px | 1.1 | `-0.04em` | Primary marketing hero headlines |
| `type-heading-lg` | Geist Sans | 32px | 1.2 | `-0.03em` | Core section titles, module headers |
| `type-heading-md` | Geist Sans | 24px | 1.3 | `-0.02em` | Grid card headers, modal titles |
| `type-body-base` | Inter | 15px | 1.5 | `0.00em` | Explanatory copy, content blocks |
| `type-body-sm` | Inter | 13px | 1.4 | `0.01em` | Data forms, text labels, tooltips |
| `type-mono-base` | Geist Mono | 14px | 1.4 | `0.00em` | Active logs, system metrics, code |

To ensure smooth visual proportions across varied viewports, headings must scale fluidly using this standardized calculation formula:

$$FS = FS_{min} + (FS_{max} - FS_{min}) \times \left(\frac{W - W_{min}}{W_{max} - W_{min}}\right)$$

Where $W_{min} = 375\text{px}$, $W_{max} = 1440\text{px}$, and individual text components adapt dynamically between their specified point boundaries.

### The 8px Spatial Layout Matrix

All layout spacing, card padding, and structural margins must use exact increments of 8px to guarantee visual consistency across the platform.

```
[4px: Micro-gap] ──► [8px: Base Step] ──► [16px: Card Padding] ──► [24px: Module Gap]
```

- **Component Corner Contours:** Apply a strict 4px radius to interactive buttons and input fields. Structural modules like dashboard cards and code frames use a 6px corner radius. Never use round, pill-shaped corners or organic curves.

---

## 8. Applied Interface Elements: Asset Guidelines

### Icon Design Principles

All system icons must feature a single 1.5px stroke width aligned precisely to a 24px grid layout. Use sharp geometric shapes and avoid filled backgrounds, dual-tone highlights, or drop shadows.

### Illustration Architecture

Replace decorative graphics with clean technical wireframes, system architecture charts, and vector blueprints. Render illustrations using thin monochrome lines, explicit flow arrows, and monospaced label descriptions to clarify system pathways.

### Photography Framework

Use documentary-style photography showing real development environments, natural workspace lighting, and engineering teams focused on actual work. Never use staged stock photography, artificial studio lighting, or fake corporate poses.

---

## 9. Linguistic Framework: Voice, Tone, & Messaging

### Brand Voice

Prisent speaks with the authoritative voice of an expert infrastructure engineer. We describe software capabilities with direct, factual precision, eliminating marketing fluff, superficial hype, and unnecessary adjectives.

- **Incorrect (Hype-driven):** "We are incredibly excited to bring you a magical, mind-blowing AI assistant to crush your task list!"
- **Correct (Authoritative):** "Prisent deploys asynchronous agent pipelines, orchestrating workflows with deterministic system verification."

### Tone Modulation Guidelines

While our brand voice remains consistently authoritative, our tone adjusts to suit the user's immediate context.

```
 Marketing Surface: [Informative & Direct] ──► Factual values, zero empty filler
 Product Error Logs: [Analytical & Clear] ──► Direct root causes, clear solutions
 Success Confirmations: [Quiet & Minimal] ──► Clean checkmarks, zero self-praise
```

- **Marketing Platforms:** Maintain an informative and direct tone. Use clean value definitions and straightforward capability descriptions.
- **Product Error States:** Maintain an analytical and clear tone. Provide immediate explanations of the technical issue along with actionable steps to resolve it.
- **System Success Messages:** Maintain a quiet and minimal tone. Provide immediate confirmation of completed tasks without self-congratulatory text or animations.

### Keyword Framework

- **Core Pillars (Approved for use):** Proactive, Execution, Autonomy, Precision, Deterministic, Infrastructure, System, Workflow.
- **Contextual Variables (Permitted for use):** Automation, Intelligence, Agentic, Calibration, Coordination, Flow.
- **Banned Terminology (Prohibited across all assets):** Wizard, Magic, Robot, Bot, Assistant, Co-pilot, Buddy, Brain, Guru.

---

## 10. Digital Product Layouts: Implementation Specs

### Website & Landing Page Configurations

- **Hero Sections:** Place our core corporate tagline clearly over a high-contrast structural code matrix or interactive flowchart that demonstrates real-world agent orchestration paths.
- **Layout Divisions:** Use clean 1px border lines (`#27272A`) to structure case studies and feature modules. Replace abstract marketing shapes with actual, working code blocks and performance charts.

### Dashboard Architecture & Analytics Panels

- **Structural Layout:** Divide the workspace into three distinct zones: a left-hand configuration panel (fixed at 240px width), a large, center workflow canvas, and a right-hand terminal stream for active monitoring.
- **Data Layout:** Display active processes using live monospaced text streams. Use a single amber light indicator (`#D97706`) to highlight running tasks clearly, without adding unnecessary background noise.

### Technical Documentation Systems

- **Two-Column Split Layout:** Position clear, step-by-step instructions in the left column, paired with a live, interactive execution terminal in the right column. This ensures developers can view and test code commands instantly within a single screen.

```
┌──────────────────────────────┬──────────────────────────────┐
│  Technical Instructions      │  Live API Terminal           │
│  1. Configure webhook target │  $ prisent init --token xyz  │
│  2. Define proactive triggers│  [OK] Agent stream deployed   │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 11. Media & Communications Style Guide

### Social Media Layout Matrices

- **Content Direction:** Focus content around product updates, performance benchmarks, and real-world development use cases.
- **Visual Structure:** Place text and imagery inside clear layout boxes built on our 8px grid. Use clean, high-contrast dark backdrops for all code graphics.

### Technical Presentations & Slide Decks

- **Slide Alignment:** Build presentation layouts using the 8px grid. Use structural dark backgrounds for technical developer presentations and light backgrounds for engineering documentation.
- **Data Visualization:** Present all charts, timelines, and architecture graphs clearly on clean grid lines, ensuring metrics are easy to read from the back of an auditorium.

### Corporate Email Communication Signatures

- **Plain Text Formatting:** Keep signatures clean, professional, and text-only, using a standard monospaced layout. Do not include logo images, custom font styles, or decorative color streaks.

```
Muhammad Sufyan Shah
AI Infrastructure Lead | Prisent
sufyan@prisent.com | https://prisent.com
[Proactive AI that turns ideas into execution]
```

---

## 12. Corporate Stationery & Identity Ephemera

### Business Card Architecture

To maintain our technical, high-end branding, corporate cards must use a minimal, text-focused design on heavy, premium cardstock.

- **Materials Parameter:** Use heavy 400gsm premium duplex cotton cardstock featuring absolute matte black edges.
- **Front Layout:** Stamp the primary horizontal logo lockup in sharp matte white ink directly in the center of the card.
- **Back Layout:** Format personal contact details cleanly on the left side using our monospaced typeface. All layout boundaries must match our strict 8px grid rules.

```
┌────────────────────────────────────────┐
│ Muhammad Sufyan Shah                   │
│ AI Infrastructure Lead                 │
│                                        │
│ sufyan@prisent.com                     │
│ Karachi, PK                            │
└────────────────────────────────────────┘
```

### Premium Merchandise & Corporate Apparel

- **Design Rule:** Corporate apparel must function as high-quality, long-lasting designer items rather than cheap promotional giveaways.
- **Apparel Style:** Use premium heavyweight organic cotton hoodies and shirts in matte black (`#09090B`). Place the logo icon as a small, high-density black-on-black embroidery on the left chest, or patch a clean white horizontal lockup onto the lower sleeve. Never print large, colorful marketing slogans across the chest.

---

## 13. System Utilities: Iconography, Mobile, & Global Compliance

### Favicon Implementation Specifications

- **Pixel Boundaries:** At the small $16\text{px} \times 16\text{px}$ scale, standard anti-aliasing can blur parallel lines. The favicon icon file must be manually aligned directly to the pixel grid, rounding our optical stroke widths back to a solid 2px line to guarantee sharp rendering across all browsers.

### Mobile & Native App Design Systems

- **App Icon Geometry:** Center our logo icon over a deep charcoal canvas background (`#0A0A0A`). The mark must occupy exactly 55% of the total bounding container box, leaving a 45% clear outer margin to balance visual weight next to native system apps.
- **Mobile Interface Layout:** Retain our strict 16px container padding and 4px button corner radius across all mobile interfaces, using a single-column layout to display tracking workflows and live terminal metrics clearly on smaller screens.

### Accessibility Framework & Compliance

The interface is engineered to comply with WCAG 2.1 AA accessibility standards, ensuring high usability across all digital touchpoints.

- **Contrast Standards:** Maintain a minimum contrast ratio of 4.5:1 for standard body text and 3:1 for large display headers.
- **Keyboard Controls:** All interactive dashboard elements, menu items, and input nodes must support full keyboard navigation, featuring high-visibility focus borders (`#D97706`).
- **Screen Reader Optimization:** Every functional icon and system diagram must include explicit descriptive labels (`aria-label`), ensuring clear navigation for users with screen readers.

---

## 14. Brand Evolution & Long-Term Roadmap

To preserve the strength of our primary corporate name, Prisent enforces a disciplined **Monolithic House Style**. All future modules, packages, and engineering updates must be integrated as core components of our main brand ecosystem rather than separate sub-brands.

```
[ Phase 1: Years 1-2 ] ──► Precision Developer Tooling (Codebase migration)
[ Phase 2: Years 3-5 ] ──► Integrated Workflow Architecture (Cross-team pipelines)
[ Phase 3: Years 6-10] ──► Global Autonomous Operating Layer (Enterprise fleets)
```

- **Phase 1 (Years 1–2): Precision Developer Tooling.** Focus branding exclusively around technical utilities, advanced code execution, and high-quality API documentation to establish absolute developer trust.
- **Phase 2 (Years 3–5): Integrated Workflow Architecture.** Expand the platform's visual identity into cross-functional team dashboards, connecting developer tracking tools seamlessly with general business operations.
- **Phase 3 (Years 6–10+): Global Autonomous Operating Layer.** Position Prisent as the global orchestration infrastructure for autonomous business operations, managing long-term agent networks for the world's leading enterprises.

---

## 15. Operational Compliance Checkpoints

Before launching any product feature, marketing campaign, or public asset, the design must clear this compliance review:

- [ ] **Grid Check:** Does the asset follow our 8px layout grid and specific corner radius rules?
- [ ] **Color Verification:** Are colors limited to our core monochrome palette, using the amber accent color strictly for active functional statuses?
- [ ] **Typography Scale:** Does text styling and tracking match our official font scale definitions?
- [ ] **Keyword Compliance:** Is the copy free of banned words like "magic," "wizard," or "co-pilot"?
- [ ] **Asset Authenticity:** Are illustrations limited to clean technical diagrams, and is all photography free of staged stock photos?
- [ ] **Accessibility Standards:** Does the interface layout meet our WCAG 2.1 AA contrast and keyboard focus standards?
