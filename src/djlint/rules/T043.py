"""Rule T043: Check for a block name used more than once.

Django, Jinja and Nunjucks all refuse a template that names two blocks
the same, and they refuse it at parse time, so the page fails to load at
all. The engines do not care that the two blocks sit in different branches
of an `{% if %}`, so no branch is tracked here: a name that appears twice
in one template scope is an error, and each occurrence after the first is
reported at its own tag.

Only what the engine itself never parses is skipped: a template comment,
a `{% comment %}` block, a `{% raw %}` or `{% verbatim %}` body, and a
`djlint:off` region. An html comment, a `<script>`, `<style>`, `<pre>` or
`<textarea>` body and a `{% filter %}` body are all read for blocks,
since the engine reads them too and raises on the duplicate all the same.

An `{% embed %}` opens a scope of its own: the blocks in it fill the
embedded template rather than this one, so two embeds of the same partial
may each write `{% block body %}`, while a name repeated inside a single
embed is still reported.
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


_TOKEN_PATTERN: Final = re.compile(
    r"""
    # a template comment hides all it holds from the engine, so it is
    # consumed whole rather than searched for tags; "{{#" opens a
    # handlebars section instead of a comment
      (?<!\{)\{\#(?:(?!\#\}|\{\#)[\s\S])*?\#\}
    # any template tag, read as its keyword and, where it names something,
    # the first token after the keyword. Neither may cross a "{%", so an
    # unclosed tag costs the scan the few characters up to the next tag
    # rather than a walk to the end of the file
    | \{%[-+]?\s*(?P<tag>\w+)
      (?:\s+(?P<name>[\w.\-]+?)(?=\s|[-+]?%\}))?
      (?:(?!%\}|\{%)[\s\S])*?[-+]?%\}
    """,
    re.X,
    cache_pattern=False,
)
_LITERAL_BLOCKS: Final = {
    "comment": "endcomment",
    "raw": "endraw",
    "verbatim": "endverbatim",
}
_SCOPE_OPENING: Final = "embed"
_SCOPE_CLOSING: Final = "endembed"
_BLOCK_OPENING: Final = "block"


def _closed_scope(
    scope: int, enclosing: dict[int, int], closed_scopes: set[int]
) -> int:
    """The innermost scope around a tag that an `{% endembed %}` closed."""
    while scope not in closed_scopes:
        scope = enclosing[scope]
    return scope


def _block_occurrences(html: str) -> list[tuple[re.Match[str], str, int]]:
    """Every block tag the engine parses, with the scope holding it.

    The document is walked once, so a tag written inside a construct the
    engine keeps whole is stepped over instead of being matched: the body
    of a `{% comment %}`, `{% raw %}` or `{% verbatim %}` block runs to its
    closing tag, whatever that tag names, since Django lets the closing
    tag of a named `{% verbatim myblock %}` carry the name back. A body
    left open runs to the end of the file, as it does for the engine.

    Only an `{% embed %}` that is closed opens a scope. Wagtail spells a
    one line oEmbed `{% embed url %}`, with no closing tag and no body to
    scope, so an opening left unclosed hands its blocks back to the scope
    around it rather than taking the rest of the file with it.
    """
    occurrences: list[tuple[re.Match[str], str, int]] = []
    literal_closing: str | None = None
    enclosing: dict[int, int] = {}
    closed_scopes = {0}
    scopes = [0]
    scopes_opened = 0

    for match in _TOKEN_PATTERN.finditer(html):
        # a template comment matches with no keyword, and stepping over it
        # is all this rule wants from it
        tag = match.group("tag")

        if literal_closing is not None:
            if tag == literal_closing:
                literal_closing = None
        elif tag in _LITERAL_BLOCKS:
            literal_closing = _LITERAL_BLOCKS[tag]
        elif tag == _SCOPE_OPENING:
            scopes_opened += 1
            enclosing[scopes_opened] = scopes[-1]
            scopes.append(scopes_opened)
        elif tag == _SCOPE_CLOSING:
            if len(scopes) > 1:
                closed_scopes.add(scopes.pop())
        elif tag == _BLOCK_OPENING and (name := match.group("name")):
            occurrences.append((match, name, scopes[-1]))

    return [
        (match, name, _closed_scope(scope, enclosing, closed_scopes))
        for match, name, scope in occurrences
    ]


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for a block name used more than once.

    Names are compared as written, since the engines treat `Content` and
    `content` as two blocks. Only the keyword `block` opens one, so
    `{% blocktrans %}` is another tag entirely and an `{% endblock name %}`
    only names the block it closes.

    A tag a `djlint:off` region covers is not an occurrence either, so
    silencing the rule over one block does not move the report onto the
    next tag carrying that name.
    """
    errors: list[LintError] = []
    seen: set[tuple[int, str]] = set()

    for match, name, scope in _block_occurrences(html):
        if inside_ignored_rule(config, html, match, rule["name"]):
            continue

        if (scope, name) not in seen:
            seen.add((scope, name))
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })

    return tuple(errors)
