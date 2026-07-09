# Prisent Visual Identity System Specification v1.0

This specification guide defines the technical implementation rules for the Prisent visual identity system. It translates the approved brand strategy and geometric logo architecture into concrete design tokens, structural layouts, UI patterns, and accessibility standards.

---

## 1. The Chromatic System & Themes

The Prisent color architecture functions as a calibration system. It uses an industrial, high-contrast monochrome base to minimize visual noise and a single functional accent color to draw immediate focus to active workflows.

### Color Palettes & Values

| Palette Layer | Color Name | Hex Code | Purpose & Application |
| --- | --- | --- | --- |
| **Primary Base** | Deep Carbon | `#09090B` | Primary interface canvas for dark mode; absolute dark text for light mode. |
| **Primary Surface** | Core Slate | `#18181B` | Secondary container backgrounds, card beds, and structural sidebars. |
| **Secondary Layer** | Mid Grey | `#71717A` | Inactive states, placeholder values, and secondary descriptive text. |
| **Secondary Border** | Steel Muted | `#27272A` | Subdued borders, structural grid lines, and canvas dividing boundaries. |
| **Accent Color** | Precision Amber | `#D97706` | Active background processes, success logs, and strategic validation points. |
| **Neutral Canvas** | Pure Light | `#FAFAFA` | Primary interface canvas for light mode; absolute white text for dark mode. |

```
[ Deep Carbon: #09090B ] ─────────────────────────► Primary Interface Bed
  [ Steel Muted: #27272A ] ───────────────────────► Structural Grid Dividers
    [ Precision Amber: #D97706 ] ─────────────────► Asynchronous Action Alerts
```

### Dark Theme Blueprint (Default)

The dark theme serves as Prisent’s default environment. It mimics the look of a developer’s code editor to reduce eye strain during extended work sessions.

- **Application:** Set the primary background to Deep Carbon (`#09090B`), use Core Slate (`#18181B`) for component surfaces, and render primary typography in Pure Light (`#FAFAFA`). Internal layout dividers must use crisp 1px lines in Steel Muted (`#27272A`).
- **Professional Reasoning:** Dark mode reduces visual fatigue for technical users and developers. It sets a serious, focused tone that frames the software as permanent background infrastructure.

### Light Theme Blueprint (Alternative)

The light theme acts as a clean, high-contrast alternative that mirrors the look of printed technical documentation.

- **Application:** Invert the canvas by setting the background to Pure Light (`#FAFAFA`), using an off-white tint (`#F4F4F5`) for component surfaces, and rendering primary typography in Deep Carbon (`#09090B`). Borders transition to a clean light grey (`#E4E4E7`).
- **Professional Reasoning:** A light theme ensures text remains easy to read in bright outdoor environments or high-glare workspaces, meeting professional usability standards across all conditions.

---

## 2. Typographic Architecture

Prisent's typography relies on a strict, mathematical type scale. It pairs clean, structured geometric headers with a high-readability monospace font for system states and technical metrics.

### Family Selections

- **Display & Heading Font:** *Geist Sans* (or standard *Inter Tight* fallback). A clean, neo-grotesque sans-serif with tight character spacing designed for highly visible structural headers.
- **Body Font:** *Inter* (or standard *SF Pro Text* fallback). A highly legible font with clear character shapes that remains easy to read across dense lines of text.
- **Monospace Font:** *Geist Mono* (or standard *SF Mono* fallback). Used for all system code examples, terminal logs, status values, and numerical metrics.

### Typographic Hierarchy Matrix

| Step | Token Name | Size (px) | Line Height | Tracking | Applied Use Case |
| --- | --- | --- | --- | --- | --- |
| **01** | `display-xl` | 48px | 1.1 | `-0.04em` | Main landing page hero headlines |
| **02** | `heading-la` | 32px | 1.2 | `-0.03em` | Primary section headers, main titles |
| **03** | `heading-md` | 24px | 1.3 | `-0.02em` | Card titles, dashboard module headers |
| **04** | `body-base` | 15px | 1.5 | `0.00em` | Standard descriptive copy, text paragraphs |
| **05** | `body-sm` | 13px | 1.4 | `0.01em` | Tooltips, form labels, secondary descriptions |
| **06** | `mono-base` | 14px | 1.4 | `0.00em` | Active terminal views, code streams, status logs |

