"""Pure authored-document rendering, scoped file selection, and curated navigation."""

import mimetypes
import os
import posixpath
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote, unquote, urlsplit

import bleach
import tinycss2
import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token

from .models import HubError, Registration
from .sources import AcquiredSource

EXCLUDED = {
    "test",
    "tests",
    "vendor",
    "vendored",
    "node_modules",
    "templates",
    "template",
    "fixtures",
    "__pycache__",
    "dist",
    "build",
}
DOCUMENT_SUFFIXES = {".md", ".markdown"}
ASSET_SUFFIXES = {
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".avif",
    ".ico",
    ".pdf",
    ".txt",
    ".csv",
    ".tsv",
    ".json",
    ".yml",
    ".yaml",
    ".zip",
    ".gz",
    ".mmd",
}
ALLOWED_TAGS = {
    "a",
    "p",
    "div",
    "span",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "pre",
    "code",
    "blockquote",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "s",
    "hr",
    "br",
    "img",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "dl",
    "dt",
    "dd",
}


@dataclass
class Publication:
    """A fully prepared publication awaiting one atomic database commit."""

    documents: list[dict[str, Any]]
    assets: list[tuple[str, bytes, str]]
    navigation: list[dict[str, Any]]
    nav_mode: str
    warnings: list[str]


def hosted_url(slug: str, path: str, asset: bool = False) -> str:
    """Build a stable namespaced URL, preserving repository-relative extensions."""
    return f"/projects/{slug}/{'assets' if asset else 'docs'}/{quote(path, safe='/')}"


def _checked(root: Path, relative: str) -> Path:
    candidate = root / relative
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise HubError(f"Publication scope contains a symlink: {relative}")
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise HubError("Publication path escapes the repository.")
    return candidate


def scoped_files(root: Path, selections: list[str]) -> list[Path]:
    """Select declared files while excluding implicit hidden, test, and vendor trees."""
    found: dict[str, Path] = {}
    for selected in selections:
        path = _checked(root, selected)
        if not path.exists():
            raise HubError(f"Declared publication path does not exist: {selected}")
        if path.is_file():
            found[path.relative_to(root).as_posix()] = path
            continue
        for directory, children, files in os.walk(path, followlinks=False):
            children[:] = sorted(
                name for name in children if not name.startswith(".") and name.lower() not in EXCLUDED
            )
            for name in children + sorted(files):
                child = Path(directory) / name
                if name.startswith(".") or name.lower() in EXCLUDED:
                    continue
                relative = child.relative_to(root).as_posix()
                _checked(root, relative)
                if child.is_file():
                    found[relative] = child
    return [found[name] for name in sorted(found)]


def _plain(tokens: list[Token]) -> str:
    pieces: list[str] = []
    for token in tokens:
        if token.children:
            pieces.append(_plain(token.children))
        elif token.type in {"text", "code_inline", "code_block", "fence", "html_block", "html_inline"}:
            pieces.append(token.content)
        elif token.type in {"softbreak", "hardbreak"} or token.block:
            pieces.append("\n")
    return re.sub(r"[ \t]+", " ", "".join(pieces)).strip()


def _anchor(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).casefold()
    result = "".join(
        character for character in normalized if character.isalnum() or character in {" ", "-", "_"}
    )
    return re.sub(r"[-\s]+", "-", result).strip("-") or "section"


def _resolve_link(
    target: str,
    path: str,
    slug: str,
    documents: set[str],
    assets: set[str],
    repo_url: str = "",
    revision: str = "",
) -> str | None:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme.lower() not in {"https", "http", "mailto"} or parsed.username or parsed.password:
            return None
        return target
    if not parsed.path:
        return "#" + quote(unquote(parsed.fragment), safe="-_") if parsed.fragment else target
    raw = unquote(parsed.path)
    if "\\" in raw or "\x00" in raw:
        return None
    combined = raw.lstrip("/") if raw.startswith("/") else posixpath.join(posixpath.dirname(path), raw)
    relative = posixpath.normpath(combined)
    if relative == ".." or relative.startswith("../"):
        return None
    candidates = [
        relative,
        relative + ".md",
        relative.rstrip("/") + "/index.md",
        relative.rstrip("/") + "/README.md",
    ]
    for candidate in candidates:
        if candidate in documents:
            return hosted_url(slug, candidate) + (
                ("#" + quote(unquote(parsed.fragment), safe="-_")) if parsed.fragment else ""
            )
    if relative in assets:
        return hosted_url(slug, relative, asset=True)
    if repo_url and re.fullmatch(r"[0-9a-fA-F]{40,64}", revision):
        return f"{repo_url}/-/blob/{revision}/{quote(relative, safe='/')}" + (
            ("#" + quote(unquote(parsed.fragment), safe="-_")) if parsed.fragment else ""
        )
    return None


