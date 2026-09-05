"""Rule T045: Check for a template tag inside an html comment.

An html comment hides markup from the browser, not from the template
engine. `<!-- {% include "debug.html" %} -->` still includes the file and
`<!-- {% if x %}...{% endif %} -->` still evaluates, in Django, Jinja,
Nunjucks, Handlebars and Go alike; only a template comment disables a
tag. A value written into a comment, as in `<!-- built {{ version }} -->`,
is a deliberate way to print into one and is left alone, so only a
statement tag is reported: `{% %}` in Django and its relatives, a
handlebars section, close or partial, and a Go control keyword.

The linter skips html comments as a whole, so this rule reads them for
itself. A comment inside a template comment, a `{% comment %}` block, a
raw block or a `djlint:off` region never runs and is left alone, as is a
downlevel-hidden conditional comment, `<!--[if IE]> ... <![endif]-->`,
whose body is markup for the browser it names rather than a comment.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    child_of_ignored_block,
    inside_ignored_linter_block,
    inside_ignored_rule,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_HTML_COMMENT_PATTERN: Final = re.compile(
    r"""
    <!--
    (?:
        -?>
      | \s*\[if\b(?:(?!-->).)*?-->
      | (?P<body>(?:(?!-->).)*?)-->
    )
    """,
    re.S | re.X,
    cache_pattern=False,
)
_BODY_PATTERN: Final = re.compile(
    r"""
      (?<!\{)\{\#.*?\#\}
    | \{\{!--.*?--\}\}
    | \{\{!.*?\}\}
    | \{\{-?\s*/\*.*?\*/\s*-?\}\}
    | \{%[-+]?\s*comment\b(?:(?!%\}).)*?%\}.*?\{%[-+]?\s*endcomment\s*[-+]?%\}
    | (?P<statement>
          \{%
        | \{\{~?(?:[#>]|/(?!\*))
        | \{\{-?\s*(?:if|range|with|template|block|define|else|end)(?=\s|-?\}\})
      )
    """,
    re.S | re.I | re.X,
    cache_pattern=False,
)


def _holds_statement(body: str) -> bool:
    """Whether a comment body has a statement tag that is not commented out.

    A template comment inside the body is stepped over whole, so a tag
    written inside `{# #}`, `{{! }}`, `{{/* */}}` or `{% comment %}` does
    not count. A go keyword is read only where a go template could write
    it, ahead of a space or the closing braces, so `{{ block.super }}` and
    `{{ range(3) }}` stay values.
    """
    return any(
        match.group("statement") for match in _BODY_PATTERN.finditer(body)
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

    A conditional comment is consumed whole, so its downlevel-revealed
    form `<!--[if !IE]><!--> ... <!--<![endif]-->` leaves the markup
    between, which every other browser renders, outside any comment;
    `<!-->` and `<!--->` are the empty comments html reads them as.

    The comment is reported at its start. `child_of_ignored_block` asks
    for a block that begins before the comment, so the comment's own
    ignored span does not hide it while a template comment, `{% comment %}`
    block or `djlint:off` region around it does.
    """
    errors: list[LintError] = []

    for match in _HTML_COMMENT_PATTERN.finditer(html):
        if not _holds_statement(match.group("body") or ""):
            continue
        if (
            child_of_ignored_block(config, html, match)
            or inside_ignored_rule(config, html, match, rule["name"])
            or inside_ignored_linter_block(config, html, match)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })

    return tuple(errors)
