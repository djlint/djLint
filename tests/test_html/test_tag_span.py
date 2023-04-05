"""Test html span tag.

poetry run pytest tests/test_html/test_tag_span.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '<span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span>\n'
        ),
        (
            '<span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span>\n'
        ),
        id="icon",
    ),
    # issue #171, span is an inline tag
    pytest.param(
        (
            '<div class="hi">\n'
            '    <div class="poor">\n'
            '        <p class="format">\n'
            "            <strong>H</strong>ello stranger, <strong>do not wrap span</strong>, <strong>pls</strong>.\n"
            '            <span class="big">H</span>ello stranger, <strong>do not wrap span</strong>, <span class="big">pls</span>.\n'
            "        </p>\n"
            "    </div>\n"
            "</div>\n"
        ),
        (
            '<div class="hi">\n'
            '    <div class="poor">\n'
            '        <p class="format">\n'
            "            <strong>H</strong>ello stranger, <strong>do not wrap span</strong>, <strong>pls</strong>.\n"
            '            <span class="big">H</span>ello stranger, <strong>do not wrap span</strong>, <span class="big">pls</span>.\n'
            "        </p>\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="inline",
    ),
    pytest.param(
        ("<p><p><span><strong>asdf</strong><br></span></p></p>\n"),
        (
            "<p>\n"
            "    <p>\n"
            "        <span><strong>asdf</strong>\n"
            "            <br>\n"
            "        </span>\n"
            "    </p>\n"
            "</p>\n"
        ),
        id="nested string",
    ),
    pytest.param(
        (
            "<ul>\n"
            "    <li>\n"
            "        <span>C</span> <a>D</a> <strong>Q</strong>\n"
            "    </li>\n"
            "</ul>\n"
        ),
        (
            "<ul>\n"
            "    <li>\n"
            "        <span>C</span> <a>D</a> <strong>Q</strong>\n"
            "    </li>\n"
            "</ul>\n"
        ),
        id="more_strings",
    ),
    pytest.param(
        ("{% if this %}<p>Text <span>text</span></p>{% endif %}\n"),
        (
            "{% if this %}\n"
            "    <p>\n"
            "        Text <span>text</span>\n"
            "    </p>\n"
            "{% endif %}\n"
        ),
        id="span_leading_text",
    ),
    pytest.param(
        (
            "<p>\n"
            '    <span class="badge">New</span> You can now use <strong>this feature</strong>\n'
            "</p>\n"
        ),
        (
            "<p>\n"
            '    <span class="badge">New</span> You can now use <strong>this feature</strong>\n'
            "</p>\n"
        ),
        id="span_text_strong",
    ),
    pytest.param(
        (
            "{% block content %}\n"
            "    <span></span>{% blocktrans %}<div></div>{% endblocktrans %}\n"
            "    {% endblock content %}\n"
        ),
        (
            "{% block content %}\n"
            "    <span></span>{% blocktrans %}<div></div>{% endblocktrans %}\n"
            "{% endblock content %}\n"
        ),
        id="span_with_template",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
