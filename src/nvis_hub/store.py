"""SQLite persistence and transactional FTS publication replacement."""

import json
import re
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from urllib.parse import quote

from .content import Publication
from .models import Registration

PUBLIC_SOURCE_FIELDS = ("repo_url", "ref", "source_mode")


class Store:
    """Keep registrations, readable content, assets, and search in one database."""

    def __init__(self, path: Path | str) -> None:
        self.path = str(path)
        if self.path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._memory = sqlite3.connect(":memory:") if self.path == ":memory:" else None
        with self.connection() as database:
            database.executescript("""
                CREATE TABLE IF NOT EXISTS projects (
                    slug TEXT PRIMARY KEY, registration TEXT NOT NULL,
                    publication TEXT NOT NULL DEFAULT '{}'
                );
                CREATE TABLE IF NOT EXISTS documents (
                    project TEXT NOT NULL, path TEXT NOT NULL, body TEXT NOT NULL,
                    PRIMARY KEY(project,path)
                );
                CREATE TABLE IF NOT EXISTS assets (
                    project TEXT NOT NULL, path TEXT NOT NULL, data BLOB NOT NULL,
                    mime TEXT NOT NULL, PRIMARY KEY(project,path)
                );
                CREATE TABLE IF NOT EXISTS sections (
                    id INTEGER PRIMARY KEY, project TEXT NOT NULL,
                    path TEXT NOT NULL, body TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS sections_project ON sections(project);
                CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
                    title, heading, text, tokenize='unicode61 remove_diacritics 2'
                );
            """)

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        """Open a short transaction with deterministic commit, rollback, and close."""
        database = self._memory or sqlite3.connect(self.path, timeout=30)
        database.row_factory = sqlite3.Row
        try:
            with database:
                yield database
        finally:
            if self._memory is None:
                database.close()

    def registration(self, slug: str) -> Registration | None:
        """Read the private acquisition configuration for a registered project."""
        with self.connection() as database:
            row = database.execute("SELECT registration FROM projects WHERE slug=?", (slug,)).fetchone()
        return Registration.model_validate_json(row["registration"]) if row else None

    def register(self, config: Registration) -> None:
        """Persist source configuration while retaining an existing publication."""
        with self.connection() as database:
            previous = database.execute(
                "SELECT registration,publication FROM projects WHERE slug=?", (config.slug,)
            ).fetchone()
            publication = json.loads(previous["publication"]) if previous else {}
            if previous and publication.get("revision"):
                old_config = json.loads(previous["registration"])
                for field in PUBLIC_SOURCE_FIELDS:
                    publication.setdefault(field, old_config[field])
            database.execute(
                "INSERT INTO projects(slug,registration,publication) VALUES(?,?,?) ON CONFLICT(slug) DO UPDATE SET registration=excluded.registration,publication=excluded.publication",
                (config.slug, config.model_dump_json(), json.dumps(publication)),
            )

    def projects(self, slug: str | None = None) -> list[dict[str, Any]]:
        """Return public project metadata without local paths or credential settings."""
        with self.connection() as database:
            rows = database.execute(
                "SELECT registration,publication FROM projects"
                + (" WHERE slug=?" if slug else "")
                + ' ORDER BY json_extract(registration, "$.title") COLLATE NOCASE',
                (slug,) if slug else (),
            ).fetchall()
        result = []
        for row in rows:
            config = json.loads(row["registration"])
            public = {
                key: config[key]
                for key in (
                    "slug",
                    "title",
                    "description",
                    "repo_url",
                    "ref",
                    "topics",
                    "kind",
                    "source_mode",
                )
            }
            public.update(
                {
                    "revision": None,
                    "published_at": None,
                    "document_count": 0,
                    "last_error": None,
                    "nav_mode": "generated",
                    "navigation": [],
                    "warnings": [],
                }
            )
            public.update(json.loads(row["publication"]))
            desired_source = {field: config[field] for field in PUBLIC_SOURCE_FIELDS}
            published_source = {field: public[field] for field in PUBLIC_SOURCE_FIELDS}
            public["pending_source"] = (
                desired_source if public["revision"] and desired_source != published_source else None
            )
            result.append(public)
        return result

    def error(self, slug: str, message: str) -> None:
        """Record refresh failure separately from the last working publication."""
        with self.connection() as database:
            database.execute(
                'UPDATE projects SET publication=json_set(publication, "$.last_error", ?) WHERE slug=?',
                (message, slug),
            )

    def publish(self, slug: str, publication: Publication, metadata: dict[str, Any]) -> None:
        """Replace a complete project and its FTS entries in one atomic transaction."""
        with self.connection() as database:
            database.execute(
                "DELETE FROM search_index WHERE rowid IN (SELECT id FROM sections WHERE project=?)", (slug,)
            )
            for table in ("sections", "documents", "assets"):
                database.execute(f"DELETE FROM {table} WHERE project=?", (slug,))
            for doc in publication.documents:
                doc["published_at"] = metadata["published_at"]
                database.execute(
                    "INSERT INTO documents(project,path,body) VALUES(?,?,?)",
                    (slug, doc["path"], json.dumps(doc)),
                )
                whole_page = {"id": "", "title": doc["title"], "text": doc["text"], "is_document": True}
                for section in [*doc["sections"], whole_page]:
                    cursor = database.execute(
                        "INSERT INTO sections(project,path,body) VALUES(?,?,?)",
                        (slug, doc["path"], json.dumps(section)),
                    )
                    database.execute(
                        "INSERT INTO search_index(rowid,title,heading,text) VALUES(?,?,?,?)",
                        (
                            cursor.lastrowid,
                            doc["title"] if section.get("is_document") else "",
                            section["title"],
                            section["text"],
                        ),
                    )
            for path, data, mime in publication.assets:
                database.execute(
                    "INSERT INTO assets(project,path,data,mime) VALUES(?,?,?,?)", (slug, path, data, mime)
                )
            database.execute("UPDATE projects SET publication=? WHERE slug=?", (json.dumps(metadata), slug))

    def documents(self, slug: str, path: str | None = None) -> list[dict[str, Any]]:
        """Read complete JSON documents from the active publication."""
        with self.connection() as database:
            rows = database.execute(
                "SELECT body FROM documents WHERE project=?"
                + (" AND path=?" if path is not None else "")
                + " ORDER BY path",
                (slug, path) if path is not None else (slug,),
            ).fetchall()
        return [json.loads(row["body"]) for row in rows]

    def asset(self, slug: str, path: str) -> tuple[bytes, str] | None:
        """Retrieve an asset from the same durable publication as its documents."""
        with self.connection() as database:
            row = database.execute(
                "SELECT data,mime FROM assets WHERE project=? AND path=?", (slug, path)
            ).fetchone()
        return (bytes(row["data"]), row["mime"]) if row else None

    def search(
        self, query: str, project: str | None, topic: str | None, kind: str | None, limit: int, offset: int
    ) -> list[dict[str, Any]]:
        """Rank matching authored sections with literal FTS terms and metadata filters."""
        words = re.findall(r"\w+", query, flags=re.UNICODE)[:32]
        if not words:
            return []
        match = " AND ".join('"' + word + '"' for word in words)
        parameters: list[Any] = [match]
        conditions = ["search_index MATCH ?"]
        if project:
            conditions.append("s.project=?")
            parameters.append(project)
        if topic:
            conditions.append('EXISTS(SELECT 1 FROM json_each(d.body, "$.topics") WHERE value=?)')
            parameters.append(topic)
        if kind:
            conditions.append('json_extract(d.body, "$.kind")=?')
            parameters.append(kind)
        conditions.append("""(json_extract(s.body,'$.is_document') IS NULL OR NOT EXISTS (
            SELECT 1 FROM sections other WHERE other.project=s.project AND other.path=s.path
            AND json_extract(other.body,'$.is_document') IS NULL
            AND other.id IN (SELECT rowid FROM search_index WHERE search_index MATCH ?)
        ))""")
        parameters.append(match)
        parameters.extend(["text : (" + match + ")", max(1, min(limit, 100)), max(0, offset)])
        sql = (
            """SELECT d.body AS document, s.body AS section,
            json_extract(p.registration,'$.title') AS project_title,
            snippet(search_index,2,'','',' … ',36) AS excerpt
            FROM search_index JOIN sections s ON s.id=search_index.rowid
            JOIN documents d ON d.project=s.project AND d.path=s.path
            JOIN projects p ON p.slug=s.project
            WHERE """
            + " AND ".join(conditions)
            + " ORDER BY CASE WHEN s.id IN (SELECT rowid FROM search_index WHERE search_index MATCH ?) THEN 0 ELSE 1 END, bm25(search_index,2.0,5.0,4.0),s.project,s.path,s.id LIMIT ? OFFSET ?"
        )
        with self.connection() as database:
            rows = database.execute(sql, parameters).fetchall()
        result = []
        for row in rows:
            doc, section = json.loads(row["document"]), json.loads(row["section"])
            anchor = section["id"]
            result.append(
                {
                    **{
                        key: doc[key]
                        for key in (
                            "project_slug",
                            "path",
                            "title",
                            "kind",
                            "topics",
                            "revision",
                            "source_url",
                            "published_at",
                        )
                    },
                    "project_title": row["project_title"],
                    "heading": section["title"],
                    "anchor": anchor,
                    "snippet": re.sub(r"\s+", " ", row["excerpt"]).strip(),
                    "url": doc["url"] + (("#" + quote(anchor, safe="-_")) if anchor else ""),
                }
            )
        return result
