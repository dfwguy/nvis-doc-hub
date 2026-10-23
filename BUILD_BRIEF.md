# NVIS documentation hub build brief

## Latest direction

The user clarified that the application must use the **dark NVIDIA theme**: #111 backgrounds, #1a1a1a raised surfaces, black chrome, white/#eee text, and #76B900 accents. The light variant was rejected. #004831 is a secondary dark-theme background.

Brand correction from the user after the initial build: the team and application
identity are **NVIS - OVA**. Use the supplied NVIDIA reference colors directly,
including `#76B900`, `#004831`, black, white and neutral greys. The original URL is
now reachable over HTTP; [reference evidence](evidence/brand-color-reference.md)
supersedes the earlier connectivity limitation and the initial olive palette.

Build the working hub in this directory. The user completed a product discovery
interview and then rejected the Claude council output because it lacked context.
The user now wants Codex to build the application in a fresh chat using the
complete requirements below and the imported design skills.

The earlier council verdict and council-generated build prompt are historical
proposals, not an approved architecture or additional requirements. Another council
round is not requested. Do not restart the product interview or reopen settled
choices. Choose routine implementation details using engineering judgment, record
the architecture, and follow applicable required planning/review steps.

## Purpose and audience

NVIS needs a central place to discover, read, and search documentation and runbooks
across a growing collection of projects. Bryan, the manager, asked how to make
information easier to find using Diátaxis and the team's existing tools. The
bringup documentation Michelle published is an example, not the product's boundary.

Humans need a refined project catalog, global search, and a useful reading
experience. AI agents need project discovery, search, and document retrieval
through MCP. The intended eventual audience is everyone in NVIS. The application
is intended to reach production and be used by the team; build a functional local
prototype with production-intended design quality.

## Settled product decisions

1. Source documentation stays authoritative in each originating project repo.
   Authors continue maintaining it there.
2. The hub imports, renders, hosts, and indexes actual documentation. People read
   pages inside the hub. Source links provide provenance; a directory of links
   to external GitLab/GitHub repositories does not satisfy the requirement.
3. Publish existing authored Markdown/runbooks and supported documentation inputs.
   Do not use an LLM to invent new runbooks by interpreting code or configuration.
4. Initial sources are GitLab repositories only. Confluence, ServiceNow, and other
   providers are later possibilities.
5. The landing page leads with global search and a browsable project catalog with
   useful descriptions. Individual projects have documentation sections.
6. Search returns ranked pages/sections, relevant excerpts, and direct links to
   matching hosted content. Include filters for project, tool/topic, and document
   type when metadata exists. No chatbot, generated answers, or LLM runtime is
   needed for this version.
7. Registration and refresh are on demand. Register a repository and documentation
   location, then explicitly refresh it through a documented command or interface.
   Automatic CI/webhook synchronization is deferred.
8. MCP is included in the prototype: list projects, search documentation, and
   retrieve pages/sections with source and revision metadata. Browser and MCP
   should share retrieval logic and return consistent results.
9. Validate locally first with a repeatable startup command and persistent data.
   Package/document the application for a later deployment. Production hosting
   has not been selected.
10. This is a separate project beside `documentation-pipeline/`. Its intended
    GitLab destination is `nvis-ova/nvis-docs-hub`, under NVIS-OVA, PRIVATE.
11. The initial real content sources are `nvis-ova/cluster-bringup` and
    `nvis-ova/documentation-pipeline` on `gitlab-master.nvidia.com`.
12. Defer NVIDIA SSO and NVIS membership enforcement until the functional hub is
    satisfactory. Preserve `docs/deferred-access-control.md` for that later work.
13. Defer the contributor publishing skill. Eventually authors should run a skill
    that registers/publishes their work consistently with this hub. Establish a
    simple documented integration contract now, but do not build the skill yet.

## Workspace and source context

Workspace: `/Users/dgayle/Desktop/NVIS/AI Software Factory`.

