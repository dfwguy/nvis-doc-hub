# NVIDIA color reference evidence

**Selected mode: dark, explicitly clarified by the user.** Light-mode values below describe the reference alternative, not the application target.

Retrieved 2026-10-22 from the exact color reference supplied by the user:
[How repo_docs Works](http://omniverse-docs.s3-website-us-east-1.amazonaws.com/repo_docs/3.1.0/how-it-works.html).

The page loads the base PyData theme first, followed by the NVIDIA theme and `custom.css`. The NVIDIA stylesheet is the source of the final brand and neutral palette. `custom.css` does not override those palette tokens.

## Authoritative NVIDIA theme tokens

Source: [nvidia-sphinx-theme.css](http://omniverse-docs.s3-website-us-east-1.amazonaws.com/repo_docs/3.1.0/_static/styles/nvidia-sphinx-theme.css?v=933278ad).

Shared brand tokens:

- `--nv-color-green: #76b900`.
- `--nv-color-green-2: #004831`.
- `--pst-color-accent` resolves to `#76b900` in both modes.

Light mode (`html:not([data-theme]), html[data-theme=light]`):

- Background and on-background: `#fff`.
- Heading: `#000`.
- Body text: `#1a1a1a`.
- Muted text: `#666`.
- Surface: `#f7f7f7`.
- On-surface: `#333`.
- Shadow: `#ccc`.
- Primary, secondary and inline code: `#004831`.
- Secondary background and table hover background: `#76b900`.
- Root link and link-hover tokens: body text (`#1a1a1a`); article link underline color is `#76b900`.

Dark mode (`html[data-theme=dark]`):

- Background: `#111`.
- On-background: `#000`.
- Heading: `#fff`.
- Body text: `#eee`.
- Muted text: `#999`.
- Surface: `#1a1a1a`.
- On-surface: `#ddd`.
- Shadow: `#000`.
- Primary, secondary and inline code: `#76b900`.
- Secondary background and table hover background: `#004831`.
- Root link and link-hover tokens: body text (`#eee`); article link underline color is `#76b900`.

The NVIDIA theme also assigns `#76b900` to the selected sidebar and table-of-contents inset marker. This is a focused accent on neutral black/white/gray surfaces.

## Inherited base-theme borders

Source: [pydata-sphinx-theme.css](http://omniverse-docs.s3-website-us-east-1.amazonaws.com/repo_docs/3.1.0/_static/styles/pydata-sphinx-theme.css?digest=7f76b32a3354e82990f2).

These border tokens are not replaced by the NVIDIA theme:

- Light: border `#d1d5da`; muted border `rgba(23,23,26,.2)`; table inner border `#e5e7ea`.
- Dark: border `#48566b`; muted border `#29313d`; table inner border `#364150`.

## Implementation recommendation

Use exact NVIDIA green `#76b900`, deep green `#004831`, and the mode-specific neutral values above. Keep large surfaces neutral; apply NVIDIA green to selected navigation, small accents and interactive highlights. Use `#004831` for light-mode text accents, as the supplied reference does. Remove the previous olive/yellow palette. The team name is the user-specified **NVIS - OVA**.

## Fetch and browser verification

The supplied HTTP page and all eight linked CSS resources were downloaded successfully over HTTP. Relevant downloaded resource sizes were 9,469 bytes for the NVIDIA theme, 2,595 bytes for `custom.css`, and 396,738 bytes for the base PyData theme. The page links to those exact versioned stylesheet URLs above in that load order.

Chromium loaded the supplied URL and confirmed the page title/heading. For each `data-theme` value (`light` and `dark`), `getComputedStyle(document.documentElement).getPropertyValue(...)` confirmed every listed brand, neutral, primary and border value. Results are saved in `/tmp/nvis-color-reference/computed-palette.json`. These are root token values; more specific selectors can change rendered elements (for example, some external document links render cyan in the supplied theme).

Reference screenshots were captured and visually inspected at `/tmp/nvis-color-reference/reference-light.png` and `/tmp/nvis-color-reference/reference-dark.png`. They confirm white/gray content surfaces with black text in light mode and black/charcoal surfaces with white text in dark mode, with focused NVIDIA green marks and branding.

Raw downloaded stylesheets are stored under `/tmp/nvis-color-reference/` for local inspection. No third-party stylesheet is copied into the application.
