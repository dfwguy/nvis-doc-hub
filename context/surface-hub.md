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
search, filters, and document shelves; search lands at the precise authored section.
The project rail preserves a stable authored documentation tree.

OWN-WORLD: The supplied NVIDIA reference's dark theme: NVIDIA Green (#76b900) for
links, focus, primary actions with black text, and identity marks. Deep Green
(#004831) supplies the primary-action hover background. The background and reading sheet are
#111; raised cards, inputs, and code use #1a1a1a. Headings are white, body text is
#eee, supporting text is #999, fenced code is #ddd, and inline code is NVIDIA Green. The topbar is black; neutral
greys and 1px edges establish hierarchy, with #333 borders, #2a2a2a rules, and #666
control edges.
Team identity is NVIS - OVA. Reference evidence: evidence/brand-color-reference.md.
The sidebar bottom reads NVIS - OVA Documentation; the footer repeats that label
only when the sidebar folds.
IBM Plex Sans, the tasteskill-dealt working face, is self-hosted for offline reading.

STORY: Search, filter the document library, or choose a document from a discovery
shelf, then read source documentation centrally with a clear path back to the
project and source commit. Shared popularity reflects actual all-time browser
opens, including repeats; an unused hub shows Explore documentation instead.

FIRST VIEWPORT: A 228px labelled project rail, 48px shared chrome, and dark inset
sheet. Discovery has a 28px title, prominent labelled search, a Project filter,
and horizontal document shelves. Topic and Document type filters appear when
metadata exists or their URL filter is active. Shelves use real project documents
when explicit kinds are unavailable. Browse documents
opens the alphabetical library; text queries show ranked sections in the same
surface. Reader uses the same rail, a 65–75ch text column and a quiet contents margin.
Mobile folds the rail into a semantic disclosure and keeps search immediately usable.

KUI ADAPTATION: Apply the supplied Kaizen browse, navigation, search/filter, card,
carousel, and empty-state guidance through native Jinja markup and semantic CSS
variables with settled-theme fallbacks. KUI React components and typography CSS
are not installed; this is not a React migration. Preserve the existing reader
world and self-hosted typography. See evidence/discovery-kui-guidance.md for the
references used, adaptation details, and verification boundaries.

FORM: Reference shelf, fifth of seven grounded candidates (runbook binder,
engineering handbook, repository browser, team wiki, reference shelf, parts catalog,
service directory). seed:e15db3e576ab9146. Tasteskill framed-sheet, seed 1837803909.
Pinned palette and task conventions take precedence over decorative challengers.
Physical scene: engineers reading procedures at a desk;
a dark reading sheet supports long technical passages and copied code.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
