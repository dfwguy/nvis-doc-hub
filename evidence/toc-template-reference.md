# TOC template reference inspection

Inspected 2026-10-23 using the exact user-supplied branch. Source project remains a reference; it has not been imported into the Hub.

- Repository: ssh://git@gitlab-master.nvidia.com:12051/nvis/nvis-rack-status.git
- Branch: feature/auto-run-mode
- Actual fetched HEAD: `7e909322e467b2dd7b31e05fd6c82cdb9d70a610` (matches the supplied SHA).
- Method: isolated temporary bare clone, `git clone --bare --depth=1 --single-branch --branch feature/auto-run-mode --filter=blob:none <SSH URL> <temp>/reference.git`, with batch-mode SSH; read committed paths using `git ls-tree` and `git show`.
- No checkout, repository scripts, Sphinx configuration, application, or build was executed. No existing sibling checkout, local private files, Git index, application database, or branch was changed.
- Inspected documentation sources: `docs/_toc.yml`, `docs/conf.py`, `docs/index.md`, `docs/README.md`, `docs/requirements.txt`, `docs/_static/custom.css`, `docs/_static/local-fonts.css`, scoped Diataxis page frontmatter, and `.cursor/rules/docs-diataxis.mdc`. The root README was also inspected as plain text for surrounding documentation conventions.

## Exact navigation structure

The YAML below is copied from the committed `docs/_toc.yml`. `root` and `file` values are extensionless paths relative to `docs/`; for example, `reference/identity/index` resolves to repository path `docs/reference/identity/index.md`.

There are four caption groups with 1 tutorial, 11 how-to guides, 10 reference pages (6 top-level entries and 4 nested identity entries), and 15 explanation pages. The root landing page is `docs/index.md`. Category caption/order and nested entry order are explicit. Individual `title` overrides are optional. The source has no custom collapse property or accordion JavaScript in this declaration; collapse interaction is a presentation concern of the consuming navigation UI/theme.

```yaml
# The site structure, and the only place it is declared.
#
# sphinx-external-toc rather than per-page toctrees: with `external_toc_exclude_missing: false`
# in conf.py, a page that exists but is listed nowhere is a build failure. That is the check that
# stops a docs site accumulating pages reachable only by search.
#
# The captioned groups are the Diataxis modes, and they are not a naming convention -- a page in
# the wrong one answers a question the reader was not asking. See https://diataxis.fr/ and
# .cursor/rules/docs-diataxis.mdc.
#
# The Tutorials caption appears now that the first tutorial exists. Diataxis is explicit that empty
# categories are worse than absent ones, so a caption is added only together with its first page.

root: index

subtrees:
  - caption: Tutorials — learning by doing
    entries:
      - file: tutorials/distribute-your-first-image
        title: Distribute your first image with NVIS-P2P

  - caption: How-to guides — getting something done
    entries:
      - file: how-to/configure-a-deployment
        title: How to configure a deployment
      - file: how-to/authenticate-to-the-api
        title: How to authenticate to the API
      - file: how-to/grant-a-team-access
        title: How to grant a team access
      - file: how-to/diagnose-a-refused-request
        title: How to diagnose a refused request
      - file: how-to/add-your-own-script
        title: How to add your own script and register it as a tool
      - file: how-to/use-the-terminal
        title: How to use the terminal
      - file: how-to/stage-observability-agents
        title: How to stage the observability node-agents to a cluster
      - file: how-to/connect-a-pythoncm-cluster
        title: How to connect a PythonCM (BCM) cluster
      - file: how-to/distribute-a-catalog-image
        title: How to distribute a catalog image to the fleet
      - file: how-to/recover-p2p-peers-after-a-reimage
        title: How to bring P2P peers up on new or reimaged nodes
      - file: how-to/publish-the-deployment-tracker
        title: How to publish the deployment tracker

  - caption: Reference — the machinery, described
    entries:
      - file: reference/configuration/settings
        title: Configuration settings — every setting, generated
      - file: reference/catalog/projects-and-clusters
        title: Projects and clusters
      - file: reference/catalog/tools
        title: Tool documents
      - file: reference/actions-by-scope
        title: Actions by scope — node, rack, multirack
      - file: reference/identity/index
        title: Identity and authorization
        entries:
          - file: reference/identity/actions-and-resources
            title: Actions and resources
          - file: reference/identity/policy-schema
            title: Policy schema
          - file: reference/identity/evaluation
            title: How a decision is made
          # The generated vocabulary. It existed all along and was not in this file, so a reader
          # looking for "which services and actions are there" found the grammar on the page
          # above and never the list itself.
          - file: reference/identity/action-vocabulary
            title: Action vocabulary — every service and action
      - file: reference/p2p-catalog-distribution
        title: P2P catalog distribution — components, parameters, scripts

  - caption: Explanation — why it is like this
    entries:
      - file: explanation/the-parametric-platform
        title: The parametric platform
      - file: explanation/why-authorization-is-default-deny
        title: Why authorization is default-deny
      - file: explanation/how-a-script-path-is-chosen
        title: How a script path is chosen
      - file: explanation/the-cluster-home-directory
      - file: explanation/how-cluster-paths-reach-scripts
        title: The cluster home directory
      - file: explanation/geometry-and-hostnames
        title: Geometry and hostnames
      - file: explanation/which-storage-engine
        title: Which storage engine, and why
      - file: explanation/why-no-pythoncm-broker
        title: Why there is no PythonCM broker
      - file: explanation/porting-the-pythoncm-fork
        title: Porting the PythonCM fork
      - file: explanation/p2p-module-integration
        title: NVIS-P2P as a per-cluster capability
      - file: explanation/active-passive-and-blue-green
        title: Active/passive and blue/green (roadmap)
      - file: explanation/p2p-catalog-distribution
        title: How catalog images reach every node
      - file: explanation/auto-run-scheduled-routines
        title: "Auto-run: routines the app schedules, runs and records"
      - file: explanation/toward-hands-off-bring-up
        title: Toward hands-off bring-up and validation
      - file: explanation/auto-deploy
        title: "Auto-deploy: from an empty app server to an operating cluster"
```

