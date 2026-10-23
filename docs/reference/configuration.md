# Configuration

`nvis-hub --db PATH` overrides `NVIS_HUB_DB`. Otherwise the default database is
`data/hub.sqlite3` relative to the process working directory. Use an absolute
environment path when starting web and MCP from different directories. Parent
directories are created automatically. `NVIS_HUB_PORT` changes `scripts/dev.sh`'s
port; direct CLI `serve` accepts `--host` and `--port`.

Registrations are JSON objects with these fields:

- `slug`: stable URL-safe project identity.
- `title`, `description`: catalog text explaining the project and its docs.
- `repo_url`: HTTPS GitLab repository URL, with no credentials embedded.
- `ref`: source branch/tag/commit; default `main`.
- `docs_paths`: nonempty explicit list of repository-relative files/directories.
- `nav_path`: optional repository-relative supported RST toctree input.
- `topics`: optional list of topic labels; defaults to empty.
- `kind`: optional document type such as `how-to` or `reference`.
- `source_mode`: `gitlab` (default), `snapshot`, or `local`.
- `local_path`: required source directory for local/snapshot acquisition. Relative
  values resolve against the registration JSON directory.
- `credential_env`: environment-variable name used for a live GitLab token;
  defaults to `NVIS_GITLAB_TOKEN`. Store the variable's name, never its value.

`local` sources use Git HEAD where available, otherwise a revision labelled as a
content digest. They are intended for local development and disposable fixtures.
`snapshot` sources contain `manifest.json` and a `repository/` tree with exact
source revision and acquisition metadata. They are immutable acquired inputs;
refresh does not fetch the current branch. See [source evidence](../../evidence/source-recon.md).

Publication includes authored Markdown and supported assets in the declared
scope. Hidden paths, symlinks, traversal, tests, vendored content, and templates
are excluded unless the supported scope rules explicitly allow selection.
Unsupported document formats/nav entries are reported. Source scripts, Sphinx
configuration, and arbitrary build hooks never run during ingestion.

Raw source HTML is escaped and rendered HTML sanitized. Relative document and
asset links are rewritten to namespaced hosted routes when their targets are in
scope. Unsupported links are visible to readers. Credentials never belong in
metadata, URLs, page content, or logs.

The website and MCP are read-only; CLI administration assumes a trusted local
operator. Reader authentication and NVIDIA SSO are [deferred](../deferred-access-control.md).
