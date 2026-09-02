"""Rule H047: Check for aria-hidden on a focusable element.

Hiding an element from assistive technology while leaving it in the tab
order strands a keyboard user on a control their screen reader will not
announce. Only the element's own focusability is judged, which is the part
a template says for certain.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError

_ALWAYS_FOCUSABLE: Final = frozenset((
    "button",
    "iframe",
    "select",
    "summary",
    "textarea",
))
_FOCUSABLE_WITH_HREF: Final = frozenset(("a", "area"))
_FOCUSABLE_WITH_CONTROLS: Final = frozenset(("audio", "video"))


def _attributes(config: Config, html: str, token: TagToken) -> dict[str, str]:
    """The tag's attribute names, lowercased, with their unquoted values."""
    group = html[token.name_end : token.attributes_end]
    found: dict[str, str] = {}
    for match in config.attribute_pattern.finditer(group):
        name, value = match.group(1, 2)
        if not name:
            continue
        found[name.lower()] = (value or "").strip("\"'").strip()
    return found


def _is_focusable(name: str, attributes: dict[str, str]) -> bool:
    """Whether the element takes focus by itself.

    A tabindex decides the question outright when it is a plain number.
    One written by a template tag says nothing either way, so the element
    is judged on what it is instead.
    """
    tabindex = attributes.get("tabindex")
    if tabindex is not None:
        if tabindex.lstrip("+").isdigit():
            return True
        if tabindex.startswith("-") and tabindex[1:].isdigit():
            return False

    if "disabled" in attributes:
        return False
    if name in _ALWAYS_FOCUSABLE:
        return True
    if name in _FOCUSABLE_WITH_HREF:
        return "href" in attributes
    if name == "input":
        return attributes.get("type", "").lower() != "hidden"
    if name in _FOCUSABLE_WITH_CONTROLS:
        return "controls" in attributes
    editable = attributes.get("contenteditable")
    return editable is not None and editable.lower() != "false"


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for aria-hidden on a focusable element."""
    errors: list[LintError] = []

    for token in tokenize_markup(html):
        if token.closing or token.declaration:
            continue

        attributes = _attributes(config, html, token)
        if attributes.get("aria-hidden", "").lower() != "true":
            continue

        if not _is_focusable(token.name.lower(), attributes):
            continue

        if (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(token.start, line_ends),
            "match": html[token.start : token.end].strip()[:20],
            "message": rule["message"],
        })

    return tuple(errors)
