"""Direct unit tests for the branch-span helpers in ``djlint.helpers``.

``branched_blocks``, ``branch_context`` and ``mutually_exclusive`` back the
indentation of every conditional and loop block across the template dialects
djLint supports (Jinja/Django, Handlebars, Go, Liquid, Nunjucks, ...). They are
pure functions -- they take only the markup string (or the structures derived
from it) and no ``Config`` -- yet they were only exercised indirectly through
the linter rules, so a regression in the span math would surface only as a
silent formatting change. These tests pin the documented behavior.

uv run pytest tests/test_branch_spans.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint import helpers

if TYPE_CHECKING:
    from collections.abc import Iterable


# (markup, expected spans) -- spans are the half-open [start, end) ranges of
# each branch body, grouped per complete block. Verified against the current
# implementation for every dialect djLint claims to support.
_BRANCH_CASES: tuple[tuple[str, tuple[tuple[tuple[int, int], ...], ...]], ...] = (
    ("{% if a %}x{% else %}y{% endif %}", (((5, 11), (18, 22)),)),
    (
        "{% if a %}x{% elif b %}y{% else %}z{% endif %}",
        (((5, 11), (18, 24), (31, 35)),),
    ),
    (
        "{% if a %}{% for i in x %}p{% else %}q{% endfor %}{% else %}r{% endif %}",
        (((16, 27), (34, 38)), ((5, 50), (57, 61))),
    ),
    ("{{#if a}}x{{else}}y{{/if}}", (((5, 10), (16, 19)),)),
    ("{{if a}}x{{else}}y{{end}}", (((4, 9), (15, 18)),)),
    ("{{#if a}}x{{else}}y{{/if}}", (((5, 10), (16, 19)),)),
    ("{% if a %}x{% else %}y{% endif %}", (((5, 11), (18, 22)),)),
    # An unclosed block yields no *complete* block.
    ("{% if a %}x", ()),
    # Markup with no control flow yields no blocks at all.
    ("<div>plain</div>", ()),
)


@pytest.mark.parametrize(("markup", "expected"), _BRANCH_CASES)
def test_branched_blocks_finds_branch_spans(
    markup: str, expected: tuple[tuple[tuple[int, int], ...], ...]
) -> None:
    assert helpers.branched_blocks(markup) == expected


def test_branched_blocks_spans_are_sorted_and_disjoint() -> None:
    """Within a block the branch bodies never overlap and read left to right."""
    for markup, blocks in _BRANCH_CASES:
        if not blocks:
            continue
        for block in blocks:
            for (start, end), (next_start, _next_end) in zip(block, block[1:]):
                assert start < end, f"{markup!r}: empty branch span"
                assert end <= next_start, f"{markup!r}: overlapping branches"


# (markup, position, expected context) -- the context maps each enclosing block
# index to the index of the branch the position falls into.
_CONTEXT_CASES: tuple[tuple[str, int, dict[int, int]], ...] = (
    ("{% if a %}x{% else %}y{% endif %}", 8, {0: 0}),
    ("{% if a %}x{% else %}y{% endif %}", 20, {0: 1}),
    ("{% if a %}x{% elif b %}y{% else %}z{% endif %}", 8, {0: 0}),
    ("{% if a %}x{% elif b %}y{% else %}z{% endif %}", 21, {0: 1}),
    ("{% if a %}x{% elif b %}y{% else %}z{% endif %}", 33, {0: 2}),
    (
        "{% if a %}{% for i in x %}p{% else %}q{% endfor %}{% else %}r{% endif %}",
        21,
        {0: 0, 1: 0},
    ),
    (
        "{% if a %}{% for i in x %}p{% else %}q{% endfor %}{% else %}r{% endif %}",
        36,
        {0: 1, 1: 0},
    ),
    (
        "{% if a %}{% for i in x %}p{% else %}q{% endfor %}{% else %}r{% endif %}",
        59,
        {1: 1},
    ),
)


@pytest.mark.parametrize(("markup", "position", "expected"), _CONTEXT_CASES)
def test_branch_context_maps_interior_positions(
    markup: str, position: int, expected: dict[int, int]
) -> None:
    blocks = helpers.branched_blocks(markup)
    assert helpers.branch_context(blocks, position) == expected


def test_branch_context_is_empty_outside_any_block() -> None:
    """A position before the first tag (or at a half-open boundary) is in no branch."""
    markup = "{% if a %}x{% else %}y{% endif %}"
    blocks = helpers.branched_blocks(markup)
    # Position 0 is before the opening tag.
    assert helpers.branch_context(blocks, 0) == {}
    # The branch body spans are half open, so the closing tag index is outside.
    assert helpers.branch_context(blocks, 11) == {}
    assert helpers.branch_context(blocks, 22) == {}


def test_branch_context_of_plain_markup_is_empty() -> None:
    assert helpers.branch_context(helpers.branched_blocks("<div>x</div>"), 3) == {}


def _contexts(positions: Iterable[int], markup: str) -> list[dict[int, int]]:
    blocks = helpers.branched_blocks(markup)
    return [helpers.branch_context(blocks, pos) for pos in positions]


def test_mutually_exclusive_sibling_branches() -> None:
    """Two positions in different branches of the same block are exclusive."""
    markup = "{% if a %}x{% else %}y{% endif %}"
    cx, cy = _contexts((8, 20), markup)
    assert helpers.mutually_exclusive(cx, cy) is True


def test_mutually_exclusive_same_branch_is_not() -> None:
    """Two positions in the same branch are not mutually exclusive."""
    markup = "{% if a %}x{% else %}y{% endif %}"
    cx, cx2 = _contexts((7, 9), markup)
    assert helpers.mutually_exclusive(cx, cx2) is False


def test_mutually_exclusive_across_nested_blocks() -> None:
    """A position inside an inner block and one in the outer else are exclusive.

    ``p`` sits in both the inner ``for`` (branch 0) and the outer ``if``
    (branch 0); ``r`` sits only in the outer ``if`` (branch 1). They share the
    outer block and land in different branches, so they are exclusive.
    """
    markup = "{% if a %}{% for i in x %}p{% else %}q{% endfor %}{% else %}r{% endif %}"
    cp, cr = _contexts((21, 59), markup)
    assert helpers.mutually_exclusive(cp, cr) is True
