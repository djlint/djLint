"""DjLint tests for yaml front matter.

Some tests may be from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run:

    pytest tests/test_html/test_yaml.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_yaml.py::test_custom_parser

"""
# pylint: disable=C0116
from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_invalid(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""---
    invalid:
invalid:
---



<html><head></head><body></body></html>""",
    )
    assert (
        output.text
        == """---
    invalid:
invalid:
---
<html>
    <head></head>
    <body></body>
</html>
"""
    )


def test_valid(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""
---
hello:     world
---
<html><head></head><body></body></html>""",
    )
    assert (
        output.text
        == """---
hello:     world
---
<html>
    <head></head>
    <body></body>
</html>
"""
    )


def test_more(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""---
layout: <div><div></div></div>
---
<div></div>""",
    )
    assert output.exit_code == 0


def test_custom_parser(runner: CliRunner, tmp_file: TextIO) -> None:
    html_in = (
        b"""
---mycustomparser
title: Hello
slug: home
---
<h1>
  Hello world!</h1>
    """
    ).strip()

    html_out = """---mycustomparser
title: Hello
slug: home
---
<h1>Hello world!</h1>
"""

    output = reformat(tmp_file, runner, html_in)

    assert output.text == html_out


def test_empty(runner: CliRunner, tmp_file: TextIO) -> None:
    html_in = (
        b"""
---
---
<h1>
  Hello world!</h1>
    """
    ).strip()

    html_out = """---
---
<h1>Hello world!</h1>
"""

    output = reformat(tmp_file, runner, html_in)
    assert output.text == html_out


def test_empty_2(runner: CliRunner, tmp_file: TextIO) -> None:
    html_in = (
        b"""
---
---
<div>
---
</div>
    """
    ).strip()

    html_out = """---
---
<div>---</div>
"""

    output = reformat(tmp_file, runner, html_in)
    assert output.text == html_out


def test_issue_9042_no_empty_line(runner: CliRunner, tmp_file: TextIO) -> None:
    html_in = (
        b"""
---
layout: foo
---
Test <a
href="https://djlint.com">abc</a>.
    """
    ).strip()

    html_out = """---
layout: foo
---
Test <a href="https://djlint.com">abc</a>.
"""

    output = reformat(tmp_file, runner, html_in)
    assert output.text == html_out


def test_issue_9042(runner: CliRunner, tmp_file: TextIO) -> None:
    html_in = (
        b"""
---
layout: foo
---
Test <a
href="https://djlint.com">abc</a>.
    """
    ).strip()

    html_out = """---
layout: foo
---
Test <a href="https://djlint.com">abc</a>.
"""

    output = reformat(tmp_file, runner, html_in)
    assert output.text == html_out
