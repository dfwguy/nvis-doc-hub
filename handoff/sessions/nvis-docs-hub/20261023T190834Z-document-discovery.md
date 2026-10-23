# Unified document discovery checkpoint

Checkpoint: 2026-10-23 19:08:34 UTC. This records the finished feature on
`development`; use Git's tracking status and the linked final verification for
commit and remote synchronization state.

## Current result

Work remains in `/Users/dgayle/Desktop/NVIS/AI Software Factory/nvis-docs-hub`.
The singular remote is `nvis-ova/nvis-doc-hub`, using
`ssh://git@gitlab-master.nvidia.com:12051/nvis-ova/nvis-doc-hub.git`. `main`
retains the verified application baseline; discovery, live search and the native
reader categories belong on `development`. Do not reinitialize or force-push.

One Browse documentation navigation destination replaces All documentation and
Global search. `/` and `/search` render the same native discovery template.
Browse documents opens all actual documents alphabetically with 30 per page;
a text query ranks matching authored sections. Query, project/topic/type scope
and pagination remain in URLs. Clear search retains filters, Clear filters keeps
the query, and chips remove individual constraints.

Home shelves contain native document links with project, title, explicit type
or an honest Documentation label, and authored path. Popular documents ranks
real aggregate all-time opens, including repeats; an unused hub shows Explore
documentation. Typed How-to/Reference shelves appear only with actual metadata.
Remaining slots, up to three total shelves, use From {project title} documents
and project-filtered View all links. The authentic publications currently have
no topic/type facets: those controls remain hidden unless an active URL value
needs to stay visible, labelled unavailable and removable. Source paths/prose
and presentation categories do not invent stored types.

An additive SQLite table stores only project/path/open count. Successful browser
reader requests record an open after HTML rendering. Failed renders, HEAD,
search and API/CLI/MCP retrieval do not count. Counts survive refresh and restart;
rankings join current publications and exclude removed documents. There are no
user identities, cookies, profiles or personalized recommendations. Browser QA
uses an isolated database on port 8001, preserving the main instance's counts.

## KUI and preserved design

The supplied KUI browse/search/filter/card/carousel guidance was read and applied
to Python/FastAPI/Jinja, native HTML controls, semantic CSS variables with
settled-theme fallbacks, and small progressive enhancements. These are not KUI
React components. React/shared KUI CSS is not installed; no npm install or frontend
migration was performed. The user's pending KUI/package configuration is preserved,
including all 121 supplied KUI files; the 101 original imported skill files retain
their hashes.

Preserve the dark NVIDIA theme, NVIS - OVA identity and sidebar-bottom
documentation label. Retain keyboard/no-JavaScript forms and links, live section
suggestions, collapsible reader categories with the active category open, and
the earlier responsive reading fixes. Phone shelf cards use 88% tracks, not
shrinkable zero-minimum tracks. There is no autoplay; enhanced scrolling respects
reduced motion.

## Actual content

- Cluster Bringup: 85 pages, curated navigation, revision
  `f74950acdc451f43f8857754efad25ce5233d26c`.
- Documentation Pipeline: 7 pages, generated navigation, revision
  `0796f0212ccac88391765271f88f9aed6606f68a`, ref `feat/copier-docs-pipeline`.
- All 96 original snapshot files retain their hashes. No source snapshot was
  refreshed, edited or added to populate shelves or facets. Both registrations
  still use verified snapshots; refreshing them does not fetch a live branch.

## Verification and next-session entry

The final Python suite passes 94 tests; Ruff lint, formatting (17 Python files),
mypy (10 source modules) and diff checks pass. Existing browser, category and live-search
regressions pass 35, 34 and 28 checks. Discovery's portable suite passes all 16
checks in its final rerun. Independent review
found the hidden phone Browse documents action; browser QA found shrinking phone
shelf cards. Both fixes are independently verified, with no unresolved material
code defect. One upstream Starlette TestClient deprecation warning remains.

Read [complete discovery verification](../../../evidence/discovery-verification.md),
[browser results](../../../evidence/discovery-browser-review.json),
[code review](../../../evidence/discovery-code-review.md),
[KUI adaptation](../../../evidence/discovery-kui-guidance.md),
[KUI skill](../../../.agents/skills/kaizen-ui/SKILL.md),
[implementation plan](../../../docs/superpowers/plans/2026-10-23-document-discovery.md),
[general verification](../../../evidence/verification.md), and
[README startup/Git LFS setup](../../../README.md).
The portable discovery script is `scripts/discovery_verify.cjs`; keep browser
reader QA on an isolated database because opens intentionally affect popularity.

Preserve the earlier [category checkpoint](20261023T183032Z-collapsible-navigation.md),
[implemented checkpoint](20261022T223459Z-implemented.md), and historical resume
prompt in [latest](latest.md). Do not recreate the application or reset its data.

## Boundaries

Reader SSO/NVIS membership enforcement, contributor publishing automation,
automatic source synchronization, remote HTTP MCP, production hosting,
capacity/backups and deployment remain deferred. Git publication of the feature
is separate from the deferred contributor publishing workflow. Preserve sibling
projects, notes, source packages and the user's pre-existing pending files. Do
not restart settled discovery or treat rejected earlier proposals as policy.
