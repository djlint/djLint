"""Test django blocktrans(late) tag.

uv run pytest tests/test_django/test_blocktrans.py

blocktrans/late contents cannot be touched.

leading tag can be indented, but not trailing tag.

---

blocktrans/late "trimmed" can be fully formatted and are in separate tests

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        (
            "{% blocktranslate %} The width is: {{ width }}{% endblocktranslate %}"
        ),
        (
            "{% blocktranslate %} The width is: {{ width }}{% endblocktranslate %}\n"
        ),
        id="blocktranslate_no_attr",
    ),
    pytest.param(
        (
            "{% blocktranslate  %}The width is: {{ width }} {% endblocktranslate %}"
        ),
        (
            "{% blocktranslate  %}The width is: {{ width }} {% endblocktranslate %}\n"
        ),
        id="blocktranslate_with_attr",
    ),
    pytest.param(
        ("{% blocktrans %} The width is: {{ width }}{% endblocktrans %}"),
        ("{% blocktrans %} The width is: {{ width }}{% endblocktrans %}\n"),
        id="blocktrans_no_attr",
    ),
    pytest.param(
        ("{% blocktrans  %}The width is: {{ width }} {% endblocktrans %}"),
        ("{% blocktrans  %}The width is: {{ width }} {% endblocktrans %}\n"),
        id="blocktrans_with_attr",
    ),
    pytest.param(
        (
            "<p>\n"
            "    {% blocktrans %}If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}\n'
            "</p>\n"
            "<p>\n"
            "    {% blocktrans %}   If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.   {% endblocktrans %}\n'
            "</p>\n"
        ),
        (
            "<p>\n"
            "    {% blocktrans %}If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}\n'
            "</p>\n"
            "<p>\n"
            "    {% blocktrans %}   If you have not created an account yet, then please\n"
            '    <a href="{{ signup_url }}">sign up</a> first.   {% endblocktrans %}\n'
            "</p>\n"
        ),
        id="blocktrans_with_nested_tags",
    ),
    pytest.param(
        (
            "<div>\n"
            '     {% translate "View all" %}\n'
            "    <br />\n"
            "     ({% blocktranslate count counter=images|length  %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "{% endblocktranslate %})\n"
            "     ({% blocktrans count counter=images|length  %}\n"
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
            "    ({% blocktranslate count counter=images|length  %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            "{% endblocktranslate %})\n"
            "    ({% blocktrans count counter=images|length  %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "            {{ counter }} photos\n"
            " {% endblocktrans %})\n"
            "</div>\n"
        ),
        id="blocktrans_indent",
    ),
    pytest.param(
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "   ({% blocktranslate count counter=images|length  %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "asdf\n"
            "            {{ counter }} photos\n"
            "     {% endblocktranslate %})\n"
            "    ({% blocktrans count counter=images|length  %}\n"
            "            {{ counter }} photo\n"
            "           {% plural %}\n"
            "            {{ counter }} photos\n"
            "   {% endblocktrans %})\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    {% translate "View all" %}\n'
            "    <br />\n"
            "    ({% blocktranslate count counter=images|length  %}\n"
            "            {{ counter }} photo\n"
            "            {% plural %}\n"
            "asdf\n"
            "            {{ counter }} photos\n"
            "     {% endblocktranslate %})\n"
            "    ({% blocktrans count counter=images|length  %}\n"
            "            {{ counter }} photo\n"
            "           {% plural %}\n"
            "            {{ counter }} photos\n"
            "   {% endblocktrans %})\n"
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
            "        {% blocktranslate with obj=status.scanned_objects %}        {{ obj }} objects scanned {% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}        {{ obj }} objects scanned {% endblocktranslate %}\n"
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
            "        {% blocktranslate with obj=status.scanned_objects %} {{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        (
            "<tr>\n"
            "    {% if status.stage.value == 0 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %}{{ obj }} objects scanned {% endblocktranslate %}\n"
            "    {% elif status.stage.value == 2 %}\n"
            "        {% blocktranslate with obj=status.scanned_objects %} {{ obj }} objects scanned{% endblocktranslate %}\n"
            "    {% endif %}\n"
            "</tr>\n"
        ),
        id="blocktrans_indent_if_2",
    ),
    pytest.param(
        ("<p>{% trans 'Please do <b>Blah</b>.' %}</p>\n"),
        ("<p>\n    {% trans 'Please do <b>Blah</b>.' %}\n</p>\n"),
        id="blocktrans_indent_3",
    ),
    pytest.param(
        (
            "{% autoescape off %}\n"
            "\n"
            "  {% blocktrans %}\n"
            "  You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "  {% endblocktrans %}\n"
        ),
        (
            "{% autoescape off %}\n"
            "    {% blocktrans %}\n"
            "  You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "  {% endblocktrans %}\n"
        ),
        id="blocktrans_autoescape",
    ),
    pytest.param(
        (
            "{% autoescape off %}\n"
            "    {% blocktrans %}\n"
            "  You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "      {% endblocktrans %}\n"
        ),
        (
            "{% autoescape off %}\n"
            "    {% blocktrans %}\n"
            "  You're receiving this email because you requested a password reset for your user account at {{ site_name }}.\n"
            "      {% endblocktrans %}\n"
        ),
        id="blocktrans_autoescape_two",
    ),
    pytest.param(
        (
            "{% blocktranslate count counter=list|length  %}\n"
            "There is only one {{ name }} object.\n"
            "  {% plural %}   There are {{ counter }} {{ name }} objects.\n"
            "{% endblocktranslate %}\n"
        ),
        (
            "{% blocktranslate count counter=list|length  %}\n"
            "There is only one {{ name }} object.\n"
            "  {% plural %}   There are {{ counter }} {{ name }} objects.\n"
            "{% endblocktranslate %}\n"
        ),
        id="plural not formatted",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
