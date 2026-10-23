# Discovery refinement and theme choice

The user requested a simpler default for a large documentation collection:
one Explore popular documentation section, no extra per-project collections,
consistent display-title casing, and a light/dark toggle. The latest explicit
clarification retains the single popular carousel and removes the global Projects
sidebar list. Project dropdown is the project selector; project/reader routes
retain only local Document sections category navigation, without source-project
names or a project switcher in the sidebar.

Before any UI edit, checkpoint `4682c9d` was confirmed on `origin/development`,
with a clean worktree and zero commits ahead/behind, as explicitly requested.

- [x] Root: one bounded popular carousel, honest empty-history state and
  project-selected vertical paginated browsing. Remove extra project/type rows
  and the global Projects sidebar list; retain current-project category navigation.
- [x] Title worker: pure conservative presentation formatter with behavior tests;
  root applies to labels/cards/navigation/search without editing source content.
- [x] Theme worker: KUI-guided native accessible switch, persisted theme, default
  dark, semantic light tokens and readable surfaces, no React migration.
- [x] Browser worker: isolated SQLite QA for default/scoped views, carousel,
  local-only project navigation, casing and both theme states/persistence/
  keyboard/contrast at320–1440px.
- [x] Review/check implementation, update current design/use records and session
  checkpoint.
- [ ] Commit/push the verified refinement on development and confirm Git tracking state.

Keep API/CLI/MCP content and paths unchanged, preserve authentic snapshots and
all imported skill packages, and retain existing deferred scope. Display casing
capitalizes an initial prose letter while preserving commands/acronyms/paths;
authored Markdown headings/body remain source-faithful. Read KUI browse,
layout, card, navigation, search/filter, Switch/settings, and token references.

## Completion checkpoint — 23 October 2026

The corrected popular carousel, project-selected vertical library, local-only
Document sections navigation, conservative display formatter and native persisted
theme switch are implemented and reviewed. All 145 Python tests and 120 browser
checks (23 focused + 35 existing + 28 live-search + 34 category) pass, with Ruff
lint, formatting (19 Python files), mypy (11 source modules) and diff checks
passing. Corrected dark desktop carousel and light phone captures are clean.
Independent findings for light focus contrast,
command names and Topic-kind labels are fixed, as are the browser's narrow-menu
containment findings. Source/API/anchor preservation and QA-counter isolation
are verified. There is no React migration or dependency installation.

The corrected inspector reports zero findings; the detector's advisory/static-warning
disposition and integrated checks are recorded in
[refinement verification](../../../evidence/discovery-refinement-verification.md).
See [independent code review](../../../evidence/discovery-refinement-code-review.md),
[browser results](../../../evidence/discovery-simplification-browser.json),
[theme implementation](../../../evidence/theme-implementation.md), and the
[current checkpoint](../../../handoff/sessions/nvis-docs-hub/20261023T193823Z-discovery-refinement.md).
The pre-edit `4682c9d` publication/clean-worktree checkpoint is preserved above;
close final Git publication against its actual tracking state.
