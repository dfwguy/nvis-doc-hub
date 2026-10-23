---
name: NVIS - OVA Documentation Hub
description: A restrained reference shelf for authored engineering documentation.
colors:
  accent: "#76b900"
  brand: "#76b900"
  primary: "#76b900"
  primary-hover: "#004831"
  search-primary-hover: "#004831"
  ground: "#111"
  surface: "#111"
  raised: "#1a1a1a"
  active: "#262626"
  border: "#333"
  rule: "#2a2a2a"
  control: "#666"
  search-border: "#666"
  heading: "#fff"
  primary-text: "#000"
  text: "#eee"
  muted: "#999"
  faint: "#999"
  nav-text: "#ddd"
  nav-hover: "#262626"
  code-surface: "#1a1a1a"
  code-text: "#ddd"
  light-ground: "#f5f5f5"
  light-surface: "#fff"
  light-raised: "#f5f5f5"
  light-active: "#e8e8e8"
  light-border: "#d1d1d1"
  light-rule: "#dedede"
  light-control: "#767676"
  light-text: "#222"
  light-muted: "#595959"
  light-accent: "#004831"
  light-error: "#9f2917"
  light-error-surface: "#fff1ee"
  light-error-border: "#b57465"
typography:
  headline:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "28px"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-.025em"
  reader-headline:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "30px"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-.025em"
  reader-section:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 600
    lineHeight: 1.35
    letterSpacing: "-.015em"
  title:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-.018em"
  body:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  reader-body:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.75
  label:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 500
    lineHeight: 1.5
  metadata:
    fontFamily: "'IBM Plex Sans', system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.65
rounded:
  inline: "3px"
  tree: "4px"
  search-button: "5px"
  control: "6px"
  panel: "8px"
  sheet: "16px"
spacing:
  compact: "8px"
  small: "12px"
  medium: "16px"
  panel-compact: "20px"
  gap: "24px"
  section: "28px"
  sheet-inset: "40px"
  reader-gap: "48px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-text}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "9px 15px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.heading}"
  button-secondary:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "9px 15px"
  button-secondary-hover:
    backgroundColor: "{colors.active}"
    textColor: "{colors.text}"
  search-field:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.panel}"
    padding: "7px 8px 7px 17px"
  navigation-active:
    backgroundColor: "{colors.active}"
    textColor: "{colors.text}"
    rounded: "{rounded.control}"
    padding: "9px 10px"
  project-card:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.panel}"
    padding: "24px"
  source-trail:
    textColor: "{colors.muted}"
    typography: "{typography.metadata}"
  reference-table:
    textColor: "{colors.text}"
---

# Design System: NVIS - OVA Documentation Hub

## Overview

**Creative North Star: "The NVIS - OVA Reference Shelf"**

The default dark neutral frame and black topbar hold a dark reading sheet, one bounded popular-document carousel, and quiet source metadata for NVIS - OVA. A user-selected light mode provides white reading surfaces and dark text while preserving the same hierarchy and NVIDIA identity. The original dark-theme requirement remains the default; the later explicit request for a light/dark switch adds the second appearance.

IBM Plex Sans carries both navigation and prose; a system monospace stack distinguishes commands and exact revisions. Source paths stay in the surrounding sans unless authored as code. Fine borders and neutral tonal changes establish hierarchy. NVIDIA Green identifies links, keyboard focus, primary actions, and brand marks; Deep Green supplies the hover background for primary actions.

**Key Characteristics:**

- Dark reading sheets and raised charcoal panels by default; white reading surfaces and dark text in light mode.
- NVIDIA Green primary actions and identity marks; links and focus use the theme's readable green, with Deep Green primary-action hover backgrounds.
- Compact navigation beside generous document line spacing.
- Fine borders, modest corners, and flat resting surfaces.
- Visible source paths, revisions, and publication context.
- One bounded popular-document carousel, semantic disclosures, and contained scrolling for that carousel and authored code/tables.

## Colors

