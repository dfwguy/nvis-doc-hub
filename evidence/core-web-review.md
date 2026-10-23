# Independent core and web review

Reviewed the shared publication implementation and web adapter read-only on
2026-10-22 after the initial integrated 22-test pass. The reviewer implemented
the CLI/MCP adapters, not these modules. This review includes direct source
inspection of models, acquisition, parsing/rendering, persistence/search,
retrieval, routes, templates, and progressive browser enhancements.

## Findings at review time

**Important — page-title matches return unrelated sections.**
`src/nvis_hub/store.py` indexes the full document title in every section row.
Searching `two layers` against the authentic pipeline snapshot returns both
`Why the pipeline has two layers` and the unrelated `Sources and version selection`
section of `docs/explanation/design.md`. The latter's excerpt contains neither
search term. Page-title queries can therefore fill results with sections whose
content is irrelevant. Index document-title matching on the whole-page fallback
while preserving section-heading/body matches, or filter these duplicate title
hits. Verify a page-title query yields its useful page/section and excludes the
unrelated section. A change to publication indexing also requires refresh of
already-populated databases.

**Minor — absent local source links become `href="None"`.**
`src/nvis_hub/templates/reader.html` renders source links unconditionally.
Non-Git local development publications intentionally carry a content digest and
`source_url=None`, so their reader shows a broken `None` URL and `View in GitLab`.
Render the path/digest as text when there is no source URL.

**Minor — help refers to a nonexistent how-to path.**
`src/nvis_hub/templates/help.html` refers to `docs/how-to/sources.md`; the delivered
guide is `docs/how-to/register-and-refresh.md`.

**Important — updated registration mislabels a preserved publication.**
`Store.projects()` combines current registration source metadata with the last
successful publication revision. A disposable reproduction published the
authentic pipeline snapshot, re-registered the slug with a different repository,
ref, and local mode, and failed refresh using a nonexistent local directory. The
project then advertised the new repository/ref/mode with revision `0796f021…`,
while its documents retained the original snapshot mode and pipeline source URL.
Pin source mode, repository URL, and ref to each successful publication; expose
pending acquisition configuration separately. Preserve the original source
metadata before overwriting an older registration if its publication predates
those pinned metadata fields.

These findings were sent to the owning implementer. Subsequent fixes and
verification are recorded by that implementer; this file preserves the observed
review results rather than claiming an unobserved final state.

## Verified strengths and scope

The publication transaction replaces documents, assets, sections, and FTS rows
together. Failed acquisition/parsing preserves the working publication. Search
uses parameters and literal extracted terms. Scope handling rejects traversal
and symlinks; source acquisition blocks redirects when sending credentials.
Markdown raw HTML is escaped and rendered HTML sanitized; SVG content is
sanitized and assets carry a restrictive sandbox CSP. Reader responses exclude
local source directories and credential environment names. Private token values
are read from environment rather than stored in registration JSON.

No critical defect was identified in this pass. Reader authentication, SSO,
production hosting, and automatic publishing were explicitly deferred by the
brief, so their absence is not a defect in this local prototype. The Docker image
was not runtime-tested in this review. Browser visual/responsive validation is
owned by the parent implementation task.

Assessment at this review point: address the search relevance finding before
calling the local prototype complete.
