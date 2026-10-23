# NVIS - OVA Documentation Hub

<!-- impeccable:product-schema 1 -->

## Platform
web

## Stack
Delegated by BUILD_BRIEF.md: Python 3.12, FastAPI, Jinja templates, SQLite FTS5,
Markdown rendering, and the official Python MCP SDK. One process serves the web
application; a stdio MCP process reads the same persistent database.

## Users
NVIS - OVA engineers discovering projects, finding operational instructions, and reading
authored documentation. AI agents discover and retrieve the same publications.

## Product Purpose
Make documentation across NVIS - OVA projects easy to find and read centrally while
keeping each source repository authoritative.

## Operating Context
GitLab repositories, curated documentation navigation, exact commit provenance,
explicit registration and refresh, local evaluation before deployment.

## Capabilities and Constraints
Hosted documentation, unified document browsing and ranked section search with
available metadata filters, document discovery shelves ranked by aggregate browser opens,
persistent publications, MCP discovery/search/retrieval. Popularity stores shared
all-time opens by document, including repeats, without user profiles. No generated answers.
SSO, NVIS membership enforcement, automatic synchronization, and the contributor
publishing skill are deferred. Hosting is undecided. Keep sibling projects intact.

## Brand Commitments
Use the supplied NVIDIA reference's dark theme: #111 background and reading sheet,
#1a1a1a raised surfaces, white headings, #eee body text, and #999 supporting text.
NVIDIA Green (#76b900) carries links, focus, identity, and primary buttons with black
text; Deep Green (#004831) supplies the primary-action hover background. The topbar is black.
The app identity is NVIS - OVA, with NVIS - OVA Documentation at the sidebar bottom
and a footer fallback when the sidebar folds. Keep readable docs and clear source
provenance. Exact reference tokens are recorded in evidence/brand-color-reference.md.

## Evidence on Hand
BUILD_BRIEF.md and the linked session checkpoint contain settled user decisions.
The two real seed repositories are cluster-bringup and documentation-pipeline.
Fixtures and snapshots must be labelled according to their actual provenance.

## Product Principles
- Source authors own content; the hub publishes existing documentation.
- People and agents read a single consistent publication.
- Failed refreshes preserve the last successful publication.
- Prefer small, typed responsibilities and behavior-focused checks.

## Accessibility & Inclusion
Desktop and narrow layouts, semantic controls, visible keyboard focus, sufficient
contrast, readable code blocks, breadcrumbs, and in-page navigation.
