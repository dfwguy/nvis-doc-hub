"""Use a real SDK client and a stdio subprocess, rather than a JSON API double."""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


def decode(result: Any) -> Any:
    assert not result.isError, result.content
    if result.structuredContent is not None:
        data = result.structuredContent
        return data.get("result", data)
    return json.loads(result.content[0].text)


def test_stdio_tools_share_persistent_publications_and_section_provenance(tmp_path: Path) -> None:
    """Stale per-process copies, missing sections, or a non-MCP adapter fail this check."""
    source = tmp_path / "repo"
    docs = source / "docs"
    docs.mkdir(parents=True)
    guide = docs / "guide.md"
    guide.write_text(
        "# Prism operator guide\n\n## Recovery\n\nRestart the prism controller.\n\n## Status\n\nInspect telemetry.\n"
    )
    removed = docs / "obsolete.md"
    removed.write_text("# Obsolete\n\nLegacyquartz procedure.\n")

    def git(*args: str) -> str:
        result = subprocess.run(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", *args],
            cwd=source,
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )
        return result.stdout.strip()

    git("init", "-q")
    git("add", ".")
    git("-c", "commit.gpgsign=false", "commit", "-q", "-m", "Initial authored documentation")
    initial_commit = git("rev-parse", "HEAD")
    config = tmp_path / "registration.json"
    config.write_text(
        json.dumps(
            {
                "slug": "prism",
                "title": "Prism",
                "description": "Operations for Prism",
                "repo_url": "https://gitlab.example.test/nvis/prism",
                "source_mode": "local",
                "local_path": str(source),
                "docs_paths": ["docs"],
                "topics": ["operations"],
                "kind": "how-to",
            }
        )
    )
    db = tmp_path / "hub.sqlite3"
    env = {**os.environ, "NVIS_HUB_DB": str(db), "PYTHONPATH": str(ROOT / "src")}

    def cli(*args: str, success: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, "-m", "nvis_hub.cli", *args],
            env=env,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert (result.returncode == 0) is success, result.stdout + result.stderr
        return result

    cli("register", str(config))
    cli("refresh", "prism")
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "nvis_hub.cli", "mcp"],
        env=env,
        cwd=ROOT,
    )

    async def exercise() -> None:
        async with stdio_client(parameters) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                assert set(tools) == {"list_projects", "search_documents", "get_document"}
                assert all(tool.annotations and tool.annotations.readOnlyHint for tool in tools.values())
                projects = decode(await session.call_tool("list_projects"))
                assert projects[0]["document_count"] == 2
                original_revision = projects[0]["revision"]
                assert original_revision == initial_commit
                matches = decode(
                    await session.call_tool(
                        "search_documents",
                        {
                            "query": "controller",
                            "project": "prism",
                            "topic": "operations",
                            "kind": "how-to",
                        },
                    )
                )
                assert matches[0]["anchor"] == "recovery"
                assert matches[0]["url"].endswith("docs/guide.md#recovery")
                section = decode(
                    await session.call_tool(
                        "get_document",
                        {
                            "project": "prism",
                            "path": "docs/guide.md",
                            "section": "recovery",
                        },
                    )
                )
                assert "Restart the prism controller" in section["text"]
                assert "Inspect telemetry" not in section["text"]
                assert section["source_path"] == "docs/guide.md"
                assert section["revision"] == original_revision
                assert section["source_url"] == (
                    f"https://gitlab.example.test/nvis/prism/-/blob/{initial_commit}/docs/guide.md"
                )
                assert section["published_at"]
                missing = await session.call_tool(
                    "get_document",
                    {
                        "project": "prism",
                        "path": "docs/missing.md",
                    },
                )
                assert missing.isError
                invalid = await session.call_tool("search_documents", {"query": "prism", "limit": 0})
                assert invalid.isError

                guide.write_text("# Prism operator guide\n\n## Recovery\n\nReconcile sapphire sockets.\n")
                removed.unlink()
                git("add", "-A")
                git(
                    "-c",
                    "commit.gpgsign=false",
                    "commit",
                    "-q",
                    "-m",
                    "Revise recovery and remove obsolete page",
                )
                await asyncio.to_thread(cli, "refresh", "prism")
                assert decode(await session.call_tool("search_documents", {"query": "legacyquartz"})) == []
                changed = decode(await session.call_tool("search_documents", {"query": "sapphire"}))
                assert changed[0]["revision"] != original_revision
                source.rename(tmp_path / "unavailable-repo")
                await asyncio.to_thread(cli, "refresh", "prism", success=False)
                assert decode(await session.call_tool("search_documents", {"query": "sapphire"}))
                status = decode(await session.call_tool("list_projects"))[0]
                assert status["last_error"]
                assert status["document_count"] == 1

        async with stdio_client(parameters) as (reader, writer):
            async with ClientSession(reader, writer) as reopened:
                await reopened.initialize()
                saved = decode(
                    await reopened.call_tool(
                        "get_document",
                        {
                            "project": "prism",
                            "path": "docs/guide.md",
                            "section": "recovery",
                        },
                    )
                )
                assert "Reconcile sapphire sockets" in saved["text"]
                assert decode(await reopened.call_tool("search_documents", {"query": "legacyquartz"})) == []

    asyncio.run(exercise())
