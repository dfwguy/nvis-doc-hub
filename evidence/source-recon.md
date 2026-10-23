# Real source reconnaissance

Verified on 2026-10-22 at 22:22 UTC. No sibling source files were edited, no
repository code was executed, and no credentials were read or configured.

## Registered sources

`sources/cluster-bringup.json` publishes the authentic local snapshot for
`nvis-ova/cluster-bringup`, tracking `main`. Its exact revision is
`f74950acdc451f43f8857754efad25ce5233d26c`, the 2026-10-21 merge of the documentation
pipeline integration. GitLab MCP commit metadata and a fresh direct Git clone
agreed on this revision.

The declared reader scope is root `README.md` plus `docs/`. The snapshot contains
85 Markdown pages, the original `.docs-pipeline/navigation.rst`, the original
pipeline configuration, and two authored diagram assets: an SVG and Mermaid
source. The repository's configuration uses source directory `.`; the hub's
explicit scope narrows that to authored documentation. The curated navigation
has 85 entries, and every entry resolves to a selected Markdown page.

`sources/documentation-pipeline.json` publishes the authentic local snapshot for
`nvis-ova/documentation-pipeline`, tracking `feat/copier-docs-pipeline`. Its exact
revision is `0796f0212ccac88391765271f88f9aed6606f68a`, dated 2026-10-20. GitLab MCP
verified this remains the feature branch tip. The default `main` branch is still
the initial commit `4d8aa1f35c07c1584907500dc3749aedbc1312ff`; selecting it would
omit the actual pipeline documentation.

The declared reader scope is root `README.md` plus `docs/`: seven authored
Markdown files covering adoption, updates, configuration, validation, and design.
There is no curated navigation file for this repository, so navigation should be
reported as generated. No repository-wide topic or document-type override was
added to either registration. The descriptions summarize the authored README or
documentation home.

Matching live GitLab registrations are in `sources/live/cluster-bringup.json`
and `sources/live/documentation-pipeline.json`. They retain the same explicit
scope and refs. Local snapshot paths resolve relative to the registration files.

## Acquisition and integrity

Snapshots are stored at `data/source-snapshots/<slug>/repository/`, with a
`manifest.json` beside that directory. Each manifest records `repo_url`, `ref`,
the full `revision`, acquisition time and method, selected paths, per-file
SHA-256 and size, the declared scope, and omitted repository paths.

Cluster Bringup was fetched with a fresh depth-one HTTPS Git clone. Selected
blobs were read at the exact revision and written byte-for-byte without a
checkout or any source build. Its curated navigation SHA-256 also agrees with
the independent GitLab MCP response:
`63b46b06033bbda115949aea576afca3dab19fbf7997691f6beedf1e2fdda4d3`.

Documentation Pipeline was fetched using connected GitLab MCP
`gitlab_get_file_contents` for each of the seven selected files at the exact
revision. The connector labels its upstream file encoding `base64` while
returning already-decoded text. The returned text was written as UTF-8; every
resulting file's byte size and SHA-256 were verified against GitLab's `size` and
`content_sha256` metadata. No content was inferred, rewritten, or generated.
The sibling checkout's committed tree was read only to inventory omitted paths;
all published Pipeline bytes came from GitLab MCP.

These connected agent tools are an acquisition aid for this bootstrap. They are
separate from the new hub's own MCP interface and are not a source credential
available to the running application.

## Connectivity findings

The historical shell DNS failure is no longer reproducible. A credential-free
HTTPS HEAD request to the GitLab origin returned HTTP 302 to its sign-in page.
Noninteractive `git ls-remote` and a fresh clone of Cluster Bringup succeeded.
GitLab describes Cluster Bringup as public on this internal GitLab instance.

Noninteractive HTTPS Git access to Documentation Pipeline failed. Its configured
askpass integration pointed to an unavailable VS Code Git socket, and GitLab
reported missing or invalid credentials. GitLab describes this repository as
internal. This is a private-source credential limitation, separate from the
deferred reader-facing SSO work. No auth setup was attempted and no tokens were
requested, read, or saved.

GitLab MCP metadata, commits, and file reads worked. Two repository-tree calls
failed transiently at the connector transport; per-file reads succeeded
subsequently. For another offline acquisition, first resolve the desired ref with
`gitlab_list_commits`, then read each explicitly selected file at that immutable
revision with `gitlab_get_file_contents`, reject truncation, and validate every
file's SHA-256 and byte size before publishing a manifest. Binary assets require
a byte-preserving acquisition mechanism; the live Git path supplied the actual
Cluster Bringup SVG and Mermaid assets here.

Snapshot refresh reimports this captured revision. A new upstream capture or
working noninteractive credentials are needed to advance the internal Pipeline
source. Live Cluster Bringup refresh can use its working direct Git path.

## Authored scope, navigation, and links

An independent CommonMark token audit covered all 92 selected Markdown pages.
Cluster Bringup has 349 local document links, three local asset links, seven
same-page anchor links, and seven links to intentionally omitted source scripts.
Documentation Pipeline has 13 local document links. Every in-scope document or
asset target resolves; no authored missing local targets were found.

The seven out-of-scope occurrences point to only two source files:
`scripts/check_node_busy.sh` and `scripts/aic_bcm_headnode_add_user.sh`. These
links should visibly open their revision-pinned original GitLab files rather
than route to an unavailable hosted page. Keeping executable scripts outside the
publication scope is deliberate. Directory links inside the selected docs resolve
to README or index pages, matching the relevant behavior of the sibling Sphinx
extension.

For real-content browser verification, use
`docs/internal_app_access/explanation/architecture-and-trust.md`. It includes
nested local links, fenced source, and an authored image link on line 8 to
`architecture-and-trust.svg` in the same directory. The SVG exists in the
snapshot. The corresponding `.mmd` is also preserved as an attachment.

The source README and guides include historical statements about then-local
follow-up work. They remain original authored content even where this session's
live GitLab commit check establishes a newer publication state. The hub should
retain that wording and expose the exact source revision.

## Sibling pipeline seams considered

The sibling runtime builds a selected isolated source snapshot with NVIDIA
`repo_docs` 0.39.2 and Sphinx, copies in curated RST navigation, resolves repository
directory links to README/index pages, and writes `.docs-build/site/`. It
requires Linux, network package bootstrap, Bash, and NVIDIA dependency services.
The hub can reuse the documentation scope and link conventions without executing
this source-owned build runtime during generic import.

The Copier template records consumer-owned title, source directory, navigation,
and shared CI/runtime refs. The CI retains build artifacts for a week and
publishes Pages only from the consumer default branch. No existing Pages
deployment or immutable artifact URL was verified in this reconnaissance.
Source ingestion is therefore the evidenced bootstrap path here; artifact
ingestion remains a separate future option.
