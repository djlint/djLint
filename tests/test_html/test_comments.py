"""Djlint tests for comments.

Some tests may be from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run:

    pytest tests/test_html/test_comments.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_comments.py::test_html_comments_tag


"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import reformat, write_to_file


def test_html_comments_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <!-- asdf--><!--\n multi\nline\ncomment--></div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<div>
    <!-- asdf--><!--
 multi
line
comment-->
</div>
"""
    )


def test_before_text(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<!-- hello -->
123
    """
    ).strip()

    html_out = """<!-- hello -->
123
"""

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_bogus(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<? hello ?>
<!- world ->
    """
    ).strip()

    html_out = """<? hello ?>
<!- world ->
"""

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


# def test_conditional(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <!DOCTYPE html>
# <html>
#   <body>
#     <!--[if IE 5]>This is IE 5<br><![endif]-->
#     <!--[if IE 6]>This is IE 6<br><![endif]-->
#     <!--[if IE 7]>This is IE 7<br><![endif]-->
#     <!--[if IE 8]>This is IE 8<br><![endif]-->
#     <!--[if IE 9]>This is IE 9<br><![endif]-->
#   </body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html lang="zh-CN"><![endif]-->
# <html lang="zh-CN">
#   <head></head>
#   <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html lang="zh-CN"><div><![endif]-->
# <html lang="zh-CN">
#   <head></head>
#   <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html lang="zh-CN"><div></div><![endif]-->
# <html lang="zh-CN">
#   <head></head>
#   <body></body>
# </html>
# <body width="100%" align="center">
#   <center  >
#     <!--[if (gte mso 9)|(IE)]><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tr><td><![endif]-->
#     <div>  </div>
#     <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->
#   </center  >
# </body>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><![endif]-->
# <!--[if gte IE 9]><!--><html><!--<![endif]-->
#   <head></head>
#   <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><![endif]-->
# <!--[if gte IE 9]><!--><html hello><!--<![endif]-->
#   <head></head>
#   <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><head><![endif]-->
# <!--[if gte IE 9]><!--><html><head><!--<![endif]-->
#   </head>
#   <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><![endif]-->
# <!--[if gte IE 9
# ]><!--><html><!--<![endif]-->
#   <head></head>
#   <body></body>
# </html>
#     """
#     ).strip()

#     html_out = (
#         """
# <!DOCTYPE html>
# <html>
#     <body>
#         <!--[if IE 5]>This is IE 5<br /><![endif]-->
#         <!--[if IE 6]>This is IE 6<br /><![endif]-->
#         <!--[if IE 7]>This is IE 7<br /><![endif]-->
#         <!--[if IE 8]>This is IE 8<br /><![endif]-->
#         <!--[if IE 9]>This is IE 9<br /><![endif]-->
#     </body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html lang="zh-CN"><![endif]-->
# <html lang="zh-CN">
#     <head></head>
#     <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html lang="zh-CN"><div><![endif]-->
# <html lang="zh-CN">
#     <head></head>
#     <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html lang="zh-CN"><div></div><![endif]-->
# <html lang="zh-CN">
#     <head></head>
#     <body></body>
# </html>
# <body width="100%" align="center">
#     <center>
#         <!--[if (gte mso 9)|(IE)]><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tr><td><![endif]-->
#         <div></div>
#         <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->
#     </center>
# </body>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><![endif]-->
# <!--[if gte IE 9]><!--><html><!--<![endif]-->
#     <head></head>
#     <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><![endif]-->
# <!--[if gte IE 9]><!--><html hello><!--<![endif]-->
#     <head></head>
#     <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><head><![endif]-->
# <!--[if gte IE 9]><!-->
# <html>
#     <head>
#         <!--<![endif]-->
#     </head>
#     <body></body>
# </html>
# <!DOCTYPE html>
# <!--[if lt IE 9]><html class="legacy-ie"><![endif]-->
# <!--[if gte IE 9]><!--><html><!--<![endif]-->
#     <head></head>
#     <body></body>
# </html>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


