"""Test twig comment tags.

poetry run pytest tests/test_twig/test_comments.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% if %}\n" "    {#\n" "        line\n" "    #}\n" "{% endif %}"),
        ("{% if %}\n" "    {#\n" "        line\n" "    #}\n" "{% endif %}\n"),
        id="comments",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {#\n"
            "    multi\n"
            "    line\n"
            "    comment\n"
            "    #}\n"
            "</div>\n"
            "<div>\n"
            "    <p></p>\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            "    {#\n"
            "    multi\n"
            "    line\n"
            "    comment\n"
            "    #}\n"
            "</div>\n"
            "<div>\n"
            "    <p></p>\n"
            "</div>\n"
        ),
        id="comments",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, nunjucks_config):
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
