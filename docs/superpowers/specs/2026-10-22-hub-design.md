# Documentation hub implementation design

The user delegated routine engineering choices and explicitly asked to continue
through implementation and browser verification without repeating discovery.
BUILD_BRIEF.md remains authoritative. This records implementation choices, not
additional product scope.

## Architecture
Use Python 3.12, FastAPI with server-rendered Jinja templates, SQLite FTS5,
markdown-it-py and sanitized HTML, and the official Python MCP SDK over stdio.
A frontend SPA would add a second build and duplicate routing without helping the
current reading/search workflows. A prebuilt Sphinx-site importer would preserve
more extensions but requires arbitrary source builds and platform-specific tools;
use safe authored Markdown ingestion now and report unsupported formats explicitly.

## Publication boundary
Register an explicit list of repository files/directories. Exclude hidden paths,
tests, vendored files, and templates unless explicitly selected. Preserve supported
RST toctree navigation as structured links and captions; Markdown is the hosted
document format. Do not execute source scripts or Sphinx configuration. Render
headings with stable anchors, code, tables, local links, images and attachments.
Escape raw HTML and sanitize protocols/content. Unsupported links remain visibly
identified. Confine assets to the imported scope; reject traversal and symlinks.

Live imports use HTTPS GitLab archives with credentials read from a named environment
variable, or Git's existing credential helper where available. Token values never
enter registrations, reader responses or logs. Immutable MCP-acquired snapshots
are a separate source mode with exact revision and acquisition metadata. Snapshots
are authentic source content, but refreshing one does not contact GitLab.

## Storage and shared interfaces
Registrations, documents, sections, attachments and publication metadata live in a
single SQLite database. Stage all source acquisition and parsing before committing
one atomic replacement per project. Failed refreshes retain working content and
record an error. Deleted content disappears from documents and FTS on success.
Stable document identity is (project slug, repository-relative path); section identity
adds its deduplicated heading anchor. The Hub service owns retrieval and search;
web, CLI, and MCP call that service.

## Interface
The catalog puts a labelled global search first, then descriptive project entries.
Results are ranked sections with excerpts, project/topic/type filters, and direct
anchor links. Project views show curated navigation or an explicitly generated
fallback. Reading views use breadcrumbs, a narrow prose measure, a project tree,
in-page headings, source path/revision and publication time. CLI handles trusted
registration and refresh; the browser provides read-only publication status and
clear recovery commands. Keep administration off unauthenticated web mutations.

## Verification
Behavior tests cover scoped imports, rendering, relative links, assets, duplicate
headings, safe paths/content, ranked filtered search, failed and changed/deleted
refreshes and persistence. Exercise real stdio MCP via the SDK client. Browser
verification covers catalog, filtered results, nested reading, source details,
keyboard use, mobile navigation, empty/no-match/error states and long code blocks.
Record live-source limitations separately from deterministic local test results.

## Deployment boundary
Bind to loopback by default. Package a startup command and container with persistent
volume support. Do not publish or deploy, create a remote, implement SSO or create
the publishing skill. Document the future registration integration contract.