### Fluid Type Scale Formula

To maintain precise proportions as screens change size, titles must scale smoothly between viewport boundaries using this fluid font-size calculation:

$$FS = FS_{min} + (FS_{max} - FS_{min}) \times \left(\frac{W - W_{min}}{W_{max} - W_{min}}\right)$$

Where $W_{min} = 375\text{px}$, $W_{max} = 1440\text{px}$, and the text boundaries scale smoothly between their minimum and maximum point values.

---

## 3. Spatial Matrix & Structural Foundations

The layout system is built on an absolute mathematical grid. This structure ensures all elements align predictably, making complex technical dashboards easier to scan and navigate.

### The 8px Spacing System

All margins, padding, and layout distances must use increments of 8px to maintain consistent spatial pacing across the platform.

```
[4px: Micro] ──► [8px: Baseline] ──► [16px: Container Padding] ──► [24px: Section Gap]
```

- **Increments:** 4px (micro-adjustments), 8px (baseline step), 16px (standard component padding), 24px (card layouts), 32px (sub-sections), 48px (major modules), 64px (hero sections).

### The Grid Layer

- **Desktop Layouts (≥1280px):** 12-column symmetrical grid, 24px column gutters, 48px outer page margins.
- **Dashboard Workspaces:** Pin the left sidebar to a fixed 240px width. The remaining application workspace scales fluidly, dividing into a multi-column modular grid based on 8px grid lines.

### Border Radius & Contour Rules

- **Interactive Components (Buttons, Input Fields):** Fixed 4px corner radius.
- **Structural Modules (Dashboard Cards, Code Blocks):** Fixed 6px corner radius.
- **Banned Contours:** Do not use soft, organic curves or pill-shaped borders for structural elements. Buttons and input containers must retain sharp, architectural corners.

### Shadow Architecture (Ambient Occlusion)

Prisent avoids heavy, blurry drop shadows. Instead, it uses subtle, multi-layered ambient occlusion lines to give elements clean definition and a slight sense of depth without adding visual clutter.

- **Standard Component Edge:** `0 1px 2px 0 rgba(0, 0, 0, 0.05)`
- **Overlay Module / Command Palette Menu:**
  ```css
  box-shadow: 
    0 0 0 1px rgba(0, 0, 0, 0.1),
    0 4px 12px 0 rgba(0, 0, 0, 0.08),
    0 12px 32px 0 rgba(0, 0, 0, 0.12);
  ```

---

## 4. Visual Language Assets & Motion

Every icon, illustration, and movement within the interface must emphasize structural clarity and system responsiveness.

### Icon Architecture

- **Stroke Rules:** Use a constant 1.5px stroke width aligned precisely to a 24px grid canvas. Keep corners sharp and geometric.
- **Visual Style:** Icons must function as clean, technical labels. Do not use filled shapes, dual-tone accent colors, or decorative drop shadows.

### Illustration Style

- **Technical Outlines:** Replace generic abstract illustrations with clean system blueprints, flowcharts, and vector wireframes.
- **Presentation:** Use thin monochrome lines, explicit labels, and monospaced text annotations to clearly show data pathways and agent logic.

```
  [Input Event] ────► [Intelligent Agent Layer] ────► [Verified Output]
       │                        │                         │
  (Mono Label)             (Mono Label)              (Mono Label)
```

### Photography Direction

- **Authentic Workspaces:** Use documentary-style photography featuring real technical workspaces, natural lighting, and engineers focused on actual development challenges.
- **Prohibitions:** Do not use staged stock photos, artificial studio lighting, or fake corporate environments.

### Animation & Motion Principles

Movement inside the interface should convey high performance and mechanical precision.

- **Duration Guidelines:** Standard transitions must remain short and snappy: 150ms for small hover states, 250ms for opening larger overlay panels.
- **Easing Profiles:** Use precise linear-to-exponential easing curves (`cubic-bezier(0.16, 1, 0.3, 1)`). Avoid playful bouncing animations, slow decorative transitions, or unnecessary loading loops.

