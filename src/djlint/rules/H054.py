"""Rule H054: Check for an interactive element nested inside another.

Html forbids interactive content inside `<a>` and `<button>`. A button
inside a link, or a link inside a button, is invalid markup that browsers
repair each in their own way, and a screen reader or keyboard user is
handed one control that behaves like two. axe reports the same thing as
"nested-interactive".

Only what a template says for certain is judged. An `<a>` without an
`href` is not interactive, so it neither holds anything that is reported
nor is reported itself, and an `<input>` whose type a template tag writes
could be hidden, so it is left alone.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_VOID_ELEMENTS
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

    from djlint.settings import Config
    from djlint.types import LintError

_CONTAINERS: Final = frozenset(("a", "button"))
_INTERACTIVE: Final = frozenset(("a", "button", "input", "select", "textarea"))

_PAST_QUOTED_VALUES = r"""(?:"[^"]*"|'[^']*'|[^'"])*?"""
_HREF_PATTERN = re.compile(
    rf"{_PAST_QUOTED_VALUES}(?<![-.:\w])href(?![-.:\w])",
    re.I,
    cache_pattern=False,
)
_TYPE_PATTERN = re.compile(
    rf"""{_PAST_QUOTED_VALUES}(?<![-.:\w])type\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""",
    re.I,
    cache_pattern=False,
)
_TEMPLATE_PATTERN = re.compile(r"{[{%#]", cache_pattern=False)


def _is_interactive(name: str, html: str, start: int, end: int) -> bool:
    """Whether the element, given its attribute area, is interactive content.

    A valueless `href` still makes a link, and one written by a template
    tag counts as present. An input's type is read only when it is a plain
    word: `hidden` takes the input out of the page, and a type a template
    tag writes could be `hidden`, so neither is counted.
    """
    if name not in _INTERACTIVE:
        return False
    if name == "a":
        return _HREF_PATTERN.match(html, start, end) is not None
    if name != "input":
        return True

    match = _TYPE_PATTERN.match(html, start, end)
    if match is None:
        return True
    value = next(group for group in match.groups() if group is not None)
    if _TEMPLATE_PATTERN.search(value):
        return False
    return value.strip().lower() != "hidden"


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for an interactive element nested inside another.

    Every open element is kept on the stack, not only the links and
    buttons, and a closing tag pops back to the element it closes. A link
    or button left open, by a `</buton>` typo or markup written inside a
    template's own code, ends when the element around it ends, as it
    would in a browser, rather than swallowing the rest of the file. A
    container opened in one template branch and closed in another is
    paired as though both were plain markup.
    """
    errors: list[LintError] = []
    open_elements: list[tuple[str, bool]] = []

    for token in tokenize_markup(html):
        name = token.name.lower()
        if (
            token.declaration
            or overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        ):
            continue

        if token.closing:
            for index in range(len(open_elements) - 1, -1, -1):
                if open_elements[index][0] == name:
                    del open_elements[index:]
                    break
            continue

        interactive = _is_interactive(
            name, html, token.name_end, token.attributes_end
        )
        if interactive and any(
            holds_controls for _, holds_controls in open_elements
        ):
            errors.append({
                "code": rule["name"],
                "line": get_line(token.start, line_ends),
                "match": html[token.start : token.end].strip()[:20],
                "message": rule["message"],
            })

        if not token.self_closing and name not in HTML_VOID_ELEMENTS:
            open_elements.append((name, interactive and name in _CONTAINERS))

    return tuple(errors)
