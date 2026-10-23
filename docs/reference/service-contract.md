# Internal service contract

Shared by the independent implementation tasks. Dict results are JSON-serializable.

`nvis_hub.models.Registration` is a Pydantic model:
`slug: str`, `title: str`, `description: str`, `repo_url: str`, `ref: str = 'main'`,
`docs_paths: list[str]`, `nav_path: str | None = None`, `topics: list[str] = []`,
`kind: str | None = None`, `source_mode: Literal['gitlab','snapshot','local'] = 'gitlab'`,
`local_path: str | None = None`, `credential_env: str = 'NVIS_GITLAB_TOKEN'`.
Snapshot local_path points at a directory containing manifest.json and repository/.
Local mode points at a local source directory for disposable tests; local git sources
record HEAD, otherwise record an explicitly labelled content digest as revision.

`nvis_hub.service.Hub(db_path: Path | str)` initializes persistent storage.
`HubError` is the safe user-facing exception from nvis_hub.models.

- `register(config: Registration) -> dict`: persist validated registration; return project.
- `refresh(slug: str) -> dict`: acquire, parse, commit; return project or raise HubError.
- `list_projects() -> list[dict]`: slug,title,description,repo_url,ref,topics,kind,
  source_mode,revision,published_at,document_count,last_error,nav_mode.
- `get_project(slug: str) -> dict | None`: same fields plus navigation list.
- `list_documents(slug: str) -> list[dict]`: path,title,kind,topics,url,revision.
- `get_document(slug: str, path: str, section: str | None = None) -> dict | None`:
  project_slug,path,title,html,markdown,text,headings (id,title,level),sections,
  kind,topics,revision,source_url,published_at,url,source_path.
  Missing section returns None. Section retrieval narrows text and markdown.
- `search(query: str, project: str | None = None, topic: str | None = None,
  kind: str | None = None, limit: int = 30, offset: int = 0) -> list[dict]`:
  project_slug,project_title,path,title,heading,anchor,snippet,url,kind,topics,
  revision,source_url,published_at. Empty query returns []. Snippets are plain text.
- `suggest(query: str, project: str | None = None, topic: str | None = None,
  kind: str | None = None) -> list[dict]`: up to five ranked sections using a
  literal prefix for the final term. Earlier terms remain exact. Queries shorter
  than two trimmed characters return []. Fields: project_slug, project_title,
  title, heading, snippet, url. Normal search and MCP keep exact-term matching.
- `facets() -> dict`: topics:list[str], kinds:list[str]. Projects use list_projects.
- `get_asset(slug: str, path: str) -> tuple[bytes,str] | None`: bytes and MIME type.

Routes: `/`, `/search?q=...&project=...&topic=...&kind=...`, `/projects/{slug}`,
`/projects/{slug}/docs/{path}` and `/projects/{slug}/assets/{path}`.
Paths are repository-relative and preserve extensions. URLs percent-encode paths
while retaining slashes. HTML is sanitized and local links point to these routes.
Navigation is a flat ordered list of `{title, path, level, url}` including caption
entries with path/url None if helpful. Unsupported nav entries are reported.

`GET /api/search/suggestions` accepts `q`, `project`, `topic`, and `kind` and returns
the `suggest` array. Raw queries over 200 characters receive HTTP 400. This is a
read-only browser enhancement over the same persistent publication.

MCP tools: list_projects(), search_documents(query,project?,topic?,kind?,limit?),
get_document(project,path,section?). All use this service with the same database.
CLI: `nvis-hub --db PATH register CONFIG`, `refresh SLUG`, `list`,
`serve --host 127.0.0.1 --port 8000`, `mcp`. Default DB: data/hub.sqlite3;
NVIS_HUB_DB overrides it for the web factory and MCP.
