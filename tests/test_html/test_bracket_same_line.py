"""Djlint tests for brackets same line.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_bracket_same_line.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_bracket_same_line.py::test_long_block --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_block(runner: CliRunner, tmp_file: TextIO) -> None:
    # set bracket-same-line: false
    html_in = (
        b"""
<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</div>
<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>
<div class="a">
text
</div>
<div class="a">text</div>
    """
    ).strip()

    html_out = (
        """
<div
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
>
    text
</div>
<div
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
></div>
<div class="a">text</div>
<div class="a">text</div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    # set bracket-same-line: true
    html_in = (
        b"""
<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</div>
<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>
<div class="a">
text
</div>
<div class="a">text</div>
    """
    ).strip()

    html_out = (
        """
<div
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
    text
</div>
<div
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>
<div class="a">text</div>
<div class="a">text</div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_embed(runner: CliRunner, tmp_file: TextIO) -> None:
    # set bracket-same-line: false
    html_in = (
        b"""
<script long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
alert(1)</script>
<style long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
.a{color: #f00}</style>
<script>
alert(1)</script>
<style>
.a{color: #f00}</style>
    """
    ).strip()

    html_out = (
        """
<script
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
>
    alert(1);
</script>
<style
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
>
    .a {
      color: #f00;
    }
</style>
<script>
    alert(1);
</script>
<style>
    .a {
      color: #f00;
    }
</style>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
    # set bracket-same-line: true
    html_in = (
        b"""
<script long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
alert(1)</script>
<style long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
.a{color: #f00}</style>
<script>
alert(1)</script>
<style>
.a{color: #f00}</style>
    """
    ).strip()

    html_out = (
        """
<script
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
    alert(1);
</script>
<style
  long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
  .a {
    color: #f00;
  }
</style>
<script>
    alert(1);
</script>
<style>
  .a {
    color: #f00;
  }
</style>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_inline(runner: CliRunner, tmp_file: TextIO) -> None:
    # set bracket-same-line: false
    html_in = (
        b"""
<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</span>
<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>
<span  class="a">text</span>
<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</span>
<span  class="a">text</span><span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</span>
<span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span>
    """
    ).strip()

    html_out = (
        """
<span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
>
    text
</span>
<span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
></span>
<span class="a">text</span>
<span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
>
    text
</span>
<span class="a">text</span
><span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
>
    text
</span>
<span class="a">text</span><span class="a">text</span><span class="a">text</span
><span class="a">text</span><span class="a">text</span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    # set bracket-same-line: true
    html_in = (
        b"""
<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</span>
<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>
<span  class="a">text</span>
<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</span>
<span  class="a">text</span><span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
text
</span>
<span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span>
    """
    ).strip()

    html_out = (
        """
<span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
    text
</span>
<span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>
<span class="a">text</span>
<span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
    text
</span>
<span class="a">text</span
><span
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">
    text
</span>
<span class="a">text</span><span class="a">text</span><span class="a">text</span
><span class="a">text</span><span class="a">text</span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_void_elements(runner: CliRunner, tmp_file: TextIO) -> None:
    # set bracket-same-line: false
    html_in = (
        b"""
<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value" src="./1.jpg"/>
<img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/>
    """
    ).strip()

    html_out = (
        """
<img
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
    src="./1.jpg"
/>
<img src="./1.jpg" /><img src="./1.jpg" /><img src="./1.jpg" /><img
    src="./1.jpg"
/><img src="./1.jpg" />
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)

    # set bracket-same-line: true
    html_in = (
        b"""
<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value" src="./1.jpg"/>
<img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/>
    """
    ).strip()

    html_out = (
        """
<img
    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"
    src="./1.jpg" />
<img src="./1.jpg" /><img src="./1.jpg" /><img src="./1.jpg" /><img
    src="./1.jpg" /><img src="./1.jpg" />
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
