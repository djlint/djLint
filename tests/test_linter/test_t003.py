"""Test endblock naming style (opt-in rule).

uv run pytest tests/test_linter/test_t003.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from djlint.settings import Config
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.types import LintError

test_data = [
    pytest.param(
        ("{% endblock %}"),
        ([
            {
                "code": "T003",
                "line": "1:0",
                "match": "{% endblock %}",
                "message": "Endblock should have name. Ex: {% endblock body %}.",
            },
            # pairing correctness lives in T038
            {
                "code": "T038",
                "line": "1:0",
                "match": "{% endblock %}",
                "message": "End tag has no matching block tag.",
            },
        ]),
        id="orphan_endblock",
    ),
    pytest.param(
        ("{% block foo %}\n{% endblock bar %}"),
        ([
            {
                "code": "T038",
                "line": "2:0",
                "match": "{% endblock bar %}",
                "message": "Endblock name should match opening block name.",
            }
        ]),
        id="mismatched_block_name_is_T038s_job",
    ),
    pytest.param(
        ("{% block foo %}\n{% endblock foo %}"), ([]), id="matching_block_name"
    ),
    pytest.param(
        ("{% block foo %}{% endblock %}"), ([]), id="single_line_block"
    ),
    pytest.param(
        ("{% block foo %}\n{% endblock %}"),
        ([
            {
                "code": "T003",
                "line": "2:0",
                "match": "{% endblock %}",
                "message": "Endblock should have name. Ex: {% endblock body %}.",
            }
        ]),
        id="multi_line_block_without_name",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: list[LintError]) -> None:
    config = Config("dummy/source.html", profile="django", include="T003")
    filename = "test.html"
    output = linter(config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
