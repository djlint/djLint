"""Test jinja call tag.

poetry run pytest tests/test_jinja/test_call.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% call 'cool' %}<div>some html</div>{% endcall %}"),
        ("{% call 'cool' %}\n" "    <div>some html</div>\n" "{% endcall %}\n"),
        id="call_tag",
    ),
    pytest.param(
        ("{% call('cool') %}<div>some html</div>{% endcall %}"),
        ("{% call('cool') %}\n" "    <div>some html</div>\n" "{% endcall %}\n"),
        id="call_tag_with_function",
    ),
    pytest.param(
        ("{% call (a, b) render_form(form, '<hr>'>) %}"),
        ("{% call (a, b) render_form(form, '<hr>'>) %}\n"),
        id="call_tag_with_nested_html",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, jinja_config):
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
