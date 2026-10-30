---
name: ui-design
description: Use when building, restyling, or reviewing anything the user will see in the browser, such as pages, screens, forms, tables, dashboards, charts, navigation, color, typography, spacing, responsive layout, or accessibility. For the main agent and for workers.
---

# UI design

Searchable local design data: styles, product palettes with reasoning rules, font pairings, UX guidelines, icons, chart types, and stack-specific guidance.

The user decides the look: style, colors, and fonts. The tool supplies options, component rules, and checks.

Use it when the task changes how something looks, feels, moves, or is interacted with. Skip it for backend logic, API or database design, and scripts with no visible output.

## Rule categories by priority
Work from priority 1 down. The full rules for every category live in references/quick-reference.md; read it on demand, not every time.

| Priority | Category | Impact | Domain | Key checks (must have) | Anti-patterns (avoid) |
|---|---|---|---|---|---|
| 1 | Accessibility | CRITICAL | `ux` | Contrast 4.5:1, alt text, keyboard nav, aria-labels | Removing focus rings, icon-only buttons without labels |
| 2 | Touch & Interaction | CRITICAL | `ux` | Min size 44×44px, 8px+ spacing, loading feedback | Reliance on hover only, instant state changes (0ms) |
| 3 | Performance | HIGH | `ux` | WebP/AVIF, lazy loading, reserve space (CLS < 0.1) | Layout thrashing, cumulative layout shift |
| 4 | Style Selection | HIGH | `style`, `product` | Match product type, consistency, SVG icons (no emoji) | Mixing flat and skeuomorphic randomly, emoji as icons |
| 5 | Layout & Responsive | HIGH | `ux` | Mobile-first breakpoints, viewport meta, no horizontal scroll | Horizontal scroll, fixed px container widths, disabled zoom |
| 6 | Typography & Color | MEDIUM | `typography`, `color` | Base 16px, line-height 1.5, semantic color tokens | Body text < 12px, gray-on-gray, raw hex in components |
| 7 | Animation | MEDIUM | `ux` | Context-aware timing, motion conveys meaning | One duration for every transition, animating width/height, no reduced-motion |
| 8 | Forms & Feedback | MEDIUM | `ux` | Visible labels, error near field, helper text | Placeholder-only label, errors only at top, everything upfront |
| 9 | Navigation Patterns | HIGH | `ux` | Predictable back, deep linking | Overloaded nav, broken back behavior |
| 10 | Charts & Data | LOW | `chart` | Legends, tooltips, accessible colors | Relying on color alone to convey meaning |

For app-specific polish rules (icons, touch feedback, dark mode contrast) and the canonical pre-delivery checklist, read references/pro-rules.md.

## Running the search tool
Run it from the workspace root, where the kit installs this skill:
```sh
python3 -X utf8 -B .agents/skills/ui-design/scripts/search.py "<query>" --domain <domain>
```
- If `python3` is not found, use `python`. `-X utf8` keeps consoles from failing on symbols in the output; `-B` keeps `__pycache__` out of the workspace.
- No dependencies and no network. If Python is missing, use the priority table and the references, and say that the tool did not run.

## Query contract
Choose the smallest search mode that fits:
1. New UI or a product-wide visual direction: `--design-system`.
2. A targeted concern or a component bug: one explicit `--domain`.
3. A known implementation stack: `--stack`; add a separate domain search only for a distinct design concern.

Build each query around one dominant intent, with 2-5 meaningful terms and one useful constraint such as product, platform, or interaction.
- Verify the returned domain, the top result, and its fit for this product before applying it.
- Retry once with a narrower rewrite or an explicit domain or stack when the output is empty or off-topic.
- If that retry fails, say that no verified match was found, and label any general guidance as a fallback.
- Results are recommendations. They never override the user, the task README, or the plan.

For accessibility, search one observable outcome at a time, the semantic outcome first (`"error summary validation" --domain ux`), then a component domain (`"icon button accessible label" --domain icons`), then the stack.

## Start here
Check for a master: `ls docs/design-system/*/MASTER.md`.
- None: do steps 1 to 3 before any screen code.
- One: read it, and go to step 4.

No screen code, stylesheet, or master before the user has answered the step 2 questions or said "추천대로". This holds even when the request says to build the screen now. If another design skill is listed (for example ui-ux-pro-max), follow this one; it is the kit's.

## Step 1: Read the requirements
From docs/requirements.md and docs/plan.md:
- Product type: dashboard, form-heavy tool, admin panel, list and detail, portal, or a hybrid.
- Users and context: who uses it, where, how often, on what device.
- Style words from the stakeholder or the user, if any.
- Stack: the one in docs/plan.md.

## Step 2: Ask the user (style, colors, fonts)
1. Preview two contrasting directions, for example `--variance 3` and `--variance 7`, or two sets of style words:
   ```sh
   python3 -X utf8 -B .agents/skills/ui-design/scripts/search.py "<product type> <style words>" --design-system -f markdown -p "<Project>"
   ```
   - `--density 1-10` sets spacious to dense. Leave `--motion` unset: it attaches GSAP code, a dependency the plan does not have.
