"""Test for max_attribute_length.

--max-attribute-length 4

uv run pytest tests/test_config/test_max_attribute_length.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            "<div required\n"
            "     long\n"
            "     attributenamesarereallycool\n"
            '     class="asdf"\n'
            '     data-attr="asdf"\n'
            '     id="asdf">\n'
            "</div>\n"
            '<div class="my long classes"\n'
            '     required="true"\n'
            '     checked="checked"\n'
            '     data-attr="some long junk"\n'
            '     style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem">\n'
        ),
        ({"max_attribute_length": 10, "max_line_length": 1}),
        id="short lines",
    ),
    pytest.param(
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            "<div required\n"
            "     long\n"
            "     attributenamesarereallycool\n"
            '     class="asdf"\n'
            '     data-attr="asdf"\n'
            '     id="asdf"></div>\n'
            '<div class="my long classes"\n'
            '     required="true"\n'
            '     checked="checked"\n'
            '     data-attr="some long junk"\n'
            '     style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem">\n'
        ),
        ({"max_attribute_length": 10, "max_line_length": 1000}),
        id="longer lines",
    ),
    pytest.param(
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf"></div>\n'
            '<div class="my long classes" required="true" checked="checked" data-attr="some long junk" style="margin-left: 90px; display: contents; font-weight: bold; font-size: 1.5rem">\n'
        ),
        ({"max_attribute_length": 10000, "max_line_length": 1000}),
        id="longest lines",
    ),
    pytest.param(
        ("<tag-looooong></tag-looooong>\n"),
        ("<tag-looooong>\n</tag-looooong>\n"),
        ({"max_attribute_length": 3, "custom_html": "[\\w\\-]+"}),
        id="long tag custom_html",
    ),
    pytest.param(
        (
            '<option data-json=\'{ "icon": "<img class=\\"ss\\">" }\' {% if True %}selected{% endif %}>'
        ),
        (
            '<option data-json=\'{ "icon": "<img class=\\"ss\\">" }\'\n'
            "        {% if True %}selected{% endif %}>\n"
        ),
        ({"max_attribute_length": 1}),
        id="with_html_tag_in_attribute_escaped_and_template_tag",
    ),
    pytest.param(
        (
            '<input :name="`x[${i}]`" placeholder="some long placeholder text to exceed the attribute length limit" />\n'
        ),
        (
            '<input :name="`x[${i}]`"\n'
            '       placeholder="some long placeholder text to exceed the attribute length limit" />\n'
        ),
        ({"profile": "jinja"}),
        id="quoted js template literal (issue 2266)",
    ),
    pytest.param(
        (
            "<div ${'class=\"a\"' if x else ''} data-foo=\"some very long attribute value that exceeds the maximum attribute length\">x</div>\n"
        ),
        (
            "<div ${'class=\"a\"' if x else ''} data-foo=\"some very long attribute value that exceeds the maximum attribute length\">x</div>\n"
        ),
        ({}),
        id="unquoted_mako_expression_untouched",
    ),
    pytest.param(
        (
            '<div data-x=< class="some long value that exceeds the attribute length limit">x</div>\n'
        ),
        (
            '<div data-x=< class="some long value that exceeds the attribute length limit">x</div>\n'
        ),
        ({"max_attribute_length": 20}),
        id='malformed attributes must not be silently corrupted: the stray "=<" cannot be parsed, so the tag is left untouched',
    ),
    pytest.param(
        (
            '<div ="some long value that exceeds the attribute length limit here">z</div>\n'
        ),
        (
            '<div ="some long value that exceeds the attribute length limit here">z</div>\n'
        ),
        ({"max_attribute_length": 20}),
        id='a nameless ="value" attribute must not become None="value"',
    ),
    pytest.param(
        (
            "<a href=https://example.com/some/long/path/that/exceeds/limit>x</a>\n"
        ),
        (
            '<a href="https://example.com/some/long/path/that/exceeds/limit">x</a>\n'
        ),
        ({"max_attribute_length": 20}),
        id='an unquoted URL/path value must not be split at ":" or "/" into a bogus standalone attribute; it stays one value (quoted when spread)',
    ),
    pytest.param(
        ("<a href=/help/faq#billing-and-refunds target=_blank>x</a>\n"),
        ('<a href="/help/faq#billing-and-refunds"\n   target="_blank">x</a>\n'),
        ({"max_attribute_length": 20}),
        id="punctuation is legal in an unquoted value; it must not truncate the value and leave the rest as a bogus standalone attribute",
    ),
    pytest.param(
        ("<img src={{ MEDIA_URL }}/logo/some-long-name.png alt=logo>\n"),
        (
            '<img src="{{ MEDIA_URL }}/logo/some-long-name.png"\n'
            '     alt="logo">\n'
        ),
        ({"max_attribute_length": 20, "profile": "django"}),
        id="a template tag glued to the rest of an unquoted value is part of that value, not the start of a second attribute",
    ),
    pytest.param(
        ("<a href={{ .Permalink }}#{{ .Anchor }} rel=noopener>x</a>\n"),
        ('<a href="{{ .Permalink }}#{{ .Anchor }}"\n   rel="noopener">x</a>\n'),
        ({"max_attribute_length": 20, "profile": "golang"}),
        id="including when the value is several template tags joined by punctuation, as in a golang permalink + anchor",
    ),
    pytest.param(
        ('<div {{ prefix }}?suffix="1" class="one two three">z</div>\n'),
        ('<div {{ prefix }}?suffix="1"\n     class="one two three">z</div>\n'),
        ({"max_attribute_length": 20, "profile": "django"}),
        id="a template variable may prefix an attribute name whose remainder starts with punctuation",
    ),
    pytest.param(
        (
            '<div {% if a %}data{% endif %}?y="1" class="one two three">z</div>\n'
        ),
        (
            '<div {% if a %}data{% endif %}?y="1"\n'
            '     class="one two three">z</div>\n'
        ),
        ({"max_attribute_length": 20, "profile": "django"}),
        id="and so may a complete template block",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
