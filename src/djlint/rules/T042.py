"""Rule T042: Check for content outside a block in a template that extends another.

Once a template extends another, the parent decides what is output and
the child only fills the parent's blocks. Django, Jinja and Nunjucks
silently discard text and html written after `{% extends %}` and outside
every `{% block %}`, so a paragraph that looks fine in the source never
reaches the page.

A template tag there still runs, so `{% load %}`, `{% set %}` and an
`{% if %}` wrapped around a block are left alone. A tag that holds a
captured body, as `{% macro %}`, a block form `{% set %}`,
`{% partialdef %}` or `{% addtoblock %}`, keeps its body rather than
writing it out where it stands, so that body is left alone too, as is
anything inside `{% comment %}`, `{% raw %}`, `{% verbatim %}`, `{# #}`
or an html comment. A `{% blocktrans %}` is not a `{% block %}`: its text
is output like any other and is reported.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import inside_ignored_rule
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_HIDDEN_REGION: Final = (
    r"{%[-+]?\s*(?P<hidden>comment|raw|verbatim)\b(?:(?!%}).)*%}"
    r".*?{%[-+]?\s*end(?P=hidden)\b(?:(?!%}).)*%}"
)
_TAGS: Final = rf"{_HIDDEN_REGION}|{{#.*?#}}|{{%.*?%}}|{{{{.*?}}}}"
_TOKEN_PATTERN: Final = re.compile(rf"{_TAGS}|<!--", re.S, cache_pattern=False)
_COMMENTED_TOKEN_PATTERN: Final = re.compile(
    rf"{_TAGS}|-->", re.S, cache_pattern=False
)
_EXTENDS_PATTERN: Final = re.compile(
    r"{%[-+]?\s*extends\b", cache_pattern=False
)
_CAPTURING_PATTERN: Final = re.compile(
    r"{%[-+]?\s*(?P<end>end)?"
    r"(?P<name>block(?!trans)|macro|set|partialdef|addtoblock)\b"
    r"(?P<rest>(?:(?!%}).)*)",
    re.S,
    cache_pattern=False,
)
_CONTENT_PATTERN: Final = re.compile(r"\S(?:.*\S)?", re.S, cache_pattern=False)


def _tag_end(html: str, start: int, /, *, braces: bool) -> int | None:
    """The end of the tag at `start`, or None if it never closes.

    The lazy scan that finds a tag stops at the first closing delimiter,
    which is the wrong one when the tag writes that delimiter inside a
    string, as `{% include "x" with s="%}" %}` does, or nests braces, as
    `{{ {"a": {"b": 1}} }}` does. Reading the tag again, skipping quoted
    text and counting braces, finds the delimiter that really closes it.

    A tag that opens a quote it never closes, which no engine would parse
    either, has no end here rather than an end past the next tag along.
    """
    closing = "}}" if braces else "%}"
    quote = ""
    depth = 0
    index = start + 2
    while index < len(html):
        char = html[index]
        if quote:
            if char == "\\":
                index += 1
            elif char == quote:
                quote = ""
        elif char in {'"', "'"}:
            quote = char
        elif braces and char == "{":
            depth += 1
        elif braces and char == "}" and depth:
            depth -= 1
        elif not depth and html.startswith(closing, index):
            return index + 2
        index += 1
    return None


def _assigns(rest: str) -> bool:
    """Whether a `{% set %}` tag assigns a value instead of opening a body.

    `{% set x = 1 %}` assigns and holds nothing, while `{% set nav %}`
    opens a body that `{% endset %}` closes. Only a bare top level `=`
    assigns: a filter writes its keyword arguments inside brackets, as in
    `{% set body | indent(width=2) %}`, and a comparison writes `==`.
    """
    quote = ""
    depth = 0
    previous = ""
    for index, char in enumerate(rest):
        if quote:
            if char == quote and previous != "\\":
                quote = ""
        elif char in {'"', "'"}:
            quote = char
        elif char in {"(", "[", "{"}:
            depth += 1
        elif char in {")", "]", "}"}:
            depth -= 1
        elif (
            char == "="
            and depth <= 0
            and previous not in {"=", "!", "<", ">"}
            and not rest.startswith("=", index + 1)
        ):
            return True
        previous = char
    return False


def _captured_body(tag: str) -> tuple[str, bool] | None:
    """The name of the captured body a tag opens or closes, or None.

    The engine holds on to the body of a `{% block %}`, `{% macro %}`,
    block form `{% set %}`, `{% partialdef %}` or `{% addtoblock %}` and
    writes it out elsewhere, so markup inside one is not lost even when
    the tag stands outside every block.
    """
    match = _CAPTURING_PATTERN.match(tag)
    if match is None:
        return None
    name = match.group("name")
    closing = match.group("end") is not None
    if name == "set" and not closing and _assigns(match.group("rest")):
        return None
    return name, closing


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for content outside a block in a template that extends another.

    The template is read as a stream of tags with text between them. A
    tag whose body the engine captures is counted on a stack, and once
    the `{% extends %}` tag has gone by, each run of text found with that
    stack empty is reported once, at its start. A tag between two runs
    splits them, so each is reported on its own.

    The engine reads tags before html, so an `{% extends %}` inside an
    html comment or a `<pre>` still runs; only `{% comment %}`,
    `{% raw %}`, `{% verbatim %}` and `{# #}` really hide one. Text
    inside an html comment reaches no reader either way and is not
    reported, but the tags written there are still read. A `<!--` with
    no `-->` left to close it opens no comment, so a stray one cannot
    quietly switch the rest of the file off.
    """
    errors: list[LintError] = []
    stack: list[str] = []
    commented = False
    extended = False
    position = 0
    last_comment_close = html.rfind("-->")

    while True:
        pattern = _COMMENTED_TOKEN_PATTERN if commented else _TOKEN_PATTERN
        token = pattern.search(html, position)
        text_end = token.start() if token else len(html)
        if extended and not stack and not commented:
            content = _CONTENT_PATTERN.search(html, position, text_end)
            if content and not inside_ignored_rule(
                config, html, content, rule["name"]
            ):
                errors.append({
                    "code": rule["name"],
                    "line": get_line(content.start(), line_ends),
                    "match": content.group()[:20],
                    "message": rule["message"],
                })
        if token is None:
            break

        tag = token.group()
        position = token.end()
        if tag == "<!--":
            commented = token.start() < last_comment_close
            continue
        if tag == "-->":
            commented = False
            continue

        if token.group("hidden") is None and tag[:2] in {"{%", "{{"}:
            end = _tag_end(html, token.start(), braces=tag[1] == "{")
            if end is not None and end > position:
                longer = html[token.start() : end]
                # A tag reaching over another one has read a quote wrong.
                if "{%" not in longer[2:] and "{{" not in longer[2:]:
                    position = end
                    tag = longer

        if not extended:
            extended = _EXTENDS_PATTERN.match(tag) is not None
            if extended:
                continue

        captured = _captured_body(tag)
        if captured is None:
            continue
        name, closing = captured
        if not closing:
            stack.append(name)
        elif name in stack:
            while stack.pop() != name:
                pass

    return tuple(errors)