---

## 5. Digital Product Surfaces & Interface Architecture

The interface structure balances clear visual layout with high information density, prioritizing immediate access to system metrics and configuration options.

### UI Components (Core Elements)

- **Primary Button:** A solid block matching the primary text color (Pure Light in dark mode, Deep Carbon in light mode) with sharp 4px corners and bold, centered text. Hover states trigger a subtle opacity shift to 90%.
- **Command Palette:** Activated via `Cmd + K`. A clean, centered modal menu with a 1px border that lets users search and run complex workflows directly via keyboard shortcuts.

### Dashboard Architecture

- **Layout:** Divide the workspace into a clear configuration panel on the left, an interactive workflow canvas in the center, and a live tracking terminal stream on the right.
- **Telemetry Feeds:** Display live agent loops using monospaced text streams. Use single-color semantic indicators (like a steady amber light) to highlight active processes without cluttering the screen.

### Website & Landing Page Design

- **Hero Section:** Position the clear corporate tagline over an interactive structural wireframe that demonstrates real-world agent orchestration paths.
- **Content Sections:** Use sharp 1px grid borders to structure case studies and performance data, replacing abstract graphics with actual code blocks and performance charts.

### Documentation Style

- **Layout:** A side-by-side split layout featuring step-by-step instructions on the left and a live, interactive API terminal on the right. This ensures developers can test code configurations instantly without changing tabs.

```
┌──────────────────────────────┬──────────────────────────────┐
│  Technical Instructions      │  Live API Terminal           │
│  1. Configure webhook target │  $ prisent init --token xyz  │
│  2. Define proactive triggers│  [OK] Agent stream deployed   │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 6. Communication Media & Compliance Foundations

### Social Media Grid Systems

- **Content Approach:** Focus social content on clear product updates, engineering milestones, and real-world code use cases.
- **Visual Structure:** Format text inside crisp wireframe boxes. Frame code clips using high-contrast dark backgrounds, keeping text brief and direct.

### Technical Presentation Architecture

- **Slide Layout:** Use clean, minimal layouts built on the 8px grid. Use structural dark backgrounds for technical presentations and light backgrounds for engineering documentation.
- **Data Layout:** Present statistics and architecture diagrams clearly on clean grid lines, ensuring the information remains easy to read from the back of a room.

### Accessibility Framework & Compliance

The interface is engineered to comply with WCAG 2.1 AA accessibility standards, ensuring high usability across all digital touchpoints.

- **Contrast Standards:** Maintain a minimum contrast ratio of 4.5:1 for standard body text and 3:1 for large display headers.
- **Keyboard Controls:** All interactive dashboard elements, menu items, and input nodes must support full keyboard navigation, featuring high-visibility focus borders (`#D97706`).
- **Screen Reader Optimization:** Every functional icon and system diagram must include explicit descriptive labels (`aria-label`), ensuring clear navigation for users with screen readers.

---

## 7. Global Design Tokens

These primary design tokens serve as the single source of truth for engineering and design teams, ensuring absolute consistency across all applications and platform codebases.

```json
{
  "color": {
    "brand": {
      "primary": { "value": "#09090B", "type": "color" },
      "surface": { "value": "#18181B", "type": "color" },
      "accent": { "value": "#D97706", "type": "color" }
    },
    "border": {
      "muted": { "value": "#27272A", "type": "color" },
      "light": { "value": "#E4E4E7", "type": "color" }
    }
  },
  "spacing": {
    "baseline": { "value": "8px", "type": "dimension" },
    "container": { "value": "16px", "type": "dimension" },
    "section": { "value": "24px", "type": "dimension" }
  },
  "radius": {
    "component": { "value": "4px", "type": "dimension" },
    "module": { "value": "6px", "type": "dimension" }
  },
  "motion": {
    "snappy": { "value": "150ms", "type": "duration" },
    "easing": { "value": "cubic-bezier(0.16, 1, 0.3, 1)", "type": "easing" }
  }
}
```
