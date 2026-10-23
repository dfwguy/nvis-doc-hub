"""Read-only web views over the shared publication service."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from nvis_hub.navigation import group_navigation
from nvis_hub.service import Hub

PACKAGE = Path(__file__).parent
SOURCE_LABELS = {"snapshot": "Source snapshot", "gitlab": "GitLab", "local": "Local source"}


def doc_url(slug: str, path: str) -> str:
    """Build a namespaced, encoded document URL."""
    return f"/projects/{quote(slug, safe='')}/docs/{quote(path, safe='/')}"


def display_date(value: str | None) -> str:
    """Render stored publication dates in an explicit timezone."""
    if not value:
        return "Not published"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%d %b %Y · %H:%M UTC")
    except ValueError:
        return value


def create_app(db_path: Path | str | None = None) -> FastAPI:
    """Create a loopback-oriented web application using a persistent Hub."""
    hub = Hub(db_path or os.environ.get("NVIS_HUB_DB", "data/hub.sqlite3"))
    app = FastAPI(title="NVIS - OVA Documentation Hub", docs_url=None, redoc_url=None)
    app.state.hub = hub
    templates = Jinja2Templates(directory=str(PACKAGE / "templates"))
    templates.env.filters["display_date"] = display_date
    templates.env.filters["reader_html"] = lambda html: html.replace(
        "<table>",
        '<p class="table-scroll-hint">Scroll horizontally to see all columns.</p>'
        '<div class="table-scroll" tabindex="0" role="region" '
        'aria-label="Scrollable reference table"><table>',
    ).replace("</table>", "</table></div>")
    templates.env.globals.update(doc_url=doc_url, source_labels=SOURCE_LABELS)
    app.mount("/static", StaticFiles(directory=str(PACKAGE / "static")), name="static")

    @app.middleware("http")
    async def browser_headers(request: Request, call_next: Any) -> Response:
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "font-src 'self'; img-src 'self' data:; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
        )
        if "/assets/" in request.url.path:
            response.headers["Content-Security-Policy"] = (
                "default-src 'none'; style-src 'unsafe-inline'; sandbox"
            )
        return response

    def page(request: Request, template: str, status: int = 200, **values: Any) -> HTMLResponse:
        projects = hub.list_projects()
        project = values.get("project")
        document = values.get("document")
        navigation_groups = (
            group_navigation(
                project.get("navigation", []),
                hub.list_documents(project["slug"]),
                curated=project.get("nav_mode") == "curated",
                current_path=document["path"] if document else None,
            )
            if project
            else []
        )
        return templates.TemplateResponse(
            request=request,
            name=template,
            context={
                "projects": projects,
                "page": "catalog",
                "project": None,
                "document": None,
                "navigation_groups": navigation_groups,
                "q": "",
                **values,
            },
            status_code=status,
        )

    @app.exception_handler(StarletteHTTPException)
    async def missing_page(request: Request, exc: StarletteHTTPException) -> HTMLResponse:
        return page(
            request,
            "error.html",
            status=exc.status_code,
            page="error",
            title="Documentation not found",
            detail=str(exc.detail),
        )

    @app.get("/", response_class=HTMLResponse)
    def catalog(request: Request) -> HTMLResponse:
        projects = hub.list_projects()
        previews = {}
        for item in projects:
            docs = hub.list_documents(item["slug"])
            by_path = {doc["path"]: doc for doc in docs}
            navigation = (hub.get_project(item["slug"]) or {}).get("navigation", [])
            ordered = [by_path[entry["path"]] for entry in navigation if entry.get("path") in by_path]
            previews[item["slug"]] = (ordered or docs)[:3]
        return page(
            request,
            "catalog.html",
            title="Documentation",
            previews=previews,
            document_count=sum(p.get("document_count", 0) for p in projects),
            facets=hub.facets(),
        )

    @app.get("/search", response_class=HTMLResponse)
    def search(
        request: Request,
        q: str = "",
        project: str = "",
        topic: str = "",
        kind: str = "",
        offset: int = Query(0, ge=0, le=100000),
    ) -> HTMLResponse:
        query = q.strip()
        too_long = len(query) > 200
        results = (
            []
            if too_long
            else hub.search(
                query,
                project=project or None,
                topic=topic or None,
                kind=kind or None,
                limit=31,
                offset=offset,
            )
        )
        params = {"q": query, "project": project, "topic": topic, "kind": kind}
        next_url = "/search?" + urlencode({**params, "offset": offset + 30})
        prev_url = "/search?" + urlencode({**params, "offset": max(0, offset - 30)})
        return page(
            request,
            "search.html",
            title="Search documentation",
            page="search",
            q=query,
            results=results[:30],
            has_next=len(results) > 30,
            next_url=next_url,
            prev_url=prev_url,
            offset=offset,
            filters=params,
            facets=hub.facets(),
            too_long=too_long,
        )

    @app.get("/projects/{slug}", response_class=HTMLResponse)
    def project_view(request: Request, slug: str) -> HTMLResponse:
        project = hub.get_project(slug)
        if project is None:
            raise HTTPException(404, "This project is not registered. Browse the project catalog.")
        return page(
            request,
            "project.html",
            title=project["title"],
            page="project",
            project=project,
            documents=hub.list_documents(slug),
        )

    @app.get("/projects/{slug}/docs/{path:path}", response_class=HTMLResponse)
    def reader(request: Request, slug: str, path: str) -> HTMLResponse:
        document = hub.get_document(slug, path)
        project = hub.get_project(slug)
        if document is None or project is None:
            raise HTTPException(
                404, "This page is not in the current publication. It may have moved or been removed."
            )
        documents = hub.list_documents(slug)
        by_path = {doc["path"]: doc for doc in documents}
        nav_paths = list(
            dict.fromkeys(
                entry["path"] for entry in project.get("navigation", []) if entry.get("path") in by_path
            )
        )
        documents = [by_path[path] for path in nav_paths] + [
            doc for doc in documents if doc["path"] not in nav_paths
        ]
        position = next((i for i, d in enumerate(documents) if d["path"] == path), 0)
        return page(
            request,
            "reader.html",
            title=document["title"],
            page="reader",
            project=project,
            document=document,
            read_minutes=max(1, len(document.get("text", "").split()) // 220),
            previous=documents[position - 1] if position > 0 else None,
            following=documents[position + 1] if position + 1 < len(documents) else None,
        )

    @app.get("/projects/{slug}/assets/{path:path}")
    def asset(slug: str, path: str) -> Response:
        result = hub.get_asset(slug, path)
        if result is None:
            raise HTTPException(404, "This attachment is not in the current publication.")
        data, mime = result
        inline = mime.startswith("image/") or mime == "application/pdf"
        name = quote(Path(path).name, safe="")
        return Response(
            data,
            media_type=mime,
            headers={
                "Content-Disposition": f"{'inline' if inline else 'attachment'}; filename*=UTF-8''{name}",
            },
        )

    @app.get("/sources", response_class=HTMLResponse)
    def sources(request: Request) -> HTMLResponse:
        return page(request, "sources.html", title="Source status", page="sources")

    @app.get("/help", response_class=HTMLResponse)
    def help_view(request: Request) -> HTMLResponse:
        return page(request, "help.html", title="Using the hub", page="help")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/projects")
    def api_projects() -> list[dict[str, Any]]:
        return hub.list_projects()

    @app.get("/api/search")
    def api_search(
        q: str = "", project: str | None = None, topic: str | None = None, kind: str | None = None
    ) -> list[dict[str, Any]]:
        if len(q) > 200:
            raise HTTPException(400, "Use a search query of 200 characters or fewer.")
        return hub.search(q, project=project, topic=topic, kind=kind)

    @app.get("/api/search/suggestions")
    def api_search_suggestions(
        q: str = "", project: str | None = None, topic: str | None = None, kind: str | None = None
    ) -> list[dict[str, Any]]:
        if len(q) > 200:
            raise HTTPException(400, "Use a search query of 200 characters or fewer.")
        return hub.suggest(q, project=project, topic=topic, kind=kind)

    return app