2. Ask three [결정] questions, one block each, a blank line between blocks:
   ```
   Q12 [결정] 화면 스타일
   어떤 스타일로 할까요? 1) 밝고 간결한 목록형 2) 어두운 대시보드형 3) 직접 지정
   · 이유: 배치, 여백, 배경이 이 선택으로 정해집니다.
   · 권장: 1) (미리보기 스타일 이름)
   ```
   - Style: the previewed directions as numbered choices, plus "직접 지정".
   - Colors: primary and accent, as hex or color names. Recommend the preview's.
   - Fonts: the preview's pair, or system fonts only.
3. Wait for the answers. During $lean-plan these questions go in the plan gate, and the answers go under Decisions.

## Step 3: Save the master
1. Run the chosen direction again with `--persist --output-dir docs`. Never pass `--force` without the user's go.
2. Set the Color Palette and Typography in docs/design-system/<slug>/MASTER.md to the user's answers.
3. Check text contrast for every color and its on-color pair. Below 4.5:1, tell the user and propose the nearest shade that passes.
4. Done when MASTER.md exists and matches the answers.

## Step 4: Build pages from the master
1. If docs/design-system/<slug>/pages/<page>.md exists, its rules override the master.
2. The stylesheet starts with one `:root` block built from the master:
   - every Color Palette row as its CSS variable, for example `--color-primary: #0891B2;`
   - the Spacing Variables and Shadow Depths tokens as written
   - `--font-heading` and `--font-body` from Typography, each ending in a system fallback, for example `'Fira Sans', system-ui, sans-serif`
3. Components use only these variables. Raw hex values appear only inside `:root`.
4. Follow the master's Component Specs and avoid its Anti-Patterns.
5. Search details as needed:

| Need | Domain | Example |
|---|---|---|
| Product type patterns | `product` | `"admin dashboard" --domain product` |
| More style options | `style` | `"minimal dark" --domain style` |
| Color palettes | `color` | `"calm professional" --domain color` |
| Font pairings | `typography` | `"modern readable" --domain typography` |
| Individual Google Fonts | `google-fonts` | `"sans serif popular variable" --domain google-fonts` |
| Chart recommendations | `chart` | `"real-time dashboard" --domain chart` |
| UX best practices | `ux` | `"error summary validation" --domain ux` |
| Landing page structure | `landing` | `"hero social-proof" --domain landing` |
| Icon recommendations | `icons` | `"decorative icon aria hidden" --domain icons` |
| React performance | `react` | `"rerender memo list" --domain react` |

Domain is auto-detected when `--domain` is omitted, but overlapping terms can misroute it. If results look off-topic, pass `--domain`.

Stack guidance: `--stack <stack>` when the plan's stack is one of `react`, `nextjs`, `vue`, `svelte`, `astro`, `nuxtjs`, `nuxt-ui`, `angular`, `laravel`, `html-tailwind`, `shadcn`, `threejs`, and the native stacks in data/stacks/. For plain HTML and CSS, skip the stack search.

## Kit constraints
- No new UI dependency (CSS framework, animation, icon, or component library) unless docs/plan.md lists it. Use the master's CSS variables, plain CSS, and inline SVG icons.
- Fonts: keep a system fallback in every font-family, so the page still reads well if the font CDN is unreachable.
- Every screen shows empty, loading, and error states, labels things in the user's language, and makes one primary action obvious.
- The user checks visuals in the browser preview. Never use browser automation.

## If a search returns 0 results
Do not fabricate output.
1. Retry once with a narrower query or an explicit domain or stack.
2. If it is still empty, fall back to the priority table, and tell the user the recommendation came from the built-in defaults, not a match.
3. Never present a 0-result search as if it returned data.

## Tips
| Problem | What to do |
|---|---|
| Can't decide on style or color | Re-run `--design-system` with different keywords |
| Dark mode contrast issues | references/quick-reference.md §6: `color-dark-mode` + `color-accessible-pairs` |
| Animations feel unnatural | references/quick-reference.md §7: `easing` + `exit-faster-than-enter` |
| Form UX is poor | references/quick-reference.md §8: `inline-validation` + `error-clarity` + `focus-management` |
| Navigation feels confusing | references/quick-reference.md §9: `nav-hierarchy` + `back-behavior` |
| Layout breaks on small screens | references/quick-reference.md §5: `mobile-first` + `breakpoint-consistency` |
| Performance or jank | references/quick-reference.md §3: `virtualize-lists` + `debounce-throttle` |

## Before reporting a UI task
- Run the Pre-Delivery Checklist from MASTER.md. For mobile or native targets, also the one in references/pro-rules.md.
- Report each item as done or not done, with the file it concerns.

Sources: nextlevelbuilder/ui-ux-pro-max-skill (MIT): priority table, query contract, design-system workflow, master and page overrides, domains, 0-results rule, tips, checklists. The scripts, data, and references are copied unchanged, without the upstream's dev-only tests and three data files the search does not read. Changed: the user picks style, colors, and fonts.
