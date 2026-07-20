"""Rule T038: Check that template block tags have matching end tags."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IX,
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


ORPHAN_END_MESSAGE: Final = "End tag has no matching block tag."
MISMATCH_MESSAGE: Final = "Endblock name should match opening block name."

_TEMPLATE_TAG_PATTERN: Final = re.compile(
    r"\{%(?:(?!%\}).)*%\}|\{\{[#^/](?:(?!\}\}).)*\}\}",
    re.S,
    cache_pattern=False,
)
# {% name %}, {{#name}}, {{^name}} (inverted section), {{#> name}}
# (handlebars partial block), {{#*name}} (handlebars decorator)
_OPEN_NAME_PATTERN: Final = re.compile(
    r"(?:\{%-?|\{\{[#^][*>]?)\s*([\w.-]+)", cache_pattern=False
)
_END_NAME_PATTERN: Final = re.compile(
    r"\{%-?\s*end([\w.-]*)|\{\{/\s*([\w.-]+)", cache_pattern=False
)
# the label naming a {% block %} or {% endblock %}
_BLOCK_LABEL_PATTERN: Final = re.compile(
    r"\{%-?\s*(?:end)?block\s+([^\s%-][^\s%]*)", cache_pattern=False
)


def _ignored(
    rule: dict[str, Any], config: Config, html: str, match: re.Match[str]
) -> bool:
    return (
        overlaps_ignored_block(config, html, match)
        or inside_ignored_rule(config, html, match, rule["name"])
        or inside_ignored_linter_block(config, html, match)
    )


def _error(
    rule: dict[str, Any],
    match: re.Match[str],
    line_ends: list[dict[str, int]],
    message: str,
) -> LintError:
    return {
        "code": rule["name"],
        "line": get_line(match.start(), line_ends),
        "match": match.group().strip()[:20],
        "message": message,
    }


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that template block tags have matching end tags."""
    errors: list[LintError] = []
    open_tags: list[tuple[str, re.Match[str]]] = []

    for match in _TEMPLATE_TAG_PATTERN.finditer(html):
        tag = match.group()

        if re.match(config.template_unindent, tag, RE_FLAGS_IX):
            end_name = _END_NAME_PATTERN.match(tag)
            if end_name is None:
                continue
            if _ignored(rule, config, html, match):
                continue
            name = end_name.group(1) or end_name.group(2)
            if not name:
                # a bare {% end %} closes the innermost open block
                if open_tags:
                    open_tags.pop()
                else:
                    errors.append(
                        _error(rule, match, line_ends, ORPHAN_END_MESSAGE)
                    )
                continue
            for index in range(len(open_tags) - 1, -1, -1):
                if open_tags[index][0] == name:
                    # block tags opened inside it were never closed
                    errors.extend(
                        _error(rule, open_match, line_ends, rule["message"])
                        for _, open_match in open_tags[index + 1 :]
                    )
                    open_match = open_tags[index][1]
                    del open_tags[index:]
                    if name == "block":
                        # {% endblock foo %} must name its own block
                        close_label = _BLOCK_LABEL_PATTERN.match(tag)
                        open_label = _BLOCK_LABEL_PATTERN.match(
                            open_match.group()
                        )
                        if (
                            close_label
                            and open_label
                            and close_label.group(1) != open_label.group(1)
                        ):
                            errors.append(
                                _error(rule, match, line_ends, MISMATCH_MESSAGE)
                            )
                    break
            else:
                errors.append(
                    _error(rule, match, line_ends, ORPHAN_END_MESSAGE)
                )

        elif re.match(
            config.template_indent, tag, RE_FLAGS_IX
        ) or tag.startswith(("{{#", "{{^")):
            open_name = _OPEN_NAME_PATTERN.match(tag)
            if open_name is None or _ignored(rule, config, html, match):
                continue
            open_tags.append((open_name.group(1), match))

    errors.extend(
        _error(rule, open_match, line_ends, rule["message"])
        for _, open_match in open_tags
    )
    return tuple(errors)