def _sanitize(rendered: str) -> str:
    return bleach.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes={
            "*": ["id", "class", "title"],
            "a": ["href", "title", "class"],
            "img": ["src", "alt", "title"],
            "ol": ["start"],
            "th": ["align"],
            "td": ["align"],
        },
        protocols={"http", "https", "mailto"},
        strip=True,
    )


def _metadata(raw: str) -> tuple[dict[str, Any], str]:
    matched = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", raw, re.S)
    if not matched:
        return {}, raw
    if len(matched[1]) > 65536:
        raise HubError("Document metadata exceeds the supported size.")
    try:
        metadata = yaml.safe_load(matched[1]) or {}
    except yaml.YAMLError:
        raise HubError("Document has malformed YAML front matter.") from None
    if not isinstance(metadata, dict):
        raise HubError("Document front matter must be a metadata mapping.")
    return metadata, raw[matched.end() :]


def render_document(
    raw: str, path: str, config: Registration, source: AcquiredSource, documents: set[str], assets: set[str]
) -> dict[str, Any]:
    """Render safe Markdown and partition its authored headings into searchable sections."""
    metadata, markdown = _metadata(raw)
    parser = MarkdownIt("commonmark", {"html": False}).enable("table").enable("strikethrough")
    tokens = parser.parse(markdown)
    headings: list[dict[str, Any]] = []
    boundaries: list[tuple[int, int, dict[str, Any]]] = []
    counts: dict[str, int] = {}
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            title = _plain([tokens[index + 1]])
            base = _anchor(title)
            counts[base] = counts.get(base, 0) + 1
            anchor = base if counts[base] == 1 else f"{base}-{counts[base]}"
            while any(heading["id"] == anchor for heading in headings):
                counts[base] += 1
                anchor = f"{base}-{counts[base]}"
            token.attrSet("id", anchor)
            heading = {"id": anchor, "title": title, "level": int(token.tag[1])}
            headings.append(heading)
            boundaries.append((index, token.map[0] if token.map else 0, heading))
        children = token.children or []
        for child in children:
            if child.type not in {"link_open", "image"}:
                continue
            attribute = "src" if child.type == "image" else "href"
            original = str(child.attrGet(attribute) or "")
            resolved = _resolve_link(
                original, path, config.slug, documents, assets, config.repo_url, source.revision
            )
            if resolved is None:
                child.attrSet(attribute, "")
                child.attrSet("class", "unavailable-link")
                child.attrSet("title", "Target is unsafe, unsupported, or outside published scope")
            else:
                child.attrSet(attribute, resolved)
                if resolved.startswith(config.repo_url + "/-/blob/"):
                    child.attrSet("class", "source-link")
                    child.attrSet(
                        "title",
                        "View repository source; this target is outside the hosted documentation scope",
                    )
    title = metadata.get("title") or (
        headings[0]["title"] if headings else PurePosixPath(path).stem.replace("-", " ")
    )
    if not isinstance(title, str):
        raise HubError(f"Document title must be text: {path}")
    topics = config.topics or metadata.get("topics", [])
    if isinstance(topics, str):
        topics = [topics]
    if not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
        raise HubError(f"Document topics must be a list of text values: {path}")
    kind = config.kind or metadata.get("type", metadata.get("kind"))
    if kind is not None and not isinstance(kind, str):
        raise HubError(f"Document type must be text: {path}")
    if not boundaries or boundaries[0][0] > 0:
        boundaries.insert(0, (0, 0, {"id": "", "title": title, "level": 0}))
    lines = markdown.splitlines(keepends=True)
    sections = []
    for position, (start, line, heading) in enumerate(boundaries):
        end = boundaries[position + 1][0] if position + 1 < len(boundaries) else len(tokens)
        endline = boundaries[position + 1][1] if position + 1 < len(boundaries) else len(lines)
        fragment = tokens[start:end]
        sections.append(
            {
                **heading,
                "text": _plain(fragment),
                "markdown": "".join(lines[line:endline]),
                "html": _sanitize(parser.renderer.render(fragment, parser.options, {})),
            }
        )
    revision = source.revision
    source_url = (
        f"{config.repo_url}/-/blob/{revision}/{quote(path, safe='/')}"
        if re.fullmatch(r"[0-9a-fA-F]{40,64}", revision)
        else None
    )
    return {
        "project_slug": config.slug,
        "path": path,
        "source_path": path,
        "title": title,
        "markdown": markdown,
        "text": _plain(tokens),
        "html": _sanitize(parser.renderer.render(tokens, parser.options, {})),
        "headings": headings,
        "sections": sections,
        "kind": kind,
        "topics": list(dict.fromkeys(topics)),
        "revision": revision,
        "source_url": source_url,
        "url": hosted_url(config.slug, path),
        "source_mode": config.source_mode,
    }


