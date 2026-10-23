# Run with persistent container storage

Build locally and bind the published port to host loopback:

```bash
docker build -t nvis-docs-hub .
docker volume create nvis-hub-data
docker run --rm --name nvis-hub -p 127.0.0.1:8000:8000 \
  -v nvis-hub-data:/data nvis-docs-hub
```

The process runs as UID 10001 and stores SQLite at `/data/hub.sqlite3`. The image
contains the installed package and reading assets. Register sources separately;
source snapshots and credentials are excluded from the image.

For an existing registration and local snapshot, mount both read-only. Ensure
its `local_path` resolves inside the container, not to a host-only directory.

```bash
docker run --rm -v nvis-hub-data:/data \
  -v /absolute/source-directory:/sources:ro \
  nvis-docs-hub register /sources/project.json
docker run --rm -v nvis-hub-data:/data \
  -v /absolute/source-directory:/sources:ro \
  nvis-docs-hub refresh project-slug
```

For live GitLab acquisition, pass only the needed credential environment variable
with Docker's environment mechanism; keep its value out of command arguments.
Allow the container to reach the private GitLab host through your network. Do not
expose this application to a broader network before the deferred access-control
work and hosting decisions are completed.
