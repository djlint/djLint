"""Djlint tests for svg.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_svg.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_svg.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_svg(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<!DOCTYPE html>
<html>
  <head>
    <title>SVG</title>
  </head>
  <body>
    <svg width="100" height="100">
      <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
    </svg>
  </body>
</html>
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
<defs /> <style >
    polygon { fill: black }
    div {
  color: white;
      font:18px serif;
      height: 100%;
      overflow: auto;
    }
  </style>
 <g>
  <g><polygon points="5,5 195,10 185,185 10,195" />
      <text>    Text</text></g>
  </g>
  <!-- Common use case: embed HTML text into SVG -->
  <foreignObject x="20" y="20" width="160" height="160">
    <!--
      In the context of SVG embeded into HTML, the XHTML namespace could be avoided, but it is mandatory in the context of an SVG document
    -->
    <div xmlns="http://www.w3.org/1999/xhtml">
    <p>
  123
      </p>
      <span>
        123
        </span>
    </div>
  </foreignObject>
</svg>

    """
    ).strip()

    html_out = (
        """
<!DOCTYPE html>
<html>
    <head>
        <title>SVG</title>
    </head>
    <body>
        <svg width="100" height="100">
            <circle
                cx="50"
                cy="50"
                r="40"
                stroke="green"
                stroke-width="4"
                fill="yellow"
            />
        </svg>
    </body>
</html>
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <defs />
    <style>
        polygon {
          fill: black;
        }
        div {
          color: white;
          font: 18px serif;
          height: 100%;
          overflow: auto;
        }
    </style>
    <g>
        <g>
            <polygon points="5,5 195,10 185,185 10,195" />
            <text>Text</text>
        </g>
    </g>
    <!-- Common use case: embed HTML text into SVG -->
    <foreignObject x="20" y="20" width="160" height="160">
        <!--
            In the context of SVG embeded into HTML, the XHTML namespace could be avoided, but it is mandatory in the context of an SVG document
        -->
        <div xmlns="http://www.w3.org/1999/xhtml">
            <p>123</p>
            <span> 123 </span>
        </div>
    </foreignObject>
</svg>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
