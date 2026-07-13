"""Collection of shared djLint functions."""

from __future__ import annotations

import itertools
from bisect import bisect_right
from functools import lru_cache
from typing import TYPE_CHECKING

import regex as re

from djlint.formatter.tokenizer import tokenize_tags

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Final

    from typing_extensions import TypeVar

    from djlint.settings import Config
    from djlint.types import SpanMatch

    T = TypeVar("T")


RE_FLAGS_IS: Final = re.I | re.S
RE_FLAGS_IX: Final = re.I | re.X
RE_FLAGS_MS: Final = re.M | re.S
RE_FLAGS_MX: Final = re.M | re.X
RE_FLAGS_IMS: Final = re.I | re.M | re.S
RE_FLAGS_IMX: Final = re.I | re.M | re.X
RE_FLAGS_ISX: Final = re.I | re.S | re.X
RE_FLAGS_IMSX: Final = re.I | re.M | re.S | re.X

_SPAN_CACHE_SIZE: Final = 1
_LINE_CACHE_SIZE: Final = 64


def _last_item(iterable: Iterable[T], /) -> T | None:
    last = None
    for item in iterable:
        last = item
    return last


def _inside_non_overlapping_span(
    spans: tuple[tuple[int, int], ...], match_start: int, match_end: int, /
) -> bool:
    index = bisect_right(spans, (match_start, float("inf"))) - 1
    if index < 0:
        return False

    span_start, span_end = spans[index]
    return span_start <= match_start and match_end <= span_end


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_ignored_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    inline = _last_item(config.ignored_blocks_inline_pattern.finditer(item))
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(config.ignored_block_opening_pattern.search(item[last_index:]))


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_script_style_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    inline = _last_item(config.script_style_inline_imsx_pattern.finditer(item))
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(config.script_style_opening_pattern.search(item[last_index:]))


def inside_protected_trans_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.

    True = non indentable > inside ignored trans block
    False = indentable > either inside a trans trimmed block, or somewhere else, but not a trans non trimmed :)
    """
    close_block = config.ignored_trans_blocks_closing_pattern.search(
        match.group()
    )

    if not close_block:
        return False

    non_trimmed = _last_item(config.ignored_trans_blocks_pattern.finditer(html))

    trimmed = _last_item(config.trans_trimmed_blocks_pattern.finditer(html))

    # who is max?
    if non_trimmed and (not trimmed or non_trimmed.end() > trimmed.end()):
        # non trimmed!
        # check that this is not an inline block.
        non_trimmed_inline = bool(
            config.ignored_trans_blocks_pattern.search(match.group())
        )

        if non_trimmed_inline:
            last_index = non_trimmed.end()  # get the last index. The ignored opening should start after this.

            return bool(
                config.ignored_trans_blocks_closing_pattern.search(
                    html[last_index:]
                )
            )

        return close_block.end() <= non_trimmed.end()

    if trimmed:
        # inside a trimmed block, we can return true to continue as if
        # this is a indentable block
        return close_block.end() > trimmed.end()
    return False


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_ignored_block_closing(config: Config, item: str) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.
    """
    inline = _last_item(config.ignored_inline_blocks_ix_pattern.finditer(item))
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(config.ignored_block_closing_pattern.search(item[last_index:]))


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_script_style_block_closing(config: Config, item: str) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.
    """
    inline = _last_item(config.script_style_inline_ix_pattern.finditer(item))
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(config.script_style_closing_pattern.search(item[last_index:]))


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_safe_closing_tag(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    inline = _last_item(config.safe_closing_block_pattern.finditer(item))
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(config.safe_closing_tag_pattern.search(item[last_index:]))


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_template_block(
    html: str, /, *, template_blocks: re.Pattern[str]
) -> tuple[tuple[int, int], ...]:
    return tuple(x.span() for x in template_blocks.finditer(html))


def inside_template_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Check if a re.Match is inside of a template block."""
    match_start, match_end = match.span()
    return _inside_non_overlapping_span(
        _inside_template_block(
            html, template_blocks=config.template_blocks_pattern
        ),
        match_start,
        match_end,
    )