Source quirk: `explanation/the-cluster-home-directory` has no title override, while `explanation/how-cluster-paths-reach-scripts` explicitly uses the title “The cluster home directory”. This is the source as committed, not an inference that their content is interchangeable.

## Classification and publishing boundaries

Live content is classified explicitly in MyST YAML frontmatter, e.g.:

```yaml
---
diataxis: how-to
description: A one-line description of this page.
---
```

All 37 listed content pages were read as committed text: every page has the expected explicit `diataxis` mode and a `description` field; all referenced files exist. Observed counts: tutorial 1, how-to 11, reference 10, explanation 15. None of these 37 files actually has `nvis_generated` frontmatter at this revision, despite the authoring guidance describing that convention.

Valid `diataxis` values are `tutorial`, `how-to`, `reference`, `explanation`. They map to directories `docs/tutorials/`, `docs/how-to/`, `docs/reference/`, `docs/explanation/`. Classification is not a title/filename guess: authoring guidance applies a doing/thinking and learning/working compass. The source states that generated reference pages carry `nvis_generated: <source>` and a generated-source banner. How-to H1s begin “How to ”. The root landing page declares `description` without a `diataxis` mode.

`docs/conf.py` reads each page's frontmatter and injects an orientation banner beneath its H1:

- tutorial: “Tutorial — a lesson. Follow it start to finish.”
- how-to: “How-to guide — steps to a goal. Assumes you know the basics.”
- reference: “Reference — a description of the machinery. Look things up here.”
- explanation: “Explanation — background and reasoning. No instructions.”

The source requires every live page in `_toc.yml`: `external_toc_exclude_missing = False`, `nitpicky = True`, and documented Sphinx invocation `sphinx-build -W --keep-going -b html docs static/docs`. The documented checker verifies mode presence, valid mode, directory agreement, and how-to title convention. Those scripts were not run during this inspection.

Legacy `[A-Z]*.md` and `**/[A-Z]*.md` files, `docs/README.md`, screenshots, and `docs/superpowers/` are excluded from the published site. Their presence under docs is insufficient to put them into a live category. Empty categories are omitted until a first page exists.

## Reusable UI conventions

- Theme: `nvidia_sphinx_theme`; `show_toc_level: 2`, `public_docs_features: False`. Navigation lives in `_toc.yml` through `sphinx_external_toc`, not per-page toctrees.
- Captioned groups express reader intent with the exact wording in the YAML. Recursive `entries` expresses hierarchy; the source supports a nested “Identity and authorization” parent page with four child pages.
- Landing-page category cards use `sphinx_design` grid cards, with doc links and one short purpose sentence. The inspected landing page currently has How-to, Reference, and Explanation cards (no tutorial card despite a tutorial being present in the TOC).
- Quiet page-type marker beneath H1: muted text at 0.85rem, 3px left rule, 0.75rem left padding, 1.5rem bottom margin; accents are tutorial green `#76b900`, how-to blue `#1976d2`, reference purple `#7b1fa2`, explanation orange `#ed6c02`.
- NVIDIA green `#76b900` / dark green `#5c9200` for links, active navigation, buttons and note/tip rules; 8px cards, 6px code-block corners; code-copy buttons.
- Fonts are local NVIDIA Sans plus JetBrains Mono (mapped to the theme's `RobotoMono` family), loaded from `docs/_static/fonts/` for offline deployment. The configuration strips network font declarations after build.
- Relative links support serving the built documentation under `/docs/`; no source links or Sphinx footer badge. Build identity includes product version and Git revision.

Practical Hub application: preserve the four explicit modes, their captions and ordering, nested file entries, page title overrides, and visible per-page mode markers. Use collapsible controls in the Hub renderer as requested; the TOC source itself provides the groups and hierarchy, not a collapse flag.
