# Unified discovery browser verification

Verified on 23 October 2026 in visible Chromium 151.0.7922.34 against
`http://127.0.0.1:8001`. This server uses a separate SQLite backup of the published
catalog. Browser-generated opens affect that isolated database, not the user's
local usage counters. The popularity values in the screenshots are test opens.
The QA server remains running for final review.

Final results:

- `scripts/discovery_verify.cjs`: 16 passed, 0 failed; widths 1440, 768, 390, and 320.
- `scripts/browser_verify.cjs`: 35 passed; catalog/search/reader regressions at three widths.
- `scripts/live_search_verify.cjs`: 28 passed; real section suggestions and asynchronous edge cases.
- `scripts/navigation_verify.cjs`: 34 passed; all 92 published pages and native categories.

The discovery script preserves the five initial failing feature checks and the
first empty-history verification in
[discovery-browser-review.json](discovery-browser-review.json). The original UI
had separate navigation, no unified filter form or document shelves, and no
query-free filtered library. An empty counter history rendered Explore
documentation. Successful reader opens from two separate browser contexts then
produced the expected shared count increase and popularity order. Discovery,
search API, missing-document, and HEAD requests did not increase that count.

The complete alphabetical library exposes all 92 unique documents over four
pages (30, 30, 30, 2). Query-free project filtering browses actual documents;
query submission and automatic filter changes retain the selected scope. Clear
search preserves filters; Clear filters preserves the query. Removal links keep
the other active constraints and work by keyboard. Both published snapshots lack
topic/type metadata, so the real-content UI exposes Project and honest project
shelves rather than inventing classifications. Explicit unavailable topic/type
URL values remain visible and removable; typed shelves are checked against
`data-kind` whenever authored metadata supports them.

Three visual regressions were caught and corrected during QA: an old phone rule
hid Browse documents; `minmax(0,88%)` shrank four phone cards to roughly 70px and
prevented shelf scrolling; and unmatched scroll-snap padding started a shelf at
4px with Previous enabled. The final checks verify the header action at every
width, phone card widths of at least 80% of the rail, actual scrolling through
controls and touch, an initial scroll position of zero, and disabled Previous
controls at the start.

Keyboard focus is visible at 2px. Reduced motion uses instant shelf scrolling.
Measured card title/project/path/open-count contrast ratios range from 6.11:1 to
17.40:1. Native touch swiping moves the shelf and tapping a card opens its hosted
document. JavaScript-free query and filter forms remain functional. The final
runs reported no browser JavaScript errors or page-wide horizontal overflow.
Existing contained scrolling for authored code, tables, and document shelves is
preserved.

Fresh homepage captures load the page after an intervening blank document,
wait for fonts, and confirm that every shelf starts at its first document.
Keyboard/focus captures remain separate:

- [Desktop home](../.impeccable/review/discovery-desktop-home.png)
- [Tablet home](../.impeccable/review/discovery-tablet-home.png)
- [390px phone home](../.impeccable/review/discovery-phone-home.png)
- [320px phone home](../.impeccable/review/discovery-narrow-phone-home.png)
- [Keyboard focus with reduced motion](../.impeccable/review/discovery-phone-shelf-keyboard-reduced-motion.png)
- [Search with a project filter](../.impeccable/review/discovery-query-and-filter-results.png)
- [Project-only browsing](../.impeccable/review/discovery-project-filtered-library.png)
- [Phone card shrinkage before correction](../.impeccable/review/discovery-focused-shelf.png)

Visual inspection of the final desktop and phone captures found readable,
contained titles and paths, reachable controls, and no remaining material issue.
The existing browser scripts changed only assertions superseded by the unified
UI; section anchors, reader links, native categories, clipboard behavior, live
search races/errors, and no-JavaScript coverage remain in place. Live suggestion
assertions now scope options to the Matching documentation listbox so visible
native project options do not contaminate them.

Run each portable script with Playwright available in `NODE_PATH` and
`NVIS_HUB_URL=http://127.0.0.1:8001`; set `PW_HEADLESS=true` when no display is
available. Use an isolated database because successful reader GETs deliberately
record aggregate opens.
