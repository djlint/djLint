"""Rule T045: Check for a template tag inside an html comment.

An html comment hides markup from the browser, not from the template
engine. `<!-- {% include "debug.html" %} -->` still includes the file and
`<!-- {% if x %}...{% endif %} -->` still evaluates, in Django, Jinja,
Nunjucks, Handlebars and Go alike; only a template comment disables a
tag. A value written into a comment, as in `<!-- built {{ version }} -->`,
is a deliberate way to print into one and is left alone, so only a
statement tag is reported: `{% %}` where the engine in force has it, a
handlebars section, close or partial, and a Go control keyword.

The linter skips html comments as a whole, so this rule reads them for
itself. A comment inside a template comment, a `{% comment %}` block, a
raw block or a `djlint:off` region never runs and is left alone, as is a
downlevel-hidden conditional comment, `<!--[if IE]> ... <![endif]-->`,
whose body is markup for the browser it names rather than a comment.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    child_of_ignored_block,
    inside_ignored_linter_block,
    inside_ignored_rule,
)
from djlint.lint import get_line

if sys.version_info >= (3, 11):
    from typing import final
else:
    from typing_extensions import final

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_COMMENT_OPENING: Final = "<!--"
_COMMENT_CLOSING: Final = "-->"
# html closes a comment on "--!>" too, with a parse error
_BOGUS_COMMENT_CLOSING: Final = "--!>"
# `<!-->` and `<!--->` are the empty comments html reads them as
_ABRUPT_CLOSINGS: Final = (">", "->")

# handlebars and go have no `{% %}` syntax, so `{%` is literal text there
_PROFILES_WITHOUT_STATEMENT_TAGS: Final = frozenset(("golang", "handlebars"))
# a bare go keyword cannot be told from a variable of the same name, so it
# is read as a statement only where go templates are what is being linted
_GOLANG_PROFILES: Final = frozenset(("all", "golang"))

_CONDITIONAL_OPENING_PATTERN: Final = re.compile(
    r"\[if(?=[\s(!])", re.I, cache_pattern=False
)
_CONDITIONAL_CLOSING_PATTERN: Final = re.compile(
    r"<!\[endif\]\s*$", re.I, cache_pattern=False
)
_BODY_PATTERN: Final = re.compile(
    r"""
      (?<!\{)\{\#.*?\#\}
    | \{\{!--.*?--\}\}
    | \{\{!.*?\}\}
    | \{\{-?\s*/\*.*?\*/\s*-?\}\}
    | \{%[-+]?\s*\#(?:(?!%\}).)*?%\}
    | \{%[-+]?\s*comment\b(?:(?!%\}).)*?%\}
      .*?
      \{%[-+]?\s*endcomment\b(?:(?!%\}).)*?%\}
    | \{\{\{\{\s*raw\b(?:(?!\}\}\}\}).)*?\}\}\}\}
      .*?
      \{\{\{\{\s*/\s*raw\s*\}\}\}\}
    | (?P<statement>\{%)
    | (?P<section>\{\{~?(?:[#>]|/(?!\*)))
    | (?P<go_action>
          \{\{-?\s*(?:if|range|with|template|block|define)\s+["$.]
      )
    | (?P<go_keyword>
          \{\{-?\s*(?:if|range|with|template|block|define|else|end)
          (?=\s|-?\}\})
      )
    """,
    re.S | re.I | re.X,
    cache_pattern=False,
)
_IGNORED_BLOCK_PATTERN: Final = re.compile(
    r"""
    # the shared ignored block patterns spell these with plain spaces and
    # an unnamed closing tag, so the forms below reach this rule
      \{%[-+]?\s*(?P<block>comment|raw|verbatim)\b(?:(?!%\}).)*?%\}
      .*?
      \{%[-+]?\s*end(?P=block)\b(?:(?!%\}).)*?%\}
    | \{\{\{\{\s*raw\b(?:(?!\}\}\}\}).)*?\}\}\}\}
      .*?
      \{\{\{\{\s*/\s*raw\s*\}\}\}\}
    """,
    re.S | re.I | re.X,
    cache_pattern=False,
)


@final
@dataclass(
    repr=False,
    eq=False,
    frozen=True,
    match_args=False,
    kw_only=False,
    slots=True,
)
class _HtmlComment:
    """An html comment, from its `<!--` to past whatever closes it."""

    _html: str
    _start: int
    _end: int
    body: str

    def span(self) -> tuple[int, int]:
        return self._start, self._end

    def start(self) -> int:
        return self._start

    def group(self) -> str:
        return self._html[self._start : self._end]


def _closing(html: str, pos: int, /) -> int:
    """Where the comment opened before `pos` closes, or -1.

    The earlier of `-->` and the `--!>` html accepts with a parse error
    wins. Neither is a prefix of the other, so one search each is enough.
    """
    plain = html.find(_COMMENT_CLOSING, pos)
    bogus = html.find(_BOGUS_COMMENT_CLOSING, pos)
    if plain < 0:
        return bogus
    if bogus < 0 or plain < bogus:
        return plain
    return bogus


def _html_comments(html: str) -> Iterator[_HtmlComment]:
    """Every html comment in the source, in order.

    The scan is written with `str.find` rather than a tempered pattern so
    that it stays linear: a pattern reading `<!--(?:(?!-->).)*?-->` walks
    to the end of the file at every `<!--` it cannot close, which costs a
    file of truncated openings quadratic time. Here a comment that nothing
    closes ends the scan, since nothing closes any opening after it
    either.
    """
    pos = 0
    while (start := html.find(_COMMENT_OPENING, pos)) != -1:
        body_start = start + len(_COMMENT_OPENING)
        for abrupt in _ABRUPT_CLOSINGS:
            if html.startswith(abrupt, body_start):
                pos = body_start + len(abrupt)
                break
        else:
            body_end = _closing(html, body_start)
            if body_end < 0:
                return
            pos = body_end + (
                len(_COMMENT_CLOSING)
                if html.startswith(_COMMENT_CLOSING, body_end)
                else len(_BOGUS_COMMENT_CLOSING)
            )
            yield _HtmlComment(html, start, pos, html[body_start:body_end])


def _is_conditional_comment(body: str) -> bool:
    """Whether the comment is a downlevel-hidden conditional comment.

    `<!--[if lt IE 9]> ... <![endif]-->` is markup for the browser it
    names, so a tag in it is meant to run. The opening is read where it
    is written, straight after the `<!--` and ahead of the whitespace,
    `(` or `!` an expression starts with, so that prose reading
    `<!-- [if in doubt] ...` or a word such as `[if-modified-since]` is an
    ordinary comment; and the closing has to be there, so that a
    conditional comment left unclosed is read as the ordinary comment the
    html parser makes of it.
    """
    return bool(
        _CONDITIONAL_OPENING_PATTERN.match(body)
        and _CONDITIONAL_CLOSING_PATTERN.search(body)
    )


def _holds_statement(config: Config, body: str) -> bool:
    """Whether a comment body has a statement tag that is not commented out.

    A template comment inside the body is stepped over whole, so a tag
    written inside `{# #}`, `{{! }}`, `{{/* */}}`, `{% # %}`,
    `{% comment %}` or a handlebars raw block does not count. A go keyword
    is read only where a go template could write it, ahead of a space or
    the closing braces, so `{{ block.super }}` and `{{ range(3) }}` stay
    values; a bare one such as `{{ end }}` is a variable in every other
    engine and is read as a statement only under the go profile, while one
    carrying a go operand, as `{{ if .X }}` and `{{ template "footer" }}`
    do, is a statement no engine prints.

    An opening no closing brace follows opens nothing, so prose such as
    `battery at 50{% charge` or `log format is {%s} on error` is the text
    it looks like. The last closing brace in the body answers that for
    every opening at once, which keeps the reading linear where asking
    each opening for its own closing would not.
    """
    reads_statements = config.profile not in _PROFILES_WITHOUT_STATEMENT_TAGS
    reads_go_keywords = config.profile in _GOLANG_PROFILES
    last_statement_closing = body.rfind("%}")
    last_tag_closing = body.rfind("}}")
    for match in _BODY_PATTERN.finditer(body):
        if match.group("statement"):
            if reads_statements and match.start() < last_statement_closing:
                return True
        elif match.start() < last_tag_closing and (
            match.group("section")
            or match.group("go_action")
            or (reads_go_keywords and match.group("go_keyword"))
        ):
            return True
    return False


@lru_cache(maxsize=1)
def _ignored_block_spans(html: str) -> tuple[tuple[int, int], ...]:
    return tuple(
        match.span() for match in _IGNORED_BLOCK_PATTERN.finditer(html)
    )


def _inside_ignored_block(html: str, comment: _HtmlComment) -> bool:
    """Whether a block this rule reads for itself wraps the comment.

    The block has to open before the comment, as `child_of_ignored_block`
    asks, so that a `{% comment %}` written inside the comment does not
    hide it.
    """
    start, end = comment.span()
    return any(
        block_start < start and end <= block_end
        for block_start, block_end in _ignored_block_spans(html)
    )


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for a statement tag inside an html comment.

    A conditional comment is left alone, so its downlevel-revealed form
    `<!--[if !IE]><!--> ... <!--<![endif]-->` leaves the markup between,
    which every other browser renders, outside any comment: the opening
    closes at the `-->` inside `<!-->` and holds no tag.

    The comment is reported at its start. `child_of_ignored_block` asks
    for a block that begins before the comment, so the comment's own
    ignored span does not hide it while a template comment, `{% comment %}`
    block or `djlint:off` region around it does.
    """
    errors: list[LintError] = []

    for comment in _html_comments(html):
        if not _holds_statement(config, comment.body):
            continue
        if _is_conditional_comment(comment.body):
            continue
        if (
            child_of_ignored_block(config, html, comment)
            or inside_ignored_rule(config, html, comment, rule["name"])
            or inside_ignored_linter_block(config, html, comment)
            or _inside_ignored_block(html, comment)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(comment.start(), line_ends),
            "match": comment.group().strip()[:20],
            "message": rule["message"],
        })

    return tuple(errors)
