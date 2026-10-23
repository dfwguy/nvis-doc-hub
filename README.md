# NVIS - OVA documentation hub

Browse, read, and search authored project documentation in one local hub. The web
reader and MCP server share the same SQLite publications and section search.
Source repositories remain authoritative; registration and refresh are explicit.

**Browse documentation** combines search, live suggestions, filters, and document
discovery. **Browse documents** opens the complete paginated library; an empty
query can browse documents using any available metadata filters. The existing
`/search` URL opens the same discovery experience.

The default page has one **Explore popular documentation** section: up to six
real documents ranked by aggregate all-time opens in this hub's database,
including repeat opens. One carousel supports buttons, keyboard, and touch,
without extra per-project collections. The global Projects sidebar list is removed;
only the current document sections appear while reading. Before usage exists, an honest empty state
points to search, the Project dropdown, and Browse documents. Project selection
opens a paginated vertical library. Counts survive source refreshes; removed
pages cannot rank. No reader identity or profile is stored, and separate
installations have separate counts.

The header's **Dark mode** switch applies immediately and remembers the browser's
choice. Dark remains the default; light mode uses accessible neutral surfaces and
NVIDIA action colors. Display titles use consistent sentence case while retaining
commands, paths, acronyms, and source contents.

The Python templates follow the supplied [Kaizen UI guidance](evidence/discovery-kui-guidance.md),
using documented patterns and semantic CSS tokens with the established dark-theme
fallbacks. The frontend has not been migrated to React. The supplied npm package
configuration remains pending installation; Python startup does not require npm.

After cloning, install [Git LFS](https://git-lfs.com/) with your platform's package
manager or its installer, then run these commands from the repository root:

```bash
git lfs install --local
git lfs pull
```

Git LFS stores the unchanged imported Impeccable executable. Fetch it before
checking the imported-skill hashes or using that design tool.

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

The private GitLab repository is [`nvis-ova/nvis-doc-hub`](https://gitlab-master.nvidia.com/nvis-ova/nvis-doc-hub).
Its SSH URL is `ssh://git@gitlab-master.nvidia.com:12051/nvis-ova/nvis-doc-hub.git`.
The local project directory remains `nvis-docs-hub`. `main` holds the verified
baseline; `development` is the shared branch for testing changes before merging
them into `main`. Keep changes on `development` or a feature branch and run the
checks above before opening a merge request to `main`.

Local environments, runtime databases, logs, caches, and bulk browser captures
are excluded from Git. Source snapshots, imported skills, design context, tests,
verification reports, and representative review captures are versioned. A fresh
clone can recreate the local publications with `./scripts/seed.sh` after setup.
