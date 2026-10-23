# Single popular carousel, focused navigation, and themes

The corrected implementation was verified on 23 October 2026 in visible Chromium
151.0.7922.34 against isolated `http://127.0.0.1:8001`. This server uses a separate
SQLite backup. Browser traffic and popularity values in these captures belong to
that backup; this QA did not change the user's local usage counters.

All 120 current browser checks pass:

- Focused carousel/navigation/title/theme verification: 23 passed, 0 failed.
- Existing catalog/search/reader regression: 35 passed.
- Existing live-search regression: 28 passed.
- Existing native category/navigation regression: 34 passed, covering all 92 published pages.

The results and measurements are in
[discovery-simplification-browser.json](discovery-simplification-browser.json).
The earlier grid revision is explicitly retained under
`preCorrectionVerification` as history, not as the final implementation. Three
correction-specific red checks then demonstrated the remaining global project
links, missing carousel controls, and project navigation listing another project.
The corrected behavior passes those checks.

The default page has exactly one Explore popular documentation carousel. It
contains at most six genuinely opened documents, keeps native links and 44px
Previous/Next controls, and has no extra project slider rows. Horizontal scrolling
is contained within that one region; the page does not overflow. Controls have
accessible names and point to the correct region through `aria-controls`. The
carousel starts at scroll position zero with Previous disabled; pointer,
keyboard, reduced-motion instant scrolling, native touch swiping, and card
activation all pass at 1440, 1280, 768, 390, and 320px.

Home and search navigation contain no global project-name list or Projects
heading. Project/reader navigation contains only the active document categories,
labelled Document sections, with no project-name links. The current reader's
category remains open and its current link visible. Project identity remains in
the breadcrumb. Selecting Project in discovery opens a vertical paginated
library. All 92 unique pages, query/filter URLs, independent clear actions,
removable unavailable filter values, live section links, and JavaScript-free
forms retain their behavior.

The copied database genuinely contained zero `document_views` rows before any
QA reader opens. An earlier integrated run captured “No popular documentation
yet” with zero cards; its original timestamp and observation remain as historical
empty-state evidence. Counters were never cleared or edited to force that state.
The final corrected run used real successful reader GETs from separate browser
contexts to verify shared increments and ordering. Eight distinct published
documents exercised the six-card limit. Search, discovery, missing-document, and
HEAD requests did not increment the usage probe.

Sentence-style navigation examples retain command and acronym spelling,
including “Launch Codex for an existing group repository” and “Connect cmsh from
a non-BCM host”. Source paths and authored content remain the authority; existing
section-anchor and reader tests are green.

Dark and light themes were each checked on discovery, full search, and a reader
at five widths: 15 route/viewport states per theme. The native Dark mode switch
has an accessible label and checked state, works with Enter and Space, and
persists both selections across reloads and route changes. A fresh browser
context defaults to dark even with a light system preference. When storage
throws, the current page can still toggle and a reload safely falls back to dark
without script errors. JavaScript-free pages retain the dark fallback.

Sampled title, metadata, search-link, reader prose/link/code, and switch-label
text contrast is at least 6.11:1 dark and 6.42:1 light. Header focus rings are at
least 2px wide, with minimum contrast 8.71:1 dark / 10.65:1 light. Header controls
and open menus fit in both themes on all applicable routes, including the moon
icon at narrow widths. At 320px the menu spans x=16–289 with equal horizontal
scroll/client widths. There were no browser JavaScript errors or page-wide
horizontal overflow; authored code/table scrolling remains intentional.

Representative current captures:

- [Dark desktop carousel](../.impeccable/review/simplification-dark-home-1440.png)
- [Light desktop carousel](../.impeccable/review/simplification-light-home-1440.png)
- [Dark phone carousel](../.impeccable/review/simplification-dark-home-390.png)
- [Light phone carousel](../.impeccable/review/simplification-light-home-390.png)
- [Light 320px search](../.impeccable/review/simplification-light-search-320.png)
- [Dark 320px reader](../.impeccable/review/simplification-dark-reader-320.png)
- [Light 320px reader](../.impeccable/review/simplification-light-reader-320.png)
- [Carousel/card keyboard focus with reduced motion](../.impeccable/review/simplification-phone-carousel-keyboard-reduced-motion.png)

The [original empty-history capture](../.impeccable/review/simplification-empty-history.png)
predates the navigation correction and is retained only as historical evidence of
the genuine zero-open state. Final desktop/phone captures were visually reviewed;
no material issue remains. Existing search races/errors, reader links, clipboard,
source links, no-JavaScript behavior, and category coverage were preserved.

Run `scripts/discovery_verify.cjs` with Playwright in `NODE_PATH` and
`NVIS_HUB_URL` pointing to an isolated server; use `PW_HEADLESS=true` without a
display. Successful reader GETs deliberately record aggregate opens, so browser
QA should continue to use a separate database.
