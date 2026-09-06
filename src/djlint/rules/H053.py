"""Rule H053: Check for an id used more than once in the file.

An id names one element. A second element carrying the same id breaks
`getElementById`, `<label for>`, fragment links and `aria-labelledby`:
the browser takes the first and silently ignores the rest.

Two ids in exclusive branches of one `{% if %}...{% else %}...{% endif %}`
are never both rendered, so they are not a duplicate. A `{% for %}` loop
or a `{% block %}` is a block but not a branch: an id inside one and the
same id outside it both render, and the later one is reported. A mako
line statement, as `% else:`, branches just as `{% else %}` does and is
read the same way.

The contents of a `<template>` are a document fragment of their own, so
an id inside one is compared only with the ids of that same fragment.

A value holding template syntax is unknowable and is left alone, and so
is an empty value.
"""

from __future__ import annotations

from bisect import bisect_right
from typing import TYPE_CHECKING, NamedTuple

import regex as re

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    mutually_exclusive,
    overlaps_ignored_block,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Final

    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError


_NAME_CHAR: Final = r"[-.:\w]"
_TEMPLATE_TAG: Final = r"{{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}|{#(?:(?!#}).)*#}"
_ATTRIBUTE_PATTERN: Final = re.compile(
    rf"(?P<attribute>(?<!{_NAME_CHAR})id\s*=\s*"
    r"(?:\"(?P<dq>[^\"]*)\"|'(?P<sq>[^']*)'|(?P<uq>[^\s\"'<>`=]+)))"
    rf"|{_TEMPLATE_TAG}"
    rf"|{_NAME_CHAR}+\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'<>`=]+)"
    r"|\"[^\"]*\"|'[^']*'",
    re.I | re.S,
    cache_pattern=False,
)
_TAG_START_PATTERN: Final = re.compile(
    r"\{\{|\{%|\{#"
    r"|^[ \t]*%[ \t]*(?P<statement>if|elif|else|endif|for|endfor)\b[^\n]*",
    re.M,
    cache_pattern=False,
)
_CLOSING_DELIMITERS: Final = {"{{": "}}", "{%": "%}", "{#": "#}"}
_OPEN_NAME_PATTERN: Final = re.compile(
    r"(?:\{%[-+]?|\{\{[#^][*>]?)\s*([\w.-]+)", cache_pattern=False
)
_END_NAME_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*end([\w.-]*)|\{\{/\s*([\w.-]+)", cache_pattern=False
)
# whitespace written between a delimiter and the tag name, which every
# template language allows and the shared patterns spell as a space
_LEADING_SPACE_PATTERN: Final = re.compile(
    r"^(\{[{%#][-+~]?)\s+", cache_pattern=False
)
_ELSE_BRANCH_PATTERN: Final = re.compile(
    r"\{\{[-+~]?\s*(?:else\b|\^\s*[-+~]?\}\})", cache_pattern=False
)
_SECTION_OPEN_PATTERN: Final = re.compile(
    r"\{\{[-+~]?\s*[#^][*>]?\s*([\w.\-/]+)", cache_pattern=False
)
_SECTION_CLOSE_PATTERN: Final = re.compile(
    r"\{\{[-+~]?\s*/(?!\*)\s*([\w.\-/]*)", cache_pattern=False
)
# go writes an argument after the keyword, so the keyword is followed by
# whitespace; the jinja `{{ range(3) }}` and `{{ block.super }}` that a
# profile of "all" also has to read open nothing
_GOLANG_OPEN_PATTERN: Final = re.compile(
    r"\{\{[-+~]?\s*(if|range|with|block|define)(?=[\s}])", cache_pattern=False
)
_GOLANG_CLOSE_PATTERN: Final = re.compile(
    r"\{\{[-+~]?\s*end(?=[\s}])", cache_pattern=False
)
_LIQUID_BRANCH_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*(?:elsif|when)\b", cache_pattern=False
)
_LIQUID_OPEN_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*(case)\b", cache_pattern=False
)
_DJANGO_OPEN_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*(ifequal|ifnotequal)\b", cache_pattern=False
)
_BRANCH_STATEMENTS: Final = frozenset(("elif", "else"))
_GOLANG_PROFILES: Final = frozenset(("all", "golang"))
_LIQUID_PROFILES: Final = frozenset(("all", "liquid"))
_TEMPLATE_SYNTAX: Final = ("{{", "{%", "{#", "${")
_TEMPLATE_ELEMENT: Final = "template"


