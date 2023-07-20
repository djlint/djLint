"""Test nunjucks filters.

poetry run pytest tests/test_nunjucks/test_filters.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        (
            "{% set absoluteUrl %}{{ page.url | htmlBaseUrl(metadata.url) }}{% endset %}\n"
        ),
        (
            "{% set absoluteUrl %}\n"
            "    {{ page.url | htmlBaseUrl(metadata.url) }}\n"
            "{% endset %}\n"
        ),
        ({}),
        id="one",
    ),
    pytest.param(
        (
            "{{ post.templateContent | transformWithHtmlBase(absolutePostUrl, post.url) | dump | safe }}"
        ),
        (
            "{{ post.templateContent | transformWithHtmlBase(absolutePostUrl, post.url) | dump | safe }}\n"
        ),
        ({}),
        id="two",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args, nunjucks_config):
    args["profile"] = "nunjucks"
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
