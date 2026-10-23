# Future publishing integration contract

The contributor publishing skill is deferred. Future automation can use the
current trusted CLI contract without changing source authority or executing repo
instructions.

1. Produce or select authored documentation in the original repository. Commit it
   there through the repository's normal review process.
2. Create a registration JSON using [configuration fields](configuration.md).
   Choose stable project identity, a useful description, explicit documentation
   scope, supported navigation, and only authored/explicit metadata.
3. Make source acquisition credentials available through the named environment
   variable. The HTTPS archive adapter does not use Git credential helpers. Keep
   secrets out of artifacts.
4. Run `nvis-hub --db PATH register CONFIG`, then `nvis-hub --db PATH refresh SLUG`.
   Check process exit codes. Successful commands write JSON to stdout; failures
   report an operator-facing message on stderr and return nonzero.
5. Inspect `nvis-hub --db PATH list` for revision, publication time, document count,
   and `last_error`. A registration alone is not a successful publication.
6. Verify expected pages and sections through the read-only MCP tools or hosted
   routes; cite the exact revision and source URL.

A successful refresh replaces only that project's publication, including removal
of deleted documents and search sections. Failure preserves its last successful
publication. Project slug and repository-relative document path form the stable
identity; section anchors add heading identity. Renaming a source path changes
that identity. Concurrent or automatic publication orchestration, CI/webhook sync,
author authorization, and SSO remain future work.

The browser and MCP intentionally expose no administrative mutation endpoint.
An eventual skill should use this CLI locally or a separately designed authenticated
publishing service, and should report acquisition failure without inventing docs.
