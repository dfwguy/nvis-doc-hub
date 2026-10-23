# Live search browser review

Reviewed against `docs/superpowers/specs/2026-10-23-live-search-design.md` and `DESIGN.md` on 2026-10-23. The versioned Playwright suite passed **28 checks, 0 failures**, using visible Chromium 151.0.7922.34 against the real local publication server at `http://127.0.0.1:8000`. No browser script errors occurred.

Run with Playwright available on `NODE_PATH`:

```sh
NODE_PATH=/path/to/playwright/node_modules node scripts/live_search_verify.cjs
```

`NVIS_HUB_URL` or `TARGET_URL` can select a different running hub. The browser is visible by default; `PW_HEADLESS=true` supports environments without a display. Structured results, layout measurements and the initial red test are in `evidence/live-search-browser-review.json`.

The initial test typed `slur` in the catalog search before implementation and failed because no visible suggestion option appeared. That failure is preserved in the JSON and `.impeccable/review/live-search-initial-red.png`. The same real prefix query now returns five native links whose URLs match the live suggestions endpoint and open existing document section anchors.

Behavior checks covered pointer and phone touch activation; Arrow Up/Down selection with input focus retained; selected Enter and ordinary unselected Enter; Escape, Tab, clearing, outside click and focus dismissal; the two-character minimum and 180 ms debounce; project scope and filter changes; full-search links; loading, no-match, transport failure and recovery; IME composition; and late responses. Loading and race tests changed only transport/timing while retaining server-generated payloads. The race check deliberately ignored request abort and delayed the older response, confirming that the newer query remained visible. Full form submission and project filtering also passed with JavaScript disabled.

Visual inspection covered catalog, search and project pages at 1440 × 1000, 768 × 1024 and 390 × 844, plus 1440 × 500 and 390 × 420 viewport constraints. The popup aligned with the search field at every size, stayed within the viewport, flipped above the field when space required it, and scrolled to both the last result and full-search footer. No horizontal page overflow occurred. All measured result targets were at least 111 px high, with 12 px link padding inside the list's additional inset. Text stayed readable, long source excerpts remained contained, and charcoal surfaces, IBM Plex Sans, NVIDIA Green titles and neutral keyboard selection matched the existing design. Feedback states retained readable text and the full-search action. No unresolved visual findings remain.

The screenshot helper waits two animation frames for final paints. A targeted no-match check also verified the completed message and captured `live-search-no-match-complete.png`; this replaced the earlier transitional loading capture. Final captures are under `.impeccable/review/live-search-*.png`; obsolete test-failure captures were removed.

Accessibility checks verified the labelled combobox, controlled `Matching documentation` listbox, native result links with option identities, expanded state, active-descendant and selected states, keyboard help, polite result announcements, keyboard selection colors and touch target sizes. Phone touch and keyboard-sized viewport behavior were emulated in Chromium; an actual operating-system keyboard and screen reader were not exercised. The real publications currently have no nonempty Topic or Document type facets, so browser checks exercise active project scope; combinations involving topic/type depend on the backend fixture tests.