The default palette comes from the supplied NVIDIA documentation reference, audited in [brand-color-reference.md](evidence/brand-color-reference.md). Pure black, white, and neutral greys carry the reading hierarchy; the two NVIDIA greens carry interaction and identity. Dark remains the initial theme. The user's later request adds a persistent light mode rather than replacing that default. Frontmatter base tokens describe dark mode; `light-*` tokens record the explicit overrides. Native controls follow the active color scheme.

### Primary

- **NVIDIA Green** (`accent`): authored links, keyboard focus outlines, and selected contents links. **Deep Green** (`primary-hover` and `search-primary-hover`) supplies primary-action hover backgrounds.
- **NVIDIA Green** (`brand`): in-page NVIS - OVA marks, project-title arrows, source indicators, selection highlights, topbar hover/focus, and favicon background.
- **NVIDIA Action Green** (`primary`): primary buttons, the search submit button, and the keyboard skip link, with black text. Both `primary-hover` and `search-primary-hover` use Deep Green with white text.

### Neutral

- **Dark Frame** (`ground`): application surround, fixed rail, and mobile navigation overlay.
- **Dark Reading Sheet** (`surface`): the inset reading sheet. **Raised Charcoal** (`raised`) supports project panels, form fields, empty states, and command strips.
- **Active Neutral** (`active`) marks the current navigation location. `nav-text` and `nav-hover` carry its resting and hover treatments.
- **Fine Edge** (`border`) separates panels and reference rows; **Quiet Rule** (`rule`) divides related content. `control` and `search-border` give controls a stronger neutral edge.
- **White** (`heading`) carries headings. **Black** (`primary-text`) carries primary-action text and the topbar background. The topbar uses white identity text, light grey context/help text, and a mid-grey separator.
- **Body Text** (`text`), **Muted Grey** (`muted`), and **Metadata Grey** (`faint`) separate primary copy, supporting copy, and compact metadata.
- **Code Charcoal** (`code-surface`) identifies scrollable code blocks and their copy control; **Code Text** (`code-text`) and resting navigation use light neutral grey.

### Light appearance

- `light-ground` surrounds the white `light-surface`; `light-raised` and `light-active` separate controls, cards, and current navigation without tinted neutrals.
- `light-text` carries headings, body, and code; `light-muted` carries secondary text. `light-border`, `light-rule`, and `light-control` preserve the same edge hierarchy as dark mode.
- `light-accent` uses Deep Green for readable links and focus on light surfaces. Primary actions retain NVIDIA Action Green with black text and the same Deep Green/white hover state.
- Light feedback uses `light-error`, `light-error-surface`, and `light-error-border`. Authored images and SVG assets retain their colors; the theme never inverts them.

**The NVIDIA Palette Rule.** Keep NVIDIA Green primary actions and identity, Deep Green primary-action hover backgrounds, and neutral reading surfaces. Dark mode uses bright green links; light mode uses Deep Green links for contrast. Select appearances through semantic theme tokens rather than recoloring individual pages.

## Typography

**Display and Body Font:** IBM Plex Sans, with system-ui and sans-serif fallbacks. Regular (400), medium (500), and semibold (600) are self-hosted from the three `/static/fonts/plex-sans-*.ttf` files with `font-display: swap`.

**Label/Mono Font:** ui-monospace, SFMono-Regular, Consolas, monospace for code, source revisions, and command strips.

**Character:** A single working sans provides a coherent interface and long-form reading voice. Weight and spacing distinguish hierarchy; headings do not introduce a separate display family.

### Hierarchy

- **Headline:** the `headline` role serves page titles; the reader uses `reader-headline`, capped at 30ch. At widths through 700px, page titles become 25px and reader titles become 27px with 1.3 line height.
- **Reader section:** the `reader-section` role separates document sections; it becomes 21px through 700px. Third-level reader headings are 18px at 1.4 line height.
- **Title:** the `title` role labels project entries. Unified-library search-result titles use 19px at 1.4 line height; popular-card titles use the 18px hierarchy described below. Ordinary interface section headings range from 16px to 18px.
- **Body:** `body` supports tooling; `reader-body` supports documents. The reader remains at its full body size and line height on mobile. Project descriptions use the body size with 1.6 line height.
- **Label and metadata:** `label` identifies actions and `metadata` records paths, publication context, counts, and provenance. Source revision labels can step down to 11px. Numeric counts use tabular figures.
- **Code:** the `code` role describes code blocks. Inline code is 13px with NVIDIA Green text on a small charcoal background; block code becomes 12px through 700px, while retaining whitespace and scrolling.