SVG_CSS_PROPERTIES = {
    "alignment-baseline",
    "background-color",
    "baseline-shift",
    "clip-path",
    "clip-rule",
    "color",
    "color-interpolation",
    "direction",
    "display",
    "dominant-baseline",
    "fill",
    "fill-opacity",
    "fill-rule",
    "filter",
    "flood-color",
    "flood-opacity",
    "font-family",
    "font-size",
    "font-stretch",
    "font-style",
    "font-variant",
    "font-weight",
    "height",
    "letter-spacing",
    "lighting-color",
    "line-height",
    "margin",
    "marker",
    "marker-end",
    "marker-mid",
    "marker-start",
    "max-height",
    "max-width",
    "opacity",
    "overflow",
    "padding",
    "paint-order",
    "pointer-events",
    "shape-rendering",
    "stop-color",
    "stop-opacity",
    "stroke",
    "stroke-dasharray",
    "stroke-dashoffset",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke-miterlimit",
    "stroke-opacity",
    "stroke-width",
    "text-align",
    "text-anchor",
    "text-decoration",
    "text-rendering",
    "transform",
    "transform-origin",
    "vector-effect",
    "vertical-align",
    "visibility",
    "white-space",
    "width",
    "word-spacing",
}
SVG_CSS_FUNCTIONS = {
    "rgb",
    "rgba",
    "hsl",
    "hsla",
    "hwb",
    "lab",
    "lch",
    "oklab",
    "oklch",
    "color",
    "calc",
    "min",
    "max",
    "clamp",
    "drop-shadow",
    "blur",
    "brightness",
    "contrast",
    "grayscale",
    "hue-rotate",
    "invert",
    "saturate",
    "sepia",
    "opacity",
    "matrix",
    "matrix3d",
    "translate",
    "translatex",
    "translatey",
    "scale",
    "scalex",
    "scaley",
    "rotate",
    "skew",
    "skewx",
    "skewy",
}


def _fragment_reference(value: str) -> bool:
    return re.fullmatch(r"#[A-Za-z0-9_.:-]+", value) is not None


def _safe_css_tokens(tokens: list[Any]) -> bool:
    for token in tokens:
        if token.type in {"error", "at-keyword", "{} block", "[] block"}:
            return False
        if token.type == "url" and not _fragment_reference(token.value):
            return False
        if token.type == "function":
            if token.lower_name == "url":
                arguments = [
                    argument for argument in token.arguments if argument.type not in {"whitespace", "comment"}
                ]
                if (
                    len(arguments) != 1
                    or arguments[0].type != "string"
                    or not _fragment_reference(arguments[0].value)
                ):
                    return False
            elif token.lower_name not in SVG_CSS_FUNCTIONS or not _safe_css_tokens(token.arguments):
                return False
        if token.type == "() block" and not _safe_css_tokens(token.content):
            return False
    return True


def _svg_declarations(value: str | list[Any]) -> str:
    declarations = tinycss2.parse_declaration_list(value, skip_comments=True, skip_whitespace=True)
    safe = []
    for declaration in declarations:
        if declaration.type != "declaration" or declaration.lower_name not in SVG_CSS_PROPERTIES:
            continue
        if _safe_css_tokens(declaration.value):
            content = tinycss2.serialize(declaration.value).strip()
            safe.append(
                f"{declaration.lower_name}:{content}" + ("!important" if declaration.important else "")
            )
    return ";".join(safe)


def _svg_stylesheet(value: str) -> str:
    safe = []
    for rule in tinycss2.parse_stylesheet(value, skip_comments=True, skip_whitespace=True):
        if rule.type != "qualified-rule":
            continue
        selector = tinycss2.serialize(rule.prelude).strip()
        if not re.fullmatch(r"[A-Za-z0-9_#.,:\-\s\[\]=\"'*|>+~]+", selector):
            continue
        declarations = _svg_declarations(rule.content)
        if declarations:
            safe.append(f"{selector}{{{declarations}}}")
    return "\n".join(safe)


def _svg(data: bytes) -> bytes:
    try:
        root = ET.fromstring(data)
        if root.tag.rsplit("}", 1)[-1].lower() != "svg":
            raise HubError("An SVG asset must contain an SVG root element.")
        blocked = {
            "script",
            "foreignobject",
            "iframe",
            "object",
            "embed",
            "animate",
            "animatetransform",
            "animatemotion",
            "set",
            "discard",
        }
        for parent in root.iter():
            for child in list(parent):
                if child.tag.rsplit("}", 1)[-1].lower() in blocked:
                    parent.remove(child)
            if parent.tag.rsplit("}", 1)[-1].lower() == "style":
                parent.text = _svg_stylesheet(parent.text or "")
            for key, value in list(parent.attrib.items()):
                name = key.rsplit("}", 1)[-1].lower()
                if name == "style":
                    sanitized = _svg_declarations(value)
                    if sanitized:
                        parent.attrib[key] = sanitized
                    else:
                        del parent.attrib[key]
                elif (
                    name.startswith("on")
                    or name == "srcset"
                    or (name in {"href", "src"} and not _fragment_reference(value))
                ):
                    del parent.attrib[key]
                elif name in SVG_CSS_PROPERTIES and not _safe_css_tokens(
                    tinycss2.parse_component_value_list(value)
                ):
                    del parent.attrib[key]
        return ET.tostring(root, encoding="utf-8")
    except ET.ParseError:
        raise HubError("An SVG asset contains invalid XML.") from None


