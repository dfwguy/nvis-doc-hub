"""Behavior coverage for durable, safe documentation publication."""

import json
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvis_hub.models import HubError, Registration
from nvis_hub.service import Hub


def write(root: Path, name: str, text: str) -> None:
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


@pytest.fixture
def source(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    write(root, "README.md", "# Atlas\n\nA cluster documentation collection.")
    write(
        root,
        "docs/index.md",
        "# Operations\n\n[Install](nested/install.md#power-on) ![Rack](images/rack.svg)\n\n[Unsafe](javascript:alert(1))\n<script>alert(1)</script>",
    )
    write(
        root,
        "docs/nested/install.md",
        "---\ntitle: Rack installation\ntopics: [rack, network]\ntype: how-to\n---\n# Installation\n\nPrepare the chassis.\n\n## Power on\n\nConnect the rack power cable.\n\n```sh\necho ready\n```\n\n## Power on\n\nSecond procedure.\n\n## 日本語\n\nUnicode heading.\n\n[Home](../index.md) [Download](../attachments/checklist.txt)",
    )
    write(root, "docs/images/rack.svg", '<svg xmlns="http://www.w3.org/2000/svg"><text>rack</text></svg>')
    write(root, "docs/attachments/checklist.txt", "Check rack power.")
    write(root, "docs/tests/fixture.md", "# Hidden fixture\nInvisible secretword")
    write(root, "docs/vendor/third.md", "# Vendored\nInvisible secretword")
    write(root, "docs/.hidden/secret.md", "# Hidden\nInvisible secretword")
    write(root, "docs/templates/starter.md", "# Template\nInvisible secretword")
    write(
        root,
        ".docs-pipeline/navigation.rst",
        "Cluster guide\n=============\n\n.. toctree::\n   :caption: Operate\n   :maxdepth: 2\n\n   Overview <../docs/index>\n   ../docs/nested/install\n",
    )
    return root


def registration(source: Path, **overrides: object) -> Registration:
    values: dict[str, object] = dict(
        slug="atlas",
        title="Atlas",
        description="Rack operations",
        repo_url="https://gitlab.example/nvis/atlas",
        docs_paths=["README.md", "docs"],
        nav_path=".docs-pipeline/navigation.rst",
        source_mode="local",
        local_path=str(source),
    )
    values.update(overrides)
    return Registration(**values)


def published(tmp_path: Path, source: Path) -> Hub:
    hub = Hub(tmp_path / "hub.sqlite3")
    hub.register(registration(source))
    hub.refresh("atlas")
    return hub


def test_publication_hosts_scoped_documents_with_provenance(tmp_path: Path, source: Path) -> None:
    hub = published(tmp_path, source)
    project = hub.get_project("atlas")
    assert project and project["document_count"] == 3
    assert project["revision"].startswith("content-sha256:")
    assert project["nav_mode"] == "curated"
    assert [item["title"] for item in project["navigation"]][:2] == ["Operate", "Overview"]
    doc = hub.get_document("atlas", "docs/nested/install.md")
    assert doc and doc["title"] == "Rack installation"
    assert doc["source_path"] == "docs/nested/install.md"
    assert doc["source_url"] is None  # A local digest is not a GitLab commit.
    assert doc["kind"] == "how-to" and doc["topics"] == ["rack", "network"]
    assert [heading["id"] for heading in doc["headings"]] == [
        "installation",
        "power-on",
        "power-on-2",
        "日本語",
    ]
    assert hub.search("secretword") == []


def test_rendered_links_assets_and_raw_html_are_safe(tmp_path: Path, source: Path) -> None:
    hub = published(tmp_path, source)
    doc = hub.get_document("atlas", "docs/index.md")
    assert doc
    assert "/projects/atlas/docs/docs/nested/install.md#power-on" in doc["html"]
    assert "/projects/atlas/assets/docs/images/rack.svg" in doc["html"]
    assert "<script>" not in doc["html"] and 'href="javascript:' not in doc["html"]
    assert "&lt;script&gt;" in doc["html"]
    asset = hub.get_asset("atlas", "docs/images/rack.svg")
    assert asset and asset[1] == "image/svg+xml"
    assert hub.get_asset("atlas", "../README.md") is None
    nested = hub.get_document("atlas", "docs/nested/install.md")
    assert nested and "/projects/atlas/assets/docs/attachments/checklist.txt" in nested["html"]


def test_sections_search_filters_and_plain_snippets_share_content(tmp_path: Path, source: Path) -> None:
    hub = published(tmp_path, source)
    results = hub.search("rack power", topic="rack", kind="how-to", project="atlas")
    assert results and results[0]["anchor"] == "power-on"
    assert results[0]["url"].endswith("/docs/nested/install.md#power-on")
    assert "<" not in results[0]["snippet"]
    doc = hub.get_document("atlas", results[0]["path"], results[0]["anchor"])
    assert doc and "Connect the rack power cable." in doc["text"]
    assert "Second procedure." not in doc["text"]
    assert "Second procedure." not in doc["markdown"]
    assert hub.get_document("atlas", "docs/nested/install.md", "missing") is None
    assert hub.search("rack", topic="absent") == []
    assert hub.facets() == {"topics": ["network", "rack"], "kinds": ["how-to"]}
    assert hub.search('"') == []


def test_changed_deleted_refresh_and_restart_are_atomic(tmp_path: Path, source: Path) -> None:
    hub = published(tmp_path, source)
    before = hub.get_project("atlas")
    (source / "docs/nested/install.md").unlink()
    write(source, "docs/index.md", "# Replacement\n\nNewly published replacementword.")
    hub.refresh("atlas")
    assert hub.get_document("atlas", "docs/nested/install.md") is None
    assert not hub.search("chassis")
    assert len(hub.search("replacementword")) == 1
    restarted = Hub(tmp_path / "hub.sqlite3")
    assert restarted.get_project("atlas")["revision"] != before["revision"]
    assert restarted.get_asset("atlas", "docs/images/rack.svg")
    (source / "docs/index.md").write_bytes(b"\xff\xfe")
    with pytest.raises(HubError):
        restarted.refresh("atlas")
    assert restarted.search("replacementword")
    assert restarted.get_project("atlas")["last_error"]


def test_explicit_selection_allows_excluded_directory(tmp_path: Path, source: Path) -> None:
    hub = Hub(tmp_path / "hub.sqlite3")
    hub.register(registration(source, docs_paths=["docs/tests"]))
    hub.refresh("atlas")
    assert len(hub.list_documents("atlas")) == 1
    assert hub.search("secretword")


def test_scope_traversal_and_symlinks_are_rejected(tmp_path: Path, source: Path) -> None:
    with pytest.raises(ValidationError):
        registration(source, docs_paths=["../outside"])
    (source / "docs/escape.md").symlink_to(source / "README.md")
    hub = Hub(tmp_path / "hub.sqlite3")
    hub.register(registration(source))
    with pytest.raises(HubError, match="symlink"):
        hub.refresh("atlas")


def test_snapshot_exact_revision_and_source_links(tmp_path: Path, source: Path) -> None:
    root = tmp_path / "snapshot"
    root.mkdir()
    (root / "repository").symlink_to(source, target_is_directory=True)
    revision = "a" * 40
    write(
        root,
        "manifest.json",
        json.dumps(
            {
                "repo_url": "https://gitlab.example/nvis/atlas",
                "revision": revision,
                "ref": "main",
                "acquisition_method": "GitLab MCP",
                "files": [
                    {
                        "path": path.relative_to(source).as_posix(),
                        "sha256": sha256(path.read_bytes()).hexdigest(),
                    }
                    for path in source.rglob("*")
                    if path.is_file()
                ],
            }
        ),
    )
    hub = Hub(tmp_path / "hub.sqlite3")
    hub.register(registration(source, source_mode="snapshot", local_path=str(root)))
    hub.refresh("atlas")
    doc = hub.get_document("atlas", "docs/index.md")
    assert doc and doc["revision"] == revision
    assert doc["source_url"] == f"https://gitlab.example/nvis/atlas/-/blob/{revision}/docs/index.md"
    assert hub.get_project("atlas")["source_mode"] == "snapshot"


def test_missing_scope_fails_without_replacing_prior_publication(tmp_path: Path, source: Path) -> None:
    hub = published(tmp_path, source)
    revision = hub.get_project("atlas")["revision"]
    hub.register(registration(source, docs_paths=["does-not-exist"]))
    with pytest.raises(HubError):
        hub.refresh("atlas")
    assert hub.get_project("atlas")["revision"] == revision
    assert hub.get_document("atlas", "README.md")


def test_protocol_and_embedded_credentials_rejected(source: Path) -> None:
    for url in [
        "https://token:secret@gitlab.example/nvis/atlas",
        "file:///etc/passwd",
        "http://gitlab.example/nvis/atlas",
    ]:
        with pytest.raises(ValidationError):
            registration(source, repo_url=url)


def test_unsupported_formats_reported_and_generated_navigation(tmp_path: Path, source: Path) -> None:
    write(source, "docs/advanced.rst", "Unsupported RST document\n========================")
    hub = Hub(tmp_path / "hub.sqlite3")
    hub.register(registration(source, nav_path=None, topics=["cluster"], kind="reference"))
    result = hub.refresh("atlas")
    assert result["nav_mode"] == "generated"
    assert any("advanced.rst" in warning for warning in result["warnings"])
    assert hub.facets() == {"topics": ["cluster"], "kinds": ["reference"]}


def test_snapshot_detects_changed_and_unmanifested_files(tmp_path: Path, source: Path) -> None:
    from hashlib import sha256

    root = tmp_path / "snapshot"
    root.mkdir()
    (root / "repository").symlink_to(source, target_is_directory=True)
    files = [
        {"path": path.relative_to(source).as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()}
        for path in source.rglob("*")
        if path.is_file()
    ]
    write(
        root,
        "manifest.json",
        json.dumps({"repo_url": "https://gitlab.example/nvis/atlas", "revision": "b" * 40, "files": files}),
    )
    hub = Hub(tmp_path / "hub.sqlite3")
    hub.register(registration(source, source_mode="snapshot", local_path=str(root)))
    hub.refresh("atlas")
    write(source, "docs/additional.md", "# Unmanifested file")
    with pytest.raises(HubError, match="integrity"):
        hub.refresh("atlas")
    (source / "docs/additional.md").unlink()
    write(source, "docs/index.md", "# Altered source")
    with pytest.raises(HubError, match="integrity"):
        hub.refresh("atlas")
    assert hub.get_document("atlas", "docs/index.md")["title"] == "Operations"


def test_source_only_links_and_svg_have_safe_behavior(tmp_path: Path, source: Path) -> None:
    from nvis_hub.content import render_document
    from nvis_hub.sources import AcquiredSource

    rendered = render_document(
        "# Links\n\n[Script](../scripts/task.sh) [Escape](../../outside)",
        "docs/page.md",
        registration(source),
        AcquiredSource(source, "c" * 40),
        {"docs/page.md"},
        set(),
    )
    assert f"https://gitlab.example/nvis/atlas/-/blob/{'c' * 40}/scripts/task.sh" in rendered["html"]
    assert "source-link" in rendered["html"]
    assert "outside" not in rendered["html"].split('href="')[-1].split('"')[0]
    write(
        source,
        "docs/images/rack.svg",
        '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><script>alert(1)</script><a href="javascript:alert(1)"><text>rack</text></a></svg>',
    )
    hub = published(tmp_path, source)
    svg, mime = hub.get_asset("atlas", "docs/images/rack.svg")
    assert b"<script" not in svg and b"onload" not in svg and b"javascript:" not in svg
    assert mime == "image/svg+xml"


def test_gitlab_archive_adapter_pins_revision_and_does_not_persist_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import tarfile
    from io import BytesIO

    import nvis_hub.sources as sources

    revision = "d" * 40
    archive_data = BytesIO()
    with tarfile.open(fileobj=archive_data, mode="w:gz") as archive:
        payload = b"# Live import\n\nExactrevision content."
        entry = tarfile.TarInfo("repository-root/docs/index.md")
        entry.size = len(payload)
        archive.addfile(entry, BytesIO(payload))
    calls = []

    def fetch(url: str, token: str | None) -> bytes:
        calls.append((url, token))
        return json.dumps({"id": revision}).encode() if "/commits/" in url else archive_data.getvalue()

    monkeypatch.setattr(sources, "_fetch", fetch)
    monkeypatch.setenv("NVIS_TEST_TOKEN", "private-token-that-must-never-persist")
    hub = Hub(tmp_path / "hub.sqlite3")
    hub.register(
        Registration(
            slug="live",
            title="Live",
            description="Adapter test",
            repo_url="https://gitlab.example/team/live",
            ref="feat/docs",
            docs_paths=["docs"],
            credential_env="NVIS_TEST_TOKEN",
        )
    )
    hub.refresh("live")
    assert "/commits/feat%2Fdocs" in calls[0][0]
    assert calls[1][0].endswith("?sha=" + revision)
    assert all(token == "private-token-that-must-never-persist" for _, token in calls)
    assert "private-token-that-must-never-persist" not in json.dumps(hub.list_projects())
    assert b"private-token-that-must-never-persist" not in (tmp_path / "hub.sqlite3").read_bytes()
    assert hub.search("Exactrevision")[0]["revision"] == revision


def test_archive_traversal_and_symlinks_are_rejected(tmp_path: Path) -> None:
    import tarfile
    from io import BytesIO

    from nvis_hub.sources import _extract_archive

    for name, symlink in [("root/../../escape", False), ("root/docs/link", True)]:
        data = BytesIO()
        with tarfile.open(fileobj=data, mode="w:gz") as archive:
            item = tarfile.TarInfo(name)
            if symlink:
                item.type = tarfile.SYMTYPE
                item.linkname = "/etc/passwd"
            archive.addfile(item)
        with pytest.raises(HubError, match="unsafe"):
            _extract_archive(data.getvalue(), tmp_path)


def test_search_falls_back_to_page_when_terms_span_sections(tmp_path: Path, source: Path) -> None:
    hub = published(tmp_path, source)
    result = hub.search("chassis second")
    assert len(result) == 1
    assert result[0]["path"] == "docs/nested/install.md"
    assert result[0]["anchor"] == ""
    assert not result[0]["url"].endswith("#")
    focused = hub.search("rack power", topic="rack")
    assert all(item["anchor"] for item in focused)


def test_inline_markup_preserves_readable_titles_and_expected_anchors(tmp_path: Path, source: Path) -> None:
    write(
        source,
        "docs/inline.md",
        "# Using `git config` safely\n\n## **Network** and *power*\n\nInline **rack** power stays readable.\n\n[Jump](#network-and-power)",
    )
    hub = published(tmp_path, source)
    doc = hub.get_document("atlas", "docs/inline.md")
    assert doc["title"] == "Using git config safely"
    assert [heading["id"] for heading in doc["headings"]] == ["using-git-config-safely", "network-and-power"]
    assert "Inline rack power stays readable." in doc["text"]


def test_svg_preserves_authored_diagram_styles_without_network_or_execution(
    tmp_path: Path, source: Path
) -> None:
    import xml.etree.ElementTree as ET

    write(
        source,
        "docs/images/rack.svg",
        """<svg xmlns="http://www.w3.org/2000/svg" id="diagram" style="max-width:1600px;background-color:white" viewBox="0 0 240 80">
    <style>@import url("https://evil.example/steal.css");
      #diagram .node rect { fill:#eee;stroke:#999;stroke-width:1px }
      #diagram .node text { fill:#333;font-family:Arial,sans-serif;font-size:16px }
      #diagram .edge { fill:none;stroke:url(#gradient);marker-end:url("#arrow") }
      .bad { fill:url(https://evil.example/image.svg);stroke:expression(alert(1));background-image:url(data:image/svg+xml,evil);behavior:url(evil.htc) }
    </style>
    <defs><linearGradient id="gradient"><stop stop-color="#999"/></linearGradient><marker id="arrow"><path d="M0 0L5 5"/></marker></defs>
    <g class="node"><rect width="200" height="50"/><text x="10" y="25" style="stroke:none;fill:#333;background-image:url(https://evil.example/track)">Readable node</text></g>
    <path class="edge" marker-end="url(#arrow)" d="M0 60L240 60"/>
    <image href="https://evil.example/fetch"/><script>alert(1)</script></svg>""",
    )
    hub = published(tmp_path, source)
    svg, mime = hub.get_asset("atlas", "docs/images/rack.svg")
    parsed = ET.fromstring(svg)
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    styles = "".join(element.text or "" for element in parsed.findall("svg:style", namespace))
    assert ".node rect" in styles and "fill:#eee" in styles and "stroke:#999" in styles
    assert "font-size:16px" in styles and "fill:#333" in styles
    assert "url(#gradient)" in styles and "#arrow" in styles
    text = parsed.find(".//svg:text", namespace)
    assert text is not None and "stroke:none" in text.attrib["style"]
    edge = parsed.find("svg:path", namespace)
    assert edge is not None and edge.attrib["marker-end"] == "url(#arrow)"
    assert (
        "evil.example" not in svg.decode()
        and "expression" not in svg.decode()
        and "@import" not in svg.decode()
    )
    assert "data:" not in svg.decode() and b"<script" not in svg
    assert mime == "image/svg+xml"


def test_title_match_does_not_fabricate_unrelated_section_results(tmp_path: Path, source: Path) -> None:
    write(
        source,
        "docs/title.md",
        "# Two layers\n\nPublication architecture.\n\n## Sources and version selection\n\nRegister the authored repository.\n\n## Import boundary\n\nEach publication is atomic.",
    )
    write(
        source,
        "docs/metadata.md",
        "---\ntitle: Unique metadata title\n---\n# Plain introduction\n\n## Elsewhere\n\nUnrelated content.",
    )
    hub = published(tmp_path, source)
    title_results = hub.search("two layers")
    assert len(title_results) == 1
    assert title_results[0]["anchor"] == "two-layers"
    metadata_results = hub.search("unique metadata")
    assert len(metadata_results) == 1 and metadata_results[0]["anchor"] == ""
    body_results = hub.search("authored repository")
    assert len(body_results) == 1
    assert body_results[0]["anchor"] == "sources-and-version-selection"


def test_failed_reregistration_keeps_publication_provenance_until_success(
    tmp_path: Path, source: Path
) -> None:
    import sqlite3

    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    (snapshot / "repository").symlink_to(source, target_is_directory=True)
    write(
        snapshot,
        "manifest.json",
        json.dumps(
            {
                "repo_url": "https://gitlab.example/nvis/atlas",
                "revision": "e" * 40,
                "ref": "main",
                "files": [
                    {
                        "path": path.relative_to(source).as_posix(),
                        "sha256": sha256(path.read_bytes()).hexdigest(),
                    }
                    for path in source.rglob("*")
                    if path.is_file()
                ],
            }
        ),
    )
    database = tmp_path / "hub.sqlite3"
    hub = Hub(database)
    hub.register(registration(source, source_mode="snapshot", local_path=str(snapshot)))
    hub.refresh("atlas")
    old_document = hub.get_document("atlas", "docs/index.md")
    # Simulate a publication written before source fields were pinned in metadata.
    with sqlite3.connect(database) as connection:
        connection.execute(
            "UPDATE projects SET publication=json_remove(publication,'$.repo_url','$.ref','$.source_mode')"
        )
    desired = {"repo_url": "https://gitlab.example/nvis/replacement", "ref": "work", "source_mode": "local"}
    project = hub.register(registration(source, **desired, docs_paths=["missing"]))
    assert project["repo_url"] == "https://gitlab.example/nvis/atlas"
    assert project["source_mode"] == "snapshot" and project["ref"] == "main"
    assert project["pending_source"] == desired
    with pytest.raises(HubError):
        hub.refresh("atlas")
    restarted = Hub(database)
    project = restarted.get_project("atlas")
    assert project["revision"] == "e" * 40
    assert project["source_mode"] == "snapshot" and project["ref"] == "main"
    assert project["repo_url"] == "https://gitlab.example/nvis/atlas"
    assert restarted.get_document("atlas", "docs/index.md") == old_document
    assert project["acquisition"]["method"] != "local"
    write(source, "missing/page.md", "# Replacement publication")
    project = restarted.refresh("atlas")
    assert {key: project[key] for key in desired} == desired
    assert project.get("pending_source") is None
    assert project["acquisition"]["method"] == "local"
    document = restarted.get_document("atlas", "missing/page.md")
    assert document["source_mode"] == "local" and document["source_url"] is None
    assert document["revision"] == project["revision"]
