# Collapsible documentation categories

Implemented on `development` on 23 October 2026, following the authored category
structure in the supplied [rack-status TOC](https://gitlab-master.nvidia.com/nvis/nvis-rack-status/-/blob/feature/auto-run-mode/docs/_toc.yml).
The exact remote branch was inspected at commit
`7e909322e467b2dd7b31e05fd6c82cdb9d70a610`; the source and relevant neighboring
documentation are recorded in [toc-template-reference.md](toc-template-reference.md).
No rack-status project or additional content was imported.

## Result

Project indexes, desktop navigation, and mobile navigation share native
collapsible Tutorials, How-to guides, Reference, and Explanation sections.
Each section shows its page count; index sections start collapsed, and readers
open the section containing the current page. Empty sections are omitted.
Unclassified pages remain reachable under Other documentation. Authored labels,
source-topic context, order within each category, nested indentation, and custom
TOC captions remain visible. The presentation grouping does not change source
documents, the flat navigation API/MCP response, or reader previous/next order.

Registered YAML `_toc.yml` navigation now supports root, captioned subtrees,
explicit titles, extensionless relative file targets, and recursive entries.
Explicit `diataxis` frontmatter is supported after the existing registration,
`type`, and `kind` precedence. Generated navigation does not guess categories from
paths or prose. YAML parsing is bounded; unsupported/malformed data and aliases
produce notices and fallback navigation. Existing RST support is retained.

Cluster Bringup contains 6 Tutorials, 36 How-to guides, 9 Reference,
21 Explanation, and 13 Other documentation pages. Documentation Pipeline's
7 pages have no explicit classification and remain under Other documentation.

## Verification

- Python: **83 passed**, including real FastAPI rendering, source parsing,
  precedence, malformed YAML, grouping, coverage, nesting, and caption retention.
  The existing upstream Starlette/httpx deprecation warning remains.
- Ruff lint and format checks pass; mypy reports no issues in 10 source files;
  `git diff --check` passes.
- Category browser verification: **34 checks passed**, with all **92 page URLs**
  reachable and matching index, desktop, and mobile navigation. Covers mouse,
  Enter/Space, current-page expansion, no-JavaScript use, search, menu focus,
  long titles, and layout at 1440px, 768px, and 390px.
- Existing catalog/search/reader browser verification: **35 checks passed**.
- Existing live-search browser verification: **28 checks passed**, including
  keyboard, touch, async failure/races, IME, filters, and viewport containment.
- Independent review found and rechecked a custom-caption preservation defect;
  its regression failed before the fix and passes afterward. No unresolved
  material finding remains. See [code review](collapsible-navigation-code-review.md).
- All **101 imported skill files** and **96 source snapshot files** retain
  their original SHA-256 hashes.

Screenshots and measurements are in
[the category browser report](collapsible-navigation-browser.md). The small
scrollbar visible beneath the phone reader menu belongs to an authored code
block with intentionally contained horizontal scrolling; menu widths and all
descendants were separately checked for overflow.

## Design check disposition

The finished UI received one Impeccable detector scan. Its
[snapshot](categories-impeccable-detect.json) contains 19 type/palette metadata
advisories and the existing static hover-contrast warning. The new 11px sidebar
context and 15px compact summary reuse existing sizes and are documented in
DESIGN.md. Other flagged sizes and status colors predate this change. No palette,
font, or source package was changed to satisfy metadata inference.

The static hover warning combines unrelated color declarations. Actual browser
hover states are recorded in [runtime contrast evidence](categories-runtime-contrast.json)
and meet 4.5:1. The dark NVIDIA palette, NVIS - OVA identity, and bottom
Documentation label remain intact.

Access control, the publishing skill, deployment, and remote HTTP MCP remain
deferred. Main remains the published baseline; this feature is saved on
development.