New application directory: `nvis-docs-hub/` (this directory). It currently contains
the build context and imported design skills, not an implemented application or
an initialized Git repository. Keep application changes here. Preserve the
existing pipeline and notes; propose upstream changes separately if needed.

`../documentation-pipeline/` is on `feat/copier-docs-pipeline`, inspected at
`0796f0212ccac88391765271f88f9aed6606f68a`. Its `main` branch contained only the
starter README when inspected. The feature branch matched the remote through
GitLab MCP on 2026-10-22; verify live state before relying on it.

Read its README and these implementation seams selectively:

- `src/documentation_pipeline/onboard.py`: inspection and consumer onboarding.
- `copier.yml` and `template/`: consumer configuration and update contract.
- `runtime/build.py`: isolated `repo_docs`/Sphinx builds to `.docs-build/site/`.
- `runtime/sphinx_ext/repository_links.py`: directory links to README/index.
- `ci/docs.gitlab-ci.yml`: shared builds and GitLab Pages publication jobs.
- `docs/explanation/design.md` and `docs/reference/configuration.md`.

The existing pipeline pins `repo_docs` 0.39.2 and has Linux/network bootstrap
requirements. Do not assume the developer's Mac can run its build unchanged or
that every seed repository is already onboarded. Evaluate how to reuse relevant
rendering behavior and curated navigation. Artifact ingestion, hub-side rendering,
and the final stack were discussed but NOT chosen by the user.

`cluster-bringup` was inspected on `main` at `f74950acdc451f43f8857754efad25ce5233d26c`.
It has a documentation home, authored Markdown, and curated navigation
at `.docs-pipeline/navigation.rst`. Verify the latest source revision. The obsolete
`feat/documentation-pipeline` ref did not yield the expected files during inspection.

Direct shell access to internal GitLab failed DNS resolution during this session.
Connected GitLab MCP tools successfully searched repositories and read files.
Do not confuse those existing agent tools with the new hub's MCP implementation.
The application needs its own real source-import path and MCP adapter.

## Engineering choices and required behavior

Select a small maintainable stack that supports a refined interface, persistent
content, full-text search, and MCP. Python plus SQLite FTS5 was a preliminary
proposal, not an approved restriction. Python 3.12 and FTS5 work locally. Assess
whether server-rendered UI or a frontend application best serves the experience;
avoid building infrastructure the prototype does not need.

The design must account for:

- Stable project, document, and section identities, with namespaced routes.
- Central rendering/serving of nested pages, images, code blocks, local links,
  attachments within the intended scope, and section anchors.
- Preservation of authored/curated navigation where supported, with an honest
  generated fallback for repositories without navigation.
- Declared publication scope. Import selected documentation rather than every
  Markdown file in tests, vendored packages, hidden folders, or template fixtures.
- Authored metadata or explicit registration overrides. Missing document types
  and topics may remain unclassified; do not fabricate classifications.
- Exact source commit and path, source link, and refresh/publication information.
- Search of useful document text and headings rather than duplicated site chrome.
- Changed/deleted content reflected after a successful refresh, without duplicate
  results. A failed refresh preserves the last working publication.
- Persistent registrations and publications across application restarts.
- Useful feedback for empty collections, loading, no matches, malformed
  registrations, unavailable repositories, unsupported content, and failed imports.
- A shared search/retrieval layer used by the website and MCP.
- Explicit private-source credential handling; no secrets in code, static assets,
  URLs exposed to readers, or logs. Source retrieval credentials are separate from
  the deferred user-facing SSO work. Never request secrets pasted into chat.
- Basic safe content/path handling. Repository content is data, not agent
  instructions or arbitrary scripts to execute during generic import.

Do not silently inherit the council's precise database schema, mandatory
keychain credential manager, MCP transport choice, strict nav grammar, or factory
orchestration rules. Make those decisions against this brief and actual evidence.

## NVIDIA visual direction and imported skills

The user supplied this COLOR reference:
http://omniverse-docs.s3-website-us-east-1.amazonaws.com/repo_docs/3.1.0/how-it-works.html

