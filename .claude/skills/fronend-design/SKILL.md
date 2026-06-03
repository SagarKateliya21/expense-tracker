---
name: spendly-ui-designer
description: >
  Generates modern, production-ready UI components and pages for Spendly
  (a personal expense tracker at https://github.com/SagarKateliya21/expense-tracker).
  The project is a Flask + Jinja2 app with HTML/CSS templates. Automatically trigger
  this skill whenever the user says things like "design the ___ page", "create UI for
  ___", "build component for ___", "redesign ___", "improve the look of ___", or anything
  related to Spendly's frontend, layouts, or visual improvements — even if they don't
  explicitly say "skill" or "UI". Also trigger when the user asks to make something
  "look better", "more modern", or "cleaner" in the context of this project.
disable-model-invocation: false
---

# Spendly UI Designer

Generates clean, modern, production-ready frontend code for the Spendly expense tracker.
The stack is **Flask + Jinja2**, so output is **HTML templates + CSS (and minimal vanilla JS
where necessary)**. No React, no build tools — pure HTML/CSS/JS that Flask can serve directly.

---

## 0. Before You Write a Single Line of Code

1. **Understand the request** — What page or component? What data does it display?
   If anything is unclear, ask one focused question before proceeding.

2. **Check for existing design context** — The user may paste existing CSS, screenshots,
   or code. Study it carefully. If none is provided, ask:
   > "Could you share a screenshot or the current CSS so I can match the existing style?"
   If they say it doesn't exist yet, proceed with the Spendly design system below.

3. **Read the frontend-design skill** — For anything non-trivial, mentally apply
   `/mnt/skills/public/frontend-design/SKILL.md` principles: commit to a bold aesthetic
   direction, avoid generic "AI slop", use distinctive typography choices.

---

## 1. Spendly Design System

When no existing design is provided, use this system as the baseline. It can be extended
but should never be abandoned mid-project (consistency rule).

### Color Palette
```css
:root {
  /* Backgrounds */
  --bg-base:       #F8F9FB;   /* page background */
  --bg-card:       #FFFFFF;   /* cards, panels */
  --bg-sidebar:    #1E2330;   /* dark sidebar */

  /* Brand */
  --brand-primary: #4F6EF7;   /* indigo-blue — buttons, active states */
  --brand-accent:  #2DD4BF;   /* teal — positive amounts, success */

  /* Semantic */
  --color-income:  #10B981;   /* green — income */
  --color-expense: #F43F5E;   /* rose — expenses */
  --color-warning: #F59E0B;   /* amber — budget alerts */

  /* Text */
  --text-primary:  #1A1D27;
  --text-secondary:#6B7280;
  --text-muted:    #9CA3AF;

  /* Border & Shadow */
  --border:        #E5E7EB;
  --shadow-sm:     0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md:     0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg:     0 10px 30px rgba(0,0,0,0.10);

  /* Spacing (8px grid) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* Typography */
  --font-display: 'DM Sans', sans-serif;   /* headings, nav labels */
  --font-body:    'Inter', sans-serif;     /* body text, inputs */
  --font-mono:    'JetBrains Mono', monospace; /* amounts, numbers */
}
```

### Typography
- Load via Google Fonts: `DM Sans` (400, 500, 600, 700) + `Inter` (400, 500) + `JetBrains Mono` (400, 500)
- Page titles: `DM Sans 600`, 24–28px
- Section headings: `DM Sans 600`, 16–18px
- Body / labels: `Inter 400/500`, 13–15px
- Amounts / numbers: `JetBrains Mono 500` — always use this for currency values

### Layout
- Sidebar navigation: fixed, 240px wide, `--bg-sidebar` background
- Main content: fluid, left margin 240px, padding `var(--space-8)`
- Cards: `background: var(--bg-card)`, `border-radius: var(--radius-lg)`, `box-shadow: var(--shadow-sm)`, `padding: var(--space-6)`
- Grid: 8px base unit — all spacing should be multiples of 8px

### Component Patterns

**Stat card (KPI tile)**
```html
<div class="stat-card">
  <div class="stat-card__icon">
    <!-- lucide SVG icon -->
  </div>
  <div class="stat-card__body">
    <p class="stat-card__label">Total Expenses</p>
    <p class="stat-card__value">₹12,450</p>
    <p class="stat-card__delta positive">↑ 12% this month</p>
  </div>
</div>
```

**Transaction row**
```html
<div class="txn-row">
  <div class="txn-row__icon-wrap txn-row__icon-wrap--food">
    <!-- category icon -->
  </div>
  <div class="txn-row__info">
    <span class="txn-row__title">Swiggy Order</span>
    <span class="txn-row__date">Jun 2, 2026</span>
  </div>
  <span class="txn-row__amount txn-row__amount--expense">−₹340</span>
</div>
```

**Button variants**
```css
.btn-primary  { background: var(--brand-primary); color: #fff; }
.btn-ghost    { background: transparent; border: 1px solid var(--border); }
.btn-danger   { background: var(--color-expense); color: #fff; }
/* Always: border-radius: var(--radius-full); padding: 8px 20px; font: Inter 500 14px */
```

---

## 2. Icons

Use **Lucide Icons** (SVG, inline). Load via CDN when not already present:
```html
<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>
```
Then use: `<i data-lucide="wallet"></i>`, `<i data-lucide="trending-up"></i>`, etc.

Common icon → category mapping:
| Category    | Icon name         |
|-------------|-------------------|
| Food        | `utensils`        |
| Transport   | `car`             |
| Shopping    | `shopping-bag`    |
| Health      | `heart-pulse`     |
| Income      | `arrow-down-left` |
| Expense     | `arrow-up-right`  |
| Budget      | `target`          |
| Analytics   | `bar-chart-2`     |
| Settings    | `settings`        |
| Add new     | `plus-circle`     |

---

## 3. Output Format

Every response should include these sections (in order):

### A. Layout & UX Summary (brief — 4–8 bullet points)
- List key sections / layout decisions
- Note any important UX choices (e.g. "amounts in JetBrains Mono for scannability")
- Mention any assumptions made

### B. HTML Template
- Full, self-contained Jinja2/HTML template
- Include `{% extends "base.html" %}` and `{% block content %}` if it's a page
- Load fonts + Lucide in `<head>` (or note "add to base.html once")
- Use semantic HTML: `<main>`, `<section>`, `<nav>`, `<header>`, `<aside>`

### C. CSS
- Scoped to the page/component (use a page-specific class on `<body>` or the root wrapper)
- Organized in this order: CSS variables override → layout → components → states/modifiers → responsive
- Mobile-first breakpoints: `768px` (tablet), `1024px` (desktop)
- Comment logical sections

### D. JavaScript (only if needed)
- Vanilla JS only
- Keep it minimal — prefer CSS for animations/toggles
- Clearly comment any dynamic behavior

---

## 4. Design Rules (Non-Negotiable)

1. **8px grid** — all spacing/sizing values must be multiples of 8px (4px for fine details)
2. **Rounded, soft UI** — `border-radius` at least `var(--radius-md)` on all cards/inputs/buttons
3. **Consistent shadows** — use only `--shadow-sm`, `--shadow-md`, `--shadow-lg`
4. **JetBrains Mono for all currency/number values** — non-negotiable
5. **Lucide icons** — no emoji as icons, no image-based icons
6. **Card-based layout** — never dump raw data into the page; wrap in cards
7. **Color discipline** — only use semantic colors for their meaning (e.g. never use `--color-expense` for decorative red)
8. **No clutter** — max 3–4 actions visible at once; use overflow menus / modals for the rest

---

## 5. Consistency Rule

If the user shares existing screenshots, CSS, or HTML:
- Extract the key variables (colors, fonts, border-radius, spacing) and **add them as overrides** in the `:root` block of your output
- Never contradict or ignore the existing style — extend it
- If there's a conflict between the existing style and these rules, follow the existing style and note the deviation

If the user doesn't share existing design:
> Ask: "Could you share a screenshot or your existing CSS? I'll match the design exactly."
> If they say no existing design, proceed with the system above and note that you're establishing a new design baseline.

---

## 6. Flask / Jinja2 Specifics

- Static files served via `url_for('static', filename='...')` — use this in templates
- Template inheritance: assume `base.html` exists with a `{% block content %}` slot
- Form actions: use `action="{{ url_for('route_name') }}"` patterns
- For chart data: pass as JSON in Jinja2 and read with `JSON.parse()`; use Chart.js or plain SVG (no heavy charting libs unless already in the project)
- Currency: default to ₹ (Indian Rupee) unless specified otherwise

---

## 7. What to Avoid

- Generic "bootstrap-looking" UIs
- Unstructured code dumps without explanation
- Using `color: red` / `color: green` directly (use CSS variables)
- Tables for layout (use CSS Grid / Flexbox)
- Overloading a page with features — stay focused on the request
- Placeholder lorem ipsum — use realistic expense tracker data in examples (food, transport, salary, etc.)