class _TemplateTag(NamedTuple):
    """One template tag of the document."""

    start: int
    end: int
    text: str
    statement: str

    def span(self) -> tuple[int, int]:
        """Return the source span."""
        return self.start, self.end


def _template_tags(html: str) -> Iterator[_TemplateTag]:
    """Yield the template tags of a document in one pass.

    A tag is closed with `str.find` rather than with a pattern scanning
    forward for the closing delimiter: such a pattern re-reads the rest of
    the file from every brace of a run of them, which is quadratic. A
    delimiter that has no further occurrence never has one again, so the
    openers left over are skipped without searching for it again.
    """
    exhausted: set[str] = set()
    position = 0

    while (match := _TAG_START_PATTERN.search(html, position)) is not None:
        start = match.start()
        if statement := match.group("statement"):
            yield _TemplateTag(start, match.end(), match.group(), statement)
            position = match.end()
            continue
        closing = _CLOSING_DELIMITERS[match.group()]
        if closing not in exhausted:
            end = html.find(closing, start + 2)
            if end < 0:
                exhausted.add(closing)
            else:
                end += len(closing)
                yield _TemplateTag(start, end, html[start:end], "")
                position = end
                continue
        position = start + 1


def _canonical(tag: str) -> str:
    """The tag with the whitespace after its opening delimiter as a space.

    The shared indent patterns write that space literally, while every
    template language takes any whitespace there, so a tag broken over
    lines, or written with a tab, is read as the usual one is.
    """
    match = _LEADING_SPACE_PATTERN.match(tag)
    if match is None or tag[match.end(1) : match.end()] == " ":
        return tag
    return f"{tag[: match.end(1)]} {tag[match.end() :]}"


def _configured_role(config: Config, tag: str) -> tuple[str, str] | None:
    """The part a tag plays as the shared indent patterns read it."""
    canonical = _canonical(tag)
    if config.tag_unindent_line_ix_pattern.match(canonical):
        return "branch", ""
    if config.template_unindent_ix_pattern.match(canonical):
        end_name = _END_NAME_PATTERN.match(canonical)
        if end_name is None:
            return "close", ""
        return "close", end_name.group(1) or end_name.group(2) or ""
    if config.template_indent_ix_pattern.match(canonical):
        open_name = _OPEN_NAME_PATTERN.match(canonical)
        return "open", open_name.group(1) if open_name else ""
    return None


def _expression_role(config: Config, tag: str) -> tuple[str, str] | None:
    """The part a `{{ }}` tag plays in branching.

    Handlebars and mustache branch with `{{else}}`, with the chained
    `{{else if x}}` that is their elif, and with the inverse `{{^}}`, and
    any `{{#name}}` opens a section that `{{/name}}` closes: a custom
    block helper is as much a block as a built-in one. Go's `if`, `range`,
    `with` and `end` are read under the golang profile and under `all`,
    which is what a project naming no profile is given.
    """
    if _ELSE_BRANCH_PATTERN.match(tag):
        return "branch", ""
    if close := _SECTION_CLOSE_PATTERN.match(tag):
        return "close", close.group(1)
    if section := _SECTION_OPEN_PATTERN.match(tag):
        return "open", section.group(1)
    if config.profile in _GOLANG_PROFILES:
        if _GOLANG_CLOSE_PATTERN.match(tag):
            return "close", ""
        if golang := _GOLANG_OPEN_PATTERN.match(tag):
            return "open", golang.group(1)
    return _configured_role(config, tag)


def _statement_role(config: Config, tag: str) -> tuple[str, str] | None:
    """The part a `{% %}` tag plays in branching.

    Liquid's `{% case %}`, `{% when %}` and `{% elsif %}` are read under
    `all` as well as under the liquid profile, and django's legacy
    `{% ifequal %}` and `{% ifnotequal %}` branch wherever they are found.
    """
    if role := _configured_role(config, tag):
        return role
    if config.profile in _LIQUID_PROFILES:
        if _LIQUID_BRANCH_PATTERN.match(tag):
            return "branch", ""
        if liquid := _LIQUID_OPEN_PATTERN.match(tag):
            return "open", liquid.group(1)
    if django := _DJANGO_OPEN_PATTERN.match(tag):
        return "open", django.group(1)
    return None


