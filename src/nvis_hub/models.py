"""Validated publication registrations and safe application errors."""

import re
from pathlib import PurePosixPath
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class HubError(Exception):
    """A source or publication failure safe to display to a reader."""


class Registration(BaseModel):
    """Explicit repository scope and acquisition configuration; contains no secrets."""

    model_config = ConfigDict(extra="forbid")
    slug: str
    title: str
    description: str
    repo_url: str
    ref: str = "main"
    docs_paths: list[str] = Field(min_length=1)
    nav_path: str | None = None
    topics: list[str] = Field(default_factory=list)
    kind: str | None = None
    source_mode: Literal["gitlab", "snapshot", "local"] = "gitlab"
    local_path: str | None = None
    credential_env: str = "NVIS_GITLAB_TOKEN"

    @field_validator("slug")
    @classmethod
    def valid_slug(cls, value: str) -> str:
        """Restrict project identities to URL-safe lowercase names."""
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
            raise ValueError("slug must contain lowercase letters, numbers and hyphens")
        return value

    @field_validator("repo_url")
    @classmethod
    def valid_repository_url(cls, value: str) -> str:
        """Accept HTTPS repository URLs without embedded credentials or query data."""
        parsed = urlsplit(value)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or not parsed.path.strip("/")
        ):
            raise ValueError("repo_url must be an HTTPS repository URL without credentials")
        return value.rstrip("/").removesuffix(".git")

    @field_validator("docs_paths")
    @classmethod
    def valid_paths(cls, values: list[str]) -> list[str]:
        """Confine explicitly selected paths to the repository."""
        return [validate_path(value) for value in values]

    @field_validator("nav_path")
    @classmethod
    def valid_nav(cls, value: str | None) -> str | None:
        """Confine curated navigation to the repository."""
        return validate_path(value) if value is not None else None

    @field_validator("credential_env")
    @classmethod
    def valid_environment_name(cls, value: str) -> str:
        """Store a variable name, never a credential value."""
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
            raise ValueError("credential_env must be an environment variable name")
        return value

    @field_validator("title", "description", "ref")
    @classmethod
    def nonempty(cls, value: str) -> str:
        """Require meaningful labels and a source reference."""
        if not value.strip():
            raise ValueError("value must not be blank")
        return value.strip()

    @model_validator(mode="after")
    def local_source_required(self) -> "Registration":
        """Require a trusted local acquisition directory for offline modes."""
        if self.source_mode != "gitlab" and not self.local_path:
            raise ValueError("local_path is required for local and snapshot sources")
        return self


def validate_path(value: str) -> str:
    """Return a portable repository-relative path or reject unsafe syntax."""
    if (
        not value
        or "\\" in value
        or "\x00" in value
        or value.startswith("/")
        or ".." in PurePosixPath(value).parts
        or re.match(r"^[A-Za-z]:", value)
    ):
        raise ValueError("paths must stay inside the repository")
    return PurePosixPath(value).as_posix()
