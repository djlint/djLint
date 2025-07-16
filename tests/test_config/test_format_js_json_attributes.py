"""Test for JS/JSON attribute formatting.

--format-js-attributes
--js-attribute-pattern

uv run pytest tests/test_config/test_format_js_json_attributes.py
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
            '<div data-config=\'{"name": "value"}\'></div>'
        ),
        (
            '<div data-config=\'{"name": "value"}\'></div>\n'
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0}),
        id="json_single_property_no_formatting",
    ),
    pytest.param(
        (
            '<div data-config=\'{"name": "value", "enabled": true}\'></div>'
        ),
        (
            '<div data-config=\'{\n'
            '                      "name": "value",\n'
            '                      "enabled": true\n'
            '                  }\'></div>\n'
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0, "indent_js": 2}),
        id="json_two_properties_multiline_medium_attr",
    ),
    pytest.param(
        (
            '<div data-x=\'{"name": "value", "enabled": true}\'></div>'
        ),
        (
            '<div data-x=\'{\n'
            '                 "name": "value",\n'
            '                 "enabled": true\n'
            '             }\'></div>\n'
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0, "indent_js": 2}),
        id="json_two_properties_multiline_short_attr",
    ),
    pytest.param(
        (
            '<div data-very-long-attribute-name=\'{"name": "value", "enabled": true}\'></div>'
        ),
        (
            '<div data-very-long-attribute-name=\'{\n'
            '                                        "name": "value",\n'
            '                                        "enabled": true\n'
            '                                    }\'></div>\n'
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0, "indent_js": 2}),
        id="json_two_properties_multiline_long_attr",
    ),
    pytest.param(
        (
            '<div onclick=\'{action: "click"}\'></div>'
        ),
        (
            '<div onclick=\'{action: "click"}\'></div>\n'
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0}),
        id="js_single_property_no_formatting",
    ),
    pytest.param(
        (
            '<div onclick=\'{action: "click", preventDefault: true}\'></div>'
        ),
        (
            '<div onclick=\'{\n'
            '                  action: "click",\n'
            '                  preventDefault: true\n'
            '              }\'></div>\n'
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0, "indent_js": 2}),
        id="js_two_properties_multiline",
    ),
    pytest.param(
        (
            "<div onclick='foo();'></div>"
        ),
        (
            "<div onclick='foo();'></div>\n"
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0, "indent_js": 2}),
        id="js_code_single_function_no_formatting",
    ),
    pytest.param(
        (
            "<div onclick='foo(); var x = 1; baz();'></div>"
        ),
        (
            "<div onclick='foo();\n"
            "              var x = 1;\n"
            "              baz();'></div>\n"
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0, "indent_js": 2}),
        id="js_code_multiple_statements_multiline",
    ),
    pytest.param(
        (
            "<div onclick='foo(); baz();'></div>"
        ),
        (
            "<div onclick='foo(); baz();'></div>\n"
        ),
        ({"format_js_attributes": True, "max_attribute_length": 50, "indent_js": 2}),
        id="js_code_under_max_length_no_formatting",
    ),
    pytest.param(
        (
            "<div class='foo-baz'></div>"
            "<div id='my-element-id'></div>"
            "<input name='user-name' />"
            "<div title='Page Title'></div>"
            "<input type='text' />"
            "<input value='some-value' />"
            "<div role='button'></div>"
            "<div aria-label='Close Button'></div>"
            "<a href='/path/to/page'></a>"
            "<img src='/path/to/image.jpg' />"
            "<img alt='Image Description' />"
        ),
        (
            "<div class='foo-baz'></div>\n"
            "<div id='my-element-id'></div>\n"
            "<input name='user-name' />\n"
            "<div title='Page Title'></div>\n"
            "<input type='text' />\n"
            "<input value='some-value' />\n"
            "<div role='button'></div>\n"
            "<div aria-label='Close Button'></div>\n"
            "<a href='/path/to/page'></a>\n"
            "<img src='/path/to/image.jpg' />\n"
            "<img alt='Image Description' />\n"
        ),
        ({"format_js_attributes": True, "max_attribute_length": 0, "indent_js": 2}),
        id="non_js_attributes_no_formatting",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)
    printer(expected, source, output)
    assert expected == output
