# Implementation progress

23 October, discovery refinement: one Explore popular documentation carousel now
shows at most six documents ranked by actual shared all-time opens, including
repeats. Zero history shows an honest empty message. The default has no
alphabetical popularity substitute or extra project/type shelves. The user's
latest clarification retains the one popular carousel, including keyboard/touch
scrolling, 44px previous/next controls and 88% phone cards. The global Projects
sidebar list is removed; the Project dropdown chooses projects. Project/reader
routes retain local category navigation under Document sections, without a
source-project name list or project switcher in the sidebar.
Project selection opens the existing 30-per-page vertical document library;
search, filters, URLs, SQL and API/CLI/MCP retrieval retain their contracts.

Display formatting changes only an initial prose letter. Technical tokens,
acronyms, paths and commands such as `dpkg`, `grep`, `npm` and `apt` keep their
spelling. Reader formatting affects only an initial plain-text heading node;
stored HTML/Markdown, body prose, code, API content and anchors remain unchanged.
Topic labels retain their authored meaning separately from Document type labels.

A native KUI-guided Dark mode switch applies light/dark appearance immediately,
persists `nvis-hub-theme` locally, defaults to dark and remains usable when
storage is blocked. No JavaScript leaves the established dark surface usable.
Light surfaces use readable dark text and Deep Green links/focus. No React
migration or dependency install was performed.

The corrected implementation passes 145 Python tests, Ruff lint, formatting
(19 Python files), mypy (11 source modules) and diff checks. Its 23 focused
browser checks pass in both themes at 1440, 1280, 768, 390 and 320 pixels.
Corrected existing/live-search/category regressions pass 35/28/34 checks, for
120 browser checks total. Dark desktop carousel and light phone captures are clean.
The preceding review findings—light focus contrast, command casing and Topic-kind
label separation—and the narrow mobile menu issues are resolved. The corrected
Tasteskill inspector has zero findings; detector advisories and runtime contrast
disposition are recorded in
[refinement verification](discovery-refinement-verification.md), with
[code review](discovery-refinement-code-review.md),
[browser results](discovery-simplification-browser.json),
[theme implementation](theme-implementation.md), and the
[current checkpoint](../handoff/sessions/nvis-docs-hub/20261023T193823Z-discovery-refinement.md).

As explicitly requested, `4682c9d` was confirmed pushed to `origin/development`
and the worktree clean/zero ahead-behind before UI edits. This checkpoint
accompanies the finished `development` refinement; use Git tracking for current
remote synchronization. `main` remains the verified baseline. Main port 8000 is
healthy after restart; port-8001 QA uses isolated data and does not pollute its
opens. Authentic content remains 85 + 7 documents with source hashes unchanged.
Imported packages and deferred access/publishing/deployment scope are preserved.
Earlier entries below retain historical features and verification results.

23 October, unified document discovery: one Browse documentation destination
replaces the separate catalog/search choices. `/` and `/search` share a search,
filter and document-browse surface. Browse documents opens the complete
alphabetical library; a text query keeps ranked matching sections. Query and
filters clear independently and remain in shared URLs and pagination.

Home shelves link directly to documents. Popular documents uses real shared
all-time opens, including repeats; empty history uses Explore documentation.
Typed shelves require explicit metadata. The actual snapshots have empty
topic/type facets, so remaining slots, up to three shelves total, show real
From {project title} documents. Their View all links filter by project. Empty
metadata controls stay hidden unless their URL value is active, visible as
unavailable and removable. No source classification was inferred or changed.

An additive aggregate counter stores project/path/count without a user
identifier, cookie or profile. Successful browser reader rendering records an
open; API, CLI and MCP retrieval remain side-effect-free. Counts survive refresh
and restart while rankings exclude removed documents. Browser QA runs against an
isolated database on port 8001, preserving the user's main-instance counts.