Interface labels, document titles, navigation, result headings, and reader heading displays use conservative sentence case: only an initial lowercase prose letter is capitalized. Commands, paths, flags, acronyms, mixed-case identifiers, encoded entities, and headings beginning with nested markup remain as authored. Stored documents and API/CLI/MCP content are unchanged; reader display formatting touches only an initial plain-text heading node and excludes code/preformatted regions.

**The Same Voice Rule.** Use IBM Plex Sans for interface text and authored prose; use the system monospace stack for code and revisions. Keep sentence-case labels consistent without rewriting technical names or source content.

## Layout

The sidebar's bottom identity label is **NVIS - OVA Documentation**. At desktop
widths it appears there once; the workspace footer retains its source-authority
line. Through 1100px, when the sidebar folds, the documentation label appears in
the workspace footer instead.

The desktop frame has a fixed 228px rail, a 48px topbar, and a sheet inset 8px from the right edge. The sheet uses 38px 40px 48px padding; reader sheets use 28px top padding above 1100px. Unified discovery and its results cap their content at 80rem; project and source surfaces cap at 1160px. The homepage shows one popular-document carousel, not separate project/type rows. The global sidebar has no Projects heading or full project list; the Browse dropdown is the main project selector. Dedicated project and reader routes retain only the active project's authored category navigation. Project selection and Browse documents open the paginated vertical library described below.

The reader pairs a flexible text column capped at 76ch with a 176px contents rail and the reader-gap token. The contents rail sticks 28px from the viewport top. Authored paragraphs use an 18px bottom gap, section headings begin after 38px, and the typography supplies the reading rhythm rather than spacious decorative separators.

- **1101–1250px:** sheet horizontal padding becomes 30px; the reader contents rail becomes 154px with a 28px gap. Project panels use 20px padding and stack their header metadata and footer action.
- **Through 1100px:** the fixed rail becomes a native menu disclosure. The topbar becomes 52px high, the sheet uses 8px side margins and 30px padding, and the reader retains a 160px contents rail with a 28px gap. Available discovery filters remain visible. The navigation overlay is capped at `min(360px, calc(100vw - 24px))`, with a 290px minimum and viewport-bounded vertical scrolling.
- **Through 700px:** the sheet becomes edge-to-edge, drops its side borders and rounded silhouette, and uses 27px 20px 36px padding. Project entries become one column with an 18px gap. The reader contents rail becomes an inline native disclosure. Filter fields stack and selects become 44px high. Primary controls become at least 44px high; the search submit is 42px within its 54px field. Prose and source paths wrap; code and tables retain their own horizontal scrolling. Reference tables have a 580px minimum width inside their scroll region.
- **Through 620px:** the reference-table instruction “Scroll horizontally to see all columns.” becomes visible immediately before the table. The wrapper remains keyboard focusable at every width.

The spacing tokens capture repeated intervals rather than imposing a strict grid. Compact icon gaps, panel padding, section gaps, and reading margins retain their distinct observed roles.

## Elevation & Depth

Sheets and panels are flat. Theme-specific reading surfaces, raised panels, fine rules, and a neutral current-location fill provide depth. A focused search field adds an accent ring (`0 0 0 1px var(--accent)`) without becoming a lifted surface. Keyboard controls use a 2px accent outline with a 4px offset; code-copy controls reduce the offset to 2px. The theme switch uses a 3px outline offset.

### Shadow Vocabulary

- **Floating navigation:** `0 8px 24px #00000066` separates the open mobile menu from the reading sheet.
- **Light overlays:** the active light theme uses the KUI `--shadow-md` role (`0 6px 20px #0000001f`) for the mobile menu and live-search popup.

