"""Test for comments.

uv run pytest tests/test_html/test_comments.py
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
        ("<div>\n    <!-- asdf--><!--\n multi\nline\ncomment--></div>"),
        ("<div>\n    <!-- asdf--><!--\n multi\nline\ncomment-->\n</div>\n"),
        id="comments_tag",
    ),
    pytest.param(
        ("<!-- hello -->\n123\n"), ("<!-- hello -->\n123\n"), id="before_text"
    ),
    pytest.param(
        ("<? hello ?>\n<!- world ->\n"),
        ("<? hello ?>\n<!- world ->\n"),
        id="bogus",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <body>\n"
            "    <!--[if IE 5]>This is IE 5<br><![endif]-->\n"
            "    <!--[if IE 6]>This is IE 6<br><![endif]-->\n"
            "    <!--[if IE 7]>This is IE 7<br><![endif]-->\n"
            "    <!--[if IE 8]>This is IE 8<br><![endif]-->\n"
            "    <!--[if IE 9]>This is IE 9<br><![endif]-->\n"
            "  </body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html lang="zh-CN"><![endif]-->\n'
            '<html lang="zh-CN">\n'
            "  <head></head>\n"
            "  <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html lang="zh-CN"><div><![endif]-->\n'
            '<html lang="zh-CN">\n'
            "  <head></head>\n"
            "  <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html lang="zh-CN"><div></div><![endif]-->\n'
            '<html lang="zh-CN">\n'
            "  <head></head>\n"
            "  <body></body>\n"
            "</html>\n"
            '<body width="100%" align="center">\n'
            "  <center  >\n"
            '    <!--[if (gte mso 9)|(IE)]><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tr><td><![endif]-->\n'
            "    <div>  </div>\n"
            "    <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->\n"
            "  </center  >\n"
            "</body>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><![endif]-->\n'
            "<!--[if gte IE 9]><!--><html><!--<![endif]-->\n"
            "  <head></head>\n"
            "  <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><![endif]-->\n'
            "<!--[if gte IE 9]><!--><html hello><!--<![endif]-->\n"
            "  <head></head>\n"
            "  <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><head><![endif]-->\n'
            "<!--[if gte IE 9]><!--><html><head><!--<![endif]-->\n"
            "  </head>\n"
            "  <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><![endif]-->\n'
            "<!--[if gte IE 9\n"
            "]><!--><html><!--<![endif]-->\n"
            "  <head></head>\n"
            "  <body></body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <body>\n"
            "        <!--[if IE 5]>This is IE 5<br><![endif]-->\n"
            "        <!--[if IE 6]>This is IE 6<br><![endif]-->\n"
            "        <!--[if IE 7]>This is IE 7<br><![endif]-->\n"
            "        <!--[if IE 8]>This is IE 8<br><![endif]-->\n"
            "        <!--[if IE 9]>This is IE 9<br><![endif]-->\n"
            "    </body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html lang="zh-CN"><![endif]-->\n'
            '<html lang="zh-CN">\n'
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html lang="zh-CN"><div><![endif]-->\n'
            '<html lang="zh-CN">\n'
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html lang="zh-CN"><div></div><![endif]-->\n'
            '<html lang="zh-CN">\n'
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
            '<body width="100%" align="center">\n'
            "    <center>\n"
            '        <!--[if (gte mso 9)|(IE)]><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tr><td><![endif]-->\n'
            "        <div></div>\n"
            "        <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->\n"
            "    </center>\n"
            "</body>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><![endif]-->\n'
            "<!--[if gte IE 9]><!-->\n"
            "<html>\n"
            "    <!--<![endif]-->\n"
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><![endif]-->\n'
            "<!--[if gte IE 9]><!-->\n"
            "<html hello>\n"
            "    <!--<![endif]-->\n"
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><head><![endif]-->\n'
            "<!--[if gte IE 9]><!-->\n"
            "<html>\n"
            "    <head>\n"
            "        <!--<![endif]-->\n"
            "    </head>\n"
            "    <body></body>\n"
            "</html>\n"
            "<!DOCTYPE html>\n"
            '<!--[if lt IE 9]><html class="legacy-ie"><![endif]-->\n'
            "<!--[if gte IE 9\n"
            "]><!--><html><!--<![endif]-->\n"
            "<head></head>\n"
            "<body></body>\n"
            "</html>\n"
        ),
        id="conditional",
    ),
    # opened https://github.com/djlint/djLint/issues/247
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <body>\n"
            "<!-- Do not display this at the moment\n"
            '<img border="0" src="pic_trulli.jpg" alt="Trulli">\n'
            "-->\n"
            "  <!-- Do not display this at the moment\n"
            '  <img border="0" src="pic_trulli.jpg" alt="Trulli">\n'
            "  -->\n"
            "    <!-- Do not display this at the moment\n"
            '    <img border="0" src="pic_trulli.jpg" alt="Trulli">\n'
            "    -->\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <body>\n"
            "        <!-- Do not display this at the moment\n"
            '<img border="0" src="pic_trulli.jpg" alt="Trulli">\n'
            "-->\n"
            "        <!-- Do not display this at the moment\n"
            '  <img border="0" src="pic_trulli.jpg" alt="Trulli">\n'
            "  -->\n"
            "        <!-- Do not display this at the moment\n"
            '    <img border="0" src="pic_trulli.jpg" alt="Trulli">\n'
            "    -->\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="debugging",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <body>\n"
            "        <!--This is a comment-->\n"
            "        <!-- This is a comment -->\n"
            "        <!--  This is a comment  -->\n"
            "        <!--   This   is   a   comment   -->\n"
            "        <p>This is a paragraph.</p>\n"
            "        <!-- Comments are not displayed in the browser -->\n"
            "    </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <body>\n"
            "        <!--This is a comment-->\n"
            "        <!-- This is a comment -->\n"
            "        <!--  This is a comment  -->\n"
            "        <!--   This   is   a   comment   -->\n"
            "        <p>This is a paragraph.</p>\n"
            "        <!-- Comments are not displayed in the browser -->\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="hidden",
    ),
    pytest.param(
        (
            "<ul><!-- 123\n"
            "--><li>First</li><!-- 123\n"
            "456\n"
            "   789\n"
            "--><li>Second</li><!--\n"
            "    123\n"
            "       456\n"
            "          789\n"
            "--><li>Second</li><!--\n"
            "           123\n"
            "        456\n"
            "    789\n"
            "--></ul>\n"
            "<span><!--\n"
            "--><span>a</span><!--\n"
            "--><span>b</span><!--\n"
            "--></span>\n"
            "<span><!-- 1\n"
            "--><span>a</span><!-- 2\n"
            "--><span>b</span><!-- 3\n"
            "--></span>\n"
            "<span><!--\n"
            "1 --><span>a</span><!--\n"
            "2 --><span>b</span><!--\n"
            "3 --></span>\n"
            "123<!---->456\n"
            "123<!--x-->456\n"
            "<!-- A\n"
            "     B -->\n"
            "<!--\n"
            "The null hero's name is {{nullHero.name}}\n"
            "See console log:\n"
            "  TypeError: Cannot read property 'name' of null in [null]\n"
            "-->\n"
            "<!--\n"
            "    The null hero's name is {{nullHero.name}}\n"
            "    See console log:\n"
            "    TypeError: Cannot read property 'name' of null in [null]\n"
            "-->\n"
        ),
        (
            "<ul>\n"
            "    <!-- 123\n"
            "-->\n"
            "    <li>First</li>\n"
            "    <!-- 123\n"
            "456\n"
            "   789\n"
            "-->\n"
            "    <li>Second</li>\n"
            "    <!--\n"
            "    123\n"
            "       456\n"
            "          789\n"
            "-->\n"
            "    <li>Second</li>\n"
            "    <!--\n"
            "           123\n"
            "        456\n"
            "    789\n"
            "-->\n"
            "</ul>\n"
            "<span><!--\n"
            "--><span>a</span><!--\n"
            "--><span>b</span><!--\n"
            "--></span>\n"
            "<span><!-- 1\n"
            "--><span>a</span><!-- 2\n"
            "--><span>b</span><!-- 3\n"
            "--></span>\n"
            "<span><!--\n"
            "1 --><span>a</span><!--\n"
            "2 --><span>b</span><!--\n"
            "3 --></span>\n"
            "123<!---->456\n"
            "123<!--x-->456\n"
            "<!-- A\n"
            "     B -->\n"
            "<!--\n"
            "The null hero's name is {{nullHero.name}}\n"
            "See console log:\n"
            "  TypeError: Cannot read property 'name' of null in [null]\n"
            "-->\n"
            "<!--\n"
            "    The null hero's name is {{nullHero.name}}\n"
            "    See console log:\n"
            "    TypeError: Cannot read property 'name' of null in [null]\n"
            "-->\n"
        ),
        id="surrounding_empty_line",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
