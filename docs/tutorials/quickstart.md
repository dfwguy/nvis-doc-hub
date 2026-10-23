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

Browse documentation is the shared homepage and search destination. Choose
Browse documents for the complete library, or leave the query empty and select
an available filter. Empty metadata dimensions are omitted. Filters apply when
changed; without JavaScript, use Apply filters. Clear search preserves filters,
and Clear filters preserves the query.

Explore popular documentation is the only default discovery section. It shows
up to six genuinely opened documents in one carousel, with a clear empty
state before usage exists. Use its arrow buttons, keyboard, or touch to explore. Choose a Project or Browse documents for a paginated
vertical list. The default page does not expand extra project collections, and
the sidebar does not list every project. Reader navigation contains only the
current project’s document sections. Popularity counts shared all-time opens, including repeats, without
reader profiles.

Use the Dark mode switch in the header to choose light or dark appearance. The
preference persists across pages and reloads; dark is the initial default. With
JavaScript disabled the switch is hidden and the native dark interface, search,
filters, document links and disclosures continue to work.

Project indexes and navigation have collapsible document categories. Expand a
section to see its pages; the category containing the current document opens
automatically. Counts show actual pages, and uncategorized content stays under
Other documentation. These controls also work without JavaScript.

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
