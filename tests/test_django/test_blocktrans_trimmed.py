"""Test django blocktrans(late) tag.

poetry run pytest tests/test_django/test_blocktrans_trimmed.py

blocktrans/late contents cannot be touched.

leading tag can be indented, but not trailing tag.

---

blocktrans/late "trimmed" can be fully formatted.

"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        (
            "{% blocktranslate trimmed %} The width is: {{ width }}{% endblocktranslate %}"
        ),
        (
            "{% blocktranslate trimmed %}\n"
            "    The width is: {{ width }}\n"
            "{% endblocktranslate %}\n"
        ),
        ({"max_line_length": 10}),
        id="blocktranslate_no_attr",
    ),
    pytest.param(
        (
            "{% blocktranslate trimmed %}The width is: {{ width }} {% endblocktranslate %}"
        ),
        (
            "{% blocktranslate trimmed %}\n"
            "    The width is: {{ width }}\n"
            "{% endblocktranslate %}\n"
        ),
        ({"max_line_length": 10}),
        id="blocktranslate_with_attr",
    ),
    pytest.param(
        ("{% blocktrans trimmed %} The width is: {{ width }}{% endblocktrans %}"),
        (
            "{% blocktrans trimmed %}\n"
            "    The width is: {{ width }}\n"
            "{% endblocktrans %}\n"
        ),
        ({"max_line_length": 10}),
        id="blocktrans_no_attr",
    ),
    pytest.param(
        (
            "{% blocktranslate trimmed %}The width is: {{ width }} {% endblocktranslate %}"
        ),
        (
            "{% blocktranslate trimmed %}\n"
            "    The width is: {{ width }}\n"
            "{% endblocktranslate %}\n"
        ),
        ({"max_line_length": 10}),
        id="blocktranslage",
    ),
    pytest.param(
        (
            "<p>\n"
            "    {% blocktrans trimmed%}If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}\n'
            "</p>\n"
            "<p>\n"
            "    {% blocktrans trimmed%}   If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.   {% endblocktrans %}\n'
            "</p>\n"
        ),
        (
            "<p>\n"
            "    {% blocktrans trimmed %}\n"
            "        If you have not created an account yet, then please\n"
            '        <a href="{{ signup_url }}">sign up</a> first.\n'
            "    {% endblocktrans %}\n"
            "</p>\n"
            "<p>\n"
            "    {% blocktrans trimmed %}\n"
            "        If you have not created an account yet, then please\n"
            '        <a href="{{ signup_url }}">sign up</a> first.\n'
            "    {% endblocktrans %}\n"
            "</p>\n"
        ),
        ({"max_line_length": 10}),
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
            " {% endblocktrans %})\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "    (\n"
            "    {% blocktranslate count counter=images|length trimmed %}\n"
            "        {{ counter }} photo\n"
            "    {% plural %}\n"
            "        {{ counter }} photos\n"
            "    {% endblocktranslate %}\n"
            "    )\n"
            "    (\n"
            "    {% blocktrans count counter=images|length trimmed %}\n"
            "        {{ counter }} photo\n"
            "    {% plural %}\n"
            "        {{ counter }} photos\n"
            "    {% endblocktrans %}\n"
            "    )\n"
            "</div>\n"
        ),
        ({"max_line_length": 10}),
        id="blocktrans_indent",
    ),
    pytest.param(
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "   ({% blocktranslate count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "asdf\n"
            "            {{ counter }} photos\n"
            "     {% endblocktranslate %})\n"
            "     ({% blocktrans count counter=images|length trimmed %}\n"
            "            {{ counter }} photo\n"
            "           {% plural %}\n"
            "            {{ counter }} photos\n"
            "     {% endblocktrans %})\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "    (\n"
            "    {% blocktranslate count counter=images|length trimmed %}\n"
            "        {{ counter }} photo\n"
            "    {% plural %}\n"
            "        asdf\n"
            "        {{ counter }} photos\n"
            "    {% endblocktranslate %}\n"
            "    )\n"
            "    (\n"
            "    {% blocktrans count counter=images|length trimmed %}\n"
            "        {{ counter }} photo\n"
            "    {% plural %}\n"
            "        {{ counter }} photos\n"
            "    {% endblocktrans %}\n"
            "    )\n"
            "</div>\n"
        ),
        ({"max_line_length": 10}),
        id="blocktrans_indent_2",
    ),
    pytest.param(
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects trimmed%}{{ obj }} objects scanned{% endblocktranslate %}\n"
            "          {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}        {{ obj }} objects scanned {% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects trimmed %}\n"
            "            {{ obj }} objects scanned\n"
            "        {% endblocktranslate %}\n"
            "    {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}        {{ obj }} objects scanned {% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        ({"max_line_length": 10}),
        id="blocktrans_indent_if",
    ),
    pytest.param(
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate trimmed with obj=status.scanned_objects %}{{ obj }} objects scanned {% endblocktranslate %}\n"
            "          {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %} {{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate trimmed with obj=status.scanned_objects %}\n"
            "            {{ obj }} objects scanned\n"
            "        {% endblocktranslate %}\n"
            "    {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %} {{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        ({"max_line_length": 10}),
        id="blocktrans_indent_if_2",
    ),
    pytest.param(
        (
            "{% autoescape off %}\n"
            "\n"
            "  {% blocktrans trimmed %}\n"
            "  You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "  {% endblocktrans %}\n"
        ),
        (
            "{% autoescape off %}\n"
            "    {% blocktrans trimmed %}\n"
            "        You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "    {% endblocktrans %}\n"
        ),
        ({"max_line_length": 10}),
        id="blocktrans_autoescape",
    ),
    pytest.param(
        (
            "{% autoescape off %}\n"
            "    {% blocktrans trimmed %}\n"
            "  You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "      {% endblocktrans %}\n"
        ),
        (
            "{% autoescape off %}\n"
            "    {% blocktrans trimmed %}\n"
            "        You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "    {% endblocktrans %}\n"
        ),
        ({"max_line_length": 10}),
        id="blocktrans_autoescape_two",
    ),
    pytest.param(
        (
            "{% blocktranslate count counter=list|length trimmed  %}\n"
            "There is only one {{ name }} object.\n"
            "  {% plural %}   There are {{ counter }} {{ name }} objects.\n"
            "{% endblocktranslate %}\n"
        ),
        (
            "{% blocktranslate count counter=list|length trimmed %}\n"
            "    There is only one {{ name }} object.\n"
            "{% plural %}\n"
            "    There are {{ counter }} {{ name }} objects.\n"
            "{% endblocktranslate %}\n"
        ),
        ({}),
        id="plural formatted",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    args["profile"] = "django"
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
