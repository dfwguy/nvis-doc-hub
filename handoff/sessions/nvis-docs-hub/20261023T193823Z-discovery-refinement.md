# Discovery refinement and appearance checkpoint

Checkpoint: 2026-10-23 19:38:23 UTC. This accompanies the finished `development`
refinement; use Git tracking and the linked final evidence for publication state.

## User checkpoint and branch state

Before any refinement UI edit, `4682c9d` was confirmed pushed to
`origin/development`, with a clean worktree and zero ahead/behind commits. This
satisfied the user's explicit instruction to save and verify the prior state
before changing the UI.

Work remains in `/Users/dgayle/Desktop/NVIS/AI Software Factory/nvis-docs-hub`.
The sole remote is `nvis-ova/nvis-doc-hub`, using
`ssh://git@gitlab-master.nvidia.com:12051/nvis-ova/nvis-doc-hub.git`. `main`
retains the verified baseline; refinement, discovery, live search and reader
categories belong on `development`. Preserve Git history and follow the README's
Git LFS setup when cloning.

## Current result

Default `/` and `/search` have one Explore popular documentation region, capped
at six genuinely opened documents ranked by aggregate all-time opens, including
repeats. Zero history shows No popular documentation yet. The user's latest
clarification retains one popular carousel while removing the extra project/type
collections and alphabetic substitute. It uses keyboard/touch scrolling, 44px
previous/next controls and 88% phone cards. The global Projects sidebar list is
removed: Project dropdown chooses projects; project/reader routes retain only
the current project's categories under Document sections, without source-project
names or a project switcher in the sidebar.
Selecting Project opens that project's vertical document library, 30 per page;
Browse documents opens the full library. Search still ranks authored sections;
filter/query independence, URLs, pagination, SQL and API contracts are preserved.

Display formatting capitalizes only an initial lowercase prose letter, retaining
technical tokens, acronyms, paths and commands including `dpkg`, `grep`, `npm`
and `apt`. Reader HTML formatting touches only initial plain-text heading nodes.
Stored HTML/Markdown, body prose, code/preformatted regions, API/CLI/MCP content,
heading IDs and links remain unchanged. Topic labels are formatted independently
of Document type labels. Do not apply global title case or CSS capitalization.

The native KUI-guided Dark mode switch changes appearance immediately, uses
stable switch semantics and keyboard operation, and saves `nvis-hub-theme` in
localStorage. Missing, invalid or blocked storage defaults to dark; blocked
storage still allows page-local changes. The head script applies preference
before styles. No JavaScript leaves the default dark interface usable. Light
mode uses white/pale surfaces, dark text and Deep Green readable links/focus;
source images/diagrams are not inverted. Native semantic CSS fallbacks preserve
the existing Python/FastAPI/Jinja frontend, with no React or new dependencies.

Preserve the NVIDIA identity, 44px controls, visible focus, reduced-motion
behavior, active reader category, live suggestions and contained code/table
scrolling. The topbar-based mobile overlay accounts for the theme switch and
available header width, including the narrow 320px layout.

## Content and runtime

- Cluster Bringup: 85 pages at `f74950acdc451f43f8857754efad25ce5233d26c`.
- Documentation Pipeline: 7 pages at
  `0796f0212ccac88391765271f88f9aed6606f68a`, ref `feat/copier-docs-pipeline`.
- Source snapshots, classifications and original hashes remain unchanged.
  Existing registrations use verified snapshots; refresh does not fetch a live
  branch. Original imported packages and supplied KUI/package files are preserved.
- The main app is healthy on loopback port 8000 after restart. Browser QA uses
  isolated port-8001 data so generated reader opens do not affect its counters.
  Aggregate popularity stores project/path/count without identities or profiles;
  retrieval through API/CLI/MCP remains side-effect-free.

## Verification and next-session entry

The corrected refinement passes 145 Python tests, Ruff lint, formatting
(19 Python files), mypy (11 source modules) and diff checks. All 23 focused
browser checks pass for the single popular carousel, local-only document
navigation, scoped views, honest zero history, display casing, preference persistence,
Enter/Space, blocked storage, no-JavaScript fallback, reduced motion, focus,
contrast and menu containment in dark/light at 1440, 1280, 768, 390 and 320 pixels.
Corrected existing/live-search/category regressions pass 35/28/34 checks, for
120 browser checks total. Dark desktop carousel and light phone captures were
reviewed with no material issue.
The 49-test presentation suite passed. The corrected inspector has zero findings;
detector advisories and
the known static hover false positive are documented in the aggregate report,
with actual runtime contrast passing.
Independent focus/command/Topic-label findings and browser menu findings are
resolved. One upstream Starlette TestClient deprecation warning remains.

Read [complete refinement verification](../../../evidence/discovery-refinement-verification.md),
[code review](../../../evidence/discovery-refinement-code-review.md),
[browser results](../../../evidence/discovery-simplification-browser.json),
[theme implementation and KUI references](../../../evidence/theme-implementation.md),
[implementation plan](../../../docs/superpowers/plans/2026-10-23-discovery-refinement.md),
[general verification](../../../evidence/verification.md), and
[README setup](../../../README.md). Use the final aggregate report for full Python,
lint/type and regression-suite results, and Git tracking for remote synchronization.

The [earlier discovery checkpoint](20261023T190834Z-document-discovery.md),
[category checkpoint](20261023T183032Z-collapsible-navigation.md) and original
[implemented checkpoint](20261022T223459Z-implemented.md) retain historical proof.
The multiple-shelf presentation described there is superseded by this
popular-only refinement; its single carousel is retained. Do not recreate the app or reset its database.

Historical intermediate proof: before the retained-carousel/sidebar clarification,
the grid iteration passed 144 Python tests and 120 browser checks. The current
145-test/120-check results above verify the user's corrected presentation.

## Boundaries

Reader SSO/NVIS membership enforcement, contributor publishing automation,
automatic source synchronization, remote HTTP MCP, hosting, capacity/backups
and production deployment remain deferred. Git publication is separate from
the deferred contributor workflow. Preserve sibling projects, notes, source
packages and the user's existing files; keep settled discovery decisions intact.
