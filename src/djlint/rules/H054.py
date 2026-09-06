"""Rule H054: Check for an interactive element nested inside another.

Html forbids interactive content inside `<a>` and `<button>`. A button
inside a link, or a link inside a button, is invalid markup that browsers
repair each in their own way, and a screen reader or keyboard user is
handed one control that behaves like two. axe reports the same thing as
"nested-interactive".

Only what a template says for certain is judged. An `<a>` without an
`href` is not interactive, so it neither holds anything that is reported
nor is reported itself, and an `<input>` whose type a template tag writes
could be hidden, so it is left alone. An attribute is read where a tag
writes one and nowhere else: the `href` of `{% if not href %}` names a
variable and the one in `{# href="{{ url }}" #}` is commented out, while
the one an `{% if %}` writes between its own tags is an attribute like
any other.
"""

from __future__ import annotations

from bisect import bisect_right
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
    from collections.abc import Iterator, Sequence
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError

_CONTAINERS: Final = frozenset(("a", "button"))
_INTERACTIVE: Final = frozenset(("a", "button", "input", "select", "textarea"))
# A template's content is not rendered, so nothing in one is nested
# inside the elements around it.
_INERT: Final = frozenset(("template",))

_AFTER_EVERY_SPAN: Final = float("inf")

_HREF_PATTERN = re.compile(
    r"(?<![-.:\w])href(?![-.:\w])", re.I, cache_pattern=False
)
_TYPE_PATTERN = re.compile(
    r"(?<![-.:\w])type(?![-.:\w])", re.I, cache_pattern=False
)
_TEMPLATE_PATTERN = re.compile(r"{[{%#]", cache_pattern=False)
_TEMPLATE_STATEMENT_PATTERN = re.compile(
    r"{%(?:(?!%}).)*%}", re.S, cache_pattern=False
)
# djLint's shared skip reads "{% comment %}" but not the "{%- comment -%}"
# a liquid theme is written in, so the rule finds those bodies itself.
_COMMENT_OPENING_PATTERN = re.compile(
    r"{%[-+]?[ \t]*comment\b", re.I, cache_pattern=False
)
_COMMENT_CLOSING_PATTERN = re.compile(
    r"{%[-+]?[ \t]*endcomment[ \t]*[-+]?%}", re.I, cache_pattern=False
)


def _attributes(config: Config, area: str) -> Iterator[tuple[str, str | None]]:
    """Yield the attribute names the tag writes, with their raw values.

    Only a name in attribute position is one: a word inside a comment, in
    a template tag's own code or in another attribute's value is not. An
    `{% if %}` block is opened up, because what it writes between its
    tags is an attribute like any other.
    """
    for match in config.attribute_pattern.finditer(area):
        name, value, template = match.group(1, 2, 3)
        if name:
            yield name, value
        elif template and template.startswith("{%"):
            written = _TEMPLATE_STATEMENT_PATTERN.sub("", template)
            for inner in config.attribute_pattern.finditer(written):
                inner_name, inner_value = inner.group(1, 2)
                if inner_name:
                    yield inner_name, inner_value


def _unquote(value: str) -> str:
    """The attribute value without the quotes around it."""
    value = value.strip()
    if len(value) > 1 and value[0] in {'"', "'"} and value[-1] == value[0]:
        value = value[1:-1]
    return value.strip()


def _is_interactive(config: Config, name: str, area: str) -> bool:
    """Whether the element, given its attribute area, is interactive content.

    A valueless `href` still makes a link, and one written by a template
    tag counts as present. An input's type is read only when it is a plain
    word: `hidden` takes the input out of the page, and a type a template
    tag writes could be `hidden`, so neither is counted.

    The name is looked for in the attribute area before the attributes
    are read, because reading them is the expensive half and a tag
    without the word anywhere cannot be writing that attribute.
    """
    if name not in _INTERACTIVE:
        return False
    if name == "a":
        return _HREF_PATTERN.search(area) is not None and any(
            _HREF_PATTERN.search(attribute)
            for attribute, _ in _attributes(config, area)
        )
    if name != "input":
        return True
    if _TYPE_PATTERN.search(area) is None:
        return True

    for attribute, value in _attributes(config, area):
        if not _TYPE_PATTERN.search(attribute):
            continue
        if value is None:
            return True
        written = _unquote(value)
        if _TEMPLATE_PATTERN.search(written):
            return False
        return written.lower() != "hidden"
    return True


