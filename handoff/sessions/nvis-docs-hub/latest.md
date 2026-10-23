# Latest NVIS documentation hub session

Timestamp: 2026-10-23 19:38:23 UTC.

Topic: Popular-only discovery, source-preserving display casing and light/dark choice.

Read the [current refinement checkpoint](20261023T193823Z-discovery-refinement.md)
first. Default Browse retains one Explore popular documentation carousel, at most six
actually opened documents and an honest empty-history state. Extra project/type
rows and the global Projects sidebar list are removed; the Project dropdown
chooses projects, and project/reader routes retain local Document sections category
navigation. Project selection opens its vertical paginated library. Display
casing preserves technical spelling and authored source; a native persisted
light/dark switch defaults to dark.
The corrected carousel/sidebar implementation passes 145 Python tests and
120 browser checks (23 focused + 35 existing + 28 live-search + 34 category).
Lint, formatting, mypy and diff checks also pass; the inspector has zero findings.
This accompanies the finished
`development` refinement; use Git tracking to confirm remote synchronization.
`main` retains the baseline; access, contributor publishing and deployment remain
deferred. The main app is healthy on port 8000; current QA uses isolated port 8001.

Before refinement UI edits, `4682c9d` was confirmed pushed with a clean worktree
and zero ahead/behind commits, satisfying the user's explicit checkpoint request.

The [earlier discovery checkpoint](20261023T190834Z-document-discovery.md)
preserves the multi-shelf iteration and its 94/16-test proof. The current
refinement replaces that default with one bounded popular carousel.

Historical discovery feature commit `58912f5` was published to `origin/development`; Git tracking showed
zero commits ahead or behind after the push. The local app is healthy on port
8000. That iteration's temporary browser-QA server/database on port 8001 was stopped/removed.

The earlier feature and repository notes below are retained as historical
context; the linked current checkpoint gives the present source and branch state.

The [category checkpoint](20261023T183032Z-collapsible-navigation.md) records
native category groups and YAML/Diataxis support; preserve that reader behavior.

Latest feature, 23 October: live search suggestions are implemented and verified
on `development`. Start typing two characters on the catalog, project page, or
search page; results link to matching sections and support click/keyboard/touch.
44 Python tests plus 35 existing and 28 new browser checks pass. Read
[live-search verification](../../../evidence/live-search-verification.md).

23 October follow-up: the local server was restarted. The user-created GitLab
project `nvis-ova/nvis-doc-hub`, requested as **Private**, now has published `main` and `development`
branches. The initial application baseline is `35f18d8` after migrating the unchanged
imported Impeccable executable to Git LFS for GitLab's 5 MiB Git-blob limit. A fresh
remote `main` clone passed LFS download, all 101 imported-skill hashes, and all 96
source-snapshot hashes; a separate empty-cache LFS download also verified the
official destination's executable. Read [repository setup](../../../evidence/repository-setup.md)
and the README's Git LFS setup before resuming. Live-search suggestions remain on
`development`; `main` retains the baseline application. Do not
reinitialize or force-push the published repository.

The singular remote name is the user's final destination and supersedes the
planned plural name in the historical prompt below. Local directory names remain
`nvis-docs-hub`.

The singular repository is the only configured remote. The user confirmed
deleting the earlier plural GitLab project on 23 October. Repository publishing
does not require webpage verification; use Git checks for commits and pushes.

The earlier [implemented application checkpoint](20261022T223459Z-implemented.md)
records the original local build and repository setup.

The local application is now built. See [startup](../../../README.md) and
[verification](../../../evidence/verification.md). The original resume prompt below
is retained as historical context; it is no longer a request to start from scratch.

## Exact resume prompt

Work in `/Users/dgayle/Desktop/NVIS/AI Software Factory/nvis-docs-hub`. Read
`START_HERE.md`, `BUILD_BRIEF.md`, `SKILLS.md`, and
`handoff/sessions/nvis-docs-hub/20261022T221411Z-direct-build.md`, then applicable
project guidance. Build the functional hub using the imported tasteskill and
impeccable skills. Preserve the settled product scope; the rejected Claude council
output is background, not an approved implementation plan. Choose and document
the remaining technical details, follow applicable planning requirements, and
continue through local implementation, meaningful tests, and browser verification.
Keep SSO/access control and the contributor publishing skill deferred. Preserve
the sibling pipeline and notes. The eventual remote is PRIVATE
`nvis-ova/nvis-docs-hub`; the immediate deliverable is a working local application.
