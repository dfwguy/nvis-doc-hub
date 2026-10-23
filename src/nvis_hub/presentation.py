"""Conservative display formatting that leaves authored content unchanged."""

import re

# These unambiguous command names can also begin a plain-text document title.
# Do not add ordinary prose verbs such as make, install, test, or find here.
TITLE_COMMANDS = frozenset(
    {
        "apt",
        "awk",
        "bash",
        "cmake",
        "cmsh",
        "curl",
        "docker",
        "dpkg",
        "git",
        "grep",
        "jq",
        "journalctl",
        "kubectl",
        "nvinfo",
        "npm",
        "npx",
        "pip",
        "podman",
        "pnpm",
        "python",
        "rsync",
        "sbatch",
        "scontrol",
        "scp",
        "sed",
        "sh",
        "sinfo",
        "squeue",
        "srun",
        "ssh",
        "sudo",
        "systemctl",
        "zsh",
    }
)
_INITIAL_WORD = re.compile(r"^(\s*[\"'“‘(]*)(\S+)")
_TECHNICAL_CHARACTERS = frozenset("/\\._-$@=<>`:")
_HEADING_HTML = re.compile(
    r"""
    (?P<code><(?P<code_tag>pre|code)(?=[\s>])(?:[^>"']|"[^"]*"|'[^']*')*>
        .*?</(?P=code_tag)\s*>)
    |(?P<opening><h[1-6](?=[\s>])(?:[^>"']|"[^"]*"|'[^']*')*>)
        (?P<text>[^<]*)
    """,
    re.IGNORECASE | re.DOTALL | re.VERBOSE,
)


def display_title(value: str) -> str:
    """Uppercase one initial prose letter, retaining all other authored characters.

    Preserve command names, paths, flags, filenames, identifier-like first tokens,
    and mixed-case names. This is a presentation helper, not general title case or
    a prose/command classifier; unknown plain alphabetic words are treated as prose.
    """
    match = _INITIAL_WORD.match(value)
    if match is None:
        return value
    token = match[2].rstrip(",;:!?)]}'\"”’")
    if (
        not token
        or not token[0].islower()
        or not token[0].isalpha()
        or token in TITLE_COMMANDS
        or any(character.isdigit() or character in _TECHNICAL_CHARACTERS for character in token)
        or any(character.isupper() for character in token[1:])
    ):
        return value
    uppercase = token[0].upper()
    if len(uppercase) != 1:
        return value
    position = len(match[1])
    return value[:position] + uppercase + value[position + 1 :]


def display_heading_html(html: str) -> str:
    """Format only the initial plain-text node of rendered h1–h6 headings.

    Preserve markup and encoded entities verbatim. Headings starting with nested
    markup stay as authored, and code/preformatted regions are excluded entirely.
    """

    def replace(match: re.Match[str]) -> str:
        if match["code"] is not None:
            return match[0]
        return match["opening"] + display_title(match["text"])

    return _HEADING_HTML.sub(replace, html)
