# NVIS - OVA documentation hub

Browse, read, and search authored project documentation in one local hub. The web
reader and MCP server share the same SQLite publications and section search.
Source repositories remain authoritative; registration and refresh are explicit.

Requires Python 3.12 or newer with SQLite FTS5. From this directory:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
./scripts/seed.sh
./scripts/dev.sh
```

Open <http://127.0.0.1:8000>. `seed.sh` registers every checked-in `sources/*.json`
and refreshes them. Inspect [source evidence](evidence/source-recon.md)
for the authentic seeds, exact revisions, and whether acquisition was live or
snapshot-based. A failed refresh preserves the last successful publication.

```bash
.venv/bin/nvis-hub list
.venv/bin/nvis-hub register sources/project.json
.venv/bin/nvis-hub refresh project-slug
.venv/bin/nvis-hub mcp
```

Set `NVIS_HUB_DB` to an absolute path to share another database between the web,
CLI, and MCP processes. The default is `data/hub.sqlite3`, relative to the current
directory. No source credential or user-facing access control is built into the
website. Keep this prototype on loopback; GitLab credentials used for source
acquisition are separate from [deferred SSO](docs/deferred-access-control.md).

```bash
.venv/bin/python -m pytest
.venv/bin/ruff check .
.venv/bin/mypy src/nvis_hub
.venv/bin/python scripts/verify_mcp.py --query bringup
```

The test suite uses disposable local sources and a real SDK stdio MCP client.
It does not prove live GitLab connectivity. Review [verification evidence](evidence/progress.md)
for the implementation ledger, or [final verification](evidence/verification.md)
for observed checks, screenshots, and remaining limitations.

Read the [quickstart](docs/tutorials/quickstart.md),
[registration and refresh guide](docs/how-to/register-and-refresh.md),
[configuration reference](docs/reference/configuration.md),
[content support](docs/reference/content-support.md),
[MCP reference](docs/reference/mcp.md),
[architecture](docs/explanation/architecture.md), and
[future publishing contract](docs/reference/integration.md).

## Development branches

The private GitLab repository is `nvis-ova/nvis-docs-hub`. `main` holds the verified
baseline; `development` is the shared branch for testing changes before merging
them into `main`. Keep changes on `development` or a feature branch and run the
checks above before opening a merge request to `main`.

Local environments, runtime databases, logs, caches, and bulk browser captures
are excluded from Git. Source snapshots, imported skills, design context, tests,
verification reports, and representative review captures are versioned. A fresh
clone can recreate the local publications with `./scripts/seed.sh` after setup.
