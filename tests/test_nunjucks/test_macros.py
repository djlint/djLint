"""Test nunjucks macro tag.

poetry run pytest tests/test_nunjucks/test_macros.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% macro 'cool' %}<div>some html</div>{% endmacro %}"),
        ("{% macro 'cool' %}\n" "    <div>some html</div>\n" "{% endmacro %}\n"),
        id="macro_tag",
    ),
    pytest.param(
        (
            "<ul>\n"
            "  {# djlint:off #}\n"
            "  <li>{{foo(1)}}</li>\n"
            "  {# djlint:on #}\n"
            "</ul>"
        ),
        (
            "<ul>\n"
            "    {# djlint:off #}\n"
            "  <li>{{foo(1)}}</li>\n"
            "    {# djlint:on #}\n"
            "</ul>\n"
        ),
        id="ignored code should not be touched",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, nunjucks_config):
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
