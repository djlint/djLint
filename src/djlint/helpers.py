"""Collection of shared djLint functions."""

from __future__ import annotations

import itertools
from bisect import bisect_left, bisect_right
from functools import lru_cache
from typing import TYPE_CHECKING

import regex as re

from djlint.formatter.tokenizer import tokenize_tags

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Final

    from typing_extensions import TypeVar

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import SpanMatch

    T = TypeVar("T")


RE_FLAGS_IS: Final = re.I | re.S
RE_FLAGS_IX: Final = re.I | re.X
RE_FLAGS_MSX: Final = re.M | re.S | re.X
RE_FLAGS_MX: Final = re.M | re.X
RE_FLAGS_IMS: Final = re.I | re.M | re.S
RE_FLAGS_IMX: Final = re.I | re.M | re.X
RE_FLAGS_ISX: Final = re.I | re.S | re.X
RE_FLAGS_IMSX: Final = re.I | re.M | re.S | re.X

_SPAN_CACHE_SIZE: Final = 1
_AFTER_EVERY_SPAN: Final = float("inf")
_LINE_CACHE_SIZE: Final = 256

YAML_FRONT_MATTER: Final = r"""
    # front matter opens the file and holds the site generator's own data,
    # so a block tag in it means "---" is a yaml document separator instead
    \A---(?:(?!\{%)[\s\S])*?^---[^\S\n]*$
"""


def split_option_list(value: str | None) -> list[str]:
    """Split a comma separated option, dropping blank entries.

    A blank entry would build a pattern matching everywhere, so a trailing
    comma in the configuration must not change what an option means.
    """
    if not value:
        return []
    return [entry for x in value.split(",") if (entry := x.strip())]


def _last_item(iterable: Iterable[T], /) -> T | None:
    last = None
    for item in iterable:
        last = item
    return last


def _inside_non_overlapping_span(
    spans: tuple[tuple[int, int], ...], match_start: int, match_end: int, /
) -> bool:
    index = bisect_right(spans, (match_start, _AFTER_EVERY_SPAN)) - 1
    if index < 0:
        return False

    span_start, span_end = spans[index]
    return span_start <= match_start and match_end <= span_end


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def ignored_block_opening_start(config: Config, item: str) -> int:
    """Where the line opens an ignored block it does not close, or -1.

    An opening that is not part of a block closed on this line leaves a
    block open, even when a self-contained one follows it, as in
    `<pre>a<!--b-->`. Only the marker's last character is probed for
    containment: some alternatives start one character early, so `[^{]{#`
    matches the quote in `class="{# x #}"`.

    A line holding neither a `<` nor a `{` carries no markup and no
    template syntax, so it opens nothing, and ruling it out that way costs
    far less than asking the pattern.
    """
    if "<" not in item and "{" not in item:
        return -1

    inline = None
    for match in config.ignored_block_opening_pattern.finditer(item):
        if inline is None:
            inline = tuple(
                block.span()
                for block in config.ignored_blocks_inline_pattern.finditer(item)
            )
        if not _inside_non_overlapping_span(
            inline, match.end() - 1, match.end()
        ):
            return match.start()
    return -1


def is_ignored_block_opening(config: Config, item: str) -> bool:
    """Whether the line opens an ignored block it does not close."""
    return ignored_block_opening_start(config, item) >= 0


def _past_inline_blocks(item: str, inline_blocks: re.Pattern[str], /) -> str:
    """What is left of the line beyond every block it opens and closes.

    A marker inside such a block belongs to it, so it leaves nothing open.
    """
    last_inline = _last_item(inline_blocks.finditer(item))
    return item[last_inline.end() :] if last_inline else item


def _marker_past_inline_blocks(
    item: str, inline_blocks: re.Pattern[str], marker: re.Pattern[str], /
) -> bool:
    """Whether a marker sits past every block the line opens and closes."""
    return bool(marker.search(_past_inline_blocks(item, inline_blocks)))


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_raw_text_block_opening(config: Config, item: str) -> bool:
    """Whether the line opens a raw text element it does not close."""
    return _marker_past_inline_blocks(
        item,
        config.raw_text_inline_imsx_pattern,
        config.raw_text_opening_pattern,
    )


