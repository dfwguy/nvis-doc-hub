# Collapsible documentation categories checkpoint

Checkpoint: 2026-10-23 18:30:32 UTC, accompanying the finished development change
after implementation, independent review, and final regression checks.

## Current result

Work remains in `/Users/dgayle/Desktop/NVIS/AI Software Factory/nvis-docs-hub` on
`development`. The existing singular remote is `nvis-ova/nvis-doc-hub`, using
`ssh://git@gitlab-master.nvidia.com:12051/nvis-ova/nvis-doc-hub.git`. Published
`main` retains the verified application baseline; live search and the new category
feature belong on `development`. Do not reinitialize or force-push the repository.

Project indexes and desktop/mobile navigation now share native `details/summary`
groups for Tutorials, How-to guides, Reference and Explanation, with Other
documentation for unclassified pages. Index groups start collapsed; reader routes
open the current document's category. Counts, authored order, nested entry levels,
source-topic context and all published links are preserved. Empty groups are
omitted. Keyboard operation and navigation without JavaScript work.

Classification follows explicit authored captions, curated navigation labels or
document metadata. Paths and arbitrary prose do not classify pages. Explicit
`diataxis` frontmatter supplements the existing registration/type/kind precedence.
Registered YAML TOCs support root pages, captioned subtrees, relative
extensionless files, optional titles and recursive entries. Parsing reads data
only, rejects aliases before construction, bounds input complexity, confines
targets to published repository paths, and reports generated fallbacks. Existing
RST navigation remains supported. The inspected `nvis-rack-status` reference was
not imported, and source snapshots were not edited.

## Published content and design

- Cluster Bringup: 85 pages, curated navigation, revision
  `f74950acdc451f43f8857754efad25ce5233d26c`.
- Documentation Pipeline: 7 pages, generated navigation, revision
  `0796f0212ccac88391765271f88f9aed6606f68a`, ref `feat/copier-docs-pipeline`.
- Both registrations use verified snapshots. Refreshing them does not fetch a
  live branch. No catalog source was added by the category feature.
- Preserve the dark NVIDIA theme: `#111` canvas, `#1a1a1a` panels, white/`#eee`
  text and `#76b900` accents, NVIS - OVA identity, and sidebar-bottom documentation
  label. Preserve live search and the earlier responsive reading fixes.

## Verification

The full Python suite passes 83 tests. The category browser suite passes 34 checks
at desktop, tablet and phone widths, verifies all 92 published URLs, and covers
both project indexes, desktop/mobile navigation, active groups, counts, keyboard
operation, JavaScript-disabled behavior, scoped search and overflow containment.
Independent code review found a custom-caption context loss; the correction and
regression test pass, with no unresolved material finding. The independent
browser/visual review found no material layout issue.

Read [feature verification](../../../evidence/collapsible-navigation-verification.md),
[verification](../../../evidence/verification.md),
[TOC source inspection](../../../evidence/toc-template-reference.md),
[category browser results](../../../evidence/collapsible-navigation-browser.md),
[code review](../../../evidence/collapsible-navigation-code-review.md), and the
[implementation plan](../../../docs/superpowers/plans/2026-10-23-collapsible-navigation.md).
The portable category check is `scripts/navigation_verify.cjs`.

Final Ruff lint, formatting (16 Python files), mypy (10 source modules) and diff
checks pass. Fresh existing-browser and live-search reruns pass 35 and 28 checks
respectively in visible Chromium 151.0.7922.34. The design scan and actual hover
contrast measurements are recorded in the feature verification. All 101 imported
skill files and 96 source snapshot files retain their original SHA-256 hashes.
Keep feature work on `development`; use Git's tracking status to confirm remote
synchronization before resuming. Main remains the baseline.
The existing repository setup and Git LFS instructions remain in
[repository setup](../../../evidence/repository-setup.md) and
[README](../../../README.md). One upstream Starlette TestClient deprecation
warning remains documented.

## Boundaries

Reader SSO/NVIS membership enforcement, the contributor publishing skill,
automatic synchronization, remote HTTP MCP, production hosting, capacity/backups
and deployment remain deferred. Repository Git publication is separate from the
deferred contributor publishing workflow. Preserve the sibling pipeline, notes,
source snapshots, imported skills and historical checkpoints. Do not repeat
settled discovery or recreate the application/database.

The earlier [implemented checkpoint](20261022T223459Z-implemented.md) and original
resume prompt in [latest](latest.md) remain historical context.
