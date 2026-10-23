# Discovery refinement independent code review

Reviewed 23 October 2026 on `development`, before the refinement commit.

No unresolved material defects remain after the corrections below.

## Scope

Read the refinement plan, pure title/heading formatter, shared command-name
contract, Jinja integration, live suggestions, popular-only discovery markup,
native theme switch, pre-stylesheet preference loading, semantic theme roles and
light bridges, and focused tests. Checked correctness, authored-content
preservation, escaping, theme accessibility and the bounded discovery behavior.
The root recorded checkpoint `4682c9d` as pushed and clean before UI work; this
review did not change Git state or repeat that publication.

## Latest carousel and navigation clarification

After the initial grid review, the user explicitly retained the single popular
carousel and removed the global Projects list. Re-read the corrected shared
navigation macro, popular template, CSS and scrolling enhancement. No additional
material defect was found in this narrow delta.

Independent 390px browser probes on isolated port 8001 verified one carousel,
six genuinely opened documents, 300.95px cards in a 350px rail, a 44px Next
control and successful Enter-triggered scrolling under reduced motion. Home
and search render no project navigation. Project and reader routes have no
project-name switcher links and retain only Document sections: both navigation
variants contain the current project's 85 hosted page links, and the reader
opens exactly one active category/current link. Theme/casing/source/API behavior
is unchanged by this delta. No full-suite rerun was performed for this review.

## Findings

1. Resolved: the light topbar retained NVIDIA Green focus outlines on white,
   giving only 2.41:1 contrast. A real keyboard probe reproduced the Menu
   summary's solid 2px `#76b900` indicator. The new light-theme focus bridge uses
   `--accent`; the same independent probe now reads `#004831` with visible focus.
2. Resolved: plain command names outside the initial exclusion list were
   capitalized (`dpkg -x options` became `Dpkg -x options`, likewise `grep` and
   `npm`). The shared command list now preserves these unambiguous commands,
   with regression cases. Independently verified both server tests and live
   suggestion formatting for `dpkg`, `grep`, `npm` and `apt`; ordinary prose
   still capitalizes its first letter.
3. Resolved: Topic options and active Topic chips also used the document-kind
   label map. An authored `how-to` topic consequently displayed as `How-to guide`,
   adding a word beyond the requested casing change. A disposable source fixture
   reproduced both labels. Kind-label mapping is now restricted to Document type;
   Topic uses the pure display formatter. The independent correction probe
   preserves authored `how-to` for the Topic option/chip, retains the intentional
   `How-to guide` Document type label, formats the Project chip, and confirms
   stored metadata is unchanged.

The browser worker separately found that adding the theme switch after Menu
could position the mobile menu outside the header. Re-read the new header-based
positioning and independently measured the corrected light-theme overlay at
320, 390 and 768 pixels. Its left/right bounds stay inside the viewport, with
equal scroll/client widths at each size. The independent browser review owns
the full two-theme responsive pass. After the additional inherited-minimum-width
correction, a further independent 320-pixel probe with a reserved scrollbar
gutter measured the panel at x=16–289 with equal 271-pixel scroll/client widths
in both dark and light themes.

## Focused verification and reasoning

- `.venv/bin/python -m pytest -q tests/test_presentation.py`: 49 passed after
  the command-name correction. The full suite was not rerun by this reviewer.
- A disposable web fixture verifies that rendered heading prose capitalizes
  while the complete stored document dictionary, HTML, Markdown, heading IDs,
  body prose and fenced code remain unchanged. API section results retain their
  authored lowercase headings. Links and anchors retain their original targets.
- The formatter changes at most one initial prose letter, preserves mixed case,
  technical punctuation, paths and known commands, and skips code/preformatted
  regions and headings that start with nested markup. It does not decode or
  replace encoded HTML. Jinja escaping remains enabled for labels, and live
  suggestions still use `textContent` and the existing safe URL checks.
- Default discovery has one popular section, requests only six actual opened
  documents, and shows an honest empty-history state. There are no project/type
  shelves or alphabetic substitutes. The single popular carousel retains native
  scrolling, named 44px controls and reduced-motion support. Explicit project/filter
  and full-library routes continue using the existing vertical paginated browse
  query; search/API/SQL contracts are unchanged by the refinement.
- The named native button switch has stable `Dark mode` semantics and updates
  `aria-checked` immediately. The head script loads the valid saved preference
  before styles, defaults to dark, guards storage failures, and handles
  cross-tab preference changes. Without JavaScript, the switch stays hidden and
  the default dark surface remains usable. The implementation uses the existing
  Python frontend and native KUI guidance without adding dependencies.

Only this evidence file was written by the reviewer. No application, source,
imported-package, screenshot, database or other documentation file was edited.