The final Python suite passes 94 tests; Ruff lint, formatting (17 Python files),
mypy (10 source modules) and diff checks pass. Existing browser and category regressions pass
35 and 34 checks; the live-search regression passes all 28. Discovery's portable
suite passes all 16 checks in its final rerun.
Both real phone findings—hidden Browse documents and collapsing shelf cards—are
fixed and independently verified. KUI guidance is applied through native HTML,
CSS semantic-token fallbacks and progressive enhancement, with no React migration
or npm install. All 101 original skill files, 121 user-supplied KUI files and 96
source snapshot files retain their original hashes.

Read [complete discovery verification](discovery-verification.md),
[KUI guidance](discovery-kui-guidance.md),
[code review](discovery-code-review.md),
[browser evidence](discovery-browser-review.json), and the
[current checkpoint](../handoff/sessions/nvis-docs-hub/20261023T190834Z-document-discovery.md).
This checkpoint accompanies the finished `development` feature; Git's tracking
status gives the remote state. `main` retains the verified baseline, and actual
content remains 85 Cluster Bringup + 7 Documentation Pipeline pages. Reader access
control, contributor publishing automation, source synchronization and production
deployment remain deferred. Earlier entries below preserve their original
verification counts and publication-stage context.

23 October, collapsible categories: implementation and independent code/browser
review are complete on `development`. Project indexes and desktop/mobile trees
share native disclosure groups for Tutorials, How-to guides, Reference and
Explanation, with Other documentation for unclassified pages. Counts match
their links, empty groups are omitted, reader routes open the current category,
and authored order, nested levels and source context remain available.

Explicitly registered YAML TOCs now support root pages, captioned subtrees,
extensionless files relative to the TOC, title overrides and recursive entries.
Parsing is data only, bounded, and repository confined, with generated fallback
notices for unsupported input. Existing RST navigation remains supported;
explicit `diataxis` frontmatter supplements the existing metadata precedence.
The actual reference TOC was inspected without importing that project or changing
the two source snapshots.

The Python suite passes 83 tests. The category browser suite passes 34 checks,
including all 92 published URLs, both indexes/navigation variants, keyboard and
JavaScript-disabled behavior, active groups, search and responsive containment.
The review's custom-caption preservation defect is fixed with a regression test;
no material code or visual finding remains. See
[browser evidence](collapsible-navigation-browser.md),
[code review](collapsible-navigation-code-review.md), and the
[current checkpoint](../handoff/sessions/nvis-docs-hub/20261023T183032Z-collapsible-navigation.md).

Final Ruff lint/formatting, mypy and diff checks pass; fresh existing-browser and
live-search reruns pass 35 and 28 checks respectively in visible Chromium
151.0.7922.34. The finished change is recorded on `development`; use Git's
tracking status to confirm synchronization with the remote.
The singular `nvis-ova/nvis-doc-hub` remote already
exists; `main` retains the verified baseline and feature work stays on
`development`. The publications remain 85 Cluster Bringup + 7 Documentation
Pipeline pages. Reader access control, contributor publishing automation and
production deployment remain deferred. Earlier dated progress below records the
state before repository access and publication were completed.

23 October: live search is implemented on `development`. All three search surfaces
show clickable prefix-matched sections with project/filter scope, keyboard and
touch support, asynchronous request cancellation, and full-search fallback.
44 Python tests, 35 existing browser checks, and 28 new live-search checks pass;
independent code/visual review found no material issues. See
`live-search-verification.md`. Remote GitLab publishing remains deferred.

Latest user requirement: dark NVIDIA theme. All app surfaces/native controls now use dark mode, retaining NVIS - OVA identity and the sidebar-bottom documentation label. Final dark captures, contrast measurements and browser checks are recorded in the existing evidence files.

Presentation polish: corrected the initial Global Search panel inset, wrapped
result arrows, heading-code sizing, last-page Previous alignment, and Copy controls
during horizontal code scrolling. Every one of the 92 readers was checked at three
widths; 276 final renders and 35 reusable browser checks pass. Independent visual
reviews cover all reader arrivals and representative long-page interiors. See
`presentation-polish.md` for scoped coverage and evidence. Dark branding and source
content are preserved.

