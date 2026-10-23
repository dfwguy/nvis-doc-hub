# Resume the NVIS documentation hub build

**Implementation status (2026-10-22):** the local application is now built. Start
with [README.md](README.md), [verification evidence](evidence/verification.md), and
the [latest checkpoint](handoff/sessions/nvis-docs-hub/latest.md). The original
build prompt below is preserved as project context.

Open a new chat with this directory as the working project:

`/Users/dgayle/Desktop/NVIS/AI Software Factory/nvis-docs-hub`

Paste this prompt:

> Build the functional NVIS documentation hub in this directory. First read
> `BUILD_BRIEF.md`, `SKILLS.md`, and
> `handoff/sessions/nvis-docs-hub/latest.md`, then the referenced session checkpoint
> and applicable project guidance. The brief contains the settled product decisions
> from our previous conversation; do not repeat the discovery interview.
>
> Use the complete local `design-taste-frontend` (tasteskill) and `impeccable` skills
> under `.agents/skills/`. Make a refined NVIDIA-themed catalog, search, and reading
> experience backed by actual imported documentation, persistent search, and working
> MCP discovery/search/retrieval. Read `context/manager-notes.md` for the team's
> maintainability priorities. The earlier Claude council outputs were rejected and
> are not approved implementation requirements; no further council round is needed.
>
> Verify current state, settle the remaining technical choices, follow applicable
> planning requirements, and carry the local implementation through meaningful
> tests and browser verification. Make routine engineering choices without reopening
> settled product scope. Work in this new project and preserve the sibling pipeline
> and notes. Use both agreed GitLab seed repositories, report real connectivity
> limitations honestly, and continue useful local work with labelled fixtures if
> necessary. Access control and the future publishing skill remain deferred.
>
> The eventual remote is PRIVATE `nvis-ova/nvis-docs-hub`. The immediate deliverable
> is a working local application, its startup instructions, and verification
> evidence. This directory already exists and contains context and imported skills;
> preserve them while building.

The checkpoint records what is already present and what has not been implemented.
`docs/deferred-access-control.md` preserves the SSO/NVIS group discussion for later.
