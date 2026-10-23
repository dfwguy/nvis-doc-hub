# Unified documentation discovery

The user's feedback calls for one Browse documentation destination, a Browse
documents action, and homepage shelves of documents rather than projects. The
user explicitly selected popularity ranked by shared document opens. Apply the
imported Kaizen UI references; preserve the Python frontend and dark NVIDIA theme.

## Approach

Keep FastAPI/Jinja and progressive enhancement. `/` and the existing `/search`
route render one discovery surface. One search form offers live section results
plus the available Project, Topic, and Document type filters. Empty metadata
dimensions are omitted unless an active URL filter needs to be shown/removed.
Full-text searches retain
section ranking; an empty query browses actual documents alphabetically. URL
parameters preserve query, filters, and pagination. Clear search and Clear filters
operate independently. One navigation item replaces All documentation and Global
search. The project/category rail remains for authored document navigation.

The initial homepage shows up to three bounded horizontal shelves: Popular
documents (real all-time opens), How-to guides, and Reference when explicit
matching metadata exists. Actual project-document shelves fill remaining rows
when classifications are absent; the current sources have no type/topic metadata.
Before opens exist, the first shelf is honestly labeled Explore documentation.
Browse documents opens the complete paginated library. Cards are native links to
authored documents with project, title, type, and path; no invented descriptions,
images, classification, or popularity. Shelf buttons, keyboard and touch scrolling
are supported without autoplay. Native links and the library work without JS.

An additive SQLite counter stores aggregate opens by project/path, incrementing
only successful browser reader requests. Counts survive refresh and restart;
removed documents are excluded. No identity, cookie, or user profile is stored.
Hub retrieval and existing CLI/MCP/search contracts stay side-effect-free.

## Alternatives and constraints

A rename-only change would retain two separate discovery experiences and would
not implement popular documents. A React migration could use KUI React components
directly but is outside the user's authorization. Use KUI's documented layouts,
native control semantics, and semantic CSS token names with settled-theme
fallbacks. Do not install the pending React package or modify the imported skills.
The user's supplied skill/package configuration is preserved.

Routine choices above follow the existing delegated engineering scope. Shared
opens are the user's explicit choice; all-time scope and the empty-history
fallback are implementation choices. Access control, contributor publishing,
deployment and automatic source updates remain deferred.

## Verification

Behavior tests cover persistence, ranking, refresh/removal, metadata filtering,
unified rendering, independent clear actions, and successful web-only counting.
Browser verification covers real search, filters, shelves, fallback/popularity,
native navigation, no-JS operation, keyboard/touch, reduced motion, focus,
contrast, and containment across desktop/tablet/phone widths. Use a separate
database for browser QA so generated visits do not affect the user's local counts.
