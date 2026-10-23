# Collapsible navigation implementation

1. Independently add red-to-green source parsing tests and support for the
   reference YAML TOC plus explicit diataxis metadata, preserving the existing
   flat navigation contract and RST behavior.
2. Root owns a pure presentation grouping helper and its behavior tests. Reuse
   authored labels/metadata, preserve context/order/depth, append uncategorized
   published documents, and mark the active group without mutating source data.
3. Root renders native, shared collapsible groups in project lists and both
   navigation variants, with existing palette/type, counts, and clear hit areas.
4. Independently exercise browser behavior and visual layout; run Python checks,
   existing browser suites, and one design detector pass for the finished UI.
   Resolve findings, update authoring/design/checkpoint records, and commit/push
   only development. Main remains the baseline.

## Completion checkpoint — 23 October 2026

Steps 1–3 are complete. Source parsing preserves the flat navigation contract and
RST behavior while adding explicit `diataxis` metadata and registered YAML TOCs.
Shared native disclosures preserve published pages, authored order, nested levels
and source context in project indexes and desktop/mobile navigation. Readers
open their current category; empty categories are omitted and unknown modes use
Other documentation.

Step 4 implementation and independent review are complete: 83 Python tests pass;
the category browser suite passes 34 checks and confirms all 92 published URLs.
Final Ruff lint/formatting, mypy and diff checks pass; fresh existing-browser and
live-search reruns pass 35 and 28 checks respectively in visible Chromium
151.0.7922.34.
The custom-caption context defect found during code review is corrected with a
regression test. Browser checks cover keyboard and JavaScript-disabled operation,
active groups, responsive layouts and scoped search. Authoring/use documentation
and the current checkpoint are updated. See
[browser verification](../../../evidence/collapsible-navigation-browser.md) and
[code review](../../../evidence/collapsible-navigation-code-review.md).

The finished UI received one design detector pass, with known metadata
advisories and the static hover false positive documented alongside actual
passing browser contrast measurements in the
[aggregate verification](../../../evidence/collapsible-navigation-verification.md).
All 101 imported skill files and 96 source snapshot files retain their hashes.
This checkpoint accompanies the finished `development` change. Main keeps the
application baseline; the 85 + 7 authentic published pages and deferred
access/publishing automation scope remain unchanged.
