# Appearance switch and simplified discovery

The user requested a persistent light/dark toggle and a simpler Browse
documentation view after the multi-carousel discovery iteration. The existing
Python/FastAPI/Jinja application remains the frontend; no React migration or npm
installation is required for this change.

## Current presentation

The default page has one **Explore popular documentation** region with at most six
genuinely opened documents. Real aggregate all-time opens determine rank; repeats
are included. An unused hub shows **No popular documentation yet**, not an
alphabetical fallback labeled popular. No From {project} or type shelves appear
on the default view. Selecting the Project dropdown opens that project's
paginated vertical document library; Browse documents opens the full library.

The native ordered popular list remains one horizontal carousel. Explicit 44px
previous/next controls, native keyboard navigation, and touch scrolling reveal
more cards. There is no autoplay; reduced motion makes control-triggered scrolling
immediate. Controls appear only with JavaScript and overflow and disable at the
ends. No extra project/type carousel rows appear.

The global sidebar no longer contains a Projects heading or complete project list.
The Browse dropdown is the main project selector. Dedicated project and reader
routes retain only their current project's category navigation.

Cards show project, sentence-case title, rank, and opens; raw paths do not
dominate the card and remain available as link tooltips and reader provenance.
Cards have 168px minimum height and 24px padding, becoming 16px on phones, with
280px minimum / 31% preferred desktop columns and 88% width through 700px.
A 4px focus gutter and matching scroll padding preserve an honest initial
Previous-button state.

Display formatting capitalizes only an initial lowercase prose letter. It does
not apply title case or lowercase the rest of a string. Commands, identifiers,
acronyms, paths, flags, and encoded text are preserved. Reader HTML changes only
an initial plain-text heading node; nested markup and code/preformatted content
stay as authored. Source bytes, stored publications, and API/CLI/MCP content are
not rewritten.

## Switch behavior

- [theme.js](../src/nvis_hub/static/theme.js) runs in the document head before
  stylesheets, reading `nvis-hub-theme` from localStorage. Valid values are `dark`
  and `light`; missing, invalid, or unreadable storage defaults to dark.
- The topbar control is a native button with `role="switch"`, stable accessible
  name **Dark mode**, a decorative moon SVG, and synchronized `aria-checked`.
  Native click, Space, and Enter apply the change immediately. The action title
  announces Use light mode or Use dark mode.
- The selected theme persists across page loads. Blocked storage does not prevent
  a page-local change, and storage events update other open tabs without write
  loops. The active color-scheme metadata follows the selection.
- The control starts hidden and is revealed only when its listener is connected.
  Without JavaScript, the application remains dark and the unavailable toggle
  does not create a dead keyboard target.
- Targets are at least 44px square. The visible label hides through 575px while
  the accessible name remains. The 30px × 18px track has a 12px thumb; its 150ms
  translation is removed under reduced motion.

## Tokens and references

[themes.css](../src/nvis_hub/static/themes.css) loads after the existing stylesheet.
It maps documented KUI semantic surface, interaction, text, border, and overlay
shadow roles to both appearances, bridging legacy dark literals explicitly.
Dark-mode colors retain the established palette. Light mode uses white reading
surfaces, neutral pale raised surfaces, dark text, and Deep Green links/focus for
contrast. NVIDIA Green primary buttons retain black text; hover retains white
text on Deep Green. Authored diagrams and images are not inverted.

References read for this work:

- [KUI skill](../.agents/skills/kaizen-ui/SKILL.md).
- [Switch](../.agents/skills/kaizen-ui/references/components/Switch.md): labeled,
  immediate-effect binary preference and native control behavior.
- [Settings](../.agents/skills/kaizen-ui/references/patterns/settings.md): discrete
  preference controls and immediate application.
- [Semantic colors](../.agents/skills/kaizen-ui/references/design-tokens/COLORS.md)
  and [effects/layout](../.agents/skills/kaizen-ui/references/design-tokens/EFFECTS_AND_LAYOUT.md):
  theme roles, control edges, overlay depth, and reduced motion.
- [Carousel](../.agents/skills/kaizen-ui/references/components/Carousel.md):
  a single bounded collection with explicit navigation and no autoplay.
- [Page shell](../.agents/skills/kaizen-ui/references/layouts/page-shell.md) and
  [typography](../.agents/skills/kaizen-ui/references/design-tokens/TYPOGRAPHY.md):
  shared application chrome and consistent typography roles.

KUI's React component/runtime CSS is not installed. These native controls follow
the documented Switch pattern and semantic tokens; they are not represented as
the actual KUI React component. Existing self-hosted IBM Plex Sans and explicit
type sizes remain in place.

## Verification performed by the theme worker

The initial executable check failed because the new theme script did not exist.
After implementation, Node VM checks pass for default and stored preferences,
invalid values, synchronized ARIA, storage failures, cross-tab events, and
color-scheme metadata. JavaScript syntax and CSS parsing checks pass.

An isolated real Chromium 151.0.7922.34 fixture using the actual application and
theme styles passes Space/Enter operation, reload persistence, stable switch
semantics, visible focus, reduced motion, no-JavaScript control hiding, and blocked
storage fallback. Measured light-mode text contrast passes 4.5:1: headings
15.91:1, card title 14.59:1, project metadata 6.42:1, navigation 15.91:1, source
links 10.65:1, inline code 9.77:1, block code 14.59:1, and primary button 8.71:1.

These fixture results cover the switch/palette behavior. The root verification
records integrated page, mobile-header, reader, live-search, and responsive
checks separately; this document does not substitute a fixture for that audit.
