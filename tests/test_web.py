"""Public reading surfaces exercise the same persisted publications as the service."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from nvis_hub.models import Registration
from nvis_hub.service import Hub
from nvis_hub.web import create_app


def published_client(tmp_path: Path) -> TestClient:
    source = tmp_path / "source"
    (source / "docs" / "guides").mkdir(parents=True)
    (source / "docs" / "index.md").write_text(
        "# Bringup docs\n\n[Start here](guides/setup.md#network-check)\n", encoding="utf-8"
    )
    (source / "docs" / "guides" / "setup.md").write_text(
        "---\ntype: how-to\ntopics: [networking]\n---\n"
        "# Network setup\n\n## Network check\n\nVerify the switch.\n\n"
        "```sh\nprintf 'ready'\n```\n\n![Topology](../topology.png)\n\n"
        "| Check | Value |\n|---|---|\n| Switch | Ready |\n",
        encoding="utf-8",
    )
    (source / "docs" / "topology.png").write_bytes(b"image-content")
    db = tmp_path / "hub.db"
    hub = Hub(db)
    hub.register(
        Registration(
            slug="bringup",
            title="Cluster bringup",
            description="Bring clusters online.",
            repo_url="https://gitlab.example.com/team/bringup",
            source_mode="local",
            local_path=str(source),
            docs_paths=["docs"],
        )
    )
    hub.refresh("bringup")
    return TestClient(create_app(db))


def test_catalog_search_and_nested_reader(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    catalog = client.get("/")
    assert catalog.status_code == 200
    assert "Cluster bringup" in catalog.text
    assert 'name="q"' in catalog.text
    result = client.get("/search", params={"q": "switch", "topic": "networking"})
    assert result.status_code == 200
    assert "Network check" in result.text
    assert "/projects/bringup/docs/docs/guides/setup.md#network-check" in result.text
    reader = client.get("/projects/bringup/docs/docs/guides/setup.md")
    assert reader.status_code == 200
    assert "printf" in reader.text
    assert "Source revision" in reader.text
    assert 'id="network-check"' in reader.text
    assert "Content-Security-Policy" in reader.headers
    assert client.get("/projects/bringup/assets/docs/topology.png").content == b"image-content"


def test_empty_no_matches_missing_and_asset_safety(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path / "empty.db"))
    assert "No documents published yet" in client.get("/").text
    assert "No matching documentation" in client.get("/search?q=nonexistent").text
    assert client.get("/projects/missing").status_code == 404
    assert client.get("/projects/missing/docs/README.md").status_code == 404
    assert client.get("/projects/missing/assets/secret.txt").status_code == 404
    assert client.get("/api/projects").json() == []


def test_filters_and_source_status_are_real(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    assert "No matching documentation" in client.get("/search?q=switch&kind=tutorial").text
    assert "Bringup docs" in client.get("/projects/bringup").text
    status = client.get("/sources")
    assert status.status_code == 200
    assert "Local source" in status.text
    assert "nvis-hub" in status.text
    assert client.get("/api/search?q=switch").json()[0]["project_slug"] == "bringup"


def test_suggestions_return_clickable_section_context_without_changing_search(tmp_path: Path) -> None:
    client = published_client(tmp_path)

    response = client.get("/api/search/suggestions", params={"q": "swi"})

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    result = results[0]
    assert set(result) == {"project_slug", "project_title", "title", "heading", "snippet", "url"}
    assert result["project_slug"] == "bringup"
    assert result["project_title"] == "Cluster bringup"
    assert result["title"] == "Network setup"
    assert result["heading"] == "Network check"
    assert result["url"] == "/projects/bringup/docs/docs/guides/setup.md#network-check"
    assert "Verify the switch." in result["snippet"]
    assert "<" not in result["snippet"]
    assert client.get(result["url"]).status_code == 200
    assert client.get("/api/search", params={"q": "swi"}).json() == []
    assert client.get("/api/search", params={"q": "switch"}).json()[0]["heading"] == "Network check"


def test_suggestions_apply_project_topic_and_kind_filters(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    hub = client.app.state.hub
    hub.register(
        Registration(
            slug="other",
            title="Other project",
            description="Another publication.",
            repo_url="https://gitlab.example.com/team/other",
            source_mode="local",
            local_path=str(tmp_path / "source"),
            docs_paths=["docs"],
        )
    )
    hub.refresh("other")
    unfiltered = client.get("/api/search/suggestions", params={"q": "swi"})
    assert unfiltered.status_code == 200
    assert len(unfiltered.json()) == 2

    filters = {"q": "swi", "project": "bringup", "topic": "networking", "kind": "how-to"}
    results = client.get("/api/search/suggestions", params=filters).json()

    assert len(results) == 1
    assert results[0]["project_slug"] == "bringup"
    for key, value in [("project", "missing"), ("topic", "rack"), ("kind", "tutorial")]:
        assert client.get("/api/search/suggestions", params={**filters, key: value}).json() == []


@pytest.mark.parametrize("query", ["", " ", "a", " a ", '""', "***", "() : -"])
def test_suggestions_ignore_short_or_punctuation_only_queries(tmp_path: Path, query: str) -> None:
    client = published_client(tmp_path)

    response = client.get("/api/search/suggestions", params={"q": query})

    assert response.status_code == 200
    assert response.json() == []


def test_suggestions_validate_raw_query_length_before_trimming(tmp_path: Path) -> None:
    client = published_client(tmp_path)

    for query in ["s" * 201, " " * 201, "swi" + " " * 198]:
        response = client.get("/api/search/suggestions", params={"q": query})
        assert response.status_code == 400
    boundary = client.get("/api/search/suggestions", params={"q": " " * 197 + "swi"})
    assert boundary.status_code == 200
    assert boundary.json()[0]["heading"] == "Network check"


def test_suggestions_prefix_the_final_term_even_after_many_completed_terms(tmp_path: Path) -> None:
    client = published_client(tmp_path)

    response = client.get("/api/search/suggestions", params={"q": "check " * 32 + "zz"})

    assert response.status_code == 200
    assert response.json() == []
    matching = client.get("/api/search/suggestions", params={"q": "check " * 32 + "swi"})
    assert matching.status_code == 200
    assert matching.json()[0]["heading"] == "Network check"


def test_reader_tables_and_contents_have_narrow_layout_affordances(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    result = client.get("/search?q=switch")
    assert '<legend class="sr-only">Filter documents</legend>' in result.text
    assert 'id="project-filter"' in result.text
    reader = client.get("/projects/bringup/docs/docs/guides/setup.md")
    assert 'class="mobile-contents"' in reader.text
    assert 'class="table-scroll"' in reader.text
    assert "Scroll horizontally to see all columns." in reader.text
    assert 'href="None"' not in reader.text


def test_source_status_shows_pending_registration_without_relabeling_publication(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    client.app.state.hub.register(
        Registration(
            slug="bringup",
            title="Cluster bringup",
            description="Bring clusters online.",
            repo_url="https://gitlab.example.com/team/next",
            ref="next",
            source_mode="local",
            local_path=str(tmp_path / "missing"),
            docs_paths=["docs"],
        )
    )
    status = client.get("/sources")
    assert "Registration changed" in status.text
    assert "awaiting a successful refresh" in status.text


def test_unified_discovery_replaces_duplicate_destinations_and_project_previews(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    for route in ["/", "/search"]:
        response = client.get(route)
        assert response.status_code == 200
        assert "<h1>Browse documentation</h1>" in response.text
        assert "Global search" not in response.text
        assert "All documentation" not in response.text
        assert "Browse projects" not in response.text
        assert ">Explore popular documentation</h2>" in response.text
        assert "No popular documentation yet" in response.text
        assert response.text.count('class="discovery-shelf"') == 1
        assert 'class="document-card"' not in response.text
        assert "From Cluster bringup" not in response.text
        assert 'class="project-navigation"' not in response.text
        assert "data-discovery-form" in response.text


def test_empty_query_can_browse_and_filter_documents_on_either_entry_route(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    for route in ["/", "/search"]:
        response = client.get(route, params={"view": "all", "kind": "how-to"})
        assert response.status_code == 200
        assert "Network setup" in response.text
        assert "Bringup docs" not in response.text
        assert "1 document" in response.text
        assert "Explore documentation" not in response.text
    assert "No matching documentation" in client.get("/?kind=tutorial").text


def test_only_successful_browser_reader_opens_feed_shared_popularity(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    hub = client.app.state.hub
    assert hub.popular_documents() == []
    assert client.get("/api/projects").status_code == 200
    client.get("/search?q=switch")
    client.get("/api/search/suggestions?q=swi")
    client.get("/projects/bringup/docs/missing.md")
    assert hub.popular_documents() == []
    assert client.get("/projects/bringup/docs/docs/guides/setup.md").status_code == 200
    assert hub.popular_documents()[0]["view_count"] == 1
    home = client.get("/").text
    assert ">Explore popular documentation</h2>" in home
    assert "1 open" in home
    assert hub.popular_documents()[0]["view_count"] == 1


def test_default_discovery_does_not_fetch_project_preview_collections(tmp_path: Path) -> None:
    client = published_client(tmp_path)

    def unexpected_preview(*args: object, **kwargs: object) -> None:
        raise AssertionError("The default view must not enumerate project document previews")

    client.app.state.hub.browse_documents = unexpected_preview
    response = client.get("/")
    assert response.status_code == 200
    assert "No popular documentation yet" in response.text


def test_reading_shows_only_current_document_sections_not_a_project_directory(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    hub = client.app.state.hub
    hub.register(
        Registration(
            slug="other",
            title="Other project",
            description="Another project",
            repo_url="https://gitlab.example.com/team/other",
            source_mode="local",
            local_path=str(tmp_path / "source"),
            docs_paths=["docs"],
        )
    )
    hub.refresh("other")
    for route in ["/projects/bringup", "/projects/bringup/docs/docs/guides/setup.md"]:
        response = client.get(route)
        assert response.status_code == 200
        assert 'aria-label="Document sections"' in response.text
        assert "Other project" not in response.text
        assert 'class="project-nav-link"' not in response.text
        assert "Network setup" in response.text