# def test_for_debugging(runner: CliRunner, tmp_file: TextIO) -> None:
#     # opened https://github.com/Riverside-Healthcare/djLint/issues/247
#     html_in = (
#         b"""
# <!DOCTYPE html>
# <html>
#   <body>
# <!-- Do not display this at the moment
# <img border="0" src="pic_trulli.jpg" alt="Trulli">
# -->
#   <!-- Do not display this at the moment
#   <img border="0" src="pic_trulli.jpg" alt="Trulli">
#   -->
#     <!-- Do not display this at the moment
#     <img border="0" src="pic_trulli.jpg" alt="Trulli">
#     -->
#   </body>
# </html>
#     """
#     ).strip()

#     html_out = (
#         """<!DOCTYPE html>
# <html>
#     <body>
#         <!-- Do not display this at the moment
#         <img border="0" src="pic_trulli.jpg" alt="Trulli">
#         -->
#         <!-- Do not display this at the moment
#         <img border="0" src="pic_trulli.jpg" alt="Trulli">
#         -->
#         <!-- Do not display this at the moment
#         <img border="0" src="pic_trulli.jpg" alt="Trulli">
#         -->
#   </body>
# </html>
# """
#     )

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


def test_hidden(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<!DOCTYPE html>
<html>
    <body>
        <!--This is a comment-->
        <!-- This is a comment -->
        <!--  This is a comment  -->
        <!--   This   is   a   comment   -->
        <p>This is a paragraph.</p>
        <!-- Comments are not displayed in the browser -->
    </body>
</html>
    """
    ).strip()

    html_out = """<!DOCTYPE html>
<html>
    <body>
        <!--This is a comment-->
        <!-- This is a comment -->
        <!--  This is a comment  -->
        <!--   This   is   a   comment   -->
        <p>This is a paragraph.</p>
        <!-- Comments are not displayed in the browser -->
    </body>
</html>
"""

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


# def test_surrounding_empty_line(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <ul><!-- 123
# --><li>First</li><!-- 123
# 456
#    789
# --><li>Second</li><!--
#     123
#        456
#           789
# --><li>Second</li><!--
#            123
#         456
#     789
# --></ul>
# <span><!--
# --><span>a</span><!--
# --><span>b</span><!--
# --></span>
# <span><!-- 1
# --><span>a</span><!-- 2
# --><span>b</span><!-- 3
# --></span>
# <span><!--
# 1 --><span>a</span><!--
# 2 --><span>b</span><!--
# 3 --></span>
# 123<!---->456
# 123<!--x-->456
# <!-- A
#      B -->
# <!--
# The null hero's name is {{nullHero.name}}
# See console log:
#   TypeError: Cannot read property 'name' of null in [null]
# -->
# <!--
#     The null hero's name is {{nullHero.name}}
#     See console log:
#     TypeError: Cannot read property 'name' of null in [null]
# -->
#     """
#     ).strip()

#     html_out = (
#         """
# <ul>
#     <!-- 123
# -->
#     <li>First</li>
#     <!-- 123
# 456
#    789
# -->
#     <li>Second</li>
#     <!--
#     123
#        456
#           789
# -->
#     <li>Second</li>
#     <!--
#            123
#         456
#     789
# --></ul>
# <span
#     ><!--
# --><span>a</span
#     ><!--
# --><span>b</span
#     ><!--
# --></span>
# <span
#     ><!-- 1
# --><span>a</span
#     ><!-- 2
# --><span>b</span
#     ><!-- 3
# --></span>
# <span
#     ><!--
# 1 --><span>a</span
#     ><!--
# 2 --><span>b</span
#     ><!--
# 3 --></span
# >
# 123<!---->456 123<!--x-->456
# <!-- A
#      B -->
# <!--
# The null hero's name is {{nullHero.name}}
# See console log:
#     TypeError: Cannot read property 'name' of null in [null]
# -->
# <!--
#     The null hero's name is {{nullHero.name}}
#     See console log:
#     TypeError: Cannot read property 'name' of null in [null]
# -->
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out