def inside_protected_trans_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Whether the match closes a trans block whose contents keep their form.

    True means the match sits inside a non trimmed trans block, which is
    not indentable. False means it is indentable: either inside a trimmed
    trans block, or nowhere near one.
    """
    close_block = config.ignored_trans_blocks_closing_pattern.search(
        match.group()
    )

    if not close_block:
        return False

    non_trimmed = _last_item(config.ignored_trans_blocks_pattern.finditer(html))
    trimmed = _last_item(config.trans_trimmed_blocks_pattern.finditer(html))

    if non_trimmed and (not trimmed or non_trimmed.end() > trimmed.end()):
        if config.ignored_trans_blocks_pattern.search(match.group()):
            return bool(
                config.ignored_trans_blocks_closing_pattern.search(
                    html[non_trimmed.end() :]
                )
            )

        return close_block.end() <= non_trimmed.end()

    if trimmed:
        return close_block.end() > trimmed.end()
    return False


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_ignored_block_closing(config: Config, item: str) -> bool:
    """Whether the line closes an ignored block opened on an earlier one.

    The markers that only reach a match from where the rest of the line
    starts are looked for on their own: alongside the others they cost the
    whole search its literal prefilter, for a tenfold slowdown. Each of
    them needs a `-->` or a `#}`, which is far cheaper to rule out than to
    match.
    """
    rest = _past_inline_blocks(item, config.ignored_inline_blocks_ix_pattern)
    if config.ignored_block_closing_anywhere_pattern.search(rest):
        return True
    return ("-->" in rest or "#}" in rest) and bool(
        config.ignored_block_closing_at_start_pattern.match(rest)
    )


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_raw_text_block_closing(config: Config, item: str) -> bool:
    """Whether the line closes a raw text element opened on an earlier one."""
    return _marker_past_inline_blocks(
        item, config.raw_text_inline_ix_pattern, config.raw_text_closing_pattern
    )


@lru_cache(maxsize=_LINE_CACHE_SIZE)
def is_safe_closing_tag(config: Config, item: str) -> bool:
    """Whether the line closes an ignored block and can still be indented."""
    return _marker_past_inline_blocks(
        item, config.safe_closing_block_pattern, config.safe_closing_tag_pattern
    )


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


def _restore_unformatted_block(html: str, marker: str, replacement: str) -> str:
    def reindent(match: re.Match[str]) -> str:
        indent = match.group(1)
        lines = replacement.split("\n")
        lines[0] = indent + lines[0].lstrip()
        if "djlint:on" in lines[-1]:
            lines[-1] = indent + lines[-1].lstrip()
        return "\n".join(lines)

    escaped = re.escape(marker)
    html = re.sub(
        rf"^([ \t]*){escaped}[ \t]*$", reindent, html, flags=RE_FLAGS_MX
    )
    if replacement.startswith("\n"):
        html = re.sub(
            rf"[ \t]*{escaped}",
            lambda _match: replacement,
            html,
            flags=RE_FLAGS_MX,
        )
    return html.replace(marker, replacement)


def restore_unformatted_blocks(
    html: str, replacements: list[tuple[str, str]]
) -> str:
    """Put masked djlint:off blocks back after formatting."""
    for marker, replacement in replacements:
        html = _restore_unformatted_block(html, marker, replacement)
    return html


_RAW_TEXT_ELEMENT_PATTERN: Final = re.compile(
    r"""
    (<(script|style|textarea)\b
      (?:\"[^\"]*\"|'[^']*'|\{[^}]*\}|[^'\">{}])*>)
    (.*?)
    (?=</\2)
    """,
    RE_FLAGS_ISX,
    cache_pattern=False,
)


_NON_NEWLINE_PATTERN: Final = re.compile(r"[^\n]", cache_pattern=False)


def _blank_raw_text(match: re.Match[str]) -> str:
    return match.group(1) + _NON_NEWLINE_PATTERN.sub(" ", match.group(3))


def mask_raw_text_bodies(html: str) -> str:
    """Blank out what the tag tokenizer should not read as markup.

    A raw text element holds text, so the "<" of `var s = "<div>"` opens no
    tag, the apostrophe in `// don't` starts no attribute value, and a
    `{% %}` pair is javascript rather than a template tag. Each body is
    blanked to the same length, keeping offsets and line numbers, so
    positions still index the html that was passed in.
    """
    return _RAW_TEXT_ELEMENT_PATTERN.sub(_blank_raw_text, html)


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def tokenize_markup(html: str) -> tuple[TagToken, ...]:
    """Tokenize the tags of a document, skipping raw text bodies."""
    return tuple(tokenize_tags(mask_raw_text_bodies(html)))


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


def inside_ignored_block_span(
    config: Config, html: str, start: int, end: int
) -> bool:
    """Whether a span of the html lies inside an ignored block."""
    for ignored_match_start, ignored_match_end in _inside_ignored_block(
        html,
        ignored_blocks=config.ignored_blocks_pattern,
        ignored_inline_blocks=config.ignored_inline_blocks_ix_pattern,
    ):
        if ignored_match_start <= start and end <= ignored_match_end:
            return True
    return False


def breaks_an_ignored_block(config: Config, html: str, position: int) -> bool:
    """Whether a line break written here would land inside an ignored block.

    The point is tested rather than the tag, so a break placed against the
    outside edge of a block is allowed: the closing tag of a `<script>` is
    part of the element, but the position after it is not.
    """
    return any(
        ignored_start < position < ignored_end
        for ignored_start, ignored_end in _inside_ignored_block(
            html,
            ignored_blocks=config.ignored_blocks_pattern,
            ignored_inline_blocks=config.ignored_inline_blocks_ix_pattern,
        )
    )


def inside_ignored_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return inside_ignored_block_span(config, html, *match.span())


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
    for ignored_match_start, ignored_match_end in _inside_ignored_block(
        html,
        ignored_blocks=config.ignored_blocks_pattern,
        ignored_inline_blocks=config.ignored_inline_blocks_ix_pattern,
    ):
        if ignored_match_start < match_start and match_end <= ignored_match_end:
            return True
    return False


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _merged_ignored_blocks(
    html: str,
    /,
    *,
    ignored_blocks: re.Pattern[str],
    ignored_inline_blocks: re.Pattern[str],
) -> tuple[tuple[int, int], ...]:
    """The ignored spans, sorted and merged so a lookup can bisect them.

    Merging preserves which points are covered, and the two patterns are
    searched separately, so the raw spans arrive as two sorted runs that
    can overlap each other.
    """
    merged: list[tuple[int, int]] = []
    for start, end in sorted(
        _inside_ignored_block(
            html,
            ignored_blocks=ignored_blocks,
            ignored_inline_blocks=ignored_inline_blocks,
        )
    ):
        if merged and start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))
    return tuple(merged)


def overlaps_ignored_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Check if a match is in a block the linter skips.

    Uses the lint spans, which cover the tag closing a script/style block;
    the formatter's stop short of it so it can still be indented.

    A match need not lie wholly inside the block: poorly built html tends
    to straddle one and should be skipped all the same. Spans are half
    open, so a match that only touches an ignored block, as in
    `{% if x %}{# comment #}`, starts and ends outside of it.
    """
    spans = _merged_ignored_blocks(
        html,
        ignored_blocks=config.lint_ignored_blocks_pattern,
        ignored_inline_blocks=config.lint_ignored_inline_blocks_ix_pattern,
    )
    if not spans:
        return False

    match_start, match_end = match.span()
    index = bisect_right(spans, (match_start, _AFTER_EVERY_SPAN)) - 1
    if index >= 0:
        start, end = spans[index]
        if start <= match_start < end:
            return True

    index = bisect_left(spans, (match_end,)) - 1
    return index >= 0 and match_end <= spans[index][1]


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
    """Check if match is inside an ignored pattern.

    Spans are half open, so a match ending exactly where a pragma starts is
    outside of it. A bare pragma ignores every rule, so it only covers
    matches ending inside it; a match merely wrapping one, such as a whole
    `<div ... {# djlint:off #} ... >` tag, keeps being checked, otherwise
    rules that pair tags would lose track of it.
    """
    match_start, match_end = match.span()
    return any(
        (
            ignored_start < match_end
            and match_start < ignored_end
            and rule in ignored_rule_names
        )
        or (ignore_all_rules and ignored_start < match_end <= ignored_end)
        for (
            ignored_start,
            ignored_end,
            ignored_rule_names,
            ignore_all_rules,
        ) in _inside_ignored_rule(
            html, ignored_rules=config.ignored_rule_patterns
        )
    )


_BRANCHED_BLOCK_PATTERN: Final = re.compile(
    r"""
      \{%[-+]?\s*(?P<statement>endif|endfor|elseif|elif|else|empty|if|for)\b
    | \{\{-?\s*(?P<section>[#^/])?(?P<name>if|unless|each|with|range|block|else|end)\b
    """,
    re.X,
    cache_pattern=False,
)
_BLOCK_OPENINGS: Final = frozenset(("if", "for"))
_BLOCK_ENDINGS: Final = frozenset(("endif", "endfor"))
_MUSTACHE_OPENINGS: Final = frozenset(("if", "range", "with", "block"))


def _block_role(match: re.Match[str]) -> str:
    """Whether the tag opens a block, closes one, or starts a branch.

    Handlebars marks a section with `#` and its close with `/`; go writes
    neither and closes with `end`. A `{{ end }}` with nothing open is not
    a close, and the caller drops it.
    """
    statement = match.group("statement")
    if statement:
        if statement in _BLOCK_OPENINGS:
            return "open"
        return "close" if statement in _BLOCK_ENDINGS else "branch"

    section, name = match.group("section"), match.group("name")
    if section == "/":
        return "close"
    if section:
        return "branch" if section == "^" and name == "else" else "open"
    if name == "else":
        return "branch"
    if name == "end":
        return "close"
    return "open" if name in _MUSTACHE_OPENINGS else "branch"


def branched_blocks(html: str) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Branch spans of every complete conditional or loop block.

    A for block takes branches of its own, since jinja spells its empty
    case {% else %} and django spells it {% empty %}. Without that, the
    else of a for nested in an if would end the if's own branch.

    Handlebars `{{#if}}...{{else}}...{{/if}}` and go
    `{{if}}...{{else}}...{{end}}` are read the same way, so a wrapper
    opened in one branch and closed in another is not an orphan there
    either.
    """
    complete: list[tuple[tuple[int, int], ...]] = []
    open_blocks: list[tuple[list[tuple[int, int]], int]] = []
    for match in _BRANCHED_BLOCK_PATTERN.finditer(html):
        role = _block_role(match)
        if role == "open":
            open_blocks.append(([], match.end()))
        elif not open_blocks:
            continue
        elif role == "close":
            branches, start = open_blocks.pop()
            branches.append((start, match.start()))
            complete.append(tuple(branches))
        else:
            branches, start = open_blocks[-1]
            branches.append((start, match.start()))
            open_blocks[-1] = (branches, match.end())
    return tuple(complete)


def branch_context(
    blocks: tuple[tuple[tuple[int, int], ...], ...], pos: int
) -> dict[int, int]:
    """Map each block containing pos to the branch pos is in.

    Branches run in order and do not overlap, so a block that does not
    span pos at all is skipped without looking at its branches.
    """
    context: dict[int, int] = {}
    for index, branches in enumerate(blocks):
        if not branches[0][0] <= pos < branches[-1][1]:
            continue
        for branch, (start, end) in enumerate(branches):
            if start <= pos < end:
                context[index] = branch
                break
    return context


def mutually_exclusive(a: dict[int, int], b: dict[int, int]) -> bool:
    """Whether two positions are in sibling branches of a block."""
    return any(b.get(block, branch) != branch for block, branch in a.items())
