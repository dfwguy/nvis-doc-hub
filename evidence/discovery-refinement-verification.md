# Discovery refinement and theme verification

Before edits, the existing checkpoint `4682c9d` was confirmed committed and pushed
to `origin/development`, with a clean working tree and zero commits ahead/behind,
as requested by the user.

## Final behavior

The default Browse documentation view has one **Explore popular documentation**
carousel containing up to six genuinely opened documents. The two extra
project/type rows are removed. A cold hub keeps the same section title and shows
an honest empty-history message instead of labeling unopened pages popular.
The carousel retains native buttons, keyboard and touch scrolling, visible focus,
reduced-motion handling, and no autoplay.

The global Projects directory is removed from both desktop and mobile navigation.
Project selection uses the dropdown. Project and reader pages show only their
current **Document sections**, retaining the authored collapsible categories and
active-page state. Selected-project and complete-library results remain vertical,
alphabetical, and paginated at 30 documents. Search, live suggestions, filter
state, and independent clear actions are preserved.

Displayed document titles, navigation, search labels and plain heading starts use
consistent initial sentence case. Commands, identifiers, paths and acronyms are
preserved; the conservative formatter does not claim to classify every possible
command. Stored Markdown/HTML, API/CLI/MCP source content, link destinations,
heading IDs and code samples remain unchanged. Type labels do not rename topics.

The header has a native accessible **Dark mode** switch following KUI guidance.
Dark is the default; light mode applies immediately and persists per browser in
`nvis-hub-theme`. The preference applies before styles paint. Storage failures
are tolerated; the switch is hidden without JavaScript. Light mode uses semantic
surface/text/border tokens and readable green links while preserving NVIDIA
action colors. This remains a Python/Jinja interface without a React migration.

## Verification

- **145 Python tests pass**. Ruff lint and formatting pass for 19 Python files;
  mypy reports no issues in 11 source modules; diff checks pass. The existing
  upstream Starlette/httpx warning remains.
- **120 corrected browser checks pass**: focused refinement 23,
  catalog/search/reader 35, live search 28, and collapsible navigation 34.
- Both themes cover discovery, search, and reader layouts at 1440, 1280, 768,
  390, and 320px, including open-menu and header bounds, keyboard/focus,
  preference persistence, storage failure, native touch, no-JS use, filters,
  true aggregate popularity, and active-project-only navigation.
- Sampled text contrast is at least 6.11:1 dark and 6.42:1 light. Header focus
  contrast is 8.71:1 dark and 10.65:1 light. Light code, links, and controls were
  independently checked as well.
- Fixed and rechecked actual defects: light topbar focus contrast, mobile menu
  anchoring and narrow-width inherited minimum, missing command-preservation
  cases, and unintended type-label mapping of topics. No unresolved material
  review finding remains.
- QA uses a separate copied SQLite database/server on port 8001. Historical
  zero-history evidence was retained without clearing or fabricating counters;
  automated reader visits do not affect the user's main database.
- The main app is healthy on port 8000 with 92 published documents. All 101
  original imported skill files and 96 snapshot files retain their hashes;
  the supplied KUI package remains unchanged.

See [browser verification](discovery-simplification-browser.md),
[browser results](discovery-simplification-browser.json),
[independent review](discovery-refinement-code-review.md), and
[theme implementation](theme-implementation.md). Prior grid results in the browser
artifact are explicitly historical; the final user-approved correction retains
one carousel.

[Tasteskill's corrected browser inspection](taste-refinement.json) has no findings.
The [design scan](refinement-impeccable-detect.json) recorded 25 advisory
type/palette metadata findings and the known static hover-contrast false positive.
Its theme tokens are unchanged by the final carousel/sidebar correction; actual
corrected runtime contrast passes in both modes.

Access control, publishing automation, production deployment, automatic source
updates and remote HTTP MCP remain deferred. Main retains the baseline; this
refinement belongs on development.

Feature commit `e6c961b` was pushed to `origin/development`, with a clean tree and
zero commits ahead/behind after publication. The isolated QA server was stopped
and its owned temporary database removed; the user app remains on port8000.
