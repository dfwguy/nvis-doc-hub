# Presentation layout audit

Audited the running authentic hub at `http://127.0.0.1:8000` on 22 October 2026 using a visible Chromium browser. The existing dark NVIDIA palette, NVIS - OVA identity, IBM Plex Sans, bottom-left documentation label, source content, and persistent database were preserved. This independent audit made no application or content edits.

The review followed the imported Impeccable polish and craft-floor guidance, `DESIGN.md`, and tasteskill's app-screen review guidance. It concerns layout and interaction precision in the established system. Reader coverage is recorded separately by the main implementation pass.

## Material findings before fixes

1. **P1 — Initial global-search panel has no horizontal inset.** Route `/search`, selector `.empty-state.search-start`. Its local overrides replace the shared empty-state padding with `20px 0` at 1440 and 768, and `12px 0` at 390. Heading, prose, and example links therefore start exactly on the charcoal panel's left edge. The 1440 panel is 960×153px at x342.5/y349.5; its heading starts at x342.5. At 768 it is 675×153px at x39/y314.5; heading x39. At 390 it is 335×158px at x20/y301.25; heading x20/y313.25, only 12px below the top. Reuse the existing shared `.empty-state` inset of 38px 28px desktop/tablet and 24px 20px mobile. Evidence: `before-{1440,768,390}-search-start.png`.

2. **P2 — Search-result arrow wraps into an isolated row on phone.** Route `/search?q=slurm`, selector `.search-result:nth-child(2) h2 a` and `.search-result h2 svg`. At 390px, “Symlink the config to the default path” fills the line and the 18px arrow wraps alone to the left edge of the next line. An inline anchor with a 5px icon margin permits the orphan. Keep a shrinkable title and nonshrinking arrow together in the shared result-heading layout. Evidence: `before-390-search-results.png`.

No other material spacing, alignment, wrapping, or action-placement defect was found in the non-reader routes reviewed below. Native horizontal scrolling inside code remains deliberate and contained. Long navigation and repository names remain readable, with wrapping rather than page overflow.

## Coverage

Each of these nine route/state variants was opened, measured, captured, and visually reviewed at **1440×900**, **768×1024**, and **390×844**, for 27 core renders:

- Catalog `/`.
- Initial global search `/search`.
- Populated search `/search?q=slurm`.
- No matches `/search?q=zzzauditnomatchzz`.
- Cluster Bringup project `/projects/cluster-bringup`.
- Documentation Pipeline project `/projects/documentation-pipeline`.
- Source status `/sources`.
- Help `/help`.
- Missing project `/projects/absent` — correct 404 with visible recovery actions.

Additional rendered states:

- Open search filters at all three widths, including phone's stacked labels, 44px selects, and Apply filters action.
- Applied project filter and no matches at 390; Clear filters action removes the project parameter and preserves the query.
- Dense Cluster Bringup menu at the top and bottom at 768 and 390; desktop sidebar scrolled to bottom at 1440.
- Source-list bottom and refresh instructions at all three widths.
- Help's registration/code/agent area at all three widths.
- Visible keyboard skip-link state and sequential focus on phone.

## Interaction checks

21 route interactions passed, seven at each width:

- Click Global search from the desktop rail or mobile menu.
- Submit the real query `configuration` and receive results.
- Apply the Documentation Pipeline project filter and receive 11 matching sections.
- Click a result and reach its exact published matching-section fragment.
- Reach help through the desktop fixed footer or bottom of the long mobile navigation.
- Follow source registration instructions to `/help#sources`.
- Recover from the missing project through Browse documentation.

The open mobile menu remains inside the viewport: 360×948px at 768, 360×768px at 390, with independent vertical scrolling for 3978px of real navigation content. Escape closes it and returns focus to “Open navigation.” Main action, filter, example-link, and skip-link keyboard focus is visible in NVIDIA Green. The search input uses its containing assembly's focus ring.

Across the 27 core renders, document scroll width never exceeded the layout viewport; there were no out-of-bounds main-content elements and no browser page errors. Font loading was awaited before capture. The ordinary visible desktop scrollbar accounts for 15px of the configured viewport width.

## Evidence and reproduction

Captures and raw metrics are in `../.impeccable/presentation-audit/`. `before-metrics.json` records route/status, viewport, main element boxes, padding, and overflow. `interaction-checks.json` records the 21 actual click-through results. Before images follow `before-{width}-{route-state}.png`; long project/source/help pages also have `-full.png` captures.

Reusable browser scripts are `/tmp/playwright-test-presentation-audit.js` and `/tmp/playwright-test-presentation-interactions.js`. Both import the installed Playwright module and launch visible Chromium. They only browse the application and write audit captures.

## Resolution status

**Both findings are resolved and independently verified. No unresolved material layout or interaction issue remains in this audit's scope.**

After the implementation owner removed the local `.search-start` overrides, the initial panel inherits the shared bordered empty-state treatment. At 1440 and 768 its computed padding is `38px 28px`; the heading begins 29px from the outside left edge and 39px below the top (including the 1px border). At 390 the padding is `24px 20px`; the corresponding insets are 21px and 25px. Every tested horizontal and vertical content inset exceeds 20px. The panel is now 960×191px, 675×191px, and 335×184px at the three respective widths. Heading, prose, and examples have a consistent shared inset. See `after-{1440,768,390}-search-start.png` alongside the before images.

The shared result link now uses an inline-flex layout with a shrinkable title span and an 18px nonshrinking arrow. At 390, the previously affected second title spans two lines within a 307px text lane; its arrow remains at x337/y706.97, just 4px below the first title-line top at y702.97. The arrow has no independent row. First-four-result arrow geometry assertions passed at all three widths, and the updated result screens were visually reviewed. See `after-390-search-results.png`.

The final pass repeated the original 27 core route/viewport renders, captured and visually reviewed them, and added six more renders:

- Direct `/search?q=` with exactly 201 ASCII characters at all three widths displays “Shorten your search” and the 200-character recovery instruction in a correctly padded panel.
- `/search?q=slurm&offset=30` at all three widths displays the second page and the correct `31–60+ results` summary.

All **33 final core renders** had contained layout and no browser page errors. Filters, dense navigation, clear action, source/help tails, 404 recovery, keyboard focus, and both repaired states were recaptured. **24 final click-through checks passed**, eight at each width. These repeat the initial seven paths and add clicking Next results and Previous results, verifying `31–60` then `1–30` while preserving the real `slurm` query. Both pagination actions stay separate, aligned, and inside the page at 390.

Final raw records: `after-metrics.json` and `after-interaction-checks.json`. Final screenshots follow `after-{width}-{route-state}.png`, including `search-too-long`, `search-page-2`, and `pagination-bottom`. Reusable final scripts are `/tmp/playwright-test-presentation-audit-after.js` and `/tmp/playwright-test-presentation-interactions-after.js`.
