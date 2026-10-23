"""Display casing must not rewrite source prose or case-sensitive technical names."""

import pytest

from nvis_hub.presentation import display_heading_html, display_title


@pytest.mark.parametrize(
    ("authored", "displayed"),
    [
        ("use a Varlock GitLab group token", "Use a Varlock GitLab group token"),
        ("provision a person for passwordless access", "Provision a person for passwordless access"),
        ("deploy one Caddy-protected HTTP service", "Deploy one Caddy-protected HTTP service"),
        ("make a standalone host into a Slurm client", "Make a standalone host into a Slurm client"),
        ("install the NVIDIA driver", "Install the NVIDIA driver"),
        ("  configure the NVIS - OVA network  ", "  Configure the NVIS - OVA network  "),
        ("“verify GitLab API access”", "“Verify GitLab API access”"),
        ("évaluer le GPU", "Évaluer le GPU"),
    ],
)
def test_display_title_capitalizes_only_the_first_prose_letter(authored: str, displayed: str) -> None:
    assert display_title(authored) == displayed
    assert display_title(displayed) == displayed


@pytest.mark.parametrize(
    "authored",
    [
        "",
        "  ",
        "NVIS - OVA",
        "GitLab API reference",
        "cmsh",
        "ssh access",
        "git configuration",
        "dpkg -x options",
        "grep options",
        "npm setup",
        "apt package reference",
        "nvidia-smi options",
        "kubectl get nodes",
        "./scripts/dev.sh",
        "/etc/hosts",
        "--help",
        "docs/README.md",
        "config.yml reference",
        "my_tool options",
        "my-tool options",
        "$HOME configuration",
        "`cmsh` operations",
        "https://example.com/docs",
        "python3 setup",
        "3D GPU topology",
        "cuPyNumeric operations",
        "eBPF reference",
    ],
)
def test_display_title_preserves_technical_spelling_and_existing_case(authored: str) -> None:
    assert display_title(authored) == authored


@pytest.mark.parametrize("level", range(1, 7))
def test_display_heading_html_changes_only_initial_heading_prose(level: int) -> None:
    authored = f'<h{level} id="use-nvis">use NVIS &amp; GitLab</h{level}>'
    displayed = f'<h{level} id="use-nvis">Use NVIS &amp; GitLab</h{level}>'
    assert display_heading_html(authored) == displayed
    assert display_heading_html(displayed) == displayed


def test_display_heading_html_preserves_markup_attributes_links_and_body() -> None:
    authored = (
        "<p>use NVIS &amp; GitLab.</p>"
        '<h2 id="use-nvis" title="a > b">use NVIS &amp; '
        '<a href="#use-nvis" title="use this target">GitLab</a></h2>'
        "<pre><code>&lt;h2&gt;use NVIS&lt;/h2&gt;</code></pre>"
        "<pre><code><h3>use literal heading markup</h3></code></pre>"
        "<code><h4>use literal inline markup</h4></code>"
    )
    displayed = authored.replace('title="a > b">use NVIS', 'title="a > b">Use NVIS')
    assert display_heading_html(authored) == displayed


@pytest.mark.parametrize(
    "authored",
    [
        '<h1 id="cmsh">cmsh operations</h1>',
        "<h2><code>nvidia-smi</code> options</h2>",
        "<h2> <em>use NVIS</em> safely</h2>",
        '<h2><a href="/docs/use.md">use NVIS</a></h2>',
        "<h3>/etc/hosts reference</h3>",
        "<h2>&quot;use NVIS&quot; &amp; GitLab</h2>",
        "<p>use NVIS</p><h7>use a non-heading tag</h7>",
    ],
)
def test_display_heading_html_leaves_technical_and_nested_starts_unchanged(authored: str) -> None:
    assert display_heading_html(authored) == authored
