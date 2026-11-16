"""Rule D058: Check for a Django tag or comment that spans lines.

Django reads a tag only within one line, so a `{{ }}` broken over two, an
`{% include %}` whose arguments go on to the next line and a `{# #}`
comment written over several lines are text it prints as written, and an
`{% if %}` split that way leaves its `{% endif %}` an invalid block tag.
Jinja and Nunjucks read all of them, which is where the habit comes from.

An opener with no closing on its line is reported when its closing comes
on a later one. A `{%` or `{{` that another opener follows first was never
closed, which T039 reports. A comment runs to its `#}` whatever it holds,
since a comment is what tags are commented out with.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.helpers import (
    DJANGO_OPENER_PATTERN,
    Span,
    inside_ignored_linter_block,
    inside_ignored_rule,
    read_django_template,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Any

    from djlint.settings import Config
    from djlint.types import LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for a tag or comment that Django reads as text across lines.

    The tag is reported from its opener to past its closing, once: an
    opener inside it is part of the text it makes.
    """
    errors: list[LintError] = []
    reported_to = 0
    for start, closing in read_django_template(html).stray_openers:
        if start < reported_to or closing < 0:
            continue
        if html[start + 1] != "#" and DJANGO_OPENER_PATTERN.search(html, start + 2, closing):
            continue

        tag = Span(start, closing + 2)
        reported_to = tag.end
        if inside_ignored_rule(config, html, tag, rule["name"]) or inside_ignored_linter_block(
            config, html, tag
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(tag.start, line_ends),
            "end": get_line(tag.end, line_ends),
            "match": html[tag.start : tag.end].strip()[:20],
            "message": rule["message"],
        })
    return tuple(errors)