**The Overlay Shadow Rule.** Keep sheets and document cards flat. Soft shadows separate floating menus and the light search popup from the reading surface. A search focus ring is an interaction indicator, not elevation.

Motion is limited to color and background-color on hovered links and buttons (150ms, ease-out), smooth document scrolling, and the theme switch's 150ms thumb translation. Reduced-motion preference removes transitions and animation and switches document scrolling to auto. The single popular carousel moves only in response to native touch/keyboard use or its previous/next controls; control-triggered smooth scrolling becomes immediate under reduced motion. There is no autoplay. There is no defined pressed transform or hover lift.

## Shapes

The desktop sheet has the largest corner radius; project panels, empty states, the large search field, and the floating menu use the panel radius. Standard buttons, selects, notices, and code blocks use the control radius. Tree links and code-copy controls use the tree radius; the search submit uses its dedicated radius; inline code and keyboard outlines use the inline radius. Fine 1px borders define the edges. The tiny circular source indicator expresses provenance beside text rather than replacing it.

The mobile sheet becomes square and reaches the viewport edges at the 700px breakpoint. Inline SVG icons use `currentColor`, round caps and joins, and a 1.6px stroke in a 24-unit viewBox. The NVIS - OVA mark uses a 2px stroke in a 30-unit viewBox.

## Components

### Buttons

Compact and deliberate. Primary buttons use NVIDIA Action Green with black text, a matching 1px border, medium label type, the control radius, a 38px minimum height, and frontmatter padding. Their hover uses Deep Green with white text (`primary-hover`). Secondary buttons use Raised Charcoal, Body Text, and the control border; hover uses Active Neutral. Through 700px their minimum height becomes 44px. Disabled buttons use the muted treatment (`#999` on `#262626`) and a wait cursor. Global keyboard outlines remain visible. No separate pressed appearance is defined.

### Appearance switch

The topbar contains a native button following KUI's immediate-effect Switch
pattern, with a decorative moon SVG, a 30px × 18px track, and the stable accessible
name **Dark mode**. Its `role="switch"` and `aria-checked` describe whether dark
mode is enabled; its title names the next action. The target is at least 44px
square, with 8px gaps, 8px 12px padding, the control radius, and a 1px control
border. The 12px thumb translates 12px in 150ms. Through 575px the visible label
hides and horizontal padding becomes 6px; the accessible name and switch remain.
Reduced motion removes the thumb transition.

The saved `nvis-hub-theme` preference applies from an external head script before
CSS loads. Dark is the default when no valid preference exists. Changes apply
immediately and persist across pages/reloads; storage failures still permit a
page-local switch. Storage events synchronize open tabs. The button starts hidden
and appears after JavaScript connects it, so no-JavaScript users retain a usable
dark application without a nonfunctional control. The active color-scheme metadata
and native controls follow the selected theme. See
[theme implementation](evidence/theme-implementation.md) for source/reference and
verification details.

### Search field

A labelled, broad search assembly with a leading SVG icon and an integrated primary submit. The field uses its frontmatter padding, a 1px Search Border edge, panel corners, a 56px minimum height, and a 12px internal gap. The 15px input has a 24px line height and no separate border. Focus within changes the edge to NVIDIA Green and adds the focus ring; the input delegates its focus indication to the assembly. The submit has a 40px minimum height, 10px 17px padding, and its dedicated radius. Its disabled treatment is `#999` on `#262626`. Through 700px the input becomes 14px, its submit arrow is hidden, and field padding becomes 5px 6px 5px 12px.

Search-result titles wrap within a shrinkable text span while their arrow remains beside the first line. Unified discovery uses the same search assembly above its popular carousel or results; the earlier standalone search-start prompt is replaced by document discovery.

