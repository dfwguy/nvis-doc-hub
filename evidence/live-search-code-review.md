# Live search independent code review

Reviewed 2026-10-23 on local `development` before commit.

No material defects found in the reviewed changes.

## Scope and reasoning

- Read the live-search design and implementation plan, the backend diff in
  `service.py`, `store.py`, and `web.py`, the new publication/web tests, the
  complete previously untracked `static/live-search.js`, shared CSS additions,
  and the deferred script inclusion in `templates/base.html`.
- The backend retains exact-term matching by default. Only suggestions request
  the final literal token as an FTS prefix. Project/topic/type filters, ranking,
  plain excerpts, and hosted section URL construction reuse existing retrieval.
  The API checks raw query length before trimming, and the service limits the
  response to five results and the six specified fields.
- Each input/filter update clears old options, aborts transport, and changes a
  generation counter. Success checks generation, current parameters, and input
  focus before rendering. Dismissal changes the same counter, preventing late
  responses from reopening a dismissed popup. Composition input is deferred
  until committed.
- Keyboard selection keeps input focus, provides a valid active descendant,
  and only intercepts Enter when a displayed option is selected. Unselected
  Enter and form submission retain ordinary full search. Native result anchors
  preserve pointer navigation. Escape, Tab, external pointer/focus changes, and
  stale query/filter changes remove the active descendant.
- Result fields use `textContent`, and result destinations must resolve to the
  current origin under `/projects/`. Full search uses encoded parameters and
  keeps the available filters. Prefix suggestions and ordinary full search
  intentionally retain their documented matching semantics.
- The popup has constrained scrolling, visible-viewport resize/scroll handling,
  above-field positioning when space below is limited, and existing dark-theme
  colors. Forms and filters remain native HTML when JavaScript is absent.

## Focused browser verification

Ran an independent Playwright check against the running local application in
Chromium 151.0.7922.34, without modifying application code or publication data.
Intercepted only the suggestions response to verify:

- External, scheme-relative, `javascript:`, and non-project destinations are
  rejected while a valid same-origin project destination remains selectable.
- HTML-shaped heading, context, title, and excerpt values render as literal text
  without creating image/script/SVG/formatting elements.
- Escape clears keyboard selection, and Arrow Up reopens cached results with a
  valid active descendant.
- These interactions produce no browser script errors.

The independent full-flow browser review supplies the broader interaction,
race, filter, responsive-layout, failure-recovery, touch, and no-JavaScript
checks. This code review did not repeat that suite or claim a manual assistive
technology audit.
