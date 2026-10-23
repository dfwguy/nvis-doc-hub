# Unified documentation discovery verification

Implemented on development, 23 October 2026, following the user's navigation and
homepage feedback and their explicit choice to rank by shared document opens.

## Result

- One **Browse documentation** destination replaces All documentation and Global
  search. `/` and existing `/search` links render the same discovery page.
- One search form combines live section suggestions, full section search, and
  available metadata filters. An empty query can browse documents directly.
  Clear search and Clear filters preserve each other's state; filter removal,
  query state, and pagination remain in shareable URLs.
- **Browse documents** opens the complete alphabetical library, paginated at
  30 documents. All 92 current documents are reachable without duplicates.
- Homepage shelves link to documents. Popular documents ranks real aggregate
  all-time opens, including repeat opens. Before usage, Explore documentation
  provides an honest starting selection. Up to three shelves use explicit types
  when present and real project-document rows otherwise. Current publications
  have no type/topic metadata; empty filter dimensions are omitted unless an
  active URL filter must remain visible and removable. No classification or
  popularity is invented.
- Successful browser reader responses increment atomic SQLite counters keyed by
  project/path. No identity, cookie, profile, or session is stored. Counts survive
  refresh/restart; removed documents cannot rank. Shared retrieval and existing
  CLI/MCP/search contracts remain unchanged and side-effect-free.
- Native whole-card links, labeled shelf buttons, keyboard/touch scrolling,
  visible focus, no autoplay, reduced motion, and no-JavaScript forms work.

## KUI adaptation

Read the supplied Kaizen UI skill and relevant layout, pattern, component, and
token references. The Python/Jinja frontend uses those conventions and documented
semantic CSS variables with settled-theme fallbacks. These native controls are
not represented as actual KUI React components. No React migration or dependency
installation was performed. The user-supplied skill and pending npm configuration
are preserved. Exact references and limitations are in
[discovery-kui-guidance.md](discovery-kui-guidance.md).

## Evidence

- **94 Python tests pass**, including eight new backend discovery tests and
  three new web behavior tests. Red-to-green checks cover missing discovery UI,
  filtered empty-query browsing, aggregate counting, persistence, refresh,
  removal, concurrency, and existing response compatibility.
- Ruff lint and formatting pass (17 Python files); mypy finds no issues in
  10 source modules. Application diff whitespace checks pass. Staging the supplied
  KUI package exposes three existing whitespace warnings in its generated
  references; those imported bytes are preserved. The existing upstream
  Starlette/httpx deprecation warning remains.
- **113 browser checks pass**: discovery 16, catalog/search/reader 35, live
  search 28, and collapsible navigation 34. Discovery checks run at 1440, 768,
  390, and 320px. See [browser report](discovery-browser-review.md) and
  [machine-readable results](discovery-browser-review.json).
- Browser QA uses a separate SQLite backup and server on port 8001. Only real
  reader requests create test popularity. The local port-8000 hub remains at
  92 documents with zero popularity rows and an honest Explore shelf.
- Review fixed the hidden phone Browse documents action, narrow phone shelf
  tracks, and initial Previous-button state. Regression checks cover each fix.
  See [independent review](discovery-code-review.md).
- All 101 original imported skill files and 96 source snapshot files retain their
  recorded SHA-256 hashes. The 121 supplied KUI skill files were preserved.

The [Tasteskill browser inspection](taste-discovery.json) reports no errors and
one tiny-text advisory: document paths, project labels, and supporting metadata
use the documented 12px step; primary titles and controls remain larger. The
single [Impeccable scan](discovery-impeccable-detect.json) contains 24 advisory
type/palette metadata findings and the known static hover-contrast false positive.
Added type steps reuse the established system and are recorded in DESIGN.md.
Actual card contrast and focus checks pass in the discovery browser results;
unchanged primary-action hover colors were measured in
[runtime contrast evidence](categories-runtime-contrast.json). No theme or package
was changed to silence metadata warnings.

The dark NVIDIA palette, NVIS - OVA identity, sidebar-bottom Documentation label,
source documents, and reader category behavior remain intact. Access control,
the publishing skill, automatic source updates, deployment, and remote HTTP MCP
remain deferred. Main retains the application baseline.
