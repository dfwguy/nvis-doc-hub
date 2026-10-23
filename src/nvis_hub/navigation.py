"""Presentation groups derived only from authored navigation and classifications."""

import re
from typing import Any

_GROUPS = (
    ("tutorial", "Tutorials", "Tutorials — learning by doing"),
    ("how-to", "How-to guides", "How-to guides — getting something done"),
    ("reference", "Reference", "Reference — the machinery, described"),
    ("explanation", "Explanation", "Explanation — why it is like this"),
    ("other", "Other documentation", "Other documentation"),
)
_NAMES = {
    "tutorial": "tutorial",
    "tutorials": "tutorial",
    "how-to": "how-to",
    "how to": "how-to",
    "how-to guide": "how-to",
    "how-to guides": "how-to",
    "how to guide": "how-to",
    "how to guides": "how-to",
    "reference": "reference",
    "explanation": "explanation",
    "explanations": "explanation",
}
_MODE = r"Tutorials?|How[- ]to(?: guides?)?|Reference|Explanations?"
_CAPTION = re.compile(rf"^({_MODE})(?:\s*[—–:]\s*.*|\s+-\s+.*)?$", re.IGNORECASE)
_LABEL = re.compile(rf"^({_MODE})\s*:\s*(.+)$", re.IGNORECASE)


def group_navigation(
    navigation: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    *,
    curated: bool,
    current_path: str | None = None,
) -> list[dict[str, Any]]:
    """Group published links, retaining author order/context without changing metadata."""
    by_path = {doc["path"]: doc for doc in documents}
    groups: dict[str, dict[str, Any]] = {
        key: {"key": key, "label": label, "title": title, "entries": [], "active": False}
        for key, label, title in _GROUPS
    }
    used: set[str] = set()
    caption_kind: str | None = None
    context: str | None = None

    def add(entry: dict[str, Any], *, authored: bool) -> None:
        path = entry.get("path")
        if not isinstance(path, str) or path not in by_path or path in used:
            return
        doc = by_path[path]
        title = entry.get("title") or doc["title"]
        prefix = _LABEL.fullmatch(title) if authored else None
        label_kind = _NAMES[prefix[1].casefold()] if prefix else None
        explicit_kind = _NAMES.get((doc.get("kind") or "").strip().casefold())
        kind = caption_kind or label_kind or explicit_kind or "other"
        if prefix and kind == label_kind:
            title = prefix[2]
        level = entry.get("level", 1)
        level = max(1, level) if isinstance(level, int) else 1
        active = path == current_path
        groups[kind]["entries"].append(
            {
                "path": path,
                "url": doc["url"],
                "title": title,
                "context": context if authored else None,
                "level": level,
                "depth": min(level - 1, 3),
                "active": active,
            }
        )
        groups[kind]["active"] |= active
        used.add(path)

    for entry in navigation:
        if not entry.get("path"):
            if curated:
                title = entry.get("title", "")
                match = _CAPTION.fullmatch(title)
                caption_kind = _NAMES[match[1].casefold()] if match else None
                standard_caption = caption_kind and (
                    title.casefold() in _NAMES or title.casefold() == groups[caption_kind]["title"].casefold()
                )
                context = None if standard_caption else title or None
            continue
        add(entry, authored=curated)
    caption_kind = None
    context = None
    for document in documents:
        add(document, authored=False)
    return [group for group in groups.values() if group["entries"]]
