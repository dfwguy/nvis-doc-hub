# Run the hub locally

Use Python 3.12+ and keep all commands in the project root. A source import needs
authored Markdown within an explicit scope; it never runs repository scripts.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
./scripts/seed.sh
./scripts/dev.sh
```

Visit <http://127.0.0.1:8000>. Search for a phrase from a published page, select
a project or metadata filter, and open a result at its matching heading. The
reader includes source path, revision, and publication time. Missing topic or
document-type metadata stays unclassified.

In a second terminal, inspect publication status:

```bash
.venv/bin/nvis-hub list
.venv/bin/python scripts/verify_mcp.py --query bringup
```

The MCP check starts its own stdio subprocess against the same database. To
retrieve a known page and section, add `--project SLUG --path docs/page.md
--section heading-anchor`. Paths and anchors come from search results, rather
than guesses. The JSON response includes provenance.

Stop the website with Ctrl-C, then rerun `./scripts/dev.sh`. Registrations and
published content remain in `data/hub.sqlite3`. To choose a different persistent
location, export an absolute `NVIS_HUB_DB` before running either adapter.

Seed registrations and [source evidence](../../evidence/source-recon.md)
distinguish live imports from immutable acquired snapshots. A snapshot refresh
rebuilds the stored snapshot; obtaining a newer revision is a separate action.
