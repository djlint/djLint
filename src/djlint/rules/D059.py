"""Rule D059: Check for consecutive lines of Django {# #} comments.

A `{# #}` comment ends on its line, so a longer note is often written one
`{# #}` per line, where Django's `{% comment %}` block holds it in one.

A line counts when the comment is all it holds. A `djlint:` directive works
only as a comment of its own, and makemessages hands translators every line
of a `{% comment %}` block from the one starting with "Translators" on, so
neither joins a run. Inside `<pre>` and `<textarea>` the line breaks the
comments leave behind show on the page, and a block would leave fewer, so
comments there are left alone.
"""

from __future__ import annotations

from bisect import bisect_right
from typing import TYPE_CHECKING

from djlint.helpers import (
    Span,
    compile_pattern,
    inside_ignored_linter_block,
    inside_ignored_rule,
    read_django_template,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Final

    from djlint.formatter.tokenizer import TagToken
    from djlint.helpers import DjangoTemplate
    from djlint.settings import Config
    from djlint.types import LintError


_PREFORMATTED: Final = frozenset(("pre", "textarea"))
_NON_NEWLINE_PATTERN: Final = compile_pattern(r"[^\n]")


def _preformatted_bodies(
    html: str, comment_blocks: tuple[Span, ...]
) -> tuple[tuple[int, int], ...]:
    """The bodies of `<pre>` and `<textarea>`, in order.

    Neither nests, so an opening is closed by the next closing tag of its
    name, or by the end of the document as a browser reads it. Django drops
    a `{% comment %}` block before any browser sees it, so the tags in one
    are blanked first, keeping every offset.
    """
    pieces: list[str] = []
    previous = 0
    for block in comment_blocks:
        pieces.extend((
            html[previous : block.start],
            _NON_NEWLINE_PATTERN.sub(" ", html[block.start : block.end]),
        ))
        previous = block.end
    pieces.append(html[previous:])
    bodies: list[tuple[int, int]] = []
    opening: TagToken | None = None
    for tag in tokenize_markup("".join(pieces)):
        name = tag.name.lower()
        if name not in _PREFORMATTED:
            continue
        if opening is None:
            if not tag.closing:
                opening = tag
        elif tag.closing and name == opening.name.lower():
            bodies.append((opening.end, tag.start))
            opening = None
    if opening is not None:
        bodies.append((opening.end, len(html)))
    return tuple(bodies)


def _joins_a_block(html: str, comment: Span, bodies: tuple[tuple[int, int], ...]) -> bool:
    """Whether the comment is all its line holds and could go in a block."""
    line_start = html.rfind("\n", 0, comment.start) + 1
    line_end = html.find("\n", comment.end)
    if line_end < 0:
        line_end = len(html)
    if html[line_start : comment.start].strip() or html[comment.end : line_end].strip():
        return False

    contents = html[comment.start + 2 : comment.end - 2].strip()
    if contents.lower().startswith("djlint:") or contents.startswith("Translators"):
        return False

    index = bisect_right(bodies, (comment.start, len(html))) - 1
    return index < 0 or not bodies[index][0] <= comment.start < bodies[index][1]


def _runs(html: str, template: DjangoTemplate) -> Iterator[Span]:
    """Each run of two or more comment lines in a row, as one span."""
    bodies = _preformatted_bodies(html, template.comment_blocks)
    lines: list[Span] = []
    for comment in template.comments:
        if not _joins_a_block(html, comment, bodies):
            if len(lines) > 1:
                yield Span(lines[0].start, lines[-1].end)
            lines = []
            continue
        if lines:
            gap = html[lines[-1].end : comment.start]
            if gap.count("\n") != 1 or gap.strip():
                if len(lines) > 1:
                    yield Span(lines[0].start, lines[-1].end)
                lines = []
        lines.append(comment)
    if len(lines) > 1:
        yield Span(lines[0].start, lines[-1].end)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for consecutive lines that each hold one `{# #}` comment."""
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(lines.start, line_ends),
            "end": get_line(lines.end, line_ends),
            "match": html[lines.start : lines.end].strip()[:20],
            "message": rule["message"],
        }
        for lines in _runs(html, read_django_template(html))
        if not inside_ignored_rule(config, html, lines, rule["name"])
        and not inside_ignored_linter_block(config, html, lines)
    )
