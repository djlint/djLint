"""Test liquid profile.

uv run pytest tests/test_liquid/test_liquid.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import config_builder, lint_printer, printer

test_data = [
    pytest.param(
        (
            "{% case product.type %}\n"
            '{% when "shirt" %}\n'
            "<p>shirt</p>\n"
            '{% when "pants" %}\n'
            "<p>pants</p>\n"
            "{% else %}\n"
            "<p>other</p>\n"
            "{% endcase %}\n"
        ),
        (
            "{% case product.type %}\n"
            '{% when "shirt" %}\n'
            "    <p>shirt</p>\n"
            '{% when "pants" %}\n'
            "    <p>pants</p>\n"
            "{% else %}\n"
            "    <p>other</p>\n"
            "{% endcase %}\n"
        ),
        id="case_when_branches",
    ),
    pytest.param(
        (
            "{% capture note %}\n<span>hi</span>\n{% endcapture %}\n"
            "{% assign x = 1 %}\n"
        ),
        (
            "{% capture note %}\n    <span>hi</span>\n{% endcapture %}\n"
            "{% assign x = 1 %}\n"
        ),
        id="capture_block_assign_single",
    ),
    pytest.param(
        (
            "{% unless sold_out %}\n<button>buy</button>\n{% elsif backorder %}\n"
            "<p>soon</p>\n{% endunless %}\n"
        ),
        (
            "{% unless sold_out %}\n    <button>buy</button>\n{% elsif backorder %}\n"
            "    <p>soon</p>\n{% endunless %}\n"
        ),
        id="unless_elsif",
    ),
    pytest.param(
        (
            "{% tablerow product in collection.products cols:2 %}\n"
            "{{ product.title }}\n"
            "{% endtablerow %}\n"
        ),
        (
            "{% tablerow product in collection.products cols:2 %}\n"
            "    {{ product.title }}\n"
            "{% endtablerow %}\n"
        ),
        id="tablerow_block",
    ),
    pytest.param(
        (
            "{% schema %}\n"
            '{ "name": "x",   "settings": [] }\n'
            "{% endschema %}\n"
            "{% style %}\n"
            ".a  {color:red}\n"
            "{% endstyle %}\n"
        ),
        (
            "{% schema %}\n"
            '{ "name": "x",   "settings": [] }\n'
            "{% endschema %}\n"
            "{% style %}\n"
            ".a  {color:red}\n"
            "{% endstyle %}\n"
        ),
        id="shopify_section_bodies_untouched",
    ),
    pytest.param(
        (
            "{% comment %}note{% endcomment %}\n"
            "{%- if a -%}\n<p>x</p>\n{%- endif -%}\n"
        ),
        (
            "{% comment %}note{% endcomment %}\n"
            "{%- if a -%}\n    <p>x</p>\n{%- endif -%}\n"
        ),
        id="comment_block_and_whitespace_control",
    ),
    pytest.param(
        ("{% capture t %}{{ a }}{% endcapture %}\n<p>after</p>\n"),
        ("{% capture t %}{{ a }}{% endcapture %}\n<p>after</p>\n"),
        id="single_line_capture_does_not_leak_indent",
    ),
    pytest.param(
        (
            '{% form "cart", cart %}\n<button>go</button>\n{% endform %}\n'
            "{% paginate items by 12 %}\n<p>x</p>\n{% endpaginate %}\n"
        ),
        (
            '{% form "cart", cart %}\n    <button>go</button>\n{% endform %}\n'
            "{% paginate items by 12 %}\n    <p>x</p>\n{% endpaginate %}\n"
        ),
        id="form_and_paginate_blocks",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {% schema %}\n"
            '{ "a": 1,\n'
            '  "b": 2 }\n'
            "{% endschema %}\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            "    {% schema %}\n"
            '{ "a": 1,\n'
            '  "b": 2 }\n'
            "{% endschema %}\n"
            "</div>\n"
        ),
        id="nested_schema_idempotent_and_untouched",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_formatter(source: str, expected: str) -> None:
    output = formatter(config_builder({"profile": "liquid"}), source)

    printer(expected, source, output)
    assert expected == output


def test_profile_defaults() -> None:
    config = Config("dummy/source.html", profile="liquid")

    names = {x["rule"]["name"] for x in config.linter_rules}
    assert "D004" not in names
    assert "J004" not in names
    assert "J018" not in names
    assert "H005" in names
    assert "T038" in names


def test_liquid_tags_do_not_leak_into_other_profiles() -> None:
    # the djangosnippets switch/case idiom uses {% case %} as a single tag
    source = "<div>\n    {% case foo %}\n    <span>a</span>\n</div>\n"
    django = config_builder({"profile": "django"})

    output = formatter(django, source)
    printer(source, source, output)
    assert output == source

    result = linter(django, source, "test.html", "test.html")
    lint_printer(source, [], result["test.html"])
    assert not [x for x in result["test.html"] if x["code"] == "T038"]
