"""Authored navigation and explicit classification from real source files."""

from pathlib import Path

import pytest

from nvis_hub.content import Publication, prepare
from nvis_hub.models import HubError, Registration
from nvis_hub.sources import AcquiredSource


def write(root: Path, path: str, text: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def publication(root: Path, nav_path: str | None, **overrides: object) -> Publication:
    values: dict[str, object] = {
        "slug": "atlas",
        "title": "Atlas",
        "description": "Authored navigation",
        "repo_url": "https://gitlab.example/nvis/atlas",
        "docs_paths": ["docs"],
        "nav_path": nav_path,
        "source_mode": "local",
        "local_path": str(root),
    }
    values.update(overrides)
    return prepare(AcquiredSource(root, "a" * 40), Registration(**values))


@pytest.mark.parametrize("suffix", ["yml", "yaml"])
def test_yaml_preserves_root_captions_titles_order_and_nested_entries(tmp_path: Path, suffix: str) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    write(tmp_path, "docs/start.md", "# Page heading")
    write(tmp_path, "docs/identity/index.md", "# Identity heading")
    write(tmp_path, "docs/identity/policies.md", "# Policy heading")
    write(tmp_path, "docs/catalog/README.md", "# Catalog heading")
    write(tmp_path, "docs/unlisted.md", "# Unlisted page")
    nav_path = f"docs/_toc.{suffix}"
    write(
        tmp_path,
        nav_path,
        """root: index
subtrees:
  - caption: Tutorials — learning by doing
    entries:
      - file: start
        title: Follow this lesson
  - caption: Reference — the machinery, described
    entries:
      - file: identity
        title: Identity and authorization
        entries:
          - file: identity/policies
            title: Policy schema
      - file: catalog
""",
    )

    result = publication(tmp_path, nav_path)

    assert result.nav_mode == "curated"
    assert result.warnings == []
    assert [(row["title"], row["path"], row["level"]) for row in result.navigation] == [
        ("Welcome", "docs/index.md", 1),
        ("Tutorials — learning by doing", None, 0),
        ("Follow this lesson", "docs/start.md", 1),
        ("Reference — the machinery, described", None, 0),
        ("Identity and authorization", "docs/identity/index.md", 1),
        ("Policy schema", "docs/identity/policies.md", 2),
        ("Catalog heading", "docs/catalog/README.md", 1),
        ("Additional documentation", None, 0),
        ("Unlisted page", "docs/unlisted.md", 1),
    ]
    assert result.navigation[5]["url"] == "/projects/atlas/docs/docs/identity/policies.md"
    assert {row["path"] for row in result.navigation if row["path"]} == {
        doc["path"] for doc in result.documents
    }


def test_yaml_unpublished_entries_warn_and_keep_all_published_documents(tmp_path: Path) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    write(tmp_path, "docs/extra.md", "# Extra page")
    write(
        tmp_path,
        "docs/_toc.yml",
        "root: index\nsubtrees:\n  - caption: Reference\n    entries:\n      - file: missing\n",
    )

    result = publication(tmp_path, "docs/_toc.yml")

    assert result.nav_mode == "curated"
    assert any("unpublished navigation entry: missing" in warning for warning in result.warnings)
    assert [(row["title"], row["path"]) for row in result.navigation] == [
        ("Welcome", "docs/index.md"),
        ("Reference", None),
        ("Additional documentation", None),
        ("Extra page", "docs/extra.md"),
    ]


@pytest.mark.parametrize(
    "target",
    ["../../outside", "/outside", "https://evil.example/page", "http://[", "..%2f..%2foutside", "C:/outside"],
)
def test_yaml_unsafe_targets_cannot_select_published_repository_paths(tmp_path: Path, target: str) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    write(tmp_path, "outside.md", "# Outside page")
    write(tmp_path, "docs/_toc.yml", f"root: '{target}'\n")

    result = publication(tmp_path, "docs/_toc.yml", docs_paths=["docs", "outside.md"])

    assert result.nav_mode == "generated"
    assert any("Unsupported or unpublished navigation entry" in warning for warning in result.warnings)
    assert {row["path"] for row in result.navigation} == {"docs/index.md", "outside.md"}


def test_yaml_resolves_safe_parent_reference_relative_to_registered_toc(tmp_path: Path) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    write(tmp_path, "README.md", "# Repository introduction")
    write(tmp_path, "docs/_toc.yml", "root: ../README\n")

    result = publication(tmp_path, "docs/_toc.yml", docs_paths=["docs", "README.md"])

    assert result.nav_mode == "curated"
    assert result.navigation[0]["path"] == "README.md"
    assert result.warnings == []


@pytest.mark.parametrize(
    "text",
    [
        "root: [unterminated",
        "- not a mapping\n",
        "root: index\nunknown_schema: true\n",
        "root: !!timestamp 2026-13-01\n",
        "root: index\nsubtrees: wrong\n",
        "root: index\nsubtrees:\n  - caption: Reference\n    entries:\n      - file: [index]\n",
        "root: index\nsubtrees:\n  - caption: Reference\n    entries:\n      - file: index\n        title: 7\n",
        "root: index\nsubtrees:\n  - caption: Reference\n    entries:\n      - file: index\n        url: https://example.com\n",
        "root: index\nsubtrees:\n  - caption: Reference\n    entries:\n      - &cycle\n        file: index\n        entries: [*cycle]\n",
    ],
)
def test_invalid_yaml_uses_generated_navigation_with_safe_notice(tmp_path: Path, text: str) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    write(tmp_path, "docs/_toc.yml", text)

    result = publication(tmp_path, "docs/_toc.yml")

    assert result.nav_mode == "generated"
    assert result.navigation == [
        {"title": "Welcome", "path": "docs/index.md", "level": 1, "url": "/projects/atlas/docs/docs/index.md"}
    ]
    assert any(
        "YAML navigation" in warning and "generated navigation used" in warning for warning in result.warnings
    )


def test_yaml_object_tags_are_data_errors_and_never_execute(tmp_path: Path) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    marker = tmp_path / "executed"
    write(
        tmp_path,
        "docs/_toc.yml",
        f"root: !!python/object/apply:os.system ['touch {marker}']\n",
    )

    result = publication(tmp_path, "docs/_toc.yml")

    assert not marker.exists()
    assert result.nav_mode == "generated"
    assert any("YAML navigation" in warning for warning in result.warnings)


def test_yaml_excessive_nesting_and_alias_expansion_have_bounded_fallback(tmp_path: Path) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    deeply_nested = "root: index\nsubtrees:\n  - caption: Reference\n    entries:\n"
    for _ in range(70):
        deeply_nested += " " * (6 + _ * 4) + "- file: index\n" + " " * (8 + _ * 4) + "entries:\n"
    deeply_nested += " " * (6 + 70 * 4) + "- file: index\n"
    aliases = "root: index\nsubtrees:\n  - caption: Reference\n    entries:\n      - &a {file: index}\n"
    for index in range(1, 5):
        previous = "a" if index == 1 else f"a{index - 1}"
        aliases += f"      - &a{index} {{file: index, entries: [" + ", ".join([f"*{previous}"] * 8) + "]}\n"
    for text in [deeply_nested, aliases, "root: " + "[" * 2000 + "index" + "]" * 2000]:
        write(tmp_path, "docs/_toc.yml", text)

        result = publication(tmp_path, "docs/_toc.yml")

        assert result.nav_mode == "generated"
        assert any("YAML navigation" in warning for warning in result.warnings)


def test_yaml_merge_alias_expansion_is_bounded_before_mapping_construction(tmp_path: Path) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    text = "root: index\nsubtrees:\n  - &a {caption: Reference, entries: [{file: index}]}\n"
    for index in range(1, 5):
        previous = "a" if index == 1 else f"a{index - 1}"
        text += f"  - &a{index} {{<<: [" + ", ".join([f"*{previous}"] * 8) + "]}\n"
    write(tmp_path, "docs/_toc.yml", text)

    result = publication(tmp_path, "docs/_toc.yml")

    assert result.nav_mode == "generated"
    assert any("YAML navigation" in warning for warning in result.warnings)


@pytest.mark.parametrize("data", [b"\xff\xfe", b"root: " + b"9" * 5000, b"#" * 262145])
def test_invalid_encoding_and_excessive_yaml_size_or_scalar_use_fallback(tmp_path: Path, data: bytes) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    (tmp_path / "docs/_toc.yml").write_bytes(data)

    result = publication(tmp_path, "docs/_toc.yml")

    assert result.nav_mode == "generated"
    assert any("YAML navigation" in warning for warning in result.warnings)


def test_yaml_requires_explicit_navigation_registration(tmp_path: Path) -> None:
    write(tmp_path, "docs/index.md", "# Welcome")
    write(tmp_path, "docs/_toc.yml", "root: index\n")

    result = publication(tmp_path, None)

    assert result.nav_mode == "generated"
    assert result.warnings == []


@pytest.mark.parametrize(
    ("metadata", "registration_kind", "expected"),
    [
        ("diataxis: tutorial", None, "tutorial"),
        ("diataxis: how-to", None, "how-to"),
        ("diataxis: explanation\nkind: reference", None, "reference"),
        ("diataxis: explanation\nkind: reference\ntype: how-to", None, "how-to"),
        ("diataxis: explanation\nkind: reference\ntype: how-to", "tutorial", "tutorial"),
        ("description: A tutorial in a directory", None, None),
    ],
)
def test_explicit_diataxis_is_lowest_priority_classification(
    tmp_path: Path, metadata: str, registration_kind: str | None, expected: str | None
) -> None:
    write(tmp_path, "docs/tutorials/lesson.md", f"---\n{metadata}\n---\n# A lesson\n")

    result = publication(tmp_path, None, kind=registration_kind)

    assert result.documents[0]["kind"] == expected


def test_explicit_diataxis_requires_text(tmp_path: Path) -> None:
    write(tmp_path, "docs/index.md", "---\ndiataxis: [tutorial]\n---\n# Welcome")

    with pytest.raises(HubError, match="Document type must be text"):
        publication(tmp_path, None)
