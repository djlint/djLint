"""Tests for doctype.

poetry run pytest tests/test_html/test_doctype_declarations.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<!DocType htMl>"),
        ("<!DOCTYPE htMl>\n"),
        id="case",
    ),
    pytest.param(
        ("<!DocType htMl  >"),
        ("<!DOCTYPE htMl>\n"),
        id="case_2",
    ),
    pytest.param(
        (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"\n'
            '  "http://www.w3.org/TR/html4/frameset.dtd">\n'
            "<html>\n"
            "  <head>\n"
            "    <title>An HTML standard template</title>\n"
            '    <meta charset="utf-8"  />\n'
            "  </head>\n"
            "  <body>\n"
            "    <p>… Your HTML content here …</p>\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">\n'
            "<html>\n"
            "    <head>\n"
            "        <title>An HTML standard template</title>\n"
            '        <meta charset="utf-8" />\n'
            "    </head>\n"
            "    <body>\n"
            "        <p>… Your HTML content here …</p>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="html4_01_frameset",
    ),
    pytest.param(
        (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"\n'
            '  "http://www.w3.org/TR/html4/strict.dtd">\n'
            "<html>\n"
            "  <head>\n"
            "    <title>An HTML standard template</title>\n"
            '    <meta charset="utf-8" />\n'
            "  </head>\n"
            "  <body>\n"
            "    <p>… Your HTML content here …</p>\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'
            "<html>\n"
            "    <head>\n"
            "        <title>An HTML standard template</title>\n"
            '        <meta charset="utf-8" />\n'
            "    </head>\n"
            "    <body>\n"
            "        <p>… Your HTML content here …</p>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="html4_01_strict",
    ),
    pytest.param(
        (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n'
            '  "http://www.w3.org/TR/html4/loose.dtd">\n'
            "<html>\n"
            "  <head>\n"
            "    <title>An HTML standard template</title>\n"
            '    <meta charset="utf-8" />\n'
            "  </head>\n"
            "  <body>\n"
            "    <p>… Your HTML content here …</p>\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n'
            "<html>\n"
            "    <head>\n"
            "        <title>An HTML standard template</title>\n"
            '        <meta charset="utf-8" />\n'
            "    </head>\n"
            "    <body>\n"
            "        <p>… Your HTML content here …</p>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="html4_01_transitional",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <head>\n"
            "    <title>An HTML standard template</title>\n"
            '    <meta charset="utf-8" />\n'
            "  </head>\n"
            "  <body>\n"
            "    <p>… Your HTML content here …</p>\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <head>\n"
            "        <title>An HTML standard template</title>\n"
            '        <meta charset="utf-8" />\n'
            "    </head>\n"
            "    <body>\n"
            "        <p>… Your HTML content here …</p>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="html5",
    ),
    pytest.param(
        (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
            '<html xmlns="http://www.w3.org/1999/xhtml">\n'
            "  <head>\n"
            '    <meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />\n'
            "    <title>XHTML markup</title>\n"
            "  </head>\n"
            '  <body style="background-color:#ffffcc; color:#008800">\n'
            "    <br />\n"
            '    <h2 align="center">Sample XHTML page</h2>\n'
            "    <br />\n"
            '    <div align="center">\n'
            '      <img src="../images/bee3.jpg" width="400" height="250" alt="Beep" vspace="20" />\n'
            "    </div>\n"
            '    <p align="center" style="font-size:17px">Bar Foo,<br />\n'
            "      Foo,<br />\n"
            "      Bar<br />\n"
            "      Foo</p>\n"
            '    <p align="center"><em>String</em></p>\n'
            "    <br />\n"
            "    <hr />\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
            '<html xmlns="http://www.w3.org/1999/xhtml">\n'
            "    <head>\n"
            '        <meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />\n'
            "        <title>XHTML markup</title>\n"
            "    </head>\n"
            '    <body style="background-color:#ffffcc; color:#008800">\n'
            "        <br />\n"
            '        <h2 align="center">Sample XHTML page</h2>\n'
            "        <br />\n"
            '        <div align="center">\n'
            '            <img src="../images/bee3.jpg"\n'
            '                 width="400"\n'
            '                 height="250"\n'
            '                 alt="Beep"\n'
            '                 vspace="20" />\n'
            "        </div>\n"
            '        <p align="center" style="font-size:17px">\n'
            "            Bar Foo,\n"
            "            <br />\n"
            "            Foo,\n"
            "            <br />\n"
            "            Bar\n"
            "            <br />\n"
            "            Foo\n"
            "        </p>\n"
            '        <p align="center">\n'
            "            <em>String</em>\n"
            "        </p>\n"
            "        <br />\n"
            "        <hr />\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="xhtml1_1",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
