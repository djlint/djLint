"""Djlint tests for case.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_case.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_case.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat

def test_case(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""

<!DOCTYPE html>
<HTML CLASS="no-js mY-ClAsS">
  <HEAD>
    <META CHARSET="utf-8">
    <TITLE>My tITlE</TITLE>
    <META NAME="description" content="My CoNtEnT">
  </HEAD>
  <body>
    <P>Hello world!<BR> This is HTML5 Boilerplate.</P>
    <SCRIPT>
      window.ga = function () { ga.q.push(arguments) }; ga.q = []; ga.l = +new Date;
      ga('create', 'UA-XXXXX-Y', 'auto'); ga('send', 'pageview')
    </SCRIPT>
    <SCRIPT src="https://www.google-analytics.com/analytics.js" ASYNC DEFER></SCRIPT>
  </body>
</HTML>

    """).strip()

    html_out = ("""

<!DOCTYPE html>
<html class="no-js mY-ClAsS">
  <head>
    <meta charset="utf-8" />
    <title>My tITlE</title>
    <meta name="description" content="My CoNtEnT" />
  </head>
  <body>
    <p>
      Hello world!<br />
      This is HTML5 Boilerplate.
    </p>
    <script>
      window.ga = function () {
        ga.q.push(arguments);
      };
      ga.q = [];
      ga.l = +new Date();
      ga("create", "UA-XXXXX-Y", "auto");
      ga("send", "pageview");
    </script>
    <script
      src="https://www.google-analytics.com/analytics.js"
      async
      defer
    ></script>
  </body>
</html>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)


    assert output.text == html_out
