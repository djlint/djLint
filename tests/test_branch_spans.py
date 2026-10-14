"""Test the branch spans the linter uses to pair tags across branches.

Rules H025, H044 and H053 ask whether two positions sit in sibling
branches of a conditional or loop block. Each case below marks branch
bodies with capital letters and checks which branch every letter falls in.

uv run pytest tests/test_branch_spans.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint import helpers

if TYPE_CHECKING:
    from typing import Final


def _context(markup: str, marker: str) -> dict[int, int]:
    return helpers.branch_context(
        helpers.branched_blocks(markup), markup.index(marker)
    )


# Blocks are numbered in the order they close, so an inner block comes
# before the one wrapping it.
_CONTEXTS: Final[tuple[tuple[str, dict[str, dict[int, int]]], ...]] = (
    (
        "{% if a %}A{% elif b %}B{% else %}C{% endif %}",
        {"A": {0: 0}, "B": {0: 1}, "C": {0: 2}},
    ),
    ("{% if a %}A{% elseif b %}B{% endif %}", {"A": {0: 0}, "B": {0: 1}}),
    ("{%- if a -%}A{%- else -%}B{%- endif -%}", {"A": {0: 0}, "B": {0: 1}}),
    ("{% for i in a %}A{% empty %}B{% endfor %}", {"A": {0: 0}, "B": {0: 1}}),
    (
        "{% if a %}{% for i in a %}A{% else %}B{% endfor %}{% else %}C{% endif %}",
        {"A": {0: 0, 1: 0}, "B": {0: 1, 1: 0}, "C": {1: 1}},
    ),
    (
        "{{#if a}}A{{else if b}}B{{else}}C{{/if}}",
        {"A": {0: 0}, "B": {0: 1}, "C": {0: 2}},
    ),
    ("{{#unless a}}A{{else}}B{{/unless}}", {"A": {0: 0}, "B": {0: 1}}),
    ("{{if a}}A{{else}}B{{end}}", {"A": {0: 0}, "B": {0: 1}}),
    ("{{- range .items }}A{{- else }}B{{- end }}", {"A": {0: 0}, "B": {0: 1}}),
    # An end with nothing open is dropped.
    ("{{ end }}{% if a %}A{% else %}B{% endif %}", {"A": {0: 0}, "B": {0: 1}}),
    # Outside of a complete block a position is in no branch.
    ("A{% if a %}B{% endif %}C", {"A": {}, "B": {0: 0}, "C": {}}),
    ("{% if a %}A", {"A": {}}),
    ("<div>A</div>", {"A": {}}),
)


@pytest.mark.parametrize(("markup", "expected"), _CONTEXTS)
def test_branch_context(
    markup: str, expected: dict[str, dict[int, int]]
) -> None:
    assert {marker: _context(markup, marker) for marker in expected} == expected


_NESTED: Final = (
    "{% if a %}{% if b %}A{% else %}B{% endif %}D{% else %}C{% endif %}E"
)


@pytest.mark.parametrize(
    ("markup", "first", "second", "expected"),
    [
        ("{% if a %}AB{% else %}C{% endif %}", "A", "B", False),
        ("{% if a %}AB{% else %}C{% endif %}", "A", "C", True),
        (_NESTED, "A", "B", True),
        (_NESTED, "A", "C", True),
        (_NESTED, "A", "D", False),
        (_NESTED, "D", "C", True),
        (_NESTED, "A", "E", False),
    ],
)
def test_mutually_exclusive(
    markup: str, first: str, second: str, expected: bool
) -> None:
    first_context = _context(markup, first)
    second_context = _context(markup, second)

    assert helpers.mutually_exclusive(first_context, second_context) is expected
    assert helpers.mutually_exclusive(second_context, first_context) is expected
