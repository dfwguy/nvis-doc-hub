"""Acquire repository data without executing repository configuration or builds."""

import json
import os
import re
import subprocess
import tarfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .models import HubError, Registration

MAX_SOURCE_BYTES = 128 * 1024 * 1024


@dataclass
class AcquiredSource:
    """A materialized repository and explicit immutable revision metadata."""

    root: Path
    revision: str
    acquisition: dict[str, Any] = field(default_factory=dict)


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def _fetch(url: str, token: str | None) -> bytes:
    headers = {"User-Agent": "nvis-docs-hub/0.1"}
    if token:
        headers["PRIVATE-TOKEN"] = token
    try:
        with build_opener(_NoRedirect).open(Request(url, headers=headers), timeout=45) as response:
            data = response.read(MAX_SOURCE_BYTES + 1)
        if len(data) > MAX_SOURCE_BYTES:
            raise HubError("Repository response exceeds the 128 MiB import limit.")
        return data
    except HTTPError as error:
        raise HubError(
            f"GitLab acquisition failed (HTTP {error.code}); check access and credential environment."
        ) from None
    except (URLError, TimeoutError, OSError):
        raise HubError(
            "GitLab could not be reached; check network access and source configuration."
        ) from None


def _extract_archive(data: bytes, destination: Path) -> None:
    try:
        with tarfile.open(fileobj=BytesIO(data), mode="r:*") as archive:
            members = archive.getmembers()
            if len(members) > 30000 or sum(item.size for item in members) > MAX_SOURCE_BYTES:
                raise HubError("Repository archive exceeds import limits.")
            for item in members:
                parts = PurePosixPath(item.name).parts
                if (
                    not parts
                    or item.name.startswith("/")
                    or ".." in parts
                    or item.issym()
                    or item.islnk()
                    or not (item.isfile() or item.isdir())
                ):
                    raise HubError("Repository archive contains an unsafe path or symlink.")
                relative = Path(*parts[1:])
                if not relative.parts:
                    continue
                target = destination / relative
                if item.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    stream = archive.extractfile(item)
                    if stream is None:
                        raise HubError("Repository archive could not be read.")
                    target.write_bytes(stream.read())
    except (tarfile.TarError, OSError):
        raise HubError("GitLab returned an invalid repository archive.") from None


def _snapshot(config: Registration) -> AcquiredSource:
    base = Path(config.local_path or "")
    try:
        manifest = json.loads((base / "manifest.json").read_text())
        root = (base / "repository").resolve(strict=True)
        revision = manifest["revision"]
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", revision):
            raise HubError("Snapshot revision must be an exact commit hash.")
        if manifest["repo_url"].rstrip("/").removesuffix(".git") != config.repo_url:
            raise HubError("Snapshot repository does not match the registration.")
        files = manifest.get("files")
        if not isinstance(files, list) or not files:
            raise HubError("Snapshot integrity manifest must list source file digests.")
        declared = {item["path"] for item in files}
        actual = set()
        for path in root.rglob("*"):
            if path.is_symlink():
                raise HubError("Snapshot manifest contains an unsafe symlink.")
            if path.is_file():
                actual.add(path.relative_to(root).as_posix())
        if actual != declared or len(declared) != len(files):
            raise HubError("Snapshot integrity check failed; file inventory differs from its manifest.")
        for item in files:
            relative = PurePosixPath(item["path"])
            if relative.is_absolute() or ".." in relative.parts:
                raise HubError("Snapshot manifest contains an unsafe path.")
            target = root / relative
            if target.is_symlink() or not target.resolve().is_relative_to(root):
                raise HubError("Snapshot manifest contains an unsafe symlink.")
            if sha256(target.read_bytes()).hexdigest() != item["sha256"]:
                raise HubError("Snapshot integrity check failed; a source file has changed.")
        return AcquiredSource(
            root,
            revision,
            {
                "method": manifest.get("acquisition_method", manifest.get("acquisition", "snapshot")),
                "acquired_at": manifest.get("acquired_at", manifest.get("fetched_at")),
                "ref": manifest.get("ref"),
            },
        )
    except HubError:
        raise
    except (OSError, ValueError, KeyError, TypeError):
        raise HubError("Snapshot is missing or its manifest is invalid.") from None


def _local(root: Path) -> AcquiredSource:
    if not root.is_dir():
        raise HubError("Local source directory does not exist.")
    digest = sha256()
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or ".git" in path.relative_to(root).parts or not path.is_file():
            continue
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\x00")
        digest.update(path.read_bytes())
    revision = "content-sha256:" + digest.hexdigest()
    if (root / ".git").exists():
        try:
            head = subprocess.run(
                ["git", "-C", str(root), "-c", "core.fsmonitor=false", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                timeout=10,
                check=True,
            ).stdout.strip()
            status = subprocess.run(
                ["git", "-C", str(root), "-c", "core.fsmonitor=false", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=10,
                check=True,
            ).stdout
            if not status and re.fullmatch(r"[0-9a-f]{40,64}", head):
                revision = head
        except (OSError, subprocess.SubprocessError):
            pass
    return AcquiredSource(root, revision, {"method": "local"})


@contextmanager
def acquire(config: Registration) -> Iterator[AcquiredSource]:
    """Acquire a snapshot, a disposable local directory, or an HTTPS GitLab archive."""
    if config.source_mode == "snapshot":
        yield _snapshot(config)
        return
    if config.source_mode == "local":
        yield _local(Path(config.local_path or "").resolve())
        return
    parsed = urlsplit(config.repo_url)
    base = f"{parsed.scheme}://{parsed.netloc}/api/v4/projects/{quote(parsed.path.strip('/'), safe='')}/repository"
    token = os.environ.get(config.credential_env)
    try:
        commit = json.loads(_fetch(f"{base}/commits/{quote(config.ref, safe='')}", token))
        revision = commit["id"]
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", revision):
            raise HubError("GitLab did not return an exact commit revision.")
    except (KeyError, ValueError, TypeError):
        raise HubError("GitLab returned an invalid commit response.") from None
    archive = _fetch(f"{base}/archive.tar.gz?sha={quote(revision, safe='')}", token)
    with TemporaryDirectory(prefix="nvis-hub-") as directory:
        root = Path(directory)
        _extract_archive(archive, root)
        yield AcquiredSource(root, revision, {"method": "gitlab-https-archive"})
