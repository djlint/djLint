"""Sort the names a `{% load %}` tag loads."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.helpers import (
    compile_pattern,
    inside_ignored_block,
    inside_ignored_linter_block,
)

if TYPE_CHECKING:
    from typing import Final

    import regex as re

    from djlint.settings import Config


# The names stop at a brace or a percent sign, so a tag left unclosed is
# read only up to the next one rather than to the end of the file.
_LOAD_TAG_PATTERN: Final = compile_pattern(
    r"{%[-+]?\s*load\s+(?P<names>[^{}%]+?)\s*[-+]?%}"
)


def _sorted_names(names: list[str]) -> list[str]:
    """The names in order, each once, or as written for a broken tag.

    `{% load a b from lib %}` loads tags out of one library, so only the
    names before `from` move. A tag with `from` anywhere else is not one
    django reads that way, and it is left as written.
    """
    if "from" not in names:
        return sorted(set(names))
    loaded = names[:-2]
    if loaded and names[-2] == "from":
        return [*sorted(set(loaded)), *names[-2:]]
    return names


def sort_load_tags(html: str, config: Config) -> str:
    """Sort the libraries in `{% load %}` and drop the repeated ones.

    A tag already in order is left as written, so only a tag that changes
    has its names joined by single spaces. One in a comment, `{% verbatim %}`
    or the like is text rather than a tag, and is not touched.
    """
    if not config.sort_load_tags or "load" not in html:
        return html

    def replace(match: re.Match[str]) -> str:
        names = match.group("names").split()
        ordered = _sorted_names(names)
        if (
            ordered == names
            or inside_ignored_block(config, html, match)
            or inside_ignored_linter_block(config, html, match)
        ):
            return match.group()

        start, end = match.span("names")
        return (
            html[match.start() : start]
            + " ".join(ordered)
            + html[end : match.end()]
        )

    return _LOAD_TAG_PATTERN.sub(replace, html)
