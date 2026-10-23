"""CLI integration checks against disposable publications."""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, db: Path, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run the installed adapter with an isolated shared database."""
    env = {**os.environ, "NVIS_HUB_DB": str(db), "PYTHONPATH": str(ROOT / "src")}
    return subprocess.run(
        [sys.executable, "-m", "nvis_hub.cli", *args],
        cwd=cwd or ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def make_config(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "source"
    (source / "docs").mkdir(parents=True)
    (source / "docs" / "guide.md").write_text(
        "# Operator guide\n\n## Recovery\n\nRestart the prism service.\n"
    )
    config = tmp_path / "project.json"
    config.write_text(
        json.dumps(
            {
                "slug": "prism",
                "title": "Prism",
                "description": "Prism operations",
                "repo_url": "https://gitlab.example.test/nvis/prism",
                "source_mode": "local",
                "local_path": "source",
                "docs_paths": ["docs"],
                "topics": ["operations"],
                "kind": "how-to",
            }
        )
    )
    return config, source


def test_register_resolves_source_against_config_and_survives_restart(tmp_path: Path) -> None:
    """A cwd-relative local_path would prevent refresh from a different directory."""
    config, _ = make_config(tmp_path)
    db = tmp_path / "state" / "hub.sqlite3"
    result = run_cli("register", str(config), db=db, cwd=tmp_path.parent)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["slug"] == "prism"
    result = run_cli("refresh", "prism", db=db, cwd=tmp_path.parent)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["document_count"] == 1
    projects = run_cli("list", db=db)
    assert projects.returncode == 0, projects.stderr
    project = json.loads(projects.stdout)[0]
    assert project["slug"] == "prism"
    assert project["revision"]
    assert project["published_at"]


def test_explicit_db_takes_precedence_and_refresh_all_is_repeatable(tmp_path: Path) -> None:
    config, _ = make_config(tmp_path)
    env_db = tmp_path / "unused.sqlite3"
    explicit = tmp_path / "chosen.sqlite3"
    result = run_cli("--db", str(explicit), "register", str(config), db=env_db)
    assert result.returncode == 0, result.stderr
    for _ in range(2):
        result = run_cli("--db", str(explicit), "refresh", "--all", db=env_db)
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout)[0]["document_count"] == 1
    assert not env_db.exists()


def test_bad_registration_does_not_echo_unknown_secret_fields(tmp_path: Path) -> None:
    config = tmp_path / "invalid.json"
    config.write_text(json.dumps({"slug": "invalid", "token": "must-not-appear-123"}))
    result = run_cli("register", str(config), db=tmp_path / "hub.sqlite3")
    assert result.returncode != 0
    assert "Invalid registration" in result.stderr
    assert "must-not-appear-123" not in result.stdout + result.stderr
    assert "Traceback" not in result.stderr


def test_unknown_project_reports_actionable_failure(tmp_path: Path) -> None:
    result = run_cli("refresh", "absent", db=tmp_path / "hub.sqlite3")
    assert result.returncode != 0
    assert "absent" in result.stderr
    assert "Traceback" not in result.stderr


def test_unusable_database_reports_failure_without_traceback(tmp_path: Path) -> None:
    """A database path pointing to a directory should remain an operator-facing error."""
    result = run_cli("list", db=tmp_path)
    assert result.returncode != 0
    assert "database" in result.stderr.lower()
    assert "Traceback" not in result.stderr
