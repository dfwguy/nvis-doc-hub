"""Authored categories become accessible navigation without inventing metadata."""

from pathlib import Path

from fastapi.testclient import TestClient

from nvis_hub.models import Registration
from nvis_hub.service import Hub
from nvis_hub.web import create_app


def test_project_and_reader_render_native_categories_with_current_group_open(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "index.md").write_text("# Welcome\n")
    (source / "operate.md").write_text("# Operate the system\n")
    (source / "navigation.rst").write_text(
        ".. toctree::\n   :caption: System guide\n\n"
        "   Overview <index>\n   How-to: Operate safely <operate>\n"
    )
    db = tmp_path / "hub.sqlite3"
    hub = Hub(db)
    hub.register(
        Registration(
            slug="system",
            title="System",
            description="System docs",
            repo_url="https://gitlab.example.com/team/system",
            source_mode="local",
            local_path=str(source),
            docs_paths=["index.md", "operate.md"],
            nav_path="navigation.rst",
        )
    )
    hub.refresh("system")
    client = TestClient(create_app(db))
    project = client.get("/projects/system")
    assert project.status_code == 200
    assert '<details class="document-category"' in project.text
    assert "How-to guides — getting something done" in project.text
    assert 'href="/projects/system/docs/operate.md"' in project.text
    reader = client.get("/projects/system/docs/operate.md")
    assert reader.status_code == 200
    assert '<details class="nav-category" open' in reader.text
    assert 'aria-current="page"' in reader.text


def test_curated_labels_group_by_mode_and_keep_source_context_and_order() -> None:
    from nvis_hub.navigation import group_navigation

    documents = [
        {"path": name, "title": name, "url": "/docs/" + name, "kind": None}
        for name in ["overview.md", "learn.md", "first.md", "second.md", "facts.md", "why.md"]
    ]
    labels = [
        "Overview",
        "Tutorial: Learn it",
        "How-to: First task",
        "How-to: Second task",
        "Reference: Facts",
        "Explanation: Why it works",
    ]
    rows = [{"title": "System guide", "path": None, "level": 0}]
    rows += [{**doc, "title": label, "level": 1} for doc, label in zip(documents, labels, strict=True)]
    groups = group_navigation(rows, documents, curated=True)
    assert [g["key"] for g in groups] == ["tutorial", "how-to", "reference", "explanation", "other"]
    how_to = groups[1]
    assert [e["title"] for e in how_to["entries"]] == ["First task", "Second task"]
    assert [e["context"] for e in how_to["entries"]] == ["System guide", "System guide"]
    assert not any(g["active"] for g in groups)
    assert rows[2]["title"] == "Tutorial: Learn it", "Grouping must not rewrite authored navigation"


def test_generated_navigation_uses_only_explicit_metadata_not_paths_or_heading_guesses() -> None:
    from nvis_hub.navigation import group_navigation

    documents = [
        {"path": "docs/how-to/task.md", "title": "How-to: Task", "url": "/task", "kind": None},
        {"path": "facts.md", "title": "Facts", "url": "/facts", "kind": "reference"},
    ]
    groups = group_navigation(documents, documents, curated=False)
    assert [g["key"] for g in groups] == ["reference", "other"]
    assert groups[0]["entries"][0]["path"] == "facts.md"
    assert groups[1]["entries"][0]["title"] == "How-to: Task"


def test_authored_caption_controls_category_and_preserves_nested_levels_and_active_page() -> None:
    from nvis_hub.navigation import group_navigation

    documents = [
        {"path": "identity.md", "title": "Identity", "url": "/identity", "kind": None},
        {"path": "policy.md", "title": "Policy", "url": "/policy", "kind": None},
    ]
    rows = [{"title": "Reference — the machinery, described", "path": None, "level": 0}]
    rows += [{**documents[0], "level": 1}, {**documents[1], "level": 2}]
    groups = group_navigation(rows, documents, curated=True, current_path="policy.md")
    assert len(groups) == 1
    assert groups[0]["key"] == "reference"
    assert groups[0]["active"] is True
    assert [e["level"] for e in groups[0]["entries"]] == [1, 2]
    assert groups[0]["entries"][1]["active"] is True
    assert groups[0]["entries"][0]["context"] is None


def test_all_published_pages_remain_available_once_and_empty_groups_are_omitted() -> None:
    from nvis_hub.navigation import group_navigation

    documents = [
        {"path": "one.md", "title": "One", "url": "/one", "kind": None},
        {"path": "two.md", "title": "Two", "url": "/two", "kind": None},
    ]
    rows = [documents[0], documents[0], {"path": "missing.md", "title": "Missing", "url": "/missing"}]
    groups = group_navigation(rows, documents, curated=True)
    assert len(groups) == 1
    assert groups[0]["key"] == "other"
    assert [e["path"] for e in groups[0]["entries"]] == ["one.md", "two.md"]


def test_distinct_authored_category_captions_remain_as_context_after_grouping() -> None:
    from nvis_hub.navigation import group_navigation

    documents = [
        {"path": "api.md", "title": "API", "url": "/api", "kind": None},
        {"path": "grammar.md", "title": "Grammar", "url": "/grammar", "kind": None},
    ]
    rows = [
        {"title": "Reference — API contracts", "path": None, "level": 0},
        documents[0],
        {"title": "Reference — Protocol grammar", "path": None, "level": 0},
        documents[1],
    ]
    groups = group_navigation(rows, documents, curated=True)
    assert len(groups) == 1
    assert [e["context"] for e in groups[0]["entries"]] == [
        "Reference — API contracts",
        "Reference — Protocol grammar",
    ]
