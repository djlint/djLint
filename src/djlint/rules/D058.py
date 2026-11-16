"""Rule D058: Check for a Django tag or comment that spans lines.

Django reads a tag only within one line, so a `{{ }}` broken over two, an
`{% include %}` whose arguments go on to the next line and a `{# #}`
comment written over several lines are text it prints as written, and an
`{% if %}` split that way leaves its `{% endif %}` an invalid block tag.
Jinja and Nunjucks read all of them, which is where the habit comes from.

An opener with no closing on its line is reported when its closing comes
on a later one. A `{%` or `{{` is read as T039 reads it, so a delimiter in
a quoted string neither closes it nor opens another, and what T039 reports
as unclosed, T034 as a `}%` typo or T027 as an unterminated string is left
to them. A comment runs to its first `#}` whatever it holds, since a
comment is what tags are commented out with.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.helpers import (
    Span,
    inside_ignored_linter_block,
    inside_ignored_rule,
    read_django_template,
)
from djlint.lint import get_line
from djlint.rules.T039 import scan_tag

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
        if start < reported_to:
            continue
        kind = html[start + 1]
        if kind == "#":
            end = closing + 2 if closing >= 0 else -1
        else:
            end = scan_tag(html, start + 2, "%}" if kind == "%" else "}}").end
        if end < 0:
            continue

        tag = Span(start, end)
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