def _comment_block_spans(html: str) -> tuple[tuple[int, int], ...]:
    """The bodies of the comment blocks written with whitespace control.

    The opening tag ends at the first "%}" after its name and each search
    starts where the last block ended, so a file of half written comment
    tags is read in one pass rather than one pass per tag.
    """
    spans: list[tuple[int, int]] = []
    position = 0
    while (
        opening := _COMMENT_OPENING_PATTERN.search(html, position)
    ) is not None:
        body_start = html.find("%}", opening.end())
        if body_start < 0:
            break
        closing = _COMMENT_CLOSING_PATTERN.search(html, body_start + 2)
        if closing is None:
            break
        spans.append((body_start + 2, closing.start()))
        position = closing.end()
    return tuple(spans)


def _within(spans: Sequence[tuple[int, int]], position: int) -> bool:
    """Whether the position falls in one of the sorted, disjoint spans."""
    index = bisect_right(spans, (position, _AFTER_EVERY_SPAN)) - 1
    return index >= 0 and spans[index][0] <= position < spans[index][1]


def _close(
    open_elements: list[tuple[str, int, int]],
    open_by_name: dict[str, list[int]],
    name: str,
) -> None:
    """Pop back to the element a closing tag closes, if one is open.

    The name is looked up rather than the stack walked, so a closing tag
    that matches nothing costs the same against a deep stack as against
    an empty one and a file full of them stays linear.
    """
    indexes = open_by_name.get(name)
    if not indexes:
        return
    closed = indexes[-1]
    for popped in reversed(open_elements[closed:]):
        open_by_name[popped[0]].pop()
    del open_elements[closed:]


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
    would in a browser, rather than swallowing the rest of the file; one
    left open at the top level, with nothing around it to end it, does
    run to the end. A container opened in one template branch and closed
    in another is paired as though both were plain markup.
    """
    errors: list[LintError] = []
    # Each open element carries the number of containers it sits in and
    # the number of `<pre>` elements, so both are read in one step
    # however deep the markup is.
    open_elements: list[tuple[str, int, int]] = []
    open_by_name: dict[str, list[int]] = {}
    comment_spans = _comment_block_spans(html)

    for token in tokenize_markup(html):
        name = token.name.lower()
        _, containers, pres = open_elements[-1] if open_elements else ("", 0, 0)
        skipped = (
            token.declaration
            or overlaps_ignored_block(config, html, token)
            or _within(comment_spans, token.start)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        )
        # A `<pre>` body is parsed as html, so a closing tag written in
        # one closes the element it names for the browser too and has to
        # be popped, even though nothing inside a pre body is reported.
        if skipped and not (token.closing and pres):
            continue

        if token.closing:
            _close(open_elements, open_by_name, name)
            continue

        interactive = _is_interactive(
            config, name, html[token.name_end : token.attributes_end]
        )
        if interactive and containers:
            errors.append({
                "code": rule["name"],
                "line": get_line(token.start, line_ends),
                "match": html[token.start : token.end].strip()[:20],
                "message": rule["message"],
            })

        if token.self_closing or name in HTML_VOID_ELEMENTS:
            continue
        if name in _INERT:
            containers = 0
        elif interactive and name in _CONTAINERS:
            containers += 1
        open_by_name.setdefault(name, []).append(len(open_elements))
        open_elements.append((
            name,
            containers,
            pres + 1 if name == "pre" else pres,
        ))

    return tuple(errors)
