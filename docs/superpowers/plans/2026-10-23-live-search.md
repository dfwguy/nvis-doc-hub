# Live search implementation plan

1. **Backend suggestions, independently owned.** Add behavior tests for partial
   last-word matches, exact preceding terms, metadata filters, five-result cap,
   short queries, and overlong queries. Observe red, then add
   `Store.search(..., *, prefix=False)`, `Hub.suggest(query, project=None,
   topic=None, kind=None)`, and the bounded `/api/search/suggestions` route.
   Existing `Hub.search` callers keep exact-term behavior. API fields follow the
   linked design. Run focused tests and lint/type checks.
2. **Shared frontend, root owned.** First reproduce absent live suggestions in
   the actual browser. Add a separate progressive-enhancement search script,
   shared popup styling, and its deferred script tag. Reuse the three existing
   form layouts, input labels, filters, and ordinary submissions.
3. **Integration and edge cases.** Test real prefix results, anchor navigation,
   project/filter changes, keyboard selection and dismissal, stale responses,
   empty/failure states, composition input, touch-sized rows, constrained popup
   height, and operation without JavaScript. Extend the reusable browser checks
   with the key live-search regression paths.
4. **Review and finish.** Run all Python tests, Ruff, mypy, JS syntax checks, and
   the browser regression suite. Review desktop/tablet/phone captures and request
   independent code and visual review. Run the Impeccable detector once after UI
   completion. Update design/use documentation and checkpoint, then commit only
   this feature on `development`.

## Review focus

- Late network responses must not replace newer results or reopen dismissal.
- A project filter must not leak suggestions from another project.
- Enter without a selected option must retain normal search submission.
- Result clicks must survive focus changes; text must be rendered without HTML
  injection and result links must remain inside the hub.
- A phone keyboard must not leave the dropdown outside the visible viewport.

## Completion

All four steps are complete. Verified 44 passing Python tests, 35 existing browser
checks, and 28 live-search browser checks; lint, formatting, type, syntax, and
source-diff checks pass. Code and visual reviews found no material defects.
See `evidence/live-search-verification.md` for coverage and detector dispositions.
