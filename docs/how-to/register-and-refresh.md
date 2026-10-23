# Register and refresh documentation

Create a JSON registration with a stable slug, a useful description, and selected
documentation paths. For example, use this shape for a live GitLab source:

```json
{
  "slug": "project-slug",
  "title": "Project name",
  "description": "What the documentation helps a reader do",
  "repo_url": "https://gitlab-master.nvidia.com/nvis-ova/project-slug",
  "ref": "main",
  "source_mode": "gitlab",
  "docs_paths": ["README.md", "docs"],
  "nav_path": ".docs-pipeline/navigation.rst",
  "credential_env": "NVIS_GITLAB_TOKEN"
}
```

Select actual authored files and directories; omit nonexistent or inappropriate
paths. Topics and kind are optional authored metadata or explicit overrides.
Supply a credential through the named local environment variable. The hub's
HTTPS archive adapter does not read Git credential helpers. Never put a token in
registration JSON, a repository URL, or chat. Source
credentials grant acquisition access; they do not authenticate website readers.

```bash
.venv/bin/nvis-hub register /path/to/registration.json
.venv/bin/nvis-hub refresh project-slug
.venv/bin/nvis-hub list
```

Registration saves configuration without publishing. Refresh stages acquisition
and rendering, then replaces the project's publication atomically. Successful
refresh removes deleted pages and their search entries. An error returns a
nonzero exit status, records the error, and retains the last working content.
Correct the source/configuration or restore access and rerun the same command.

```bash
.venv/bin/nvis-hub refresh --all
```

`--all` continues through other projects if one fails and returns nonzero when
any project fails. `scripts/seed.sh` registers the available `sources/*.json`
before performing this refresh. No scheduled, webhook, or CI sync is enabled.

For disposable local tests, set `source_mode` to `local` and `local_path` to a
source directory. For authentic offline acquisitions, use `snapshot` and a
snapshot directory. Relative `local_path` values resolve against the JSON file's
directory. See [configuration](../reference/configuration.md) for the boundaries.
