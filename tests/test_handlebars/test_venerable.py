"""Djlint tests for handlebars.

Some tests may be from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_handlebars_venerable.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_handlebars_venerable.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

# from typing import TextIO

# from click.testing import CliRunner

# from tests.conftest import reformat


# def test_template(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script id="entry-template" type="text/x-handlebars-template">
# <div class="entry">
# <h1>{{title}}</h1>
# <div class="body">{{body}}</div></div>
# </script>
# <script type="text/x-handlebars-template">
#   {{component arg1='hey' arg2=(helper this.arg7 this.arg4) arg3=anotherone arg6=this.arg8}}
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script id="entry-template" type="text/x-handlebars-template">
#   <div class="entry">
#     <h1>{{title}}</h1>
#     <div class="body">{{body}}</div></div>
# </script>
# <script type="text/x-handlebars-template">
#   {{component
#     arg1="hey"
#     arg2=(helper this.arg7 this.arg4)
#     arg3=anotherone
#     arg6=this.arg8
#   }}
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)
