"""One publication and retrieval service shared by browser, CLI, and MCP clients."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .content import prepare
from .models import HubError, Registration, validate_path
from .sources import acquire
from .store import Store


class Hub:
    """Publish source-authored documentation into durable, searchable shared storage."""

    def __init__(self, db_path: Path | str) -> None:
        self.store = Store(db_path)

    def register(self, config: Registration) -> dict[str, Any]:
        """Persist a validated registration without replacing its working publication."""
        self.store.register(config)
        return self.get_project(config.slug) or {}

    def refresh(self, slug: str) -> dict[str, Any]:
        """Stage acquisition/rendering then atomically replace one project publication."""
        config = self.store.registration(slug)
        if config is None:
            raise HubError(f"Project is not registered: {slug}")
        try:
            with acquire(config) as source:
                publication = prepare(source, config)
                metadata = {
                    "revision": source.revision,
                    "repo_url": config.repo_url,
                    "ref": config.ref,
                    "source_mode": config.source_mode,
                    "published_at": datetime.now(UTC).isoformat(),
                    "document_count": len(publication.documents),
                    "last_error": None,
                    "nav_mode": publication.nav_mode,
                    "navigation": publication.navigation,
                    "warnings": publication.warnings,
                    "acquisition": source.acquisition,
                }
                self.store.publish(slug, publication, metadata)
        except HubError as error:
            self.store.error(slug, str(error))
            raise
        except (OSError, ValueError):
            message = "Source could not be imported; check the declared paths and document formats."
            self.store.error(slug, message)
            raise HubError(message) from None
        return self.get_project(slug) or {}

    def list_projects(self) -> list[dict[str, Any]]:
        """List registered projects and last-publication status without private settings."""
        return [
            {key: value for key, value in project.items() if key != "navigation"}
            for project in self.store.projects()
        ]

    def get_project(self, slug: str) -> dict[str, Any] | None:
        """Retrieve a project with curated or explicitly generated navigation."""
        projects = self.store.projects(slug)
        return projects[0] if projects else None

    def list_documents(self, slug: str) -> list[dict[str, Any]]:
        """List document identity and authored/registered classification metadata."""
        return [
            {key: doc[key] for key in ("path", "title", "kind", "topics", "url", "revision")}
            for doc in self.store.documents(slug)
        ]

    def get_document(self, slug: str, path: str, section: str | None = None) -> dict[str, Any] | None:
        """Read a complete hosted document or narrow content to one exact heading."""
        try:
            validate_path(path)
        except ValueError:
            return None
        docs = self.store.documents(slug, path)
        if not docs:
            return None
        doc = docs[0]
        if section:
            fragment = next((item for item in doc["sections"] if item["id"] == section), None)
            if fragment is None:
                return None
            for key in ("text", "markdown", "html"):
                doc[key] = fragment[key]
            doc["headings"] = [heading for heading in doc["headings"] if heading["id"] == section]
            doc["sections"] = [fragment]
            from urllib.parse import quote

            doc["url"] += "#" + quote(section, safe="-_")
        return doc

    def record_document_view(self, slug: str, path: str) -> bool:
        """Count an explicit browser open without changing normal retrieval calls."""
        try:
            validate_path(path)
        except ValueError:
            return False
        return self.store.record_document_view(slug, path)

    def popular_documents(self, limit: int = 6) -> list[dict[str, Any]]:
        """Return real published documents ranked by shared all-time page opens."""
        return self.store.popular_documents(limit)

    def browse_documents(
        self,
        project: str | None = None,
        topic: str | None = None,
        kind: str | None = None,
        limit: int = 30,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List published document cards using explicit classification filters."""
        return self.store.browse_documents(project, topic, kind, limit, offset)

    def document_count(
        self, project: str | None = None, topic: str | None = None, kind: str | None = None
    ) -> int:
        """Count documents matching the same browse metadata filters."""
        return self.store.document_count(project, topic, kind)

    def search(
        self,
        query: str,
        project: str | None = None,
        topic: str | None = None,
        kind: str | None = None,
        limit: int = 30,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Return ranked, filtered hosted sections with plain excerpts and provenance."""
        return self.store.search(query, project, topic, kind, limit, offset)

    def suggest(
        self,
        query: str,
        project: str | None = None,
        topic: str | None = None,
        kind: str | None = None,
    ) -> list[dict[str, Any]]:
        """Suggest up to five sections using a literal prefix for the final query term."""
        query = query.strip()
        if len(query) < 2:
            return []
        fields = ("project_slug", "project_title", "title", "heading", "snippet", "url")
        return [
            {key: result[key] for key in fields}
            for result in self.store.search(query, project, topic, kind, 5, 0, prefix=True)
        ]

    def facets(self) -> dict[str, list[str]]:
        """List only classifications actually present in published documents."""
        docs = [doc for project in self.list_projects() for doc in self.store.documents(project["slug"])]
        return {
            "topics": sorted({topic for doc in docs for topic in doc["topics"]}),
            "kinds": sorted({doc["kind"] for doc in docs if doc["kind"]}),
        }

    def get_asset(self, slug: str, path: str) -> tuple[bytes, str] | None:
        """Read an imported scoped attachment without touching source files."""
        try:
            validate_path(path)
        except ValueError:
            return None
        return self.store.asset(slug, path)
