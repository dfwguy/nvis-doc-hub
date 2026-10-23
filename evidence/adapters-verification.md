# CLI, package, and MCP verification

Observed on 2026-10-22 using Python 3.12.15 and the installed official MCP Python
SDK 1.30.0. All source checks used separate persistent databases so browser
verification could use the default database independently.

## Deterministic integration

Before implementation, `pytest tests/test_cli.py tests/test_mcp.py -q` produced
four failures for the missing CLI adapter. After implementation and shared-service
integration, the initial five tests passed in 3.95 seconds. A later regression
test exposed an unhandled SQLite path error, then passed after CLI error handling
was added; the adapter suite now passes all six tests in 3.83 seconds.

The CLI checks registration-relative source paths from another working directory,
environment/explicit database precedence, repeated `refresh --all`, restart
persistence, invalid registration without secret echo, missing-project errors,
and an unusable database path without a Python traceback.

The MCP check uses `mcp.ClientSession` and `mcp.client.stdio.stdio_client` to start
an actual Python subprocess. It verifies tool discovery/read-only annotations,
filtered section search, exact committed Git provenance, section retrieval,
missing-page errors, argument bounds, changed/deleted documents after refresh
while the server remains running, failed refresh preserving the working copy,
and a second MCP process reopening the saved database. Its source is a disposable
fixture, not evidence of private GitLab connectivity.

The integrated suite run at this point passed **22 tests in 7.63 seconds**, with
one upstream Starlette TestClient deprecation warning. Focused Ruff checks passed
for the CLI/MCP adapters, verification script, and tests. Mypy passed for both
adapter modules. The complete suite is rerun by the parent task after subsequent
core/web changes; this count records the integration state at this check.
The command help and both shell scripts' syntax were exercised.

## Authentic snapshot publications

```bash
NVIS_HUB_DB="$PWD/data/adapter-verify.sqlite3" ./scripts/seed.sh
NVIS_HUB_DB="$PWD/data/adapter-verify.sqlite3" .venv/bin/nvis-hub list
```

Both registrations published successfully with no refresh errors:

- `cluster-bringup`: 85 Markdown pages; curated navigation;
  `f74950acdc451f43f8857754efad25ce5233d26c`; acquisition recorded as `git`.
- `documentation-pipeline`: 7 Markdown pages; generated navigation;
  `0796f0212ccac88391765271f88f9aed6606f68a`; acquisition recorded as `gitlab-mcp`;
  selected ref `feat/copier-docs-pipeline`.

```bash
NVIS_HUB_DB="$PWD/data/adapter-verify.sqlite3" .venv/bin/python scripts/verify_mcp.py \
  --query Copier --project documentation-pipeline \
  --path docs/explanation/design.md --section sources-and-version-selection
```

The real stdio client discovered `list_projects`, `search_documents`, and
`get_document`, listed both projects, returned 18 `Copier` matches, and retrieved
the selected authored section. The result carried the exact pipeline revision,
repository-relative source path, publication time, and commit-specific GitLab
source URL. Snapshot refresh republishes the acquisition; it does not fetch the
latest branch.

## Live GitLab adapter

```bash
.venv/bin/nvis-hub --db data/adapter-live.sqlite3 register sources/live/cluster-bringup.json
.venv/bin/nvis-hub --db data/adapter-live.sqlite3 refresh cluster-bringup
```

The implemented HTTPS GitLab commit/archive acquisition succeeded for
`cluster-bringup`: 85 pages at
`f74950acdc451f43f8857754efad25ce5233d26c`, method `gitlab-https-archive`, curated
navigation, and no refresh error. This proves the real hub acquisition path for
that repository, independently of snapshot/fixture tests. No credential value
was displayed or stored in a registration.

The same implemented HTTPS adapter was then exercised separately against
`sources/live/documentation-pipeline.json`. Registration succeeded, but refresh
returned status 1 with the safe error `GitLab acquisition failed (HTTP 404); check
access and credential environment.` No Pipeline publication was installed in
this live-test database. The currently available process environment therefore
does not support this source through the hub's API path. A 404 response alone
does not distinguish a missing endpoint from masked private-source authorization;
MCP reconnaissance independently verified the repository and requested ref.
No authentication was configured or changed. The authentic Pipeline snapshot
remains the demonstrated acquisition path for its seven hosted pages.

## Packaging

Editable installation via `.venv/bin/python -m pip install -e '.[dev]'` completed.
`pip wheel --no-deps --wheel-dir /tmp/nvis-hub-wheels .` produced the package wheel.
Its archive contained the `nvis-hub` console entry point, all nine current HTML
templates, and all seven bundled static files including CSS, JavaScript, favicon,
and fonts. Installing that wheel with `--no-deps --target` in a disposable
directory, then importing it outside the source tree, returned HTTP 200 for the
catalog, stylesheet, JavaScript, and regular font through the ASGI test client.
The Docker recipe is provided with a
persistent `/data` volume and non-root process; a container runtime was not
exercised by these adapter checks.

The final integrated test command before adapter handoff passed **29 tests in
4.84 seconds**, with the same upstream TestClient deprecation warning. Focused
adapter/script/test Ruff checks and adapter mypy checks remained clean.
