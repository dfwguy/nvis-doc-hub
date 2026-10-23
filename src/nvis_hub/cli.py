"""Trusted local administration and adapter entry points."""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from nvis_hub.models import HubError, Registration
from nvis_hub.service import Hub


def database_path(value: str | Path | None = None) -> Path:
    """Use an explicit database, the shared environment setting, or the local default."""
    return Path(value or os.environ.get("NVIS_HUB_DB", "data/hub.sqlite3")).expanduser()


def load_registration(path: Path) -> Registration:
    """Read JSON registration and resolve source paths relative to that file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise HubError(f"Cannot read registration JSON: {path}") from exc
    if not isinstance(data, dict):
        raise HubError("Registration must be a JSON object.")
    if isinstance(data.get("local_path"), str):
        local_path = Path(data["local_path"]).expanduser()
        if not local_path.is_absolute():
            local_path = path.resolve().parent / local_path
        data["local_path"] = str(local_path.resolve())
    try:
        return Registration.model_validate(data)
    except ValidationError as exc:
        # ValidationError.__str__ echoes input values, which may contain credentials.
        fields = ", ".join(".".join(map(str, error["loc"])) for error in exc.errors())
        raise HubError(
            f"Invalid registration fields: {fields}. See docs/reference/configuration.md."
        ) from exc


def parser() -> argparse.ArgumentParser:
    """Build the command interface."""
    command = argparse.ArgumentParser(prog="nvis-hub", description="NVIS - OVA documentation hub")
    command.add_argument("--db", type=Path, help="SQLite path (default: NVIS_HUB_DB or data/hub.sqlite3)")
    sub = command.add_subparsers(dest="command", required=True)
    register = sub.add_parser("register", help="Register or update one project from JSON")
    register.add_argument("config", type=Path)
    refresh = sub.add_parser("refresh", help="Publish source content atomically")
    refresh.add_argument("slug", nargs="?")
    refresh.add_argument("--all", action="store_true", help="Refresh every registered project")
    sub.add_parser("list", help="List projects and publication status as JSON")
    serve = sub.add_parser("serve", help="Start the read-only local website")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    sub.add_parser("mcp", help="Start the read-only MCP server over stdio")
    return command


def emit(value: Any) -> None:
    """Write machine-readable administration results."""
    print(json.dumps(value, indent=2, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    """Execute a command, returning a process status without exposing tracebacks."""
    command = parser()
    args = command.parse_args(argv)
    db = database_path(args.db)
    if args.command == "refresh" and bool(args.slug) == bool(args.all):
        command.error("refresh requires either SLUG or --all")
    try:
        if args.command == "serve":
            import uvicorn

            from nvis_hub.web import create_app

            uvicorn.run(create_app(db), host=args.host, port=args.port)
        elif args.command == "mcp":
            from nvis_hub.mcp_server import create_mcp

            create_mcp(db).run(transport="stdio")
        else:
            hub = Hub(db)
            if args.command == "register":
                emit(hub.register(load_registration(args.config)))
            elif args.command == "list":
                emit(hub.list_projects())
            elif args.all:
                projects = []
                failed = False
                for project in hub.list_projects():
                    try:
                        projects.append(hub.refresh(project["slug"]))
                    except HubError as exc:
                        failed = True
                        print(f"{project['slug']}: {exc}", file=sys.stderr)
                emit(projects)
                return int(failed)
            else:
                emit(hub.refresh(args.slug))
    except sqlite3.Error:
        print(
            "nvis-hub: Database is unavailable; check its path, permissions, and SQLite FTS5 support.",
            file=sys.stderr,
        )
        return 1
    except (HubError, OSError) as exc:
        print(f"nvis-hub: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
