"""Test symbol entities.

uv run pytest tests/test_html/test_symbol_entities.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        (
            "<p>I will display &euro;</p>\n"
            "<p>I will display &excl;</p>\n"
            "<p>I will display &#8364;</p>\n"
            "<p>I will display &#x20AC;</p>\n"
        ),
        (
            "<p>I will display €</p>\n"
            "<p>I will display !</p>\n"
            "<p>I will display €</p>\n"
            "<p>I will display €</p>\n"
        ),
        id="symbol_entities_become_the_character",
    ),
    pytest.param(
        ("<p>&lt;div&gt; &amp; &quot; &nbsp; &zwnj; &shy;</p>\n"),
        ("<p>&lt;div&gt; &amp; &quot; &nbsp; &zwnj; &shy;</p>\n"),
        id="syntax_and_invisible_entities_are_kept",
    ),
    pytest.param(
        (
            "<p>&lbrace;&lbrace; name &rbrace;&rbrace; &#123;% if a %&#125; &#x7B;# note #&#x7D; {&percnt; for x in y &#37;} {&num; c &#x23;} &dollar;{ m }</p>\n"
        ),
        (
            "<p>&lbrace;&lbrace; name &rbrace;&rbrace; &#123;% if a %&#125; &#x7B;# note #&#x7D; {&percnt; for x in y &#37;} {&num; c &#x23;} &dollar;{ m }</p>\n"
        ),
        id="template_delimiters_are_kept",
    ),
    pytest.param(
        ("<p>&mdsah; names nothing</p>\n"),
        ("<p>&mdsah; names nothing</p>\n"),
        id="a_misspelled_entity_is_left_for_the_rule_to_report",
    ),
    pytest.param(
        ("<pre>&euro;</pre>\n<script>var s = '&euro;';</script>\n"),
        ("<pre>&euro;</pre>\n<script>var s = '&euro;';</script>\n"),
        id="verbatim_and_script_bodies_are_left_alone",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output


def test_no_entity_formatting_keeps_them() -> None:
    source = "<p>I will display &euro;</p>\n"
    config = config_builder({"no_entity_formatting": True})

    assert formatter(config, source) == source
