"""Public reading surfaces exercise the same persisted publications as the service."""

from pathlib import Path

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
    assert "No projects published yet" in client.get("/").text
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


def test_reader_tables_and_contents_have_narrow_layout_affordances(tmp_path: Path) -> None:
    client = published_client(tmp_path)
    result = client.get("/search?q=switch")
    assert '<details class="search-filters" open' in result.text
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
