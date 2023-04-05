"""Test css.

poetry run pytest tests/test_html/test_css.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<style></style>\n"),
        ("<style></style>\n"),
        id="empty",
    ),
    pytest.param(
        (
            '<style type="text/less">\n'
            "  @nice-blue: #5B83AD;\n"
            "  @light-blue: @nice-blue + #111;\n"
            "  #header {\n"
            "    color: @light-blue;\n"
            "  }\n"
            "</style>\n"
            '<style lang="less">\n'
            "  @nice-blue: #5B83AD;\n"
            "  @light-blue: @nice-blue + #111;\n"
            "  #header {\n"
            "    color: @light-blue;\n"
            "  }\n"
            "</style>\n"
        ),
        (
            '<style type="text/less">\n'
            "  @nice-blue: #5B83AD;\n"
            "  @light-blue: @nice-blue + #111;\n"
            "  #header {\n"
            "    color: @light-blue;\n"
            "  }\n"
            "</style>\n"
            '<style lang="less">\n'
            "  @nice-blue: #5B83AD;\n"
            "  @light-blue: @nice-blue + #111;\n"
            "  #header {\n"
            "    color: @light-blue;\n"
            "  }\n"
            "</style>\n"
        ),
        id="less",
    ),
    pytest.param(
        (
            '<style type="text/css">\n'
            "  body { background: navy; color: yellow; }\n"
            "</style>\n"
            '<style lang="postcss">\n'
            "  body { background: navy; color: yellow; }\n"
            "</style>\n"
        ),
        (
            '<style type="text/css">body { background: navy; color: yellow; }</style>\n'
            '<style lang="postcss">body { background: navy; color: yellow; }</style>\n'
        ),
        id="postcss",
    ),
    pytest.param(
        (
            '<style type="text/x-scss">\n'
            "  $font-stack:    Helvetica, sans-serif;\n"
            "  $primary-color: #333;\n"
            "  body {\n"
            "    font: 100% $font-stack;\n"
            "    color: $primary-color;\n"
            "  }\n"
            "</style>\n"
            '<style lang="scss">\n'
            "  $font-stack:    Helvetica, sans-serif;\n"
            "  $primary-color: #333;\n"
            "  body {\n"
            "    font: 100% $font-stack;\n"
            "    color: $primary-color;\n"
            "  }\n"
            "</style>\n"
            '<style lang="scss">\n'
            ".someElement {\n"
            "    @include bp-medium {\n"
            "      display: flex;\n"
            "    }\n"
            "\n"
            "    @include bp-large {\n"
            "      margin-top: 10px;\n"
            "      margin-bottom: 10px;\n"
            "    }\n"
            "}\n"
            "</style>\n"
        ),
        (
            '<style type="text/x-scss">\n'
            "  $font-stack:    Helvetica, sans-serif;\n"
            "  $primary-color: #333;\n"
            "  body {\n"
            "    font: 100% $font-stack;\n"
            "    color: $primary-color;\n"
            "  }\n"
            "</style>\n"
            '<style lang="scss">\n'
            "  $font-stack:    Helvetica, sans-serif;\n"
            "  $primary-color: #333;\n"
            "  body {\n"
            "    font: 100% $font-stack;\n"
            "    color: $primary-color;\n"
            "  }\n"
            "</style>\n"
            '<style lang="scss">\n'
            ".someElement {\n"
            "    @include bp-medium {\n"
            "      display: flex;\n"
            "    }\n"
            "\n"
            "    @include bp-large {\n"
            "      margin-top: 10px;\n"
            "      margin-bottom: 10px;\n"
            "    }\n"
            "}\n"
            "</style>\n"
        ),
        id="scss",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <head>\n"
            "    <title>Sample styled page</title>\n"
            "    <style>a { color: red; }</style>\n"
            "    <style>\n"
            "      body { background: navy; color: yellow; }\n"
            "    </style>\n"
            "  </head>\n"
            "  <body>\n"
            "    <h1>Sample styled page</h1>\n"
            "    <p>This page is just a demo.</p>\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <head>\n"
            "        <title>Sample styled page</title>\n"
            "        <style>a { color: red; }</style>\n"
            "        <style>body { background: navy; color: yellow; }</style>\n"
            "    </head>\n"
            "    <body>\n"
            "        <h1>Sample styled page</h1>\n"
            "        <p>This page is just a demo.</p>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="simple",
    ),
    pytest.param(
        (
            "<style>a { color: red; }</style>\n"
            "<style>\n"
            "  h1 {\n"
            "    font-size: 120%;\n"
            "    font-family: Verdana, Arial, Helvetica, sans-serif;\n"
            "    color: #333366;\n"
            "  }\n"
            "</style>\n"
        ),
        (
            "<style>a { color: red; }</style>\n"
            "<style>\n"
            "  h1 {\n"
            "    font-size: 120%;\n"
            "    font-family: Verdana, Arial, Helvetica, sans-serif;\n"
            "    color: #333366;\n"
            "  }\n"
            "</style>\n"
        ),
        id="single_style",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
