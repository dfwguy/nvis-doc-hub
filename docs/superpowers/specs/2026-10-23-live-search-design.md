# Live documentation search

The user requested clickable results beneath the search input while typing. This
extends the existing search controls on the catalog, project indexes, and search
page. Preserve the dark NVIDIA theme, authored documentation, existing full search,
and deferred hosting/access work. Implement on the local `development` branch.

## Approach

Use the existing SQLite section index through a small suggestions endpoint. Match
completed terms literally and the final term as a prefix, return at most five
ranked sections, and preserve active project/topic/type filters. Keep normal
search and MCP matching unchanged. A client-side index would duplicate retrieval
logic and download unnecessary content; polling the exact-term search endpoint
would not find partially typed words. These are implementation choices within the
user's delegated technical scope.

`GET /api/search/suggestions?q=...&project=...&topic=...&kind=...` returns an array
of objects with `project_slug`, `project_title`, `title`, `heading`, `snippet`, and
`url`. Fewer than two trimmed characters returns an empty array; queries longer
than 200 characters return HTTP 400. Results link to the matching hosted section.

## Interaction

- Enhance existing forms without requiring JavaScript for ordinary search.
- Debounce typing by 180ms, abort superseded requests, and reject late responses.
- Render titles, project/document context, and short plain-text excerpts in a
  charcoal dropdown aligned to the search field. Provide an Open full search link.
- Keep focus in the input. Arrow Down/Up selects an option; Enter opens a selected
  result. Enter without a selection submits the ordinary search. Escape, Tab,
  clearing the query, and leaving the control dismiss suggestions.
- Expose combobox/listbox state, active-option identity, and polite live feedback.
  Support composition input, touch, native result links, and pointer interaction.
- Clear stale choices immediately when query or filters change. Loading, no-match,
  and request-failure states remain readable; full search stays available.
- Constrain the popup to the visible viewport, including phone keyboard resizing.
  Maintain the current focus colors, spacing, readable text, and touch targets.

## Verification

Tests must first demonstrate missing prefix suggestions and missing browser
interaction. Exercise real indexed publications, filters, bounds, input limits,
click/keyboard navigation, dismissal, request races, failure recovery, composition,
phone layout, and the JavaScript-free fallback. Run the full Python suite and
existing browser regression script, then visually review the dropdown at desktop,
tablet, and phone sizes. Commit completed work locally on `development`; remote
publishing remains deferred pending group permissions.
