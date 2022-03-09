"""Djlint tests for scripts.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_script.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_script.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_babel(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
<script type="text/babel" data-presets="react" data-type="module">
import { h,
         render } from 'https://unpkg.com/preact?module';
render(
<h1>Hello World!</h1>,
         document.body
);
</script>
<script type="text/babel">
<!--
alert(1)
-->
</script>
    """).strip()

    html_out = ("""
<script type="text/babel" data-presets="react" data-type="module">
  import { h, render } from "https://unpkg.com/preact?module";
  render(<h1>Hello World!</h1>, document.body);
</script>
<script type="text/babel">
  <!--
  alert(1);
  -->
</script>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_legacy(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
<script>
<!--
alert(1)
-->
</script>
<script>
<!--
alert(2)
//-->
</script>
    """).strip()

    html_out = ("""
<script>
  <!--
  alert(1);
  -->
</script>
<script>
  <!--
  alert(2);
  //-->
</script>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_module(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
<script type="module">
import prettier from "prettier/standalone";
import parserGraphql from "prettier/parser-graphql";
prettier.format("query { }", {
                      parser: "graphql",
  plugins: [
parserGraphql],
});
</script>
<script type="module">
async function foo() {
  let x=10;while(x-->0)console.log(x)
  await(import('mod'))
}
</script>
    """).strip()

    html_out = ("""
<script type="module">
  import prettier from "prettier/standalone";
  import parserGraphql from "prettier/parser-graphql";
  prettier.format("query { }", {
    parser: "graphql",
    plugins: [parserGraphql],
  });
</script>
<script type="module">
  async function foo() {
    let x = 10;
    while (x-- > 0) console.log(x);
    await import("mod");
  }
</script>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_module_attributes(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
<script src="foo.wasm" type="module" withtype="webassembly"></script>
    """).strip()

    html_out = ("""
<script src="foo.wasm" type="module" withtype="webassembly"></script>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_script(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""
<script type="application/ld+json">
  {   "json": true }
</script>
<script type="application/json">
  {   "json":true  }
</script>
<script type="importmap">
  {   "json":true  }
</script>
<script type="systemjs-importmap">
  {   "json":true  }
</script><script type="invalid">
  {   "json":false  }
</script>
<script type="text/html">
  <div>
  <p>foo</p>
  </div>
</script>
<script
  async=""
  id=""
  src="/_next/static/development/pages/_app.js?ts=1565732195968"
></script><script></script>
<!-- #8147 -->
<script lang="vbscript">
Function hello()
End Function
</script>
<script lang="unknown">
</script>
    """).strip()

    html_out = ("""
<script type="application/ld+json">
  { "json": true }
</script>
<script type="application/json">
  { "json": true }
</script>
<script type="importmap">
  { "json": true }
</script>
<script type="systemjs-importmap">
  { "json": true }
</script>
<script type="invalid">
  {   "json":false  }
</script>
<script type="text/html">
  <div>
    <p>foo</p>
  </div>
</script>
<script
  async=""
  id=""
  src="/_next/static/development/pages/_app.js?ts=1565732195968"
></script>
<script></script>
<!-- #8147 -->
<script lang="vbscript">
  Function hello()
  End Function
</script>
<script lang="unknown"></script>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
