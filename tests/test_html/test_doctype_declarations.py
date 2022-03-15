"""Djlint tests for doctype.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_doctype_declarations.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   poetry run pytest tests/test_html/test_doctype_declarations.py::test_case --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_case(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(tmp_file, runner, b"<!DocType htMl>")
    assert "<!DOCTYPE html>" == output.text

    output = reformat(tmp_file, runner, b"<!DocType htMl  >")
    assert "<!DOCTYPE html>" == output.text


def test_html4_01_frameset(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        (
            """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
  "http://www.w3.org/TR/html4/frameset.dtd">
<html>
  <head>
    <title>An HTML standard template</title>
    <meta charset="utf-8"  />
  </head>
  <body>
    <p>… Your HTML content here …</p>
  </body>
</html>
    """
        )
        .strip()
        .encode()
    )

    html_out = (
        """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<html>
    <head>
        <title>An HTML standard template</title>
        <meta charset="utf-8" />
    </head>
    <body>
        <p>… Your HTML content here …</p>
    </body>
</html>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
    assert html_out == output.text


def test_html4_01_strict(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        (
            """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
  "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>An HTML standard template</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <p>… Your HTML content here …</p>
  </body>
</html>
    """
        )
        .strip()
        .encode()
    )

    html_out = (
        """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <title>An HTML standard template</title>
        <meta charset="utf-8" />
    </head>
    <body>
        <p>… Your HTML content here …</p>
    </body>
</html>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
    assert html_out == output.text


def test_html4_01_transitional(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        (
            """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
  "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <title>An HTML standard template</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <p>… Your HTML content here …</p>
  </body>
</html>
    """
        )
        .strip()
        .encode()
    )

    html_out = (
        """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <title>An HTML standard template</title>
        <meta charset="utf-8" />
    </head>
    <body>
        <p>… Your HTML content here …</p>
    </body>
</html>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
    assert html_out == output.text


def test_html5(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        (
            """
<!DOCTYPE html>
<html>
  <head>
    <title>An HTML standard template</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <p>… Your HTML content here …</p>
  </body>
</html>
    """
        )
        .strip()
        .encode()
    )

    html_out = (
        """
<!DOCTYPE html>
<html>
    <head>
        <title>An HTML standard template</title>
        <meta charset="utf-8" />
    </head>
    <body>
        <p>… Your HTML content here …</p>
    </body>
</html>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
    assert html_out == output.text


def test_xhtml1_1(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
    <title>XHTML markup</title>
  </head>
  <body style="background-color:#ffffcc; color:#008800">
    <br />
    <h2 align="center">Sample XHTML page</h2>
    <br />
    <div align="center">
      <img src="../images/bee3.jpg" width="400" height="250" alt="Beep" vspace="20" />
    </div>
    <p align="center" style="font-size:17px">Bar Foo,<br />
      Foo,<br />
      Bar<br />
      Foo</p>
    <p align="center"><em>String</em></p>
    <br />
    <hr />
  </body>
</html>
    """
    ).strip()

    html_out = (
        """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
        <title>XHTML markup</title>
    </head>
    <body style="background-color: #ffffcc; color: #008800">
        <br />
        <h2 align="center">Sample XHTML page</h2>
        <br />
        <div align="center">
            <img
                src="../images/bee3.jpg"
                width="400"
                height="250"
                alt="Beep"
                vspace="20"
            />
        </div>
        <p align="center" style="font-size: 17px">
            Bar Foo,<br />
            Foo,<br />
            Bar<br />
            Foo
        </p>
        <p align="center"><em>String</em></p>
        <br />
        <hr />
    </body>
</html>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
    assert html_out == output.text
