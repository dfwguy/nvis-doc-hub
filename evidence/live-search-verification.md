# Live search verification

Implemented on local `development`, 23 October 2026. GitLab publication remains
deferred until the user has the required group access.

## Result

The catalog, project indexes, and search page now show clickable matching sections
while typing. Two characters and a 180ms pause trigger up to five ranked results.
Only the last query term is prefix-matched; completed terms remain literal.
Project and available topic/type filters apply. Ordinary full search and MCP
matching retain their existing behavior.

The shared dark dropdown shows section title, project/document context, and a
short plain-text excerpt. Native links open the actual hosted section anchor.
Arrow keys select, Enter opens the selected section, and Escape or Tab closes
the popup. Enter without a selection submits full search. The Open full search
link preserves query and filters without claiming the same prefix matching as
the live preview. Normal form submission also works with JavaScript disabled.

New typing or filter changes clear old choices and abort superseded requests.
Generation and parameter checks prevent late results from replacing newer ones
or reopening a dismissed popup. Composition input is deferred until committed.
Loading, empty, and failure feedback preserve the ordinary search action.

## Verification

- **TDD:** the backend's initial 13 new cases failed before implementation; an
  additional 33-term boundary regression failed before its fix. The real-browser
  typing test also failed before the UI existed. The initial browser failure is
  preserved in [browser evidence](live-search-browser-review.json).
- **44 Python tests pass.** Coverage includes partial final terms, exact preceding
  terms, Unicode/literal safety, metadata isolation, five-result ranking bounds,
  encoded anchors, raw query length, and unchanged ordinary search/MCP behavior.
- Ruff lint and formatting, mypy, JavaScript syntax, and diff checks pass. The one
  existing upstream Starlette/httpx TestClient deprecation warning is unchanged.
- The existing browser regression passes **35 checks**, including search,
  clipboard, navigation, reader, mobile tables, and previous presentation fixes.
- The portable [live-search browser suite](../scripts/live_search_verify.cjs)
  passes **28 checks**, covering typing, click/touch, keyboard, scope, debouncing,
  dismissal, composition, loading/empty/error recovery, request races, constrained
  viewport scrolling, and the JavaScript-free fallback. No page script errors
  occurred. [Independent visual/browser report](live-search-browser-review.md).
- Actual dropdowns were visually inspected on the catalog, search page, and
  project index at 1440px, 768px, and 390px, plus short-viewport above-field and
  scrolling states. Fields and popup edges align, targets are at least 44px,
  text has consistent insets, and no page overflows horizontally.
- [Independent code review](live-search-code-review.md) found no material issues
  and separately exercised DOM-safe text, unsafe destination rejection, cached
  keyboard reopening, and the absence of script errors.

The real publications have no topic/type facets beyond All; browser tests verify
actual project scope, while fixture-backed Python tests verify all three filters.
Browser checks emulate touch and viewport changes; they do not claim a native
phone keyboard or manual screen-reader audit.

## Design checks

The imported Impeccable detector was run once on the finished UI. Its snapshot
contains 17 advisory type/palette metadata findings and the existing static hover
contrast warning. Sixteen advisories refer to pre-existing declarations; the new
15px suggestion title follows the existing 15px input size and is explicitly
documented in DESIGN.md. Existing palette/status colors and imported code were
preserved rather than changed to satisfy metadata inference.

The hover warning combines unrelated literal declarations. Actual suggestion
hover and primary-button hover colors were measured after transitions settled;
their text contrast passes 4.5:1. [Detector snapshot](live-search-impeccable-detect.json),
[runtime contrast](live-search-runtime-contrast.json). No new visual identity or
animation was introduced.

The keyboard behavior follows the W3C's
[editable combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/).

## Reproduce

With the local app running and Playwright installed as described in
[verification.md](verification.md):

```bash
NODE_PATH="$PWD/.browser-tools/node_modules" node scripts/browser_verify.cjs
NODE_PATH="$PWD/.browser-tools/node_modules" node scripts/live_search_verify.cjs
```

Final desktop, tablet, phone, feedback, and keyboard captures are linked from the
browser review and stored under `.impeccable/review/live-search-*.png`.