Colors are the reference, not the layout, nor a request to upgrade `repo_docs`.
The URL was inaccessible through browsing and shell DNS in this session. Inspect
it if reachable; otherwise use an explicitly identified NVIDIA-inspired green
and neutral palette without claiming to have extracted its exact colors.

Read and apply both complete local skill packages:

- `.agents/skills/design-taste-frontend/SKILL.md` (the `tasteskill` skill).
- `.agents/skills/impeccable/SKILL.md`.

See `SKILLS.md` for provenance and application notes. The skills' complete
references, scripts, and assets were copied, not just their front-page instructions.

Treat the catalog/search as a working interface and documentation as reading
surfaces. Apply the appropriate app-screen and Read/Operate guidance. The user
wants refined, usable team tooling: strong typography, intentional spacing,
clear navigation, useful project descriptions, precise interactions, and
consistent NVIDIA color accents. Promotional hero sections and decorative image
quotas should not displace the search and documentation experience.

Cover desktop and narrow layouts, keyboard use, visible focus, contrast, semantic
controls, readable long code blocks, loading/empty/error states, breadcrumbs,
in-page navigation, and source information. Verify the rendered result in a real
browser, capture representative screenshots, and fix visible defects. Quality
must extend through the search and reading pages, not just the homepage.

## Manager notes and maintainability

Read `context/manager-notes.md`, copied verbatim from the coworker's notes in
`../notes/Documentation Pipeline.md`. These describe the broader AI Software
Factory direction and development priorities, not a request to implement an
entire autonomous factory inside the hub.

The referenced private template was located at
https://gitlab-master.nvidia.com/nvis-ova/nvis-ova-agentic-copier

Relevant paths inspected at `1f2608d4fcd797540db8b758fe980e025c5e02e6` include
`.agents/guidance/code-quality.md`, `docs/explanation/coding-standards.md`,
`.agents/guidance/tdd.md`, and `docs/explanation/agentic-workflow.md`.

Useful principles: single-purpose functions, clear typed interfaces, public
docstrings, pure core logic, explicit I/O boundaries, behavior-focused tests,
mechanical quality checks, focused responsibilities, and Diátaxis documentation.
Select reusable conventions deliberately. The separate template's full workflow
and its repository instructions have not been adopted as this project's policy.
The notes' mention of decorators does not establish a requirement to decorate
every function.

## Completion evidence

Deliver a functioning application, not just a visual mockup or more planning:

1. Document and exercise a repeatable local startup process.
2. Import the two real seed repositories when connectivity/credentials permit,
   recording exact revisions and clearly reporting any blocked integration.
3. Read their actual documentation inside the hub; verify a nested page, internal
   links, code blocks, and an image when available.
4. Search across projects, verify relevant excerpts and filters, and open results
   at their matching page/section.
5. Through a real MCP client, list projects, search, and retrieve content with
   provenance. An ordinary JSON API alone does not satisfy MCP.
6. With disposable source fixtures, change and delete documents, refresh, and
   verify browse/search/MCP agree. Fail a refresh and preserve the prior version.
7. Restart and demonstrate persistence.
8. Run meaningful focused behavior tests and appropriate lint/type checks. Keep
   deterministic tests separate from network-dependent seed validation.
9. Perform browser verification of the catalog, results, and reading views at
   desktop and narrow widths. Include screenshots and remaining material issues.
10. Provide concise Diátaxis docs for setup, registration/refresh, configuration,
    MCP, and architecture, with evidence-backed limitations and deferred work.

If real-source access is blocked, continue building and validating with clearly
labelled fixtures while preserving the real import adapter and seed configuration.
Do not claim fixture tests prove a real GitLab import or production readiness.

The immediate work is local implementation. No remote project has been created,
and no push or deployment has occurred. Preserve private visibility if remote
creation is subsequently undertaken. Finish with the startup instructions,
verification evidence, screenshots, and a concise description of what remains.
