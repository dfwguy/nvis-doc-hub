# Unified Documentation Discovery Implementation Plan

> **For agentic workers:** Use the established parallel implementation workflow;
> root integrates and reviews changes. Preserve other workers' edits.

**Goal:** One searchable, filterable documentation library with real popular
document shelves, following KUI guidance in the existing Python application.

**Architecture:** Add isolated aggregate counters and lightweight browse/ranking
queries to Store/Hub. Share one Jinja discovery surface between both existing
entry routes; progressively enhance native forms and shelf controls.

**Tech stack:** Python 3.12, FastAPI, Jinja, SQLite FTS5, native HTML/CSS/JavaScript.

**Spec:** ../specs/2026-10-23-document-discovery-design.md

## Global constraints

- Preserve dark NVIDIA colors, NVIS - OVA identity, and existing reader categories.
- No React migration, package installation, fabricated content, or personal data.
- Preserve the user's pending KUI skill/package configuration and 101 imported files.
- Existing API, CLI and MCP retrieval/search remain compatible.
- Publish feature work to development only; deferred product scope stays deferred.

## Review focus

- Empty popularity history: honest discovery shelf, never invented rankings.
- Missing/removed docs and refreshes: counters persist, unavailable pages never rank.
- Empty query plus filters: browse real documents, independently clear query/filters.
- Long names and short viewports: contained cards, usable filters and shelf controls.
- No JS / reduced motion: native navigation and forms work; no autoplay.

## Tasks

- [x] Backend worker: add red behavior tests in tests/test_discovery.py; implement
  Store/Hub record_document_view, popular_documents, browse_documents and
  document_count in store.py/service.py; verify persistence and existing contracts.
- [x] Root: red rendering/interaction tests in tests/test_web.py; unify web.py
  discovery handlers and catalog.html; replace duplicate navigation labels;
  add semantic-token CSS adapter and native card/filter/shelf markup. Hook only
  successful web reader opens into the counter. Enhance controls in discovery.js.
- [x] Browser worker: red-to-green discovery_verify.cjs; update only superseded
  assertions in existing verification scripts. Use copied SQLite DB on port8001.
  Check keyboard, touch, no-JS, filter URLs, real opens, responsive containment.
- [x] Review final diff independently; run Python suite, lint, formatting, mypy,
  browser regressions, and finished UI design scan. Record KUI adaptation and
  limitations and update design/checkpoint docs.
- [ ] Commit/push the verified feature on development and confirm Git tracking state.

## Completion checkpoint — 23 October 2026

Backend and frontend implementation are complete on `development`. The accepted
native KUI adaptation, real shared all-time opens, honest empty-history and
project shelf fallbacks, conditional metadata filters, independent clear actions
and URL-preserved library/search flows are implemented. Source metadata and the
85 + 7 published documents remain unchanged. User-supplied KUI/package settings
and imported files are preserved; no dependency install or React migration was
performed.

The final Python suite passes 94 tests; Ruff lint, formatting (17 Python files),
mypy (10 source modules) and diff checks pass. Existing browser/category/live-search
regressions pass 35/34/28 checks on the isolated QA instance. Discovery's portable
suite passes all 16 checks; its final rerun and final quality-check results are recorded
in [complete verification](../../../evidence/discovery-verification.md) and
[browser evidence](../../../evidence/discovery-browser-review.json). The two
actual phone findings—hidden Browse documents and collapsing shelf cards—are
corrected and independently verified. Review, design/use records and the current
checkpoint are updated. Keep publication on `development` and confirm the actual
Git tracking state when closing that task.

See [KUI guidance](../../../evidence/discovery-kui-guidance.md),
[independent code review](../../../evidence/discovery-code-review.md), and the
[current checkpoint](../../../handoff/sessions/nvis-docs-hub/20261023T190834Z-document-discovery.md).
