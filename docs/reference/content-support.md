# Supported content and publication limits

Publish UTF-8 `.md` and `.markdown` documents. The renderer supports headings,
links, images, fenced code, lists, blockquotes and Markdown tables. Source HTML is
escaped; this is not an executable Sphinx/repo_docs build. Sphinx extensions,
arbitrary RST pages, notebooks and repository build scripts are not executed.

Front matter may declare `title`, `type`/`kind` and `topics`. Registration metadata
provides explicit defaults. Missing classifications remain unclassified. Directory
names and document text are not used to invent topics or Diátaxis types.

`docs_paths` selects literal files or directories, not glob patterns. Implicit
hidden folders, tests, fixtures, templates, vendored content, build outputs and
node_modules are excluded. Explicit selection can include an otherwise excluded
location. Traversal, symlinks and paths outside the repository are rejected.

Supported scoped attachments: SVG, PNG, JPEG, GIF, WebP, AVIF, ICO, PDF, plain text,
CSV, TSV, JSON, YAML, ZIP, GZ and Mermaid source (`.mmd`). SVG derivatives preserve
allowlisted authored styling while removing scripts, external references and
unsafe CSS. The immutable source snapshot retains the original bytes. Attachments
have a sandbox CSP; non-image/non-PDF attachments download. External images are
not fetched and are blocked by the reader's content policy.

Relative links to published documents, directory indexes, assets and section
anchors become hosted links. Links outside the declared scope become visibly
labelled, revision-pinned source links when source provenance supports them.
Unsafe or unsupported targets are marked unavailable. Source paths and document
extensions remain part of stable namespaced identities.

`nav_path` accepts supported RST `toctree` blocks: captions, explicit titles,
ordered paths, and maxdepth/hidden/titlesonly options. Other options and unresolved
entries produce import notices. Documents omitted from a usable curated tree are
appended under Additional documentation. Without a usable tree, navigation is
explicitly labelled generated. Import notices appear under Source status.

Limits: 128 MiB per repository response, extracted archive and prepared publication;
16 MiB per document/attachment; 30,000 archive members. A failed import keeps the
last successful publication. Re-registration shows pending source identity until
a successful refresh, preserving the active publication's repository, ref and mode.

Search uses literal Unicode word tokens joined with AND, with a maximum of 32
tokens. Section headings/body matches rank directly; whole-page matches provide a
fallback when terms span sections. Document-title matches do not create unrelated
section hits. Results contain plain excerpts and direct hosted anchor URLs. Web
queries are limited to 200 characters; MCP result limits are 1–100.