Plan: docs/superpowers/plans/2026-10-22-hub.md

- Context, checkpoint, manager notes, and both imported skill entrypoints read.
- Design and plan recorded. User explicitly delegated technical choices and asked
  for implementation without repeating the settled discovery interview.
- Ruling: use the existing dedicated new directory, which has no parent Git repo;
  no worktree or remote is needed for this local deliverable.
- Ruling: execute independent modules in parallel against service-contract.md;
  this follows the session's proactive delegation instruction. Integration and
  final review remain centralized.
- Ruling: code-first Read/Operate surfaces; preserve the pinned NVIDIA palette and
  task navigation over decorative concept challengers. No new style-choice interview.
- Preflight: all web/CLI/MCP tasks consume the same Hub methods and dict keys in
  docs/reference/service-contract.md. Core owns models/store/content/sources/service;
  root owns web/templates/static; CLI/MCP worker owns adapters/tests/scripts.

## Completed implementation

- Task 1 complete: persistent registrations and atomic publications, safe scoped
  acquisition, Markdown/SVG, original navigation, assets, section/page FTS and
  metadata filters. Authentic snapshots publish 85 + 7 pages with zero notices.
- Task 2 complete: responsive catalog, results, project tree, hosted reader,
  source status and error/empty states. Search/filter/navigation/source links are
  functional; code and wide tables scroll within the reading surface.
- Task 3 complete: installed CLI, official real stdio MCP, reusable startup and
  source registrations, Diátaxis docs, future publishing contract and container
  recipe. Actual live cluster import succeeds; live pipeline API returns 404.
- Task 4 verification: 30 tests pass; Ruff lint/formatting, mypy and pip check
  pass. 27 real-content browser checks plus nine disposable-state checks pass.
  Main process restart preserves publications exactly. Wheel installation serves
  templates, static files and fonts. All authored local doc links resolve.
- Independent code findings fixed with red→green evidence: unsafe SVG appearance
  loss, title-only search pollution, active/pending source provenance, missing
  local-source URL handling, safe CLI database errors, and an incorrect help path.
- Independent visual fix: visible horizontal-scroll cue on phones; reviewer
  scored it resolved with disposition ship at that scope. Singular page count
  corrected and recaptured in the separate browser-state instance.
- No deferred minor review finding remains in application scope. The one upstream
  Starlette TestClient warning and unexercised container runtime are documented
  limitations. SSO, contributor publishing skill and production deployment remain
  intentionally deferred as required.
- Original context and all 101 imported skill files preserved; original SHA-256
  checks pass. Sibling pipeline status remains only its pre-existing handoff.md.
- Full evidence: verification.md; review evidence: core-web-review.md and
  visual-review.md. Latest session entry now points to the implemented checkpoint.
- Task 4 complete: final token-bearing DESIGN.md and schema-v2
  .impeccable/design.json record seven actual component patterns. Independent
  parsing verified all eight canonical sections and that frontmatter colors match
  shipped CSS. Final code checks and main-instance health/count checks pass.

## User brand correction

- Corrected the app identity to NVIS - OVA throughout its shell, titles, help,
  command descriptions, MCP identity and product/design records.
- Reached the supplied reference over HTTP and verified its theme variables in a
  real browser. Replaced the olive palette with the reference's #76B900, #004831,
  black, white and neutral greys. Source documentation bytes remain unchanged.
- Reference and runtime evidence: brand-color-reference.md and
  brand-runtime-verification.json. Primary black-on-green contrast is 8.71:1;
  readable link green on white is 10.65:1. Hover/text contrast checks pass.
- Re-ran the 30-test suite, lint/format/type checks and the 27-check browser pass;
  refreshed desktop/tablet/phone captures. All three browser inspector views have
  no findings. Fresh brand-visual-review.md reports ship at the correction scope.
- Applied the user's follow-up: sidebar bottom label now reads NVIS - OVA
  Documentation, replacing the engineering tag. The desktop content footer no
  longer duplicates that label; narrow layouts retain it when the sidebar folds.
