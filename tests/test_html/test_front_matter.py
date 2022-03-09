"""Djlint tests for front matter.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_front_matter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_front_matter.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_custom_parser(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
---mycustomparser

title: Hello
slug: home
---
<h1>
  Hello world!</h1>
    """).strip()

    html_out = ("""
---mycustomparser

title: Hello
slug: home
---
<h1>Hello world!</h1>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_empty(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
---
---
<h1>
  Hello world!</h1>
    """).strip()

    html_out = ("""
---
---
<h1>Hello world!</h1>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_empty_2(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
---
---
<div>
---
</div>
    """).strip()

    html_out = ("""
---
---
<div>---</div>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_issue_9042_no_empty_line(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
---
layout: foo
---
Test <a
href="https://prettier.io">abc</a>.
    """).strip()

    html_out = ("""
---
layout: foo
---
Test <a href="https://prettier.io">abc</a>.
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_issue_9042(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
---
layout: foo
---
Test <a
href="https://prettier.io">abc</a>.
    """).strip()

    html_out = ("""
---
layout: foo
---
Test <a href="https://prettier.io">abc</a>.
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
