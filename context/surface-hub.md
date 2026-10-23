# Catalog, search and documentation reader

Catalog/search: Operate. Documentation: Read. Code-first. Audience and scope come
from PRODUCT.md and BUILD_BRIEF.md; no additional product interview is needed.

## Data and jobs
- Two registered GitLab projects; no fabricated catalog entries.
- Exact source revision, authored paths, publication dates, source mode and errors.
- Documentation counts computed from actual successful imports.
- Topics/types from authored metadata or explicit registration only.
- Main job: find a procedure and read it in the hub.
- Discovery question: which document can help me, by search, metadata, or shared usage?
- Results question: which section answers my search?
- Reader question: what does this authored procedure say, and where did it come from?
- Source status question: what is published and how can I refresh it?
- Signature: source-to-section trail connects project, hosted path and exact revision.

## Direction contract
THESIS: An NVIS - OVA reference shelf: one Browse documentation destination combines
search, filters, and one bounded popular-document carousel; search lands at the precise
authored section. Project-specific collections appear only after a scope is chosen.
The sidebar contains application destinations and, only on project/reader routes,
the active project's authored documentation tree. It does not list all projects;
the Browse dropdown is the main project selector.

OWN-WORLD: The supplied NVIDIA reference's dark theme: NVIDIA Green (#76b900) for
links, focus, primary actions with black text, and identity marks. Deep Green
(#004831) supplies the primary-action hover background. The background and reading sheet are
#111; raised cards, inputs, and code use #1a1a1a. Headings are white, body text is
#eee, supporting text is #999, fenced code is #ddd, and inline code is NVIDIA Green. The topbar is black; neutral
greys and 1px edges establish hierarchy, with #333 borders, #2a2a2a rules, and #666
control edges.
Dark remains the initial appearance. The user's later request adds a persistent
light mode: white reading surfaces, neutral pale controls, dark primary/secondary
text, and Deep Green links/focus with the same NVIDIA Green primary actions.
The two appearances share content, hierarchy, and interaction rather than
maintaining separate page layouts. A native Dark mode switch in the topbar saves
the preference in `nvis-hub-theme` and applies it before styles load.
Team identity is NVIS - OVA. Reference evidence: evidence/brand-color-reference.md.
The sidebar bottom reads NVIS - OVA Documentation; the footer repeats that label
only when the sidebar folds.
IBM Plex Sans, the tasteskill-dealt working face, is self-hosted for offline reading.

STORY: Search, select a project, browse the paginated document library, or open one
of the genuinely popular documents, then read with a clear path back to the project
and source commit. Explore popular documentation is the single default collection,
bounded at six real all-time shared-open rankings. With no usage it shows No
popular documentation yet rather than inventing a ranking.

FIRST VIEWPORT: A 228px application rail, 48px shared chrome, and dark inset
sheet in dark mode, with equivalent light reading surfaces when selected.
Discovery has a 28px title, prominent labelled search, a Project filter, and one
popular carousel with explicit previous/next controls and native keyboard/touch
scrolling, without additional From {project} or type rows. There is no autoplay;
reduced motion makes control-triggered movement immediate.
Topic and Document type filters appear when metadata exists or their URL filter
is active. Selecting a project opens its paginated vertical list. Browse documents
opens the full alphabetical library; text queries show ranked sections in the same
surface. Reader uses the same rail, a 65–75ch text column and a quiet contents margin.
Mobile folds the rail into a semantic disclosure and keeps search immediately usable.

KUI ADAPTATION: Apply the supplied Kaizen browse, navigation, search/filter, card,
carousel, empty-state, settings, and Switch guidance through native Jinja markup and
semantic CSS variables for both appearances. KUI React components and typography CSS
are not installed; this is not a React migration. Preserve the existing reader
world and self-hosted typography. Labels and title displays use conservative
sentence case while preserving commands, paths, acronyms, and stored source/API
content. See evidence/theme-implementation.md for current switch/token behavior;
evidence/discovery-kui-guidance.md records the earlier multi-carousel iteration.

FORM: Reference shelf, fifth of seven grounded candidates (runbook binder,
engineering handbook, repository browser, team wiki, reference shelf, parts catalog,
service directory). seed:e15db3e576ab9146. Tasteskill framed-sheet, seed 1837803909.
Pinned palette and task conventions take precedence over decorative challengers.
Physical scene: engineers reading procedures at a desk;
the selected reading sheet supports long technical passages and copied code.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
