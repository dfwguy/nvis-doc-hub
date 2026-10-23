# Deferred work: NVIS documentation hub access control

Recorded: 2026-10-22

## Current decision

Build a functional documentation hub first. Defer SSO, group provisioning, and
access-control implementation until the functional approach is established.
This file preserves the findings so that discussion can resume later.
No identity, membership, hosting, or access settings have been changed.

## Product context

The hub is intended to host and search documentation and runbooks across a growing
collection of NVIS projects and repositories. Bringup documentation is one example,
not the boundary of the product.

People need a central landing page, project navigation, readable documentation,
and interactive search. AI agents need discovery, search, and document retrieval
through MCP. The intended reader audience is everyone in NVIS, rather than all
NVIDIA employees. Readers are expected to share access to the published collection.

## Proposed access model, to revisit

- Use existing NVIDIA identities and SSO for people.
- Use a centrally maintained NVIS membership group to grant reader access.
- Give publishing and portal administration to a smaller maintainer group.
- Apply the reader access policy to document delivery, search results/snippets,
  document retrieval, and MCP. Protecting only the landing page is insufficient.
- Decide separately how interactive agents act for a signed-in user and how
  unattended indexing/publishing services authenticate.

The specific NVIS group, its owner, membership lifecycle, and integration mechanism
have not been identified. Do not assume a department email list or a GitLab group
already contains every intended reader.

## Verified findings

### GitLab-Master

The internal [GitLab-Master FAQ](https://nvidia.atlassian.net/wiki/spaces/SCMU/pages/2853078241)
was read through the connected tools. It documents:

- NVIDIA SSO for the GitLab web UI.
- Linking GitLab groups to Active Directory groups/distribution lists through
  LDAP synchronization.
- GitLab group/project owners managing membership and permissions.
- GitLab Pages availability and enabled Pages access control.

For a Pages-based portal, a candidate setup is a dedicated portal project with
reader membership inherited from an appropriately synchronized group, and Pages
restricted to project members. This setup has not been configured or tested.

GitLab's [Pages access-control documentation](https://docs.gitlab.com/user/project/pages/pages_access_control/)
distinguishes project-member access from access for everyone signed in to the
instance. Broad internal visibility does not establish an NVIS-only audience.
Confirm behavior against NVIDIA's deployed GitLab version and settings.

### A separately hosted application

An internal [NVIDIA Entra ID application registration and SSO runbook](https://nvidia.atlassian.net/wiki/spaces/~zixunl/pages/3391686005)
describes application registration, SAML/OIDC, and assignment of access groups.
It is a consolidated engineering runbook, not the authoritative IT policy.
It explicitly defers to the linked IT knowledge-base articles if they conflict.
Use those current IT sources when implementation resumes.

### Existing NVIS platform to investigate

The [NVIS Central page](https://nvidia.atlassian.net/wiki/spaces/NVIS/pages/3314905227)
describes an existing agent platform with Azure AD SSO and access through the
`nvis-central-users` distribution list. It lists Peter Kweon, Pini Solomovitz,
and Nick Lesseos as platform contacts/leads. These are documented findings,
not independently verified current deployment settings.

Potential follow-up: assess whether its hosting, SSO, or MCP infrastructure can be
reused. Its access group has not been verified to cover all NVIS, and its suitability
as a documentation host/search service has not been established.

The [NVIS Lab Environment and Access Setup guide](https://nvidia.service-now.com/esc?id=kb_article&sysparm_article=KB0031224)
also describes using NVIDIA SSO to access GitLab-Master.

## Questions to resolve when this work resumes

1. Which directory group represents all intended NVIS readers, and who owns it?
2. How are joins, departures, contractors, and department transfers reflected?
3. Will the selected host use GitLab membership, an Entra application assignment,
   or an existing platform's access integration?
4. Can readers access published documentation without access to its source repo?
   Which repositories are approved to contribute to the shared collection?
5. How will the website, search API, document API, and MCP enforce the same audience?
6. Which credentials and permissions are needed by publishing/indexing automation?

When implemented, verify both successful NVIS access and rejected access for a
signed-in person outside the allowed group across pages, search, and MCP.
