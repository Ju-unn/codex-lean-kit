# Palette: Mono Ink (흑백 잉크)

A near-black and white palette for work tools: lists, forms, tables, and dashboards whose data must stand out more than the chrome around it. Structure comes from a ladder of light gray fills, not from shadows or extra hues. One blue is kept for the single thing on a page that asks for attention.

Offer it as a numbered choice in the Step 2 color question. When the user picks it, copy the table below into the docs/design.md Color Palette, replacing the generated rows, and add the usage rules under Color Notes.

## Colors

| Role | Hex | CSS Variable | Use |
|---|---|---|---|
| Primary | `#141414` | `--color-primary` | Primary buttons, headings, body text, the dark footer or header band |
| On Primary | `#FFFFFF` | `--color-on-primary` | Text and icons on Primary |
| Secondary | `#262626` | `--color-secondary` | Secondary dark text, such as labels beside a heading |
| On Secondary | `#FFFFFF` | `--color-on-secondary` | Text on Secondary |
| Accent | `#0066FF` | `--color-accent` | One attention point per screen: a "recommended" badge, a key number, the selected row marker |
| On Accent | `#FFFFFF` | `--color-on-accent` | Text on Accent |
| Background | `#FFFFFF` | `--color-background` | Page background |
| Foreground | `#141414` | `--color-foreground` | Default text |
| Card | `#FFFFFF` | `--color-card` | Resting cards, with a Border Soft outline |
| Card Foreground | `#141414` | `--color-card-foreground` | Text on cards |
| Muted | `#F3F3F3` | `--color-muted` | Raised surfaces: the nav bar, a featured card, table header, hovered row, toggle track |
| Muted Foreground | `#6B6B6B` | `--color-muted-foreground` | Secondary text: descriptions, captions, counts |
| Field | `#F0F0F0` | `--color-field` | Form input fill |
| Border Soft | `#F0F0F0` | `--color-border-soft` | 1px outline on white cards |
| Border | `#E0E0E0` | `--color-border` | Outlined buttons, dividers, table row lines |
| Border Strong | `#8A8A8A` | `--color-border-strong` | 1px input edge, so the field is visible (3:1) |
| Faint | `#ADADAD` | `--color-faint` | Text on Primary only, such as footer links; never on white |
| Destructive | `#D92D20` | `--color-destructive` | Errors and delete actions |
| On Destructive | `#FFFFFF` | `--color-on-destructive` | Text on Destructive |
| Success | `#067647` | `--color-success` | Success text and icons |
| Ring | `#141414` | `--color-ring` | 2px focus ring |

Contrast, checked: Primary on Background 18.4:1; Primary on Muted 16.6:1; Muted Foreground on Background 5.3:1, on Muted 4.8:1, on Field 4.7:1; On Accent on Accent 4.8:1; On Destructive on Destructive 4.8:1; Success on Background 5.7:1; Faint on Primary 8.2:1; Border Strong on Background 3.5:1.

## Usage rules
- Primary buttons are Primary fill with On Primary text. Accent is never a button color.
- At most two Accent elements on a screen. If everything is blue, nothing is.
- Depth by fill, not shadow: page Background → Muted for raised surfaces → Card with a Border Soft outline. No drop shadows on cards, buttons, or bars.
- Accent and Destructive as text only on Background or Card (4.8:1); on Muted they drop to 4.4:1, so use them there as fills with white text.
- Status colors (Destructive, Success) only for status, always with a text label or icon, never color alone.
- Charts: Primary for the main series, Accent for the one series or value to notice, Muted Foreground for the rest.
- Inputs: Field fill with a Border Strong edge; on focus, a 2px Ring.

Source: colors adapted from a public monochrome design-system write-up the user supplied (the Mobbin web UI). Muted Foreground changed from #707070, which fell below 4.5:1 on #F3F3F3; Border Strong, Destructive, and Success added for app states; Faint limited to dark backgrounds.
