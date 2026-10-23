"""Real document browsing and aggregate popularity over current publications."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from nvis_hub.models import Registration
from nvis_hub.service import Hub

CARD_FIELDS = {
    "path",
    "title",
    "kind",
    "topics",
    "url",
    "revision",
    "project_slug",
    "project_title",
    "view_count",
}


@pytest.fixture
def discovery(tmp_path: Path) -> tuple[Hub, Path]:
    source = tmp_path / "source"
    docs = source / "docs"
    docs.mkdir(parents=True)
    (docs / "alpha.md").write_text(
        "---\ntitle: Alpha operations\ntype: how-to\ntopics: [network, rack]\n---\n"
        "# Connect\n\nConnect the network cable."
    )
    (docs / "beta.md").write_text(
        "---\ntitle: Beta reference\ntype: reference\ntopics: [network]\n---\n"
        "# Ports\n\nNetwork port reference."
    )
    (docs / "unclassified.md").write_text("# Unclassified\n\nAn authored note.")
    hub = Hub(tmp_path / "hub.sqlite3")
    for slug, title in (("atlas", "Atlas"), ("boreal", "Boreal")):
        hub.register(
            Registration(
                slug=slug,
                title=title,
                description="Documentation",
                source_mode="local",
                repo_url=f"https://gitlab.example/nvis/{slug}",
                local_path=str(source),
                docs_paths=["docs"],
            )
        )
        hub.refresh(slug)
    return hub, source


def test_browse_filters_counts_and_pagination_match_actual_metadata(
    discovery: tuple[Hub, Path],
) -> None:
    hub, _ = discovery

    documents = hub.browse_documents(limit=10000)

    assert len(documents) == hub.document_count() == 6
    assert all(set(doc) == CARD_FIELDS for doc in documents)
    assert [(doc["title"], doc["project_slug"]) for doc in documents] == [
        ("Alpha operations", "atlas"),
        ("Alpha operations", "boreal"),
        ("Beta reference", "atlas"),
        ("Beta reference", "boreal"),
        ("Unclassified", "atlas"),
        ("Unclassified", "boreal"),
    ]
    assert hub.browse_documents(limit=2, offset=2) == documents[2:4]
    filtered = hub.browse_documents(project="boreal", topic="network", kind="reference")
    assert [(doc["project_slug"], doc["path"]) for doc in filtered] == [("boreal", "docs/beta.md")]
    assert hub.document_count(project="boreal", topic="network", kind="reference") == 1
    assert hub.document_count(topic="rack") == 2
    assert hub.browse_documents(project="missing") == []
    assert hub.browse_documents(kind="tutorial") == []
    assert hub.document_count(topic="network' OR 1=1 --") == 0
    unclassified = next(doc for doc in documents if doc["path"] == "docs/unclassified.md")
    assert unclassified["kind"] is None and unclassified["topics"] == []
    assert all(doc["view_count"] == 0 for doc in documents)


def test_popularity_starts_empty_and_reads_are_side_effect_free(
    discovery: tuple[Hub, Path],
) -> None:
    hub, _ = discovery
    documents_before = hub.list_documents("atlas")
    document_before = hub.get_document("atlas", "docs/alpha.md")
    results_before = hub.search("network")

    assert hub.popular_documents() == []
    assert hub.get_document("atlas", "docs/alpha.md", "connect") is not None
    assert hub.get_asset("atlas", "docs/missing.svg") is None
    assert hub.search("") == []
    assert hub.suggest("net")
    hub.browse_documents()
    hub.document_count()

    assert hub.popular_documents() == []
    assert hub.list_documents("atlas") == documents_before
    assert hub.get_document("atlas", "docs/alpha.md") == document_before
    assert hub.search("network") == results_before
    assert all(set(doc) == {"path", "title", "kind", "topics", "url", "revision"} for doc in documents_before)


def test_opens_are_explicit_valid_and_scoped_to_project(discovery: tuple[Hub, Path]) -> None:
    hub, _ = discovery
    assert hub.record_document_view("atlas", "docs/alpha.md") is True
    assert hub.record_document_view("atlas", "docs/alpha.md") is True
    assert hub.record_document_view("boreal", "docs/alpha.md") is True
    assert hub.record_document_view("missing", "docs/alpha.md") is False
    assert hub.record_document_view("atlas", "docs/missing.md") is False
    assert hub.record_document_view("atlas", "../docs/alpha.md") is False

    popular = hub.popular_documents()

    assert [(doc["project_slug"], doc["path"], doc["view_count"]) for doc in popular] == [
        ("atlas", "docs/alpha.md", 2),
        ("boreal", "docs/alpha.md", 1),
    ]
    assert len(hub.popular_documents(limit=1)) == 1
    assert all(set(doc) == CARD_FIELDS for doc in popular)
    assert popular[0]["url"] == "/projects/atlas/docs/docs/alpha.md"
    assert hub.browse_documents(project="atlas")[0]["view_count"] == 2


def test_popularity_survives_restart_and_refresh_but_excludes_removed_documents(
    discovery: tuple[Hub, Path],
) -> None:
    hub, source = discovery
    hub.record_document_view("atlas", "docs/alpha.md")
    hub.record_document_view("atlas", "docs/beta.md")
    restarted = Hub(hub.store.path)
    assert [doc["view_count"] for doc in restarted.popular_documents()] == [1, 1]

    (source / "docs/alpha.md").write_text("# Renamed alpha\n\nUpdated source content.")
    restarted.refresh("atlas")
    renamed = next(doc for doc in restarted.popular_documents() if doc["path"] == "docs/alpha.md")
    assert renamed["title"] == "Renamed alpha" and renamed["view_count"] == 1

    (source / "docs/alpha.md").unlink()
    restarted.refresh("atlas")

    assert [doc["path"] for doc in restarted.popular_documents()] == ["docs/beta.md"]
    assert restarted.record_document_view("atlas", "docs/alpha.md") is False
    assert restarted.document_count(project="atlas") == 2
    assert restarted.document_count() == 5


def test_popularity_ties_sort_by_title_project_and_path(discovery: tuple[Hub, Path]) -> None:
    hub, _ = discovery
    for slug, path in (
        ("boreal", "docs/beta.md"),
        ("boreal", "docs/alpha.md"),
        ("atlas", "docs/beta.md"),
        ("atlas", "docs/alpha.md"),
    ):
        hub.record_document_view(slug, path)

    assert [(doc["title"], doc["project_slug"]) for doc in hub.popular_documents()] == [
        ("Alpha operations", "atlas"),
        ("Alpha operations", "boreal"),
        ("Beta reference", "atlas"),
        ("Beta reference", "boreal"),
    ]


def test_simultaneous_opens_increment_without_lost_counts(discovery: tuple[Hub, Path]) -> None:
    hub, _ = discovery
    with ThreadPoolExecutor(max_workers=6) as executor:
        recorded = list(executor.map(lambda _: hub.record_document_view("atlas", "docs/alpha.md"), range(30)))

    assert all(recorded)
    assert hub.popular_documents()[0]["view_count"] == 30


def test_existing_database_adds_popularity_without_replacing_publications(
    discovery: tuple[Hub, Path],
) -> None:
    hub, _ = discovery
    before = hub.list_documents("atlas")
    with hub.store.connection() as database:
        database.execute("DROP TABLE document_views")

    upgraded = Hub(hub.store.path)

    assert upgraded.list_documents("atlas") == before
    assert upgraded.popular_documents() == []
    assert upgraded.record_document_view("atlas", "docs/alpha.md") is True
    assert upgraded.popular_documents()[0]["view_count"] == 1


def test_same_title_ties_use_authored_path_after_project(discovery: tuple[Hub, Path]) -> None:
    hub, source = discovery
    (source / "docs/0-alpha.md").write_text("# Alpha operations\n\nAnother authored page.")
    hub.refresh("atlas")
    for path in ("docs/alpha.md", "docs/0-alpha.md"):
        hub.record_document_view("atlas", path)

    assert [doc["path"] for doc in hub.popular_documents()] == [
        "docs/0-alpha.md",
        "docs/alpha.md",
    ]
