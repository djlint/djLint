"""Rule H042: Check that label for attributes match an id in the file.

The rule can only report a missing id when the file is the whole story.
Anything that can emit an id this file never shows makes it unsound and
silences it: `{{ }}` outputs (form widgets), `{% include %}`/`{% extends %}`
(elements living in other files), unknown custom tags (crispy,
render_field, ...) and ids built by a template tag.
"""

from __future__ import annotations

from html import unescape
from typing import TYPE_CHECKING

import regex as re

from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Final

    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError


_NAME_CHAR: Final = r"[-.:\w]"
_ATTR_PATTERN: Final = re.compile(
    rf"(?<!{_NAME_CHAR})(?P<name>id|for)(?!{_NAME_CHAR})"
    r"(?:\s*=\s*(?:\"(?P<dq>[^\"]*)\"|'(?P<sq>[^']*)'|(?P<uq>[^\s\"'<>`=]+)))?"
    rf"|{_NAME_CHAR}+\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'<>`=]+)"
    r"|\"[^\"]*\"|'[^']*'",
    re.I,
    cache_pattern=False,
)
_TEMPLATE_SYNTAX: Final = ("{{", "{%", "{#")

_TAGS_THAT_CANNOT_RENDER_AN_ID: Final = frozenset({
    "if",
    "elif",
    "else",
    "endif",
    "for",
    "empty",
    "endfor",
    "with",
    "endwith",
    "block",
    "endblock",
    "comment",
    "endcomment",
    "verbatim",
    "endverbatim",
    "autoescape",
    "endautoescape",
    "spaceless",
    "endspaceless",
    "filter",
    "endfilter",
    "load",
    "csrf_token",
    "now",
    "url",
    "static",
    "trans",
    "translate",
    "blocktrans",
    "blocktranslate",
    "endblocktrans",
    "endblocktranslate",
    "plural",
    "set",
    "endset",
    "macro",
    "endmacro",
})
_TAG_NAME: Final = re.compile(r"\{%[-+]?\s*(\w+)", cache_pattern=False)


_LABELABLE_ELEMENTS: Final = frozenset((
    "button",
    "input",
    "meter",
    "output",
    "progress",
    "select",
    "textarea",
))


def _can_check(masked: str) -> bool:
    """Whether every template construct is unable to emit an id."""
    if "{{" in masked:
        return False
    return all(
        m.group(1) in _TAGS_THAT_CANNOT_RENDER_AN_ID
        for m in _TAG_NAME.finditer(masked)
    )


def _holds_the_labelled_control(tokens: Iterable[TagToken]) -> bool:
    """Whether a control a label could be for is written in this file.

    A partial holding only the label leaves its control to the template
    that includes it, so there is nothing here to match against. The raw
    source is read, so a control that is commented out still says the
    file is about a form and its label is checked.
    """
    return any(
        token.name.lower() in _LABELABLE_ELEMENTS
        for token in tokens
        if not token.closing
    )


def _attributes(html: str, token: TagToken) -> tuple[tuple[str, str], ...]:
    """Extract id/for attribute names and values from a tag.

    A valueless attribute yields "". Other name=value pairs and stray
    quoted values are consumed wholesale, so attribute-lookalikes inside a
    value do not match; "." is a name character just as "-" is, so
    data-x.id is one name and holds no id attribute.
    """
    return tuple(
        (match.group("name").lower(), unescape(value))
        for match in _ATTR_PATTERN.finditer(
            html[token.name_end : token.attributes_end]
        )
        if match.group("name")
        for value in (
            match.group("dq") or match.group("sq") or match.group("uq") or "",
        )
    )


def _masked(config: Config, html: str) -> str:
    """Blank ignored regions (script/style bodies, comments, ...).

    Their content neither defines ids nor labels, and stray "<" or quote
    characters inside them would poison the tag tokenizer for the rest of
    the file.
    """
    spans = sorted(
        match.span()
        for pattern in (
            config.ignored_blocks_pattern,
            config.ignored_inline_blocks_ix_pattern,
        )
        for match in pattern.finditer(html)
    )
    if not spans:
        return html

    parts: list[str] = []
    cursor = 0
    for start, end in spans:
        if end <= cursor:
            continue
        blank_from = max(start, cursor)
        parts.extend((html[cursor:blank_from], " " * (end - blank_from)))
        cursor = end
    parts.append(html[cursor:])
    return "".join(parts)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that label for attributes match an id in the file."""
    ids: set[str] = set()
    labels: list[tuple[TagToken, str]] = []
    masked = _masked(config, html)
    if not _can_check(masked):
        return ()

    if not _holds_the_labelled_control(tokenize_tags(html)):
        return ()

    for token in tokenize_tags(masked):
        if token.closing or token.declaration:
            continue

        for name, value in _attributes(masked, token):
            if name == "id":
                if any(marker in value for marker in _TEMPLATE_SYNTAX):
                    return ()
                if value:
                    ids.add(value)
            elif token.name.lower() == "label":
                labels.append((token, value))

    return tuple(
        {
            "code": rule["name"],
            "line": get_line(token.start, line_ends),
            "match": html[token.start : token.end].strip()[:20],
            "message": rule["message"],
        }
        for token, value in labels
        if (
            value not in ids
            and not any(marker in value for marker in _TEMPLATE_SYNTAX)
            and not overlaps_ignored_block(config, html, token)
            and not inside_ignored_rule(config, html, token, rule["name"])
            and not inside_ignored_linter_block(config, html, token)
        )
    )
