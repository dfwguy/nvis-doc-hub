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

The homepage and existing `/search` route render a single documentation discovery
surface. Empty-query browsing uses published document metadata without changing
the shared search contract. The website records successful reader opens in an
additive SQLite `document_views` table keyed by project and path. Its aggregate
all-time counters retain no reader identifiers, survive publication replacement,
and join current documents so deleted pages cannot rank. CLI/MCP/API retrieval
does not increment these counters. Counts are shared only within one database.

Kaizen UI's documented browse, search, filter, card, and carousel patterns guide
the native server-rendered markup. Styles use documented semantic CSS token
names with established dark-theme fallbacks. React components and their runtime
CSS are not installed or represented as native Jinja components.

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
