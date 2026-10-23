# Repository setup

Recorded 23 October 2026.

## Local version control

- Initialized this project as its own Git repository, with `main` as the initial branch.
- Created `development` from the verified application baseline, now commit `35f18d8` after the Git LFS migration described below.
- Set project-local author identity to Dejaun Gayle `<dgayle@nvidia.com>`, using the local account name and existing SSH-key identity. Global Git settings were not changed.
- Configured `origin` for the user's final destination, `ssh://git@gitlab-master.nvidia.com:12051/nvis-ova/nvis-doc-hub.git`. The local project directory remains `nvis-docs-hub`.
- Retained all 101 imported skill files, reproducible source snapshots, source registrations, app code, tests, documentation, design context, reports, and representative review captures.
- Excluded environments, runtime databases, logs, caches, builds, and bulk browser captures. Existing local files remain on disk.

## Verification

All 30 tests passed. Ruff lint/format checks, mypy, and JavaScript syntax checks passed. The existing upstream Starlette deprecation warning is unchanged.

A fresh local clone successfully registered and published both tracked snapshots: 85 Cluster Bringup documents at `f74950acdc451f43f8857754efad25ce5233d26c` and seven Documentation Pipeline documents at `0796f0212ccac88391765271f88f9aed6606f68a`. All 101 imported skill files in that clone matched their original hash manifest. No actual credentials were found in the reviewed project text files; no credentials were added to Git.

## Private GitLab publication

After group access was granted, `nvis-ova/nvis-docs-hub` was initially created and both branches were published there; GitLab explicitly confirmed that project was **Private**. The user then supplied the official destination, [`nvis-ova/nvis-doc-hub`](https://gitlab-master.nvidia.com/nvis-ova/nvis-doc-hub), using the singular `doc` name, and requested removal of the earlier duplicate. The singular repository is the sole intended remote destination.

The user created the official repository following the requested **Private** setup; its exact visibility was not independently inspected through an authenticated API. Both `main` and `development` were successfully published there over SSH port 12051. The first published branch tips, before later documentation updates, were `d8d94b7` on `main` and `00b9a50` on `development`.

Only the singular repository is configured as `origin`; the earlier `old-origin`
remote was removed. The duplicate plural GitLab project still exists. The user
explicitly requested its deletion, but `glab repo delete nvis-ova/nvis-docs-hub
--yes` was rejected as unauthorized. SSH publishing access is working, while
project-deletion API authorization is unavailable in this session. Delete that
duplicate through a signed-in GitLab account with the required permissions, or
supply an authorized API session before retrying. Do not delete the official
singular `nvis-ova/nvis-doc-hub` project. No further webpage verification is needed
for commits or pushes.

`main` retains the verified application baseline. Live documentation search suggestions remain on `development`; that feature has not been merged into `main`.

## Git LFS and history migration

GitLab's 5 MiB limit for Git blobs rejected the first push because the complete imported Impeccable package includes a 17.2 MB executable at `.agents/skills/impeccable/scripts/bin/darwin-arm64/impeccable`. Only that file was migrated to Git LFS, with its original bytes and SHA-256 preserved. `.gitattributes` records the LFS rule. The other 100 imported files remain ordinary Git files.

The migration rewrote local, unpublished history before the first successful remote push. The original local history is preserved at `.git/pre-lfs-backup.bundle` in the original working repository; that backup is local only and is not published. The exact old-to-new commit IDs are retained in [lfs-history-map.csv](lfs-history-map.csv). The initial application baseline changed from `29061f2` to `35f18d8`.

A fresh clone of the initially published `main` at `d8d94b7`, from the earlier plural repository and initially made with `GIT_LFS_SKIP_SMUDGE=1`, successfully ran `git lfs install --local` and `git lfs pull`. The official repository was published with the same history and content. All 101 imported skill files matched their original manifest hashes, including the downloaded executable. All 96 source-snapshot files matched their manifests and inventories. `git lfs fsck` passed, and no reachable Git blob exceeded 5 MiB. The clone was clean after verification.

The validation clone's `origin` was then changed to the official singular repository. A separate empty LFS cache forced a new `git lfs fetch origin main` download from that destination. Its 17,192,672-byte executable matched SHA-256 `5c00c3130b961f3aa1066f04ed0e1f58e87808ad153efa00f1c44184800084f2`, the original import-manifest digest.

Fresh clones require Git LFS installation and `git lfs pull`; see [README setup](../README.md). Do not reinitialize or force-push the published repository.

Hosting, remote HTTP MCP, automatic documentation refresh, access control, and the publishing skill remain deferred.
