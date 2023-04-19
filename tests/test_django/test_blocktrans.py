"""Test django blocktrans(late) tag.

poetry run pytest tests/test_django/test_blocktrans.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% blocktranslate %}The width is: {{ width }}{% endblocktranslate %}"),
        ("{% blocktranslate %}The width is: {{ width }}{% endblocktranslate %}\n"),
        id="blocktranslate_no_attr",
    ),
    pytest.param(
        (
            "{% blocktranslate trimmed %}The width is: {{ width }}{% endblocktranslate %}"
        ),
        (
            "{% blocktranslate trimmed %}The width is: {{ width }}{% endblocktranslate %}\n"
        ),
        id="blocktranslate_with_attr",
    ),
    pytest.param(
        ("{% blocktrans %}The width is: {{ width }}{% endblocktrans %}"),
        ("{% blocktrans %}The width is: {{ width }}{% endblocktrans %}\n"),
        id="blocktrans_no_attr",
    ),
    pytest.param(
        ("{% blocktrans trimmed %}The width is: {{ width }}{% endblocktrans %}"),
        ("{% blocktrans trimmed %}The width is: {{ width }}{% endblocktrans %}\n"),
        id="blocktrans_with_attr",
    ),
    pytest.param(
        (
            "<p>\n"
            "    {% blocktrans %}If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}\n'
            "</p>\n"
        ),
        (
            "<p>\n"
            "    {% blocktrans %}If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}\n'
            "</p>\n"
        ),
        id="blocktrans_with_nested_tags",
    ),
    pytest.param(
        (
            "<div>\n"
            '     {% translate "View all" %}\n'
            "    <br />\n"
            "     ({% blocktranslate count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "{% endblocktranslate %})\n"
            "     ({% blocktrans count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "{% endblocktrans %})\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "    ({% blocktranslate count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "    {% endblocktranslate %})\n"
            "    ({% blocktrans count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "    {% endblocktrans %})\n"
            "</div>\n"
        ),
        id="blocktrans_indent",
    ),
    pytest.param(
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "    ({% blocktranslate count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "    {% endblocktranslate %})\n"
            "    ({% blocktrans count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "    {% endblocktrans %})\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "    ({% blocktranslate count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "    {% endblocktranslate %})\n"
            "    ({% blocktrans count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "    {% endblocktrans %})\n"
            "</div>\n"
        ),
        id="blocktrans_indent_2",
    ),
    pytest.param(
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned{% endblocktranslate %}\n"
            "          {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned {% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned {% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        id="blocktrans_indent_if",
    ),
    pytest.param(
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned {% endblocktranslate %}\n"
            "          {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned {% endblocktranslate %}\n"
            "    {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        id="blocktrans_indent_if_2",
    ),
    pytest.param(
        ("<p>{% trans 'Please do <b>Blah</b>.' %}</p>\n"),
        ("<p>\n" "    {% trans 'Please do <b>Blah</b>.' %}\n" "</p>\n"),
        id="blocktrans_indent_3",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