def mask_template_tags(
    config: Config, html: str
) -> tuple[str, list[tuple[str, str]]]:
    """Hide template tags from formatters that parse JS or CSS."""
    if "{%" not in html and "{{" not in html and "{#" not in html:
        return html, []

    replacements: list[tuple[str, str]] = []
    marker_prefix = "__DJLINT_TEMPLATE_TAG_"
    while marker_prefix in html:
        marker_prefix = f"_{marker_prefix}"

    def replace(match: re.Match[str]) -> str:
        marker = f"{marker_prefix}{len(replacements)}__"
        replacements.append((marker, match.group()))
        line_start = html.rfind("\n", 0, match.start()) + 1
        line_end = html.find("\n", match.end())
        if line_end < 0:
            line_end = len(html)
        if (
            not html[line_start : match.start()].strip()
            and not html[match.end() : line_end].strip()
        ):
            return f"/*{marker}*/"
        return marker

    template_tags = rf"(?:{config.template_tags})|\{{\#(?:(?!\#\}}).)*\#\}}"

    return (
        re.sub(template_tags, replace, html, flags=RE_FLAGS_ISX),
        replacements,
    )


def restore_template_tags(
    html: str, replacements: list[tuple[str, str]]
) -> str:
    """Put masked template tags back after JS or CSS formatting."""
    for marker, replacement in replacements:
        html = html.replace(f"/*{marker}*/", replacement).replace(
            marker, replacement
        )
    return html


