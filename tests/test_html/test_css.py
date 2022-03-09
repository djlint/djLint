"""Djlint tests for css.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_css.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_css.py::test_long_ --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_empty(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<style></style>
    """
    ).strip()

    html_out = (
        """
<style></style>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_less(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<style type="text/less">
  @nice-blue: #5B83AD;
  @light-blue: @nice-blue + #111;
  #header {
    color: @light-blue;
  }
</style>
<style lang="less">
  @nice-blue: #5B83AD;
  @light-blue: @nice-blue + #111;
  #header {
    color: @light-blue;
  }
</style>
    """
    ).strip()

    html_out = (
        """
<style type="text/less">
  @nice-blue: #5B83AD;
  @light-blue: @nice-blue + #111;
  #header {
    color: @light-blue;
  }
</style>
<style lang="less">
  @nice-blue: #5b83ad;
  @light-blue: @nice-blue + #111;
  #header {
    color: @light-blue;
  }
</style>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_postcss(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<style type="text/css">
  body { background: navy; color: yellow; }
</style>
<style lang="postcss">
  body { background: navy; color: yellow; }
</style>
    """
    ).strip()

    html_out = (
        """
<style type="text/css">
  body {
    background: navy;
    color: yellow;
  }
</style>
<style lang="postcss">
  body {
    background: navy;
    color: yellow;
  }
</style>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_scss(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<style type="text/x-scss">
  $font-stack:    Helvetica, sans-serif;
  $primary-color: #333;
  body {
    font: 100% $font-stack;
    color: $primary-color;
  }
</style>
<style lang="scss">
  $font-stack:    Helvetica, sans-serif;
  $primary-color: #333;
  body {
    font: 100% $font-stack;
    color: $primary-color;
  }
</style>
<style lang="scss">
.someElement {
    @include bp-medium {
      display: flex;
    }

    @include bp-large {
      margin-top: 10px;
      margin-bottom: 10px;
    }
}
</style>
    """
    ).strip()

    html_out = (
        """
<style type="text/x-scss">
  $font-stack: Helvetica, sans-serif;
  $primary-color: #333;
  body {
    font: 100% $font-stack;
    color: $primary-color;
  }
</style>
<style lang="scss">
  $font-stack: Helvetica, sans-serif;
  $primary-color: #333;
  body {
    font: 100% $font-stack;
    color: $primary-color;
  }
</style>
<style lang="scss">
  .someElement {
    @include bp-medium {
      display: flex;
    }
    @include bp-large {
      margin-top: 10px;
      margin-bottom: 10px;
    }
  }
</style>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_simple(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<!DOCTYPE html>
<html>
  <head>
    <title>Sample styled page</title>
    <style>a { color: red; }</style>
    <style>
      body { background: navy; color: yellow; }
    </style>
  </head>
  <body>
    <h1>Sample styled page</h1>
    <p>This page is just a demo.</p>
  </body>
</html>
    """
    ).strip()

    html_out = (
        """
<!DOCTYPE html>
<html>
  <head>
    <title>Sample styled page</title>
    <style>
      a {
        color: red;
      }
    </style>
    <style>
      body {
        background: navy;
        color: yellow;
      }
    </style>
  </head>
  <body>
    <h1>Sample styled page</h1>
    <p>This page is just a demo.</p>
  </body>
</html>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_single_style(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<style>a { color: red; }</style>
<style>
  h1 {
    font-size: 120%;
    font-family: Verdana, Arial, Helvetica, sans-serif;
    color: #333366;
  }
</style>
    """
    ).strip()

    html_out = (
        """
<style>
  a {
    color: red;
  }
</style>
<style>
  h1 {
    font-size: 120%;
    font-family: Verdana, Arial, Helvetica, sans-serif;
    color: #333366;
  }
</style>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


    assert output.text == html_out
