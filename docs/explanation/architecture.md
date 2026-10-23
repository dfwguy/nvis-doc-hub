# Architecture and boundaries

The hub hosts copies of authored documentation so people and agents can discover,
search, and read it consistently. Source GitLab repositories remain authoritative.
There is no LLM runtime, generated operational guidance, or automatic source sync.

A shared `Hub` service owns registration, source acquisition, rendering,
publication, retrieval, and section search. A SQLite database with FTS5 stores
registrations, successful publications, assets, navigation, and refresh status.
The FastAPI/Jinja website, CLI, and official SDK MCP stdio server call this service.
They therefore read the same revision and search index.

Live browser suggestions use a read-only endpoint over that same index. Only
suggestions prefix-match the final query term, returning five ranked sections at
most. A separate progressive-enhancement script debounces requests, discards stale
responses, and adds pointer/keyboard navigation to the existing search forms.
Ordinary full search and MCP retain their existing exact-term matching.

Acquisition reads either an HTTPS GitLab archive, an authentic revision-labelled
snapshot, or a local development directory. Parsing finishes before the service
atomically replaces a project's publication. A failed refresh records an error
and keeps working pages. Successful refresh removes deleted pages and sections.

The importer treats repository content as data. Explicit scopes prevent unrelated
templates, tests, and vendored trees entering the catalog. It does not execute
Sphinx configuration or repository scripts. Markdown becomes sanitized hosted
HTML, nested links/assets stay project-namespaced, and supported RST toctrees
preserve authored ordering and captions. Unsupported formats or links are
reported rather than silently treated as complete site builds.

The server-rendered interface avoids an extra frontend build for search and
reading workflows. SQLite provides persistent single-host storage without a
second service. This is a local prototype boundary: production hosting, capacity,
backups, NVIDIA SSO/NVIS membership enforcement, and publishing authorization
require later decisions. Source acquisition credentials are already kept separate
from that deferred reader access control.