_UNFORMATTED_BLOCK_PATTERN: Final = re.compile(
    r"""
          <!--\s*djlint\:off\s*-->.*?(?:<!--\s*djlint\:on\s*-->|\Z)
        | {\#\s*djlint\:\s*off\s*\#}.*?(?:{\#\s*djlint\:\s*on\s*\#}|\Z)
        | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}.*?(?:{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}|\Z)
        | {{!--\s*djlint\:off\s*--}}.*?(?:{{!--\s*djlint\:on\s*--}}|\Z)
        | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}.*?(?:{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}|\Z)
    """,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_OPENING_HTML_TAG_PATTERN: Final = re.compile(r"</?\w", cache_pattern=False)
_RULE_SEPARATOR_PATTERN: Final = re.compile(r"\s|,", cache_pattern=False)


def mask_unformatted_blocks(html: str) -> tuple[str, list[tuple[str, str]]]:
    """Hide djlint:off blocks from the formatter pipeline."""
    if "djlint:" not in html:
        return html, []

    replacements: list[tuple[str, str]] = []
    marker_prefix = "__DJLINT_UNFORMATTED_BLOCK_"
    while marker_prefix in html:
        marker_prefix = f"_{marker_prefix}"

    def inside_opening_tag(index: int) -> bool:
        tag_start = html.rfind("<", 0, index)
        return tag_start > html.rfind(">", 0, index) and bool(
            _OPENING_HTML_TAG_PATTERN.match(html[tag_start:])
        )

    def replace(match: re.Match[str]) -> str:
        marker = f"{marker_prefix}{len(replacements)}__"
        replacement = match.group()
        if not inside_opening_tag(match.start()):
            marker = f"/*{marker}*/"
        else:
            line_start = html.rfind("\n", 0, match.start()) + 1
            leading = html[line_start : match.start()]
            if leading and not leading.strip():
                replacement = f"\n{leading}{replacement}"
        replacements.append((marker, replacement))
        return marker

    return (_UNFORMATTED_BLOCK_PATTERN.sub(replace, html), replacements)


def restore_unformatted_blocks(
    html: str, replacements: list[tuple[str, str]]
) -> str:
    """Put masked djlint:off blocks back after formatting."""
    for marker, replacement in replacements:

        def replace_marker(
            match: re.Match[str], replacement: str = replacement
        ) -> str:
            indent = match.group(1)
            lines = replacement.split("\n")
            lines[0] = indent + lines[0].lstrip()
            if "djlint:on" in lines[-1]:
                lines[-1] = indent + lines[-1].lstrip()
            return "\n".join(lines)

        html = re.sub(
            rf"^([ \t]*){re.escape(marker)}[ \t]*$",
            replace_marker,
            html,
            flags=RE_FLAGS_MX,
        )
        if replacement.startswith("\n"):
            html = re.sub(
                rf"[ \t]*{re.escape(marker)}",
                replacement,
                html,
                flags=RE_FLAGS_MX,
            )
        html = html.replace(marker, replacement)
    return html


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _html_attribute_spans(html: str, /) -> tuple[tuple[int, int], ...]:
    return tuple(
        (token.name_end, token.attributes_end)
        for token in tokenize_tags(html)
        if token.name_end < token.attributes_end
    )


def inside_html_attribute(html: str, match: re.Match[str]) -> bool:
    """Check if a re.Match is inside of an html attribute."""
    match_start, match_end = match.span()
    return _inside_non_overlapping_span(
        _html_attribute_spans(html), match_start, match_end
    )


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_ignored_linter_block(
    html: str, /, *, ignored_linter_blocks: re.Pattern[str]
) -> tuple[tuple[int, int], ...]:
    return tuple(x.span() for x in ignored_linter_blocks.finditer(html))


def inside_ignored_linter_block(
    config: Config, html: str, match: SpanMatch
) -> bool:
    """Check if a re.Match is inside of a ignored linter block."""
    match_start, match_end = match.span()
    return _inside_non_overlapping_span(
        _inside_ignored_linter_block(
            html, ignored_linter_blocks=config.ignored_linter_blocks_pattern
        ),
        match_start,
        match_end,
    )


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_ignored_block(
    html: str,
    /,
    *,
    ignored_blocks: re.Pattern[str],
    ignored_inline_blocks: re.Pattern[str],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        x.span()
        for x in itertools.chain(
            ignored_blocks.finditer(html), ignored_inline_blocks.finditer(html)
        )
    )


def inside_ignored_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match_start, ignored_match_end in _inside_ignored_block(
        html,
        ignored_blocks=config.ignored_blocks_pattern,
        ignored_inline_blocks=config.ignored_inline_blocks_ix_pattern,
    ):
        if (
            ignored_match_start <= match_start
            and match_end <= ignored_match_end
        ):
            return True
    return False


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _child_of_unformatted_block(
    html: str,
    /,
    *,
    unformatted_blocks: re.Pattern[str],
    unformatted_blocks_coarse: re.Pattern[str],
) -> tuple[tuple[int, int], ...]:
    if not unformatted_blocks_coarse.search(html):
        return ()
    return tuple(x.span() for x in unformatted_blocks.finditer(html))


def child_of_unformatted_block(
    config: Config, html: str, match: SpanMatch
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match_start, ignored_match_end in _child_of_unformatted_block(
        html,
        unformatted_blocks=config.unformatted_blocks_pattern,
        unformatted_blocks_coarse=config.unformatted_blocks_coarse_pattern,
    ):
        if ignored_match_start < match_start and match_end <= ignored_match_end:
            return True
    return False


def child_of_ignored_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match in itertools.chain(
        config.ignored_blocks_pattern.finditer(html),
        config.ignored_inline_blocks_ix_pattern.finditer(html),
    ):
        ignored_match_start, ignored_match_end = ignored_match.span()
        if ignored_match_start < match_start and match_end <= ignored_match_end:
            return True
    return False


def overlaps_ignored_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match_start, ignored_match_end in _inside_ignored_block(
        html,
        ignored_blocks=config.ignored_blocks_pattern,
        ignored_inline_blocks=config.ignored_inline_blocks_ix_pattern,
    ):
        # don't require the match to be fully inside the ignored block.
        # poorly build html will probably span ignored blocks and should be ignored.
        if (ignored_match_start <= match_start <= ignored_match_end) or (
            ignored_match_start <= match_end <= ignored_match_end
        ):
            return True
    return False


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_ignored_rule(
    html: str, /, *, ignored_rules: tuple[re.Pattern[str], ...]
) -> tuple[tuple[int, int, frozenset[str], bool], ...]:
    rule_spans = []
    for rule_pattern in ignored_rules:
        for ignored_match in rule_pattern.finditer(html):
            ignored_match_start, ignored_match_end = ignored_match.span()
            rule_names = ignored_match.group(1).strip()
            rule_spans.append((
                ignored_match_start,
                ignored_match_end,
                frozenset(
                    x for x in _RULE_SEPARATOR_PATTERN.split(rule_names) if x
                ),
                not rule_names,
            ))
    return tuple(rule_spans)


def inside_ignored_rule(
    config: Config, html: str, match: SpanMatch, rule: str
) -> bool:
    """Check if match is inside an ignored pattern."""
    match_start, match_end = match.span()
    for (
        ignored_match_start,
        ignored_match_end,
        ignored_rule_names,
        ignore_all_rules,
    ) in _inside_ignored_rule(html, ignored_rules=config.ignored_rule_patterns):
        if (
            (ignored_match_start <= match_start <= ignored_match_end)
            and rule in ignored_rule_names
        ) or (
            (ignored_match_start <= match_end <= ignored_match_end)
            and ignore_all_rules
        ):
            return True
    return False
