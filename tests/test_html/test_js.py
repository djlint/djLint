"""Djlint tests for js.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_js.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_js.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_empty(runner: CliRunner, tmp_file: TextIO) -> None:


    html_in = (b"""
<script></script>
    """).strip()

    html_out = ("""
<script></script>
        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_js(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""

<script type="text/javascript">
  var message = "Alert!";
  alert(message);
</script>
<script type="application/javascript">
  var message = "Alert!";
  alert(message);
</script>
<script>
  var message = "Alert!";
  alert(message);
</script>
<script type="text/babel">
            const    someJS    =   'this should be formatted'
</script>
<script type="module">
      import lib from './lib.js';

        function myFunction() { return 'foo'; }
  </script>

    """).strip()

    html_out = ("""

<script type="text/javascript">
  var message = "Alert!";
  alert(message);
</script>
<script type="application/javascript">
  var message = "Alert!";
  alert(message);
</script>
<script>
  var message = "Alert!";
  alert(message);
</script>
<script type="text/babel">
  const someJS = "this should be formatted";
</script>
<script type="module">
  import lib from "./lib.js";
  function myFunction() {
    return "foo";
  }
</script>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_simple(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""

<!DOCTYPE html>
<html>
  <head>
    <title>Sample styled page</title>
    <script>alert('test');</script>
    <script>
      var message = "Alert!";
      alert(message);
    </script>
  </head>
  <body>
    <h1>Sample styled page</h1>
    <p>This page is just a demo.</p>
  </body>
</html>

    """).strip()

    html_out = ("""

<!DOCTYPE html>
<html>
  <head>
    <title>Sample styled page</title>
    <script>
      alert("test");
    </script>
    <script>
      var message = "Alert!";
      alert(message);
    </script>
  </head>
  <body>
    <h1>Sample styled page</h1>
    <p>This page is just a demo.</p>
  </body>
</html>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_single_script(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""

<script>alert('test');</script>
<script>
  document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>

    """).strip()

    html_out = ("""

<script>
  alert("test");
</script>
<script>
  document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_something_else(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""

<script type="text/template">
 <div>
    </div>
</script>

    """).strip()

    html_out = ("""

<script type="text/template">
  <div>
     </div>
</script>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_template_literal(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""

<!DOCTYPE html>
<html lang="en">
    <head>
    </head>
    <body>
        <script>
            function foo() {
                return \\`
                    <div>
                        <p>Text</p>
                    </div>
                \\`;
            }
        </script>
    </body>
</html>

    """).strip()

    html_out = ("""

<!DOCTYPE html>
<html lang="en">
  <head> </head>
  <body>
    <script>
      function foo() {
        return \\`
                    <div>
                        <p>Text</p>
                    </div>
                \\`;
      }
    </script>
  </body>
</html>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)
def test_typescript(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (b"""

<script type="application/x-typescript">
  class Student {
    fullName: string;
    constructor(public firstName: string, public middleInitial: string, public lastName: string) {
    this.fullName = firstName + " " + middleInitial + " " + lastName;
  }
  }
  interface Person {
    firstName: string;
    lastName: string;
  }
  function greeter(person : Person) {
    return "Hello, " + person.firstName + " " + person.lastName;
  }
  let user = new Student("Jane", "M.", "User");
  document.body.innerHTML = greeter(user);
</script>
<script lang="ts">
  class Student {
    fullName: string;
    constructor(public firstName: string, public middleInitial: string, public lastName: string) {
    this.fullName = firstName + " " + middleInitial + " " + lastName;
  }
  }
  interface Person {
    firstName: string;
    lastName: string;
  }
  function greeter(person : Person) {
    return "Hello, " + person.firstName + " " + person.lastName;
  }
  let user = new Student("Jane", "M.", "User");
  document.body.innerHTML = greeter(user);
</script>
<script lang="tsx">
  class CommentBox extends React.Component<{ url: string, pollInterval: number}, CommentData> {
    constructor(){
      super()
      this.state = { data: [] };
    }
    fetchComments() {
      $.ajax({
        url: this.props.url,
        dataType: 'json',
        cache: false,
        success: (data) => this.setState({ data: data }),
        error: (xhr, status, err) => console.error(status, err)
      })
    }
    componentDidMount() {
      this.fetchComments();
      setInterval(this.fetchComments.bind(this), this.props.pollInterval);
    }
    render() {
      let handleCommentSubmit = (comment: { author: string, text: string }) => {
        console.warn('comment submitted!', comment);
        const updated = this.state.data.slice(0);
        updated.push(comment);
        this.setState({ data: updated });
      }
      return (
        <div className="commentBox">
        <h1>Comments</h1>
        <CommentList data={this.state.data}/>
      <CommentForm onCommentSubmit={handleCommentSubmit} />
      </div>
    );
    }
  }
</script>

    """).strip()

    html_out = ("""

<script type="application/x-typescript">
  class Student {
    fullName: string;
    constructor(
      public firstName: string,
      public middleInitial: string,
      public lastName: string
    ) {
      this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
  }
  interface Person {
    firstName: string;
    lastName: string;
  }
  function greeter(person: Person) {
    return "Hello, " + person.firstName + " " + person.lastName;
  }
  let user = new Student("Jane", "M.", "User");
  document.body.innerHTML = greeter(user);
</script>
<script lang="ts">
  class Student {
    fullName: string;
    constructor(
      public firstName: string,
      public middleInitial: string,
      public lastName: string
    ) {
      this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
  }
  interface Person {
    firstName: string;
    lastName: string;
  }
  function greeter(person: Person) {
    return "Hello, " + person.firstName + " " + person.lastName;
  }
  let user = new Student("Jane", "M.", "User");
  document.body.innerHTML = greeter(user);
</script>
<script lang="tsx">
  class CommentBox extends React.Component<
    { url: string; pollInterval: number },
    CommentData
  > {
    constructor() {
      super();
      this.state = { data: [] };
    }
    fetchComments() {
      $.ajax({
        url: this.props.url,
        dataType: "json",
        cache: false,
        success: (data) => this.setState({ data: data }),
        error: (xhr, status, err) => console.error(status, err),
      });
    }
    componentDidMount() {
      this.fetchComments();
      setInterval(this.fetchComments.bind(this), this.props.pollInterval);
    }
    render() {
      let handleCommentSubmit = (comment: { author: string; text: string }) => {
        console.warn("comment submitted!", comment);
        const updated = this.state.data.slice(0);
        updated.push(comment);
        this.setState({ data: updated });
      };
      return (
        <div className="commentBox">
          <h1>Comments</h1>
          <CommentList data={this.state.data} />
          <CommentForm onCommentSubmit={handleCommentSubmit} />
        </div>
      );
    }
  }
</script>

        """).strip()

    output = reformat(
        tmp_file,
        runner,
        html_in)