Live suggestions progressively enhance the same input on the catalog, project,
and search pages. After two characters and a 180ms pause, up to five ranked
sections appear in a field-aligned charcoal popup. Project and selected metadata
filters apply. Each option uses a 15px medium green title, 12px muted context,
and a two-line 13px excerpt, with an 18px total inset from the popup edge and a
44px minimum target. The popup uses the panel radius, a control-colored border,
no shadow, and contained scrolling capped at 420px and the visible viewport. It
opens above the field when space below is limited. Hover and keyboard selection
use Active Neutral. Loading, no-match, and unavailable states keep the Open full
search action available. Arrow keys select without moving input focus; Enter opens
a selected section, and Escape or Tab dismisses. Ordinary form submission remains
available with JavaScript disabled. The project label names its scoped search.

### Navigation

Quiet labelled destinations and an authored document tree. One Browse documentation destination covers the homepage and results, replacing the separate All documentation and Global search destinations. Main links have a 38px minimum height and 4px vertical separation. Current links use Active Neutral, Body Text, and medium weight; hover uses `nav-hover`. The global Projects heading and full project list are absent. Dedicated project and reader routes show only the current project link and its category tree, using the same current-location language with narrower hierarchy; the Browse dropdown is the main project selector. At the 1100px breakpoint the existing navigation is reused inside a semantic menu disclosure with 44px main link targets. The reader's contents disclosure appears through 700px; its desktop alternative uses quiet text and NVIDIA Green hover/current states.

Adjacent-document links use their `prev` and `next` relationship for alignment. Previous stays left and next stays right, including the first and last document.

Project navigation and indexes group documents into native collapsible Tutorials,
How-to guides, Reference, and Explanation sections, following the supplied
`_toc.yml` template. Unknown classifications appear under Other documentation;
empty sections are omitted. The sidebar uses short category labels and the index
uses the full explanatory captions. Counts reflect the actual contained pages.
Groups start collapsed except the active reader's category, which opens to expose
its current-page link. Disclosure headers remain usable without JavaScript.

Sidebar summaries have 44px targets, 13px medium labels, quiet 12px counts, and the
existing chevron, which rotates when open. Index summaries use 16px medium labels
(15px on phones), a 16px inset (12px on phones), and fine row separators. Document
rows retain authored guide/caption context beneath their title. Nested entries
retain their order and stepped indentation. These lists remain flat surfaces with
no new shadow or color. Native focus receives the established green outline.

### Document discovery

The homepage and `/search` share one discovery surface. A flat heading and Browse
documents link sit above labelled search and available filters. Project stays
available when projects exist; Topic and Document type appear only when their
metadata has values or their URL filter is active. Active unavailable values
remain visible and removable instead of being silently dropped. Filters use equal
shrinkable columns, 16px gaps, 12px labels with 8px separation, and 44px selects.
Through 575px they stack in one column. Changes submit with JavaScript; a
no-JavaScript Apply filters button preserves ordinary form use. Applied-filter
links have 44px targets and explicit removal names. Clear search preserves filters;
Clear filters preserves the query. State stays in the URL.

Unfiltered discovery has exactly one region, **Explore popular documentation**,
with at most six documents ranked by actual shared all-time browser opens,
including repeats. No usage history shows **No popular documentation yet** and a
short direction to choose a project or Browse documents. It does not promote
alphabetical documents as popular. An empty publication shows the source-setup
state. The default page keeps exactly one popular carousel, with no additional
From {project} rows or type collections. Selecting a project opens its paginated
vertical document list. Browse documents opens the alphabetical library, paged
at 30 documents. A query shows
ranked matching sections in the same surface; filtered misses retain controls and
offer a relevant clear action. The carousel and paginated library stay bounded
as the document collection grows. The sidebar does not enumerate all projects;
only a dedicated project or reader route adds the active project's category tree.

The popular region is one native ordered list with contained horizontal scrolling.
Desktop columns use a 280px minimum and 31% preferred width; through 700px each
card uses 88% of the available carousel width. Card gaps are 16px; a 4px focus
gutter and matching scroll padding keep the first card visible without creating
a false previous action. Explicit 44px previous/next buttons appear only with
JavaScript and overflow, carry descriptive accessible names, and disable at the
ends. The list supports native keyboard and touch scrolling without autoplay.
Reduced motion makes button-triggered movement immediate. Cards are full native
links with no nested actions: muted project name and rank, a prominent
sentence-case title, then actual open count and a directional SVG. The authored
path remains a link tooltip and in the reader's provenance, rather than a large
block of card metadata. No description or image is invented.

