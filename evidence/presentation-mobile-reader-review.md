# Phone document reader review

Reviewed the dark NVIS - OVA reader against `DESIGN.md` and the project’s Impeccable polish reference. This was a read-only app/content review. Only this evidence report and captures under `.impeccable/presentation-mobile-reader-review/` were authored by this reviewer.

## Visual coverage

- Visually inspected **all 92 supplied 390 × 844 arrival screenshots**, `390-01.png` through `390-92.png`, from `.impeccable/presentation-documents/`. These cover 85 Cluster Bringup documents and seven Documentation Pipeline documents.
- Created and inspected eight numbered contact sheets covering every supplied phone screenshot. The source screenshots show the first viewport, not each document’s entire length; the review does not claim full-page visual inspection of every document.
- Read the route mapping and layout evidence in `evidence/presentation-document-verification.json`.
- Used visible Chromium against `http://127.0.0.1:8000` at 390 × 844 for four representative long documents. Captured and visually inspected their middle and bottom, including source trails and adjacent-page navigation:
  - `390-40`: installing the SSH gate on one compute node — 7,514 px live height, 14 code blocks.
  - `390-45`: internal application architecture and trust — 5,246 px, prose and a responsive SVG diagram.
  - `390-73`: observability reference — 11,112 px, 12 tables and ten code blocks.
  - `390-82`: GitLab credential tutorial — 16,687 px, 21 code blocks, a table and three lists.

## Findings and verification

1. **Resolved: code inside headings was undersized.** The global inline-code size rendered `/cluster` at 13 px inside a 27 px phone H1. Other visible examples included `md0`, `cmsh`, `cmods`, `srun`/`sbatch`, and `sinfo`/`squeue`. The root agent applied shared heading-relative code sizing. Live checks now show 22.95 px code inside 27 px H1s for Benchmark `/cluster`, Running `cmsh` from a non-BCM host, and How to troubleshoot a failing `sinfo` or `squeue`. All three were visually rechecked with clean wrapping and 375 px document client/scroll widths. Captures: `heading-code-before.png` and `390-{12,26,72}-heading-code-after.png`.
2. **Resolved: lone previous-page alignment.** The final tutorial’s single previous-page link now remains at the left edge (20 px; `text-align: start`). Captured and visually checked in `390-92-lone-previous-after.png`.
3. **Resolved: copy button clipped after horizontal code scrolling.** In the observability reference, scrolling a 622 px code block within its 333 px scroll region moved the original copy button to the clipped left edge (`390-73-code-scrolled.png`). The root agent moved the button into a containing `.code-block` and set its stacking order so the code surface cannot intercept pointer clicks. Fresh visible-browser checks at scroll positions 0, 145 and 289 px show the complete 36 px-high button staying within the block’s 20–355 px bounds, with its right edge fixed at 347 px. Pointer copying at the start/middle and keyboard Enter at the end all copied the exact full block text, retained focus, and preserved the horizontal scroll position. Visually checked all three `390-73-code-scrolled-{start,middle,end}-after.png` captures.

No material styling defect remains in the reviewed phone surfaces. The four representative middle/bottom views were recaptured and visually inspected after the final copy-control stacking fix; page heights and reading rhythm remained unchanged. No additional material styling defect was apparent in the 92 phone arrival views. Prose remains at 16 px with generous line spacing, long paths wrap, dark surfaces and green links follow the documented system, and source metadata and page endings remain coherent. The authored multiple H1s in the pipeline source documents were treated as source content and left unchanged.

## Interaction checks

- Opened each representative mobile contents disclosure and clicked one interior link on each page: **4/4 anchors landed at a visible 48 px viewport offset**. The disclosures contained 8, 4, 11 and 19 links respectively.
- Focused and keyboard-activated the first copy control on each of the three representative pages containing code: **3/3 clipboard values exactly matched the authored block text**; each displayed its Copied state. The separate wide-code regression also passed mouse copying at the start/middle and keyboard copying at the end.
- Both representative table regions expose a labelled focusable scroll area. Confirmed 335 px viewport / 580 px table width and successful contained horizontal scrolling. Verified keyboard ArrowRight scrolling while both checked table regions retained focus.
- Confirmed contained horizontal scrolling in a long reference code block without document overflow.
- Confirmed the architecture diagram loads, fits the reading column, has descriptive alt text, and exposes a full-size SVG link returning HTTP 200 with `image/svg+xml`.
- Four representative readers returned HTTP 200 and produced **no browser console errors or uncaught page errors**. All four had matching document client/scroll widths of 375 px.

Detailed read-only checks are recorded in `live-reader-checks.json`, `after-fix-checks.json` and `code-scroll-after-checks.json` in the capture directory. The contact sheets preserve the original supplied arrival captures; the heading, pager and copy-control after-captures reflect the live fixes. The final representative-reader capture pass returned no console/page errors and repeated all contents, table-keyboard and code-keyboard checks successfully.
