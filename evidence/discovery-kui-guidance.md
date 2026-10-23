# Kaizen UI guidance for unified document discovery

The supplied local Kaizen UI skill was read before this UI work. It documents
KUI Foundations React 1.18.0, skill metadata version 5. This record describes
reference selection and the implemented native adaptation. It does not claim
browser checks have passed; verification results belong to the feature's test
and browser evidence.

## Selected references

The surface is a browse page: find a document by query, explicit metadata, or
discovery. The following local references informed the change:

- Layout: [browse page](../.agents/skills/kaizen-ui/references/layouts/browse-page.md),
  [list view](../.agents/skills/kaizen-ui/references/layouts/list-view.md),
  [page shell](../.agents/skills/kaizen-ui/references/layouts/page-shell.md),
  [layout principles](../.agents/skills/kaizen-ui/references/layouts/layout-principles.md),
  and [page modification](../.agents/skills/kaizen-ui/references/layouts/page-modification.md).
- Patterns: [navigation](../.agents/skills/kaizen-ui/references/patterns/navigation.md),
  [search](../.agents/skills/kaizen-ui/references/patterns/search.md),
  [filters](../.agents/skills/kaizen-ui/references/patterns/filters.md),
  [data display](../.agents/skills/kaizen-ui/references/patterns/data-display.md),
  [entity cards](../.agents/skills/kaizen-ui/references/patterns/entity-cards.md),
  [ranked lists](../.agents/skills/kaizen-ui/references/patterns/ranked-lists.md),
  and [empty states](../.agents/skills/kaizen-ui/references/patterns/empty-states.md).
- Component contracts reviewed for applicable behavior: PageHeader, TextInput,
  Combobox, Select, Card, Carousel, Grid, Text, Tag, Badge, VerticalNav,
  StatusMessage, Button, and Anchor under the skill's `references/components/`.
- Tokens: [semantic colors](../.agents/skills/kaizen-ui/references/design-tokens/COLORS.md),
  [spacing](../.agents/skills/kaizen-ui/references/design-tokens/SPACING_SCALE.md),
  [typography](../.agents/skills/kaizen-ui/references/design-tokens/TYPOGRAPHY.md),
  and [effects/layout](../.agents/skills/kaizen-ui/references/design-tokens/EFFECTS_AND_LAYOUT.md).

## Decisions reflected in the implementation

One Browse documentation navigation destination replaces All documentation and
Global search. Both existing `/` and `/search` entry routes render the same
discovery template. The page has a flat heading, a prominent labelled search,
up to three available filters, and either shelves or results. The existing project rail
remains because authored documentation has a genuine nested hierarchy; the
change does not replace the reader shell or add another navigation layer.

The search is a native server-submitted form enhanced by existing live results.
Project, Topic, and Document type filter the same result set. Project stays
available when projects exist. Topic and Document type appear only when their
metadata is available or their URL filter is active; an unavailable active value
remains visible and removable. Filter changes
submit automatically; no-JavaScript users retain Apply filters. Current query
and filters stay in URL parameters, with explicitly named removable filter links.
Clear filters preserves the query; Clear search preserves filters. Filtered
misses retain their controls and expose a recovery action.

Discovery shelves are collections of document entities, so Card and Carousel
guidance fits better than a dashboard ranking chart. Whole-card anchors preserve
navigation semantics and avoid competing nested targets. Every card provides
project/source context, a title, kind, and authored path. The source model has no
summary field in its lightweight card projection, so no summary or imagery was
invented. Popular cards additionally show actual rank and all-time open count,
with a visible explanation that repeats count. An unused hub shows Explore
documentation rather than a fabricated popularity ranking. How-to and Reference
shelves use actual explicit document kinds; empty shelves are omitted. Remaining
slots, up to three shelves in total, use From {project title} collections of real
documents; their View all links filter by that project. The current publications
have no explicit topic/type metadata, so project shelves fill those slots and
empty metadata controls stay hidden. No type is inferred from a path, prose, or
the presentation category rail, and source publications were not changed to
populate these controls.

The alphabetical document library is paginated at 30 items. Text queries continue
to rank matching sections rather than replacing full-text relevance with opening
counts. No user identity or personalized recommendation model is introduced.

## Native integration and token boundary

The application remains Python/FastAPI/Jinja with native HTML, CSS, and small
progressive enhancements. The user supplied pending KUI package configuration;
the React components and their shared CSS are not installed. No React runtime,
frontend migration, or dependency installation is part of this change. The
native templates follow the reviewed component contracts but are not claimed
to be actual KUI React components.

The discovery stylesheet references the exact documented semantic variables:

- Surfaces: `--background-color-surface-raised` and
  `--background-color-interaction-hover`.
- Foreground: `--text-color-primary` and `--text-color-secondary`.
- Borders: `--border-color-base`, `--border-color-brand`, and
  `--border-color-interaction-base`.
- Density spacing: `--spacing-density-md`, `--spacing-density-lg`,
  `--spacing-density-xl`, `--spacing-density-2xl`, and `--spacing-density-3xl`.
- Shape: `--radius-md` and `--radius-lg`.

Each reference has an explicit fallback to the existing design token or settled
size. Undefined KUI variables therefore retain the dark NVIDIA colors and 8/12/
16/24/32px spacing. No primitive palette replaces the user's exact theme.

KUI's typography guidance exposes named React variants and generated utility
classes, but does not provide a complete font-property CSS-variable mapping.
Those classes are not loaded in this application. The adaptation retains the
self-hosted IBM Plex Sans and documented native hierarchy: 18px medium shelf/card
titles, 13px shelf descriptions and select text, 12px context/path/count labels.
These are explicit existing-system values, not invented KUI font tokens or a
claim of exact React Text rendering. Sentence case is retained throughout.

## Accessibility and responsive behavior to verify

Native forms, labels, links, buttons, fieldsets, headings, and lists provide the
base semantics. Result counts have status semantics. Shelf controls have explicit
names and `aria-controls`; each shelf list has an accessible name and is
focusable. Cards contain no nested links. Existing focus outlines and live-search
keyboard behavior remain part of the shared shell.

Filters have 44px targets and stack below 576px. Shelf buttons are 44px squares,
appear only when enhanced scrolling needs them, and disable at the relevant end.
At phone widths cards use 88% of shelf width rather than forcing a wide page;
the next card can peek into view. Long names and paths wrap. Only the shelf
scrolls horizontally. Keyboard/touch scrolling and native links remain available
without JavaScript. There is no autoplay, and reduced-motion preference disables
smooth control-triggered shelf scrolling. The existing 700px and 1100px reader
and navigation breakpoints remain intact.

Verify populated, no-history, no-publication, no-match, invalid-query, and
unavailable-filter states; keyboard focus/selection; query/filter independence;
responsive containment; and actual runtime contrast before reporting completion.
