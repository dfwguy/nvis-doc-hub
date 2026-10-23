# Unified document discovery independent code review

Reviewed 23 October 2026 on local `development`, before commit.

No unresolved material defects found after the phone action and card-width fixes.

## Scope

Read the discovery specification and plan; KUI browse, search, filter,
navigation, entity-card, carousel, ranked-list and empty-state guidance; the
Store/Hub and web changes; discovery/shared templates; discovery JavaScript and
CSS; new/changed Python tests; and browser regression script changes. KUI layout
and interaction guidance is adapted to the authorized existing Python frontend.
No React migration or package installation was performed by this review.

Checked unified discovery routing, empty-query document browsing versus ranked
section search, independent clear actions, URL/filter/pagination state, honest
metadata and popularity, data escaping, native links/forms and keyboard controls,
counter migration/persistence, current-publication joins, and retrieval
compatibility. The separate browser review owns broad interaction, responsive
layout and visual QA.

## Resolved findings

The existing phone CSS rule hiding the old catalog header action also hid the
new requested Browse documents action. The new discovery phone rule initially
changed spacing without restoring `display`. Reported the source defect; the
implementer reproduced hidden visibility before adding `display: inline-flex`
to `src/nvis_hub/static/hub.css:135`. The browser worker added phone visibility
and reachability assertions.

Independently checked the corrected action in Chromium at 1440, 768, 390 and
320 pixels: it is visible at every width.

The browser worker then reproduced phone shelf cards shrinking to 69.75 pixels
because `minmax(0, 88%)` allowed the auto-column tracks to collapse. The corrected
phone rule uses `grid-auto-columns: 88%` at `src/nvis_hub/static/hub.css:138`.
Re-read the change and independently measured the finished 390-pixel layout:
each card is 300.95 pixels wide in a 350-pixel rail, across all three shelves.
The portable browser suite now checks that phone cards occupy at least 80% of
their rail, along with touch scrolling and shelf controls. Its recorded final
run passes all 16 checks, including contrast and responsive containment.

## Final discovery delta

Re-read the bounded project fallback and conditional filter rendering. When
explicit how-to/reference metadata is absent, remaining home shelves use real
documents labelled From their project, up to three total shelves. Each View all
link filters the complete library by that actual project. The change adds no
source metadata, inferred document types or fabricated popularity.

Topic and Document type controls appear when those facets exist, or when the
URL has an active value that the user needs to inspect/remove. Unknown active
values remain selected and labelled unavailable, with removal chips. A focused
disposable fixture with three projects and unclassified documents confirmed the
three-shelf cap, real project links, hiding absent facets, preserving/removing
active unavailable filters, and no discovery-generated open counts. The full
suite was not rerun for this small review delta.

## Verification and reasoning

- `.venv/bin/python -m pytest -q tests/test_discovery.py tests/test_web.py`:
  27 passed. The existing Starlette TestClient deprecation warning remains.
- Disposable-fixture probes verified 35-document pagination with project,
  type and a topic containing ampersands, slashes and quotes; independent clear
  actions preserve the remaining query/scope. HTML-shaped project titles,
  queries and unavailable filter values remain escaped without injected tags.
- A deliberately failed template render records no open. HEAD requests,
  discovery pages, search and ordinary service retrieval do not record opens.
  Successful browser reader requests count after HTML template rendering.
- The additive `document_views` table stores only project/path/count, with no
  user identifier. Atomic insert/update increments avoid lost updates. Refresh
  replacement leaves counters intact; rankings join current documents, so
  removed paths do not appear. Tests cover restart, refresh, removal,
  concurrent increments, database upgrade and deterministic tie ordering.
- Browse and count queries share parameterized explicit metadata filters.
  Alphabetical browse and section-search ranking stay separate. Typed shelves
  use explicit metadata, unclassified documents retain an honest label, and
  empty history uses Explore documentation rather than fabricated popularity.
- Cards and results use authored document fields and native hosted links.
  Jinja escaping remains enabled. Shelf buttons are named and expose their
  target list; native scrolling/links work without JavaScript, and enhanced
  scrolling respects reduced motion. Filter state is visible and serialized
  into ordinary GET forms and links.

Only this review evidence file was written by the reviewer. Application code,
publication data, imported packages, the user's pending KUI/package files and
screenshots were not modified.
