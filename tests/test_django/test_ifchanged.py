"""Test django ifchanged tag.

poetry run pytest tests/test_django/test_ifchanged.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '{% for match in matches %}<div style="background-color:"pink">{% ifchanged match.ballot_id %}{% cycle "red" "blue" %}{% else %}gray{% endifchanged %}{{ match }}</div>{% endfor %}'
        ),
        (
            "{% for match in matches %}\n"
            '    <div style="background-color:"pink">\n'
            "        {% ifchanged match.ballot_id %}\n"
            '            {% cycle "red" "blue" %}\n'
            "        {% else %}\n"
            "            gray\n"
            "        {% endifchanged %}\n"
            "        {{ match }}\n"
            "    </div>\n"
            "{% endfor %}\n"
        ),
        id="ifchanged_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
