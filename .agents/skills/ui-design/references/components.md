# Components, spacing, and interaction (web work tools)

Read this in Step 3 to write the "Components and interaction" section of docs/design.md, and again before building each screen. The numbers are defaults; docs/design.md overrides them once written.

## 1. Shape and spacing tokens
Add these to `:root` next to the colors, and use only these values.

| Token | Value | Use |
|---|---|---|
| `--radius-sm` | 6px | Inputs, small buttons, tags, table cells with a fill |
| `--radius-md` | 10px | Buttons, menus, toasts |
| `--radius-lg` | 16px | Cards, panels, dialogs |
| `--radius-full` | 9999px | Badges, toggles, segmented controls, avatars |
| `--space-1` … `--space-8` | 4, 8, 12, 16, 24, 32, 48, 64px | All padding, margin, and gap |
| `--control-h` | 40px (44px when the README or users point to touch screens) | Buttons, inputs, selects, tabs |

- One radius per level: every button the same, every card the same. A pill-shaped style (`--radius-full` on buttons) is fine if docs/design.md chose it, then for all buttons.
- Nested corners: the inner radius is the outer radius minus the padding between them, never larger.
- Spacing by relationship, the closer the meaning, the smaller the gap:
  - inside a control: 8-12px vertical, 16px horizontal
  - label to its field, icon to its text: 4-8px
  - items in one group (fields of a form, buttons in a row): 8-12px
  - between groups inside a card: 16-24px
  - card padding: 16-24px; between cards: 16-24px
  - between page sections: 32-48px
- Same level, same gap. No values off the scale (no 13px, no 22px).
- Content width: forms at most 640px; text at most about 70 characters per line; tables may use the full width.

## 2. Pick the component by the situation

| Situation | Use | Not |
|---|---|---|
| 2-5 views of the same thing (by store, by status) | Tabs, with the count in each label ("품절 12") | Separate pages, or a select for 3 options |
| 2-3 display modes of one view (day/week, list/chart) | Segmented control | Tabs, which suggest different content |
| On/off setting that applies at once | Toggle switch, label on the left | A toggle inside a form that has a save button: use a checkbox there |
| Pick one of 2-5 visible options | Radio buttons or segmented control | A select that hides 3 options |
| Pick one of 6 or more | Select, or a search box when over about 15 | A long radio list |
| Wait under 1 second | Nothing, or the pressed button's own spinner | A full-page spinner |
| Wait 1-10 seconds, layout known | Skeleton rows or cards in the final layout | A spinner over an empty page |
| Wait over 10 seconds or a known number of steps | Progress bar with a count ("120/338") | An endless spinner |
| Short task that keeps context (edit one row) | Side panel (drawer) or inline edit | A new page |
| Must answer before going on (confirm delete) | Dialog with two buttons; the safe one first | A dialog for information only |
| Done or failed after an action | Toast for success (4 seconds); inline message next to the cause for errors | An alert() box |
| Problem affecting the whole page (data stale, offline) | Banner at the top of the content | A toast that disappears |

## 3. Long lists and data
Decide from the row count the screen will really hold (docs/requirements.md data contract, or the load answer), not from the sample.

| Rows | Pattern |
|---|---|
| Up to 20 | Show all |
| 20-1,000 | Pages of 20 (or 50 for dense tables) with page numbers, previous and next, and "총 338건 중 1–20" |
| Over 1,000, or the data comes from an API | The same pages, fetched with limit and offset from the server, never all rows at once |
| A feed read top to bottom, never compared | "더 보기" button; no infinite scroll in work tools, because people lose their place and the footer |

Every list over 20 rows also gets:
- Search and filters above the list, the most used filter as tabs or chips. Show the active filters and one "초기화".
- Sort on the columns people compare by; the sorted column shows its direction.
- A sticky table header; numbers right-aligned with tabular figures.
- The page, filters, and sort kept in the URL query, so refresh and back keep the place.
- Summary first: 2-4 key numbers above the list ("품절 12건", "발주 필요 5개 품목"), each one a link that filters the list.
- Its own empty states: "데이터 없음" differs from "조건에 맞는 결과 없음" (with a reset button).
- Rows: about 40px for scanning tables, 56-72px for cards with two lines. A whole row may be clickable, with a hover fill.

## 4. Interaction states
Every control has default, hover, focus-visible (2px ring), active, disabled, and loading where it fires a request.

- Buttons: one primary per screen area. On click: disable it, show a spinner inside it, keep its width, and block a second submit until the response.
- Feedback timing: visible response under 100ms; show a spinner only after 300ms, so fast responses do not flash; skeleton for over 1 second.
- Forms: validate a field when it loses focus, show the error under the field in words that say how to fix it, keep what the user typed, move focus to the first error on submit.
- Destructive actions: a dialog naming the item ("발주 O049를 삭제할까요?"), or an undo toast for 5 seconds. Never delete on one click.
- After a change, update the list in place and keep the scroll position and the current page.
- Motion: 150-250ms ease-out for hover, open, and close; nothing animates its layout size; honor `prefers-reduced-motion`.
- Keyboard: Tab order follows the screen, Enter submits a form, Esc closes a dialog or panel and returns focus to what opened it.
- Status changes (saved, failed, loading done) are announced with `aria-live="polite"`.

## 5. What goes into docs/design.md
A section "Components and interaction", one block per screen:
- the row count it expects, the list pattern from §3, page size, filters and sort
- the controls chosen from §2 and why, in one line each
- the radius and spacing tokens, if they differ from §1
- the loading, empty, and error states, with their Korean text

Sources: written for this kit. Thresholds follow the upstream quick-reference rules (loading-buttons, progressive-loading, virtualize-lists, inline-validation, focus-management), Nielsen Norman Group guidance on response-time limits and pagination over infinite scroll in task-based interfaces, and the Material and Apple guidance on toggles versus checkboxes.
