# Browser verification of empty and failed-refresh states

Verified with visible Google Chrome (`headless: false`) through Playwright on
2026-10-22. The browser loaded the actual locally served application; no HTML
mock or network interception was used.

The task instance used `http://127.0.0.1:59105` and the disposable database
`/tmp/nvis-state-browser-gx725m31/state.sqlite3`. The default
`data/hub.sqlite3` was not used or modified by this verification. The existing
port 8000 server remained running and returned HTTP 200 after this task's server
was stopped.

## Checks and screenshots

- An empty database rendered “No projects published yet” and a visible setup
  action. [Empty catalog](../.impeccable/review/state-empty.png).
- Searching for `unfindablefixturezz` rendered “No matching documentation” with
  clear-filter and project-browsing actions.
  [No-match state](../.impeccable/review/state-no-matches.png).
- An explicitly synthetic local source was registered and published through
  `Hub.register` and `Hub.refresh`. Its project and page title are
  “Browser verification fixture”; its description identifies it as synthetic
  test content.
- Renaming that task-local source directory made the next `Hub.refresh` fail
  with “Local source directory does not exist.” The source-status page displayed
  “Last refresh failed” and “The previous publication is still available.”
  Its full published revision remained visible.
  [Failed-refresh source status](../.impeccable/review/state-failed-refresh.png).
- Before and after the failure, the revision and publication timestamp were
  identical. The retained fixture still loaded through the browser.
- At a 390 × 844 viewport, a deliberately long code line scrolled within its
  code block. The code viewport was 333 CSS px wide, its scroll width was
  4,061 px, its computed horizontal overflow was `auto`, and setting
  `scrollLeft` to 180 succeeded. The document's client and scroll widths were
  both 375 px; the remaining viewport width was the visible browser's scrollbar.
  There was no horizontal page overflow.
  [Narrow long-code reader](../.impeccable/review/state-long-code-mobile.png).
- No browser `pageerror` events occurred. All nine final automation checks
  passed. Screenshots were opened and visually inspected.

The retained revision was
`content-sha256:bf0579b56b292fc59a0a008470071cfcf1cd170b47e96d6847b0e848b45afd32`.
The retained publication time was `2026-10-22T22:33:18.056871+00:00`.
These are a local fixture content digest and timestamp, not a GitLab revision.

Detailed measured results are in
[state-browser-results.json](state-browser-results.json).

## Commands used

From the project directory, the isolated server was started with:

```sh
.venv/bin/nvis-hub \
  --db /tmp/nvis-state-browser-gx725m31/state.sqlite3 \
  serve --host 127.0.0.1 --port 59105
```

The browser automation ran with the installed Playwright skill:

```sh
node /Users/dgayle/.agents/skills/playwright-skill/run.js \
  /tmp/playwright-test-nvis-states.js
```

The temporary script invoked
`/tmp/nvis-state-browser-gx725m31/manage-fixture.py` using this project's virtual
environment to register/publish and then fail the source through the real Hub
service. The task's source originally lived under
`/tmp/nvis-state-browser-gx725m31/repository/` and was renamed to
`unavailable-source/` for the failure check.

Both task-owned server sessions (PIDs 80213 and 80770) were stopped using
their own PTYs. A socket check confirmed port 59105 closed afterward; the main
port 8000 server still returned HTTP 200. No application code was changed by
this verification. The root agent corrected the singular page-count copy.
The source-status screenshot was recaptured in visible Chrome at the same
1440 × 1000 viewport and now shows “1 page” alongside the preserved refresh
failure and exact retained revision. The existing disposable database and
fixture were reused without reset.
