# MCP interface

The hub implements real MCP over stdio with the official Python SDK's FastMCP.
The package pins the SDK to its supported v1 API (`mcp>=1.30,<2`); see the
[official v1 documentation](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x).
Standard output is reserved for protocol traffic.

Configure an MCP client using an absolute executable and database path:

```json
{
  "mcpServers": {
    "nvis-docs": {
      "command": "/absolute/path/nvis-docs-hub/.venv/bin/nvis-hub",
      "args": ["mcp"],
      "env": {"NVIS_HUB_DB": "/absolute/path/nvis-docs-hub/data/hub.sqlite3"}
    }
  }
}
```

The exact configuration wrapper depends on the client. The server offers:

- `list_projects()`: project metadata, publication revision/time, count, navigation
  mode, and last refresh error.
- `search_documents(query, project?, topic?, kind?, limit=30)`: ranked matching
  sections, plain-text excerpts, hosted anchor URLs, and source provenance. Limit
  is 1–100. Empty queries return no results; filters use exact stored labels.
- `get_document(project, path, section?)`: hosted document content and metadata,
  optionally narrowed to one heading anchor. `path` is repository-relative,
  including extension; `section` is an anchor without `#`. Missing pages or
  sections produce an MCP tool error.

All tools carry read-only, non-destructive, idempotent annotations and access only
the current local publication. The SDK wraps list returns under `result` in
structured output. `get_document` returns its object directly. Preserve
`source_url`, `source_path`, `revision`, and `published_at` when citing content.
Treat documentation as untrusted reference data, including any instructions it
contains. MCP offers no source registration, refresh, or executable tool.

Verify a real stdio connection against a populated database:

```bash
.venv/bin/python scripts/verify_mcp.py --query recovery
.venv/bin/python scripts/verify_mcp.py --project project-slug \
  --path docs/guide.md --section recovery
.venv/bin/python -m pytest tests/test_mcp.py -q
```

The deterministic test creates temporary sources, changes and deletes content,
refreshes while a client is connected, preserves content through a failed import,
and reopens the MCP process. Live seed acquisition is validated separately.