Cards use the selected theme's raised surface, a 1px neutral border, an 8px
radius, a 168px minimum height, 24px padding (16px through 700px), and 8px internal
gaps. Titles are 18px medium at 1.4 line height; project and count use 12px
metadata. Long text wraps. Hover uses the theme's interaction-hover surface and
readable green border, without lift or shadow. Region headings use 18px type and
13px supporting text; distinct regions retain 32px separation. Reader navigation
and authored category disclosures keep their existing layout.

This refinement applies KUI's browse/search/filter/card/carousel/empty-state guidance
to the existing Python frontend. Semantic CSS variables for surfaces, text,
borders, radius, and density spacing bridge the two appearances. KUI React
components and shared typography CSS are not installed; native elements are not
presented as React components. Existing documented type values remain explicit
rather than inventing unavailable font tokens. The earlier multi-carousel
[discovery KUI guidance](evidence/discovery-kui-guidance.md) is historical context;
the current single-carousel simplification, current-project navigation, and theme
implementation are recorded in [theme implementation](evidence/theme-implementation.md).

### Source trail

A compact record following the authored text: a fine top border, 38px top margin, 22px top padding, metadata type, source icon, revision, linked path, and publication context. On desktop the revision aligns to the right. Through 700px it wraps onto its own line with a 25px inset; long source paths can wrap. The project footer and contents margin repeat the same source/revision language at their own densities.

### Code and reference tables

In default dark mode, code blocks use Code Charcoal with light grey code text, a fine neutral border, the control radius, 18px 20px padding, preserved whitespace, and contained overflow. Copy controls sit at the top-right; blocks with copy controls reserve 48px at the top, increasing to 54px through 700px. The mobile copy control has a 36px minimum height.

In light mode, blocks use the light raised surface, dark code text, and the light control edge; inline code uses Deep Green. Authored images and code text are not inverted.

The copy control belongs to the outer code frame, outside the horizontal scroller, so it remains visible while reading a wide command. The unenhanced code block keeps the same margins and scrolling behavior when JavaScript is unavailable.

Inline code in headings scales to 85% of the heading size, preserving title hierarchy. Body inline code and fenced code retain their established size.

Tables use 14px text at 1.6 line height, medium headers, 10px 14px cells, and fine bottom borders; first-column padding starts flush. Through 700px cells use 9px 12px padding. Their focusable, labelled scroll wrapper preserves every authored column and uses the keyboard outline. The visible scroll cue follows the 620px breakpoint described in Layout. This instruction is text, not an ornamental badge.

### Feedback surfaces

Empty states use Raised Charcoal, panel corners, a fine border, and 38px 28px padding, becoming 24px 20px through 700px. Informational notices use light neutral text, raised charcoal, and a fine grey border; failed-refresh notices use `#ffb4a5` text on `#301c19` with a `#71443b` border. Light mode replaces these with its neutral surface and text roles, and the matched light error token triplet. Neither redefines the primary interaction accent. Preserve meaningful status text alongside color.

## Do's and Don'ts

### Do:

- **Do** keep authored documentation on the selected reading surface with its source trail visible, using dark as the initial appearance.
- **Do** use the theme-readable green for links and focus, NVIDIA Green for primary actions and identity, and Deep Green for primary-action hover backgrounds.
- **Do** keep the reader body at its established size and line height on narrow screens.
- **Do** use real SVG strokes, semantic links, and native disclosure controls.
- **Do** preserve horizontal table and code scrolling; show the table cue at the implemented narrow breakpoint.

### Don't:

- **Don't** replace body or navigation text with a display typeface.
- **Don't** add resting shadows or hover lifts to sheets and project panels.
- **Don't** reintroduce olive or green-tinted neutrals; use the exact reference palette.
- **Don't** shrink wide tables or code to fit the viewport; retain contained scrolling.
- **Don't** replace source revisions with decorative status labels.