def navigation(
    root: Path, config: Registration, documents: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], str, list[str]]:
    """Preserve supported RST toctree captions/order and append an honest fallback."""
    by_path = {doc["path"]: doc for doc in documents}
    generated = [
        {"title": doc["title"], "path": doc["path"], "level": 1, "url": doc["url"]} for doc in documents
    ]
    if not config.nav_path:
        return generated, "generated", []
    navfile = _checked(root, config.nav_path)
    if not navfile.is_file():
        return (
            generated,
            "generated",
            [f"Navigation file unavailable: {config.nav_path}; generated navigation used."],
        )
    rows: list[dict[str, Any]] = []
    warnings: list[str] = []
    active = False
    used: set[str] = set()
    for line in navfile.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if stripped == ".. toctree::":
            active = True
            continue
        if not stripped:
            continue
        if active and not line[0].isspace():
            active = False
        if not active:
            continue
        if stripped.startswith(":caption:"):
            rows.append(
                {"title": stripped[len(":caption:") :].strip(), "path": None, "url": None, "level": 0}
            )
            continue
        if stripped.startswith(":"):
            if not stripped.startswith((":maxdepth:", ":hidden:", ":titlesonly:")):
                warnings.append(f"Unsupported navigation option: {stripped}")
            continue
        match = re.fullmatch(r"(.+?)\s*<([^>]+)>", stripped)
        label, target = (match[1], match[2]) if match else (None, stripped)
        candidates = []
        for value in [
            posixpath.normpath(posixpath.join(posixpath.dirname(config.nav_path), target)),
            target.lstrip("/"),
        ]:
            candidates.extend(
                [value, value + ".md", value.rstrip("/") + "/index.md", value.rstrip("/") + "/README.md"]
            )
        resolved = next((value for value in candidates if value in by_path), None)
        if not resolved:
            warnings.append(f"Unsupported or unpublished navigation entry: {target}")
            continue
        used.add(resolved)
        rows.append(
            {
                "title": label or by_path[resolved]["title"],
                "path": resolved,
                "url": by_path[resolved]["url"],
                "level": 1,
            }
        )
    if not used:
        return generated, "generated", warnings + ["No supported toctree entries; generated navigation used."]
    remaining = [entry for entry in generated if entry["path"] not in used]
    if remaining:
        rows.append({"title": "Additional documentation", "path": None, "url": None, "level": 0})
        rows.extend(remaining)
    return rows, "curated", warnings


def prepare(source: AcquiredSource, config: Registration) -> Publication:
    """Stage every document and asset before publication replaces durable data."""
    files = scoped_files(source.root, config.docs_paths)
    document_paths = {
        path.relative_to(source.root).as_posix() for path in files if path.suffix.lower() in DOCUMENT_SUFFIXES
    }
    asset_paths = {
        path.relative_to(source.root).as_posix() for path in files if path.suffix.lower() in ASSET_SUFFIXES
    }
    warnings = [
        f"Unsupported publication input: {path.relative_to(source.root).as_posix()}"
        for path in files
        if path.suffix.lower() not in DOCUMENT_SUFFIXES | ASSET_SUFFIXES
    ]
    if not document_paths:
        raise HubError("No supported Markdown documents found in the declared scope.")
    documents = []
    assets = []
    total = 0
    for path in files:
        relative = path.relative_to(source.root).as_posix()
        if relative not in document_paths | asset_paths:
            continue
        data = path.read_bytes()
        total += len(data)
        if total > 128 * 1024 * 1024 or len(data) > 16 * 1024 * 1024:
            raise HubError("Publication exceeds supported content size limits.")
        if relative in document_paths:
            try:
                raw = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                raise HubError(f"Document is not valid UTF-8: {relative}") from None
            documents.append(render_document(raw, relative, config, source, document_paths, asset_paths))
        else:
            mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            assets.append((relative, _svg(data) if path.suffix.lower() == ".svg" else data, mime))
    nav, mode, nav_warnings = navigation(source.root, config, documents)
    return Publication(documents, assets, nav, mode, warnings + nav_warnings)