def _role(config: Config, tag: _TemplateTag) -> tuple[str, str] | None:
    """The part a tag plays in branching, with the block name it carries.

    A tag that neither opens, closes nor branches a block, as an
    `{% include %}` or a `{{ variable }}`, plays no part and gives None.
    """
    if tag.statement:
        if tag.statement in _BRANCH_STATEMENTS:
            return "branch", ""
        if tag.statement.startswith("end"):
            return "close", tag.statement[3:]
        return "open", tag.statement
    if tag.text.startswith("{#"):
        return None
    if tag.text.startswith("{{"):
        return _expression_role(config, tag.text)
    return _statement_role(config, tag.text)


def _closed_depth(stack: list[tuple[str, int, int]], name: str) -> int:
    """How many open blocks an end tag closes, or 0 for an orphan.

    An end tag naming a block that was never opened, as the closer of a
    custom block djLint does not model, closes nothing, so it cannot pop
    the `{% if %}` around it. An unnamed closer, as go's `{{ end }}`,
    closes the innermost block.
    """
    if not name:
        return 1
    for depth, (open_name, _, _) in enumerate(reversed(stack), start=1):
        if open_name == name:
            return depth
    return 0


def _branch_paths(
    config: Config, html: str
) -> tuple[tuple[int, ...], tuple[dict[int, int], ...]]:
    """Map document offsets to the branch of each block around them.

    A path maps every open block to the branch in force, so two offsets
    are in exclusive branches when they disagree on a block they share.
    A block tag inside an ignored block never executes and opens nothing,
    matching the token filtering the rule itself applies.
    """
    boundaries = [0]
    paths: list[dict[int, int]] = [{}]
    stack: list[tuple[str, int, int]] = []
    next_block = 0

    for tag in _template_tags(html):
        if overlaps_ignored_block(
            config, html, tag
        ) or inside_ignored_linter_block(config, html, tag):
            continue
        role = _role(config, tag)
        if role is None:
            continue
        part, name = role
        if part == "branch":
            if not stack:
                continue
            open_name, block, branch = stack[-1]
            stack[-1] = (open_name, block, branch + 1)
        elif part == "close":
            closed = _closed_depth(stack, name)
            if not closed:
                continue
            del stack[-closed:]
        else:
            stack.append((name, next_block, 0))
            next_block += 1
        boundaries.append(tag.end)
        paths.append({block: branch for _, block, branch in stack})

    return tuple(boundaries), tuple(paths)


def _ids(
    html: str, name_end: int, attributes_end: int
) -> list[tuple[re.Match[str], str]]:
    """The literal, non-empty id values written between two offsets.

    Other attributes, stray quoted strings and template tags are consumed
    whole, so an `id=` written inside a title, or a `data-id`, is not read
    as an id. A value holding template syntax is unknowable and skipped.
    """
    return [
        (match, value)
        for match in _ATTRIBUTE_PATTERN.finditer(html, name_end, attributes_end)
        if match.group("attribute")
        for value in (
            match.group("dq") or match.group("sq") or match.group("uq") or "",
        )
        if value and not any(marker in value for marker in _TEMPLATE_SYNTAX)
    ]


def _is_template_element(token: TagToken) -> bool:
    """Whether the tag opens or closes a `<template>`."""
    return token.name.lower() == _TEMPLATE_ELEMENT


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for an id used more than once in the file."""
    errors: list[LintError] = []
    boundaries, paths = _branch_paths(config, html)
    seen: dict[tuple[int, str], list[dict[int, int]]] = {}
    # the document is fragment 0; each <template> opens one of its own,
    # holding a node tree that `getElementById` never reaches
    fragments = [0]
    next_fragment = 1

    for token in tokenize_markup(html):
        if token.declaration:
            continue

        if token.closing:
            if _is_template_element(token) and len(fragments) > 1:
                fragments.pop()
            continue

        ids = (
            _ids(html, token.name_end, token.attributes_end)
            if token.name_end != token.attributes_end
            else []
        )

        if ids and not (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        ):
            for match, value in ids:
                path = paths[bisect_right(boundaries, match.start()) - 1]
                earlier = seen.setdefault((fragments[-1], value), [])
                if any(
                    not mutually_exclusive(previous, path)
                    for previous in earlier
                ):
                    errors.append({
                        "code": rule["name"],
                        "line": get_line(match.start(), line_ends),
                        "match": match.group()[:20],
                        "message": rule["message"],
                    })
                earlier.append(path)

        if _is_template_element(token) and not token.self_closing:
            fragments.append(next_fragment)
            next_fragment += 1

    return tuple(errors)
