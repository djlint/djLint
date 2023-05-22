"""Test yaml front matter.

poetry run pytest tests/test_html/test_yaml.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        (
            "---\n"
            "    invalid:\n"
            "invalid:\n"
            "---\n"
            "\n"
            "\n"
            "\n"
            "<html><head></head><body></body></html>\n"
        ),
        (
            "---\n"
            "    invalid:\n"
            "invalid:\n"
            "---\n"
            "\n"
            "<html>\n"
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        ({}),
        id="invalid",
    ),
    pytest.param(
        (
            "---\n"
            "hello:     world\n"
            "---\n"
            "<html><head></head><body></body></html>\n"
        ),
        (
            "---\n"
            "hello:     world\n"
            "---\n"
            "\n"
            "<html>\n"
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        ({}),
        id="valid",
    ),
    pytest.param(
        ("---\n" "layout: <div><div></div></div>\n" "---\n" "<div></div>\n"),
        ("---\n" "layout: <div><div></div></div>\n" "---\n" "\n" "<div></div>\n"),
        ({}),
        id="more",
    ),
    pytest.param(
        (
            "---mycustomparser\n"
            "title: Hello\n"
            "slug: home\n"
            "---\n"
            "<h1>\n"
            "  Hello world!</h1>\n"
        ),
        (
            "---mycustomparser\n"
            "title: Hello\n"
            "slug: home\n"
            "---\n"
            "\n"
            "<h1>Hello world!</h1>\n"
        ),
        ({}),
        id="custom_parser",
    ),
    pytest.param(
        ("---\n" "---\n" "<h1>\n" "  Hello world!</h1>\n"),
        ("---\n" "---\n" "\n" "<h1>Hello world!</h1>\n"),
        ({}),
        id="empty",
    ),
    pytest.param(
        ("---\n" "---\n" "<div>\n" "---\n" "</div>\n"),
        ("---\n" "---\n" "\n" "<div>---</div>\n"),
        ({}),
        id="empty_2",
    ),
    pytest.param(
        ("---\n" "---\n\n\n" "<div>\n" "---\n" "</div>\n"),
        ("---\n" "---\n" "\n" "<div>---</div>\n"),
        ({}),
        id="blank_lines",
    ),
    pytest.param(
        ("---\n" "---\n\n\n\n" "{{ this }}\n"),
        ("---\n" "---\n" "\n" "{{ this }}\n"),
        ({}),
        id="blank_lines_2",
    ),
    pytest.param(
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            "Test <a\n"
            'href="https://djlint.com">abc</a>.\n'
        ),
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            "\n"
            'Test <a href="https://djlint.com">abc</a>.\n'
        ),
        ({}),
        id="issue_9042_no_empty_line",
    ),
    pytest.param(
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            "Test <a\n"
            'href="https://djlint.com">abc</a>.\n'
        ),
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            "\n"
            'Test <a href="https://djlint.com">abc</a>.\n'
        ),
        ({}),
        id="issue_9042",
    ),
    pytest.param(
        ("---\n" "---\n\n\n\n" "{{ this }}\n"),
        ("---\n" "---\n" "{{ this }}\n"),
        ({"no_line_after_yaml": True}),
        id="blank_lines_2",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
