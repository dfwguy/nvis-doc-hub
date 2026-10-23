# Collapsible navigation browser verification

Latest regression run verified against isolated `http://127.0.0.1:8001` on 23 October 2026 in visible Chromium
151.0.7922.34. The final run passed 34 checks at 1440 × 1000, 768 × 1024, and
390 × 844. The machine-readable results are in
[collapsible-navigation-browser.json](collapsible-navigation-browser.json).

Before implementation, the focused browser test failed because the project page
had no native `details.document-category` for “How-to guides — getting something
done” (expected one, found zero). The same behavior passes after implementation.

The verification covers both project indexes, the desktop rail, the mobile menu,
and reader routes. All 92 published pages appear exactly once in their project
index, match the links in each navigation variant, and return successful HTTP
responses. Cluster Bringup has 6 Tutorials, 36 How-to guides, 9 Reference,
21 Explanation, and 13 Other documentation pages. Documentation Pipeline keeps
its 7 unclassified pages under Other documentation. Counts match their links;
there are no empty groups. Authored source-topic context matches between the
index and both navigation variants.

Native disclosures work with the mouse, Enter, and Space. Keyboard focus has a
visible 2px NVIDIA Green outline. Index groups start closed; each reader opens
only its current category and shows the current document. Desktop active links
scroll into the visible rail. On tablet and phone, category expansion, navigation
links, Escape dismissal, and restored menu focus work. A separate JavaScript
disabled context verifies native index, rail, and mobile disclosures, current
reader state, and ordinary scoped form search.

Live scoped search still offers matching section links and supports keyboard
selection; ordinary scoped search still returns results. The run reported no
browser JavaScript errors. At all three widths, long document titles and paths
remain contained, category summaries keep 16px desktop/tablet or 12px mobile
insets, and the page and menu have no horizontal overflow. Both project and
reader menus assert that their scroll container and every descendant stay within
their available horizontal space.

The phone reader screenshot shows a horizontal scrollbar immediately below the
menu. Focused measurement confirmed that it belongs to the underlying authored
code block, not the menu: at 390px, that `pre` spans y=629.53–830.31 and has
347px of content inside a 333px viewport. The menu ends at y=821 and has equal
343px scroll/client widths with no overflowing descendants. At 768px the menu
also has equal 343px scroll/client widths and no overflowing descendants.
Contained horizontal scrolling for authored code is intentional in DESIGN.md;
it is excluded from the menu-overflow assertion.

Visual inspection of collapsed and expanded indexes, keyboard focus, and tablet
and phone menus found no material layout issue. Representative screenshots:

- [Desktop keyboard focus](../.impeccable/review/categories-desktop-keyboard-focus.png)
- [Desktop expanded index](../.impeccable/review/categories-desktop-index-expanded-fold.png)
- [Tablet expanded index](../.impeccable/review/categories-tablet-index-expanded-fold.png)
- [Phone collapsed index](../.impeccable/review/categories-mobile-index-collapsed.png)
- [Phone expanded index](../.impeccable/review/categories-mobile-index-expanded-fold.png)
- [Phone expanded navigation](../.impeccable/review/categories-mobile-menu-expanded.png)
- [Phone reader with current document](../.impeccable/review/categories-mobile-reader-menu-active.png)

The portable check is [scripts/navigation_verify.cjs](../scripts/navigation_verify.cjs).
Run it with Playwright available in `NODE_PATH`; set `NVIS_HUB_URL` for a different
server or `PW_HEADLESS=true` when no display is available. It resolves artifact
paths relative to the repository. The existing `scripts/browser_verify.cjs`
needs no category-specific change: its nested document link is in authored prose
and remains directly available.
