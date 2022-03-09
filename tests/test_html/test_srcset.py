"""Djlint tests for srcset.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_srcset.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_srcset.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_invalid(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
<img src="a"
srcset="
 should-not-format  400w 100h,
       should-not-format  500w 200h
"
 alt=""/>
<img src="a"
srcset="
 should-not-format ,, should-not-format 0q,,,
"
 alt=""/>
    """).strip()

    html_out = ("""
<img
  src="a"
  srcset="
 should-not-format  400w 100h,
       should-not-format  500w 200h
"
  alt=""
/>
<img
  src="a"
  srcset="
 should-not-format ,, should-not-format 0q,,,
"
  alt=""
/>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
