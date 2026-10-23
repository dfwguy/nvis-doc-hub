# Collapsible navigation independent code review

Reviewed 2026-10-23 on local `development` before commit.

No unresolved material defects found after the source-context correction.

## Scope

- Read the accepted specification, implementation plan, and exact-source TOC
  inspection evidence.
- Reviewed `navigation.py`, `content.py`, the shared and project templates,
  `web.py`, category CSS, and both new navigation test modules.
- Checked explicit classification authority, authored order and context,
  document coverage, native disclosure controls and active state, strict YAML
  path resolution, data-only parsing, bounded malformed input, and fallback
  notices. Browser interaction and visual verification belong to the separate
  browser review.

## Finding and follow-up

Found one source-context preservation defect in the initial grouping helper:
recognized custom captions such as `Reference — API contracts` and
`Reference — Protocol grammar` were both replaced by the canonical group title
and discarded from their entries. A focused helper invocation reproduced the
loss. The root implementer agreed to preserve these custom captions as entry
context while retaining the four canonical category headings. Re-read the
correction and the two-caption regression test; distinct source captions now
survive as entry context, while the canonical template captions remain
unrepeated.

## Verification

- `.venv/bin/python -m pytest -q tests/test_navigation.py
  tests/test_navigation_source.py`: 38 passed.
- Re-ran the full suite after the caption correction:
  `.venv/bin/python -m pytest -q`: 83 passed. The only warning was the existing
  FastAPI/Starlette `TestClient` deprecation.
- Six additional malformed YAML cases (unhashable keys, null subtree entries,
  binary titles, infinite numeric roots, overwritten unavailable roots, and
  set-shaped subtree data) fell back to generated navigation with notices.
- The new YAML parser rejects alias events before mapping construction and
  bounds input bytes, parse events, and collection depth. It uses `SafeLoader`,
  validates the supported schema, resolves only published relative document
  paths, and never executes repository configuration.
- Existing RST navigation parsing remains in place; explicit `diataxis`
  metadata is added below the established registration/type/kind precedence.
