"""Test html textarea tag.

poetry run pytest tests/test_html/test_tag_textarea.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<div><textarea>\n" "asdf\n" "  asdf</textarea></div>\n"),
        ("<div>\n" "    <textarea>\n" "asdf\n" "  asdf</textarea>\n" "</div>\n"),
        id="textarea",
    ),
    pytest.param(
        (
            "<div>\n"
            '    <div class="field">\n'
            "        <textarea>asdf</textarea>\n"
            "    </div>\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    <div class="field">\n'
            "        <textarea>asdf</textarea>\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="nesting",
    ),
    pytest.param(
        (
            "<div>\n"
            '    <div class="field">\n'
            '        <textarea class="this"\n'
            '                  name="that">asdf</textarea>\n'
            "    </div>\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    <div class="field">\n'
            '        <textarea class="this" name="that">asdf</textarea>\n'
            "    </div>\n"
            "</div>\n"
        ),
        id="attributes",
    ),
    pytest.param(
        ("<p>\n" '    some nice text <a href="this">asdf</a>, ok\n' "</p>\n"),
        ("<p>\n" '    some nice text <a href="this">asdf</a>, ok\n' "</p>\n"),
        id="a_tag",
    ),
    # test added for https://github.com/Riverside-Healthcare/djLint/issues/189
    pytest.param(
        (
            "<a>\n"
            "    <span>hi</span>hi</a>\n"
            "<div>\n"
            '    <h4>{{ _("Options") }}</h4>\n'
            "</div>\n"
        ),
        (
            "<a>\n"
            "    <span>hi</span>hi</a>\n"
            "<div>\n"
            '    <h4>{{ _("Options") }}</h4>\n'
            "</div>\n"
        ),
        id="a_with_nesting",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
