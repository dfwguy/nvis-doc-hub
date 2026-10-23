# Collapsible documentation categories

The user requested expandable lists for Tutorial, How-to, Reference, and
Explanation, following `nvis/nvis-rack-status`'s `docs/_toc.yml` on
`feature/auto-run-mode`. The exact source and conventions were inspected at commit
`7e909322e467b2dd7b31e05fd6c82cdb9d70a610`; see the template evidence.

Apply the four top-level categories to the project page and its desktop/mobile
navigation. Preserve the dark NVIDIA design, current search, and authored pages.
Use native details/summary controls, keyboard support, visible counts, and no
empty groups. Open the active document's group on reader routes. Other groups
start collapsed. Keep unknown classifications under Other documentation.

## Source authority

Classify display entries from explicit authored TOC category captions, explicit
navigation labels such as `How-to: ...`, or document type metadata. Do not infer
classification from directory names or arbitrary prose. Preserve author order
within each category, source-context captions, nested entry levels, links, and
all published pages. Presentation grouping does not rewrite document metadata.

Support explicit `diataxis` frontmatter in addition to existing type/kind fields.
Allow an explicitly registered YAML navigation file with `root`, captioned
`subtrees`, recursive `entries`, extensionless `file`, and optional `title`, as
used by the reference. Resolve files relative to that TOC and preserve nesting
in the flat navigation contract. Parse data only; never run repository config.
Retain RST support and honest fallback/notices for malformed or missing entries.
Do not import the reference project into the catalog or edit source snapshots.

## Verification and delivery

Tests first: YAML paths/order/nesting, safe malformed/recursive input, explicit
metadata, grouping authority, document coverage, active state, and no empty
categories. Browser checks cover both project indexes, reader active groups,
desktop and phone menus, keyboard disclosure operation, no-JavaScript behavior,
search regression, and current responsive spacing. Keep work on development and
push the verified change to the existing singular nvis-doc-hub remote.
