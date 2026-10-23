# Local implementation verification

The current default is the **dark NVIDIA theme**: #111 canvas, #1a1a1a panels, light text and #76B900 accents. The light variant was rejected; current screenshots and runtime evidence show dark mode.

Brand correction: the running application now identifies as **NVIS - OVA** and
uses the exact NVIDIA reference palette. The reference became reachable over
HTTP; see [palette evidence](brand-color-reference.md). Screenshots linked below
have been recaptured with the corrected branding and colors.

Verified 2026-10-22 on macOS, Python 3.12.15 and Chromium 151.0.7922.34.
The application is a functional local prototype. No remote was created or pushed,
and no production deployment was performed.

## Repeatable startup

From the project root:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
./scripts/seed.sh
./scripts/dev.sh
```

Open http://127.0.0.1:8000. The environment, registrations, publications and server
were exercised in this session. Startup serves the persistent `data/hub.sqlite3`.
The supplied seed command intentionally imports verified local snapshots so it
also works without private-source network access. Refreshing a snapshot does not
fetch the latest branch.

## Real sources

- Cluster Bringup: 85 pages, curated navigation, revision
  `f74950acdc451f43f8857754efad25ce5233d26c`.
- Documentation Pipeline: seven pages, generated navigation, revision
  `0796f0212ccac88391765271f88f9aed6606f68a`, ref `feat/copier-docs-pipeline`.
- All 96 captured source files match their recorded SHA-256 digests. The hub also
  validates snapshots before import. Both publications have zero import notices.
- The actual live HTTPS importer succeeded for cluster-bringup. The live pipeline
  importer returned HTTP 404 without a configured token; this alone does not
  distinguish authorization masking from another endpoint failure. GitLab MCP
  independently verified the repository/ref and supplied the authentic snapshot.

See [source acquisition](source-recon.md) and [adapter evidence](adapters-verification.md).

## Automated and protocol checks

Final integrated run:

```bash
.venv/bin/pytest -q
.venv/bin/ruff check .
.venv/bin/ruff format --check src tests
.venv/bin/mypy src/nvis_hub
```

30 tests pass; lint, formatting and type checks pass. One upstream Starlette
TestClient deprecation warning remains. Tests exercise imports/scopes, metadata,
hosted nested links/assets, safe content and paths, snapshot integrity, title and
section ranking, filters, changes/deletions, failed-refresh retention, re-registration
provenance, malformed configuration, source errors and persistent restarts.
Regressions discovered during review were reproduced failing before their fixes.

The MCP integration uses the official SDK's real stdio subprocess client. It
discovers all three read-only tools, searches and retrieves authored sections with
exact provenance, observes changed/deleted content while connected, preserves a
failed publication, and reopens the saved database. The same client also read both
real publications; see [seed MCP output](mcp-seed-verification.json).

The web process was stopped and restarted. Both project revisions, page counts
and publication timestamps remained identical. Evidence is in
[before](persistence-before-restart.json) and [after](persistence-after-restart.json).

Editable install and an isolated wheel install were exercised, including catalog,
CSS, JavaScript and bundled fonts. A Docker recipe and persistent volume instructions
are provided; no container runtime was exercised.

## Browser and design checks

The reusable [browser verification script](../scripts/browser_verify.cjs) passes
35 checks at 1440, 768 and 390 pixels using real served content. It checks search
submission, working project filters, matching section anchors, nested local links,
hosted SVG, copied commands, missing pages, no matches, page overflow, loaded fonts,
one main heading, mobile navigation/Escape, contents anchors and scrollable tables,
skip navigation and search keyboard focus. No page JavaScript errors occurred.

The presentation polish pass additionally reviewed every published reader and all
app page types at the three widths, fixed five shared layout/control defects, and
completed 276 final document renders. See [presentation evidence](presentation-polish.md)
for the exact visual coverage, interaction checks, and before/after captures.

A separate disposable served application passed nine additional browser checks
for empty collections, no matches, failed refresh retaining readable published
content and provenance, and horizontal scrolling of long code on a phone without
page overflow. Its server was stopped afterward; the main instance was preserved.
See [state evidence](state-browser-verification.md).

For a fresh browser-tools installation:

```bash
npm install --prefix .browser-tools playwright
.browser-tools/node_modules/.bin/playwright install chromium
NODE_PATH="$PWD/.browser-tools/node_modules" node scripts/browser_verify.cjs
```

The app does not require Node to run. Browser check details and runtime hover
colors are in [browser-verification.json](browser-verification.json).

Tasteskill's browser inspector reports no findings for catalog, filtered search
and reader at all three widths. Source lint has two justified warnings: monospace
is confined to literal code/identifiers; the shadow is confined to the mobile
navigation overlay. Impeccable's detector reported a static hover contrast warning;
the actual search-button hover uses white text on dark green and passes. The
independent visual reviewer confirmed this false positive.

Tasteskill direction: framed-sheet, seed `1837803909`, no redraws. The frame now uses neutral greys, black and white from the supplied NVIDIA theme,
with #76B900 on primary actions and #76B900 on readable links. Signature: the source-to-section
trail. Each screen's question is recorded in the [surface contract](../context/surface-hub.md).
No catalog entries or operational instructions were invented. All 101 imported
skill files still match their original hashes.

[DESIGN.md](../DESIGN.md) and the schema-v2 design sidecar record the finished
tokens, breakpoints, states and seven reusable component patterns. Frontmatter
color values were independently checked against the shipped CSS.

The independent [visual review](visual-review.md) required a visible phone table
scroll cue. The cue was added, its regression test and browser assertion pass, and
the reviewer scored the fix resolved with `disposition: ship` at that scope.
[Independent code findings](core-web-review.md) were also addressed: title-only
search pollution, missing local source links, a help path, and active-versus-pending
source provenance. No known material finding from these reviews remains open.

Representative screenshots:

- [Desktop catalog](../.impeccable/review/desktop.png)
- [Phone catalog](../.impeccable/review/mobile.png)
- [Search and filters](../.impeccable/review/desktop-search-fold.png)
- [Desktop reader](../.impeccable/review/desktop-reader-fold.png)
- [Phone reader](../.impeccable/review/mobile-reader-fold.png)
- [Hosted source diagram](../.impeccable/review/desktop-image-reader-fold.png)

## Boundaries

Reader SSO/NVIS membership enforcement and the contributor publishing skill remain
deferred. The integration contract exists; the publishing skill does not. Keep the
local application on loopback. Hosting, capacity, backups, broader access and
production deployment remain future work. The original color-reference URL is now
reachable over HTTP; its NVIDIA theme supplies the current brand colors directly.
