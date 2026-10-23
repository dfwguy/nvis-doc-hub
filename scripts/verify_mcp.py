#!/usr/bin/env python3
"""Check the installed hub through an actual SDK stdio client."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def payload(result: Any) -> Any:
    """Decode SDK structured results and surface tool failures."""
    if result.isError:
        raise RuntimeError(str(result.content))
    if result.structuredContent is not None:
        return result.structuredContent.get("result", result.structuredContent)
    return json.loads(result.content[0].text)


async def verify(args: argparse.Namespace) -> dict[str, Any]:
    """Initialize MCP, discover read-only tools, and inspect requested content."""
    env = dict(os.environ)
    if args.db:
        env["NVIS_HUB_DB"] = str(args.db.resolve())
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "nvis_hub.cli", "mcp"],
        env=env,
    )
    async with stdio_client(parameters) as (reader, writer):
        async with ClientSession(reader, writer) as client:
            await client.initialize()
            tools = (await client.list_tools()).tools
            expected = {"list_projects", "search_documents", "get_document"}
            if {tool.name for tool in tools} != expected:
                raise RuntimeError("MCP tool discovery differs from the hub contract")
            if not all(tool.annotations and tool.annotations.readOnlyHint for tool in tools):
                raise RuntimeError("A tool is missing its read-only annotation")
            projects = payload(await client.call_tool("list_projects"))
            report: dict[str, Any] = {"transport": "stdio", "tools": sorted(expected), "projects": projects}
            if args.query:
                report["results"] = payload(
                    await client.call_tool(
                        "search_documents",
                        {
                            "query": args.query,
                            "project": args.project,
                        },
                    )
                )
            if args.path:
                document = payload(
                    await client.call_tool(
                        "get_document",
                        {
                            "project": args.project,
                            "path": args.path,
                            "section": args.section,
                        },
                    )
                )
                for field in ("source_path", "source_url", "revision", "published_at"):
                    if not document.get(field):
                        raise RuntimeError(f"Retrieved content has no {field}")
                report["document"] = {
                    key: document[key]
                    for key in (
                        "project_slug",
                        "path",
                        "title",
                        "source_path",
                        "source_url",
                        "revision",
                        "published_at",
                        "text",
                    )
                }
            return report


def main() -> int:
    """Run a live adapter check against an existing publication database."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path)
    parser.add_argument("--query")
    parser.add_argument("--project")
    parser.add_argument("--path")
    parser.add_argument("--section")
    args = parser.parse_args()
    if args.path and not args.project:
        parser.error("--path requires --project")
    if args.section and not args.path:
        parser.error("--section requires --path")
    print(json.dumps(asyncio.run(verify(args)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
