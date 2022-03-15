"""Djlint tests for single attribute per line.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_single_attribute_per_line.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_single_attribute_per_line.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_single_attribute_per_line(runner: CliRunner, tmp_file: TextIO) -> None:
    # single-attribute-per-line: true
    html_in = (
        b"""
<div data-a="1">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div data-a="1" data-b="2" data-c="3">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div data-a="Lorem ipsum dolor sit amet" data-b="Lorem ipsum dolor sit amet" data-c="Lorem ipsum dolor sit amet">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div data-long-attribute-a="1" data-long-attribute-b="2" data-long-attribute-c="3">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<img src="/images/foo.png" />
<img src="/images/foo.png" alt="bar" />
<img src="/images/foo.png" alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit." />
    """
    ).strip()

    html_out = (
        """
<div data-a="1">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
<div
    data-a="1"
    data-b="2"
    data-c="3"
>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div
    data-a="Lorem ipsum dolor sit amet"
    data-b="Lorem ipsum dolor sit amet"
    data-c="Lorem ipsum dolor sit amet"
>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div
    data-long-attribute-a="1"
    data-long-attribute-b="2"
    data-long-attribute-c="3"
>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<img src="/images/foo.png" />
<img
    src="/images/foo.png"
    alt="bar"
/>
<img
    src="/images/foo.png"
    alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
/>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
    # single-attribute-per-line: false
    html_in = (
        b"""
<div data-a="1">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div data-a="1" data-b="2" data-c="3">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div data-a="Lorem ipsum dolor sit amet" data-b="Lorem ipsum dolor sit amet" data-c="Lorem ipsum dolor sit amet">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div data-long-attribute-a="1" data-long-attribute-b="2" data-long-attribute-c="3">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<img src="/images/foo.png" />
<img src="/images/foo.png" alt="bar" />
<img src="/images/foo.png" alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit." />
    """
    ).strip()

    html_out = (
        """
<div data-a="1">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
<div data-a="1" data-b="2" data-c="3">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div
    data-a="Lorem ipsum dolor sit amet"
    data-b="Lorem ipsum dolor sit amet"
    data-c="Lorem ipsum dolor sit amet"
>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<div
    data-long-attribute-a="1"
    data-long-attribute-b="2"
    data-long-attribute-c="3"
>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</div>
<img src="/images/foo.png" />
<img src="/images/foo.png" alt="bar" />
<img
    src="/images/foo.png"
    alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
/>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
