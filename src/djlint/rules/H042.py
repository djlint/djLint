"""Rule H042: Check that label for attributes match an id in the file."""

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
    from typing import Final

    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError


# id/for attributes with their values; a valueless attribute equals "".
# Other name=value pairs and stray quoted values are consumed wholesale so
# attribute-lookalikes inside values don't match.
_ATTR_PATTERN: Final = re.compile(
    r"(?<![-:\w])(?P<name>id|for)(?![-:\w])"
    r"(?:\s*=\s*(?:\"(?P<dq>[^\"]*)\"|'(?P<sq>[^']*)'|(?P<uq>[^\s\"'<>`=]+)))?"
    r"|[-:\w]+\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'<>`=]+)"
    r"|\"[^\"]*\"|'[^']*'",
    re.I,
    cache_pattern=False,
)
_TEMPLATE_SYNTAX: Final = ("{{", "{%", "{#")


def _attributes(html: str, token: TagToken) -> tuple[tuple[str, str], ...]:
    """Extract id/for attribute names and values from a tag."""
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
    chars: list[str] | None = None
    for pattern in (
        config.ignored_blocks_pattern,
        config.ignored_inline_blocks_ix_pattern,
    ):
        for match in pattern.finditer(html):
            start, end = match.span()
            if chars is None:
                chars = list(html)
            chars[start:end] = " " * (end - start)
    return "".join(chars) if chars else html


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

    for token in tokenize_tags(masked):
        if token.closing or token.declaration:
            continue

        for name, value in _attributes(masked, token):
            if name == "id":
                if any(marker in value for marker in _TEMPLATE_SYNTAX):
                    # a template-generated id can match anything; the
                    # file cannot be checked reliably
                    return ()
                if value:
                    # an empty id cannot be referenced by any for value
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
