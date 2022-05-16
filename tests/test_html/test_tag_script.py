"""Djlint tests for html script tags.

Some tests may be from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run:

    pytest tests/test_html/test_tag_script.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_tag_script.py::test_script_tag


"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import reformat, write_to_file


def test_script_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <script>console.log();\n    console.log();\n\n    </script>\n</div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<div>
    <script>console.log();
    console.log();

    </script>
</div>
"""
    )

    # check script includes
    output = reformat(
        tmp_file,
        runner,
        b"""<script src="{% static 'common/js/foo.min.js' %}"></script>""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<script>
    $("#x").do({
        dataBound: function () {
            this.tbody.append($("<td colspan=2'>X</td>"));
        },
    });
</script>
""",
    )

    assert output.exit_code == 0

    # check bad template tags inside scripts
    output = reformat(
        tmp_file,
        runner,
        b"""<script>{{missing_space}}</script>\n""",
    )

    assert output.exit_code == 0


# def test_empty(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script></script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script></script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_js(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script type="text/javascript">
#   var message = "Alert!";
#   alert(message);
# </script>
# <script type="application/javascript">
#   var message = "Alert!";
#   alert(message);
# </script>
# <script>
#   var message = "Alert!";
#   alert(message);
# </script>
# <script type="text/babel">
#             const    someJS    =   'this should be formatted'
# </script>
# <script type="module">
#       import lib from './lib.js';
#         function myFunction() { return 'foo'; }
#   </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script type="text/javascript">
#   var message = "Alert!";
#   alert(message);
# </script>
# <script type="application/javascript">
#   var message = "Alert!";
#   alert(message);
# </script>
# <script>
#   var message = "Alert!";
#   alert(message);
# </script>
# <script type="text/babel">
#   const someJS = "this should be formatted";
# </script>
# <script type="module">
#   import lib from "./lib.js";
#   function myFunction() {
#     return "foo";
#   }
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_simple(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>Sample styled page</title>
#     <script>alert('test');</script>
#     <script>
#       var message = "Alert!";
#       alert(message);
#     </script>
#   </head>
#   <body>
#     <h1>Sample styled page</h1>
#     <p>This page is just a demo.</p>
#   </body>
# </html>
#     """
#     ).strip()

#     html_out = (
#         """
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>Sample styled page</title>
#     <script>
#       alert("test");
#     </script>
#     <script>
#       var message = "Alert!";
#       alert(message);
#     </script>
#   </head>
#   <body>
#     <h1>Sample styled page</h1>
#     <p>This page is just a demo.</p>
#   </body>
# </html>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_single_script(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script>alert('test');</script>
# <script>
#   document.getElementById("demo").innerHTML = "Hello JavaScript!";
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script>
#   alert("test");
# </script>
# <script>
#   document.getElementById("demo").innerHTML = "Hello JavaScript!";
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_something_else(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script type="text/template">
#  <div>
#     </div>
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script type="text/template">
#   <div>
#      </div>
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_template_literal(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <!DOCTYPE html>
# <html lang="en">
#     <head>
#     </head>
#     <body>
#         <script>
#             function foo() {
#                 return \\`
#                     <div>
#                         <p>Text</p>
#                     </div>
#                 \\`;
#             }
#         </script>
#     </body>
# </html>
#     """
#     ).strip()

#     html_out = (
#         """
# <!DOCTYPE html>
# <html lang="en">
#   <head> </head>
#   <body>
#     <script>
#       function foo() {
#         return \\`
#                     <div>
#                         <p>Text</p>
#                     </div>
#                 \\`;
#       }
#     </script>
#   </body>
# </html>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_typescript(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script type="application/x-typescript">
#   class Student {
#     fullName: string;
#     constructor(public firstName: string, public middleInitial: string, public lastName: string) {
#     this.fullName = firstName + " " + middleInitial + " " + lastName;
#   }
#   }
#   interface Person {
#     firstName: string;
#     lastName: string;
#   }
#   function greeter(person : Person) {
#     return "Hello, " + person.firstName + " " + person.lastName;
#   }
#   let user = new Student("Jane", "M.", "User");
#   document.body.innerHTML = greeter(user);
# </script>
# <script lang="ts">
#   class Student {
#     fullName: string;
#     constructor(public firstName: string, public middleInitial: string, public lastName: string) {
#     this.fullName = firstName + " " + middleInitial + " " + lastName;
#   }
#   }
#   interface Person {
#     firstName: string;
#     lastName: string;
#   }
#   function greeter(person : Person) {
#     return "Hello, " + person.firstName + " " + person.lastName;
#   }
#   let user = new Student("Jane", "M.", "User");
#   document.body.innerHTML = greeter(user);
# </script>
# <script lang="tsx">
#   class CommentBox extends React.Component<{ url: string, pollInterval: number}, CommentData> {
#     constructor(){
#       super()
#       this.state = { data: [] };
#     }
#     fetchComments() {
#       $.ajax({
#         url: this.props.url,
#         dataType: 'json',
#         cache: false,
#         success: (data) => this.setState({ data: data }),
#         error: (xhr, status, err) => console.error(status, err)
#       })
#     }
#     componentDidMount() {
#       this.fetchComments();
#       setInterval(this.fetchComments.bind(this), this.props.pollInterval);
#     }
#     render() {
#       let handleCommentSubmit = (comment: { author: string, text: string }) => {
#         console.warn('comment submitted!', comment);
#         const updated = this.state.data.slice(0);
#         updated.push(comment);
#         this.setState({ data: updated });
#       }
#       return (
#         <div className="commentBox">
#         <h1>Comments</h1>
#         <CommentList data={this.state.data}/>
#       <CommentForm onCommentSubmit={handleCommentSubmit} />
#       </div>
#     );
#     }
#   }
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script type="application/x-typescript">
#   class Student {
#     fullName: string;
#     constructor(
#       public firstName: string,
#       public middleInitial: string,
#       public lastName: string
#     ) {
#       this.fullName = firstName + " " + middleInitial + " " + lastName;
#     }
#   }
#   interface Person {
#     firstName: string;
#     lastName: string;
#   }
#   function greeter(person: Person) {
#     return "Hello, " + person.firstName + " " + person.lastName;
#   }
#   let user = new Student("Jane", "M.", "User");
#   document.body.innerHTML = greeter(user);
# </script>
# <script lang="ts">
#   class Student {
#     fullName: string;
#     constructor(
#       public firstName: string,
#       public middleInitial: string,
#       public lastName: string
#     ) {
#       this.fullName = firstName + " " + middleInitial + " " + lastName;
#     }
#   }
#   interface Person {
#     firstName: string;
#     lastName: string;
#   }
#   function greeter(person: Person) {
#     return "Hello, " + person.firstName + " " + person.lastName;
#   }
#   let user = new Student("Jane", "M.", "User");
#   document.body.innerHTML = greeter(user);
# </script>
# <script lang="tsx">
#   class CommentBox extends React.Component<
#     { url: string; pollInterval: number },
#     CommentData
#   > {
#     constructor() {
#       super();
#       this.state = { data: [] };
#     }
#     fetchComments() {
#       $.ajax({
#         url: this.props.url,
#         dataType: "json",
#         cache: false,
#         success: (data) => this.setState({ data: data }),
#         error: (xhr, status, err) => console.error(status, err),
#       });
#     }
#     componentDidMount() {
#       this.fetchComments();
#       setInterval(this.fetchComments.bind(this), this.props.pollInterval);
#     }
#     render() {
#       let handleCommentSubmit = (comment: { author: string; text: string }) => {
#         console.warn("comment submitted!", comment);
#         const updated = this.state.data.slice(0);
#         updated.push(comment);
#         this.setState({ data: updated });
#       };
#       return (
#         <div className="commentBox">
#           <h1>Comments</h1>
#           <CommentList data={this.state.data} />
#           <CommentForm onCommentSubmit={handleCommentSubmit} />
#         </div>
#       );
#     }
#   }
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_babel(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script type="text/babel" data-presets="react" data-type="module">
# import { h,
#          render } from 'https://unpkg.com/preact?module';
# render(
# <h1>Hello World!</h1>,
#          document.body
# );
# </script>
# <script type="text/babel">
# <!--
# alert(1)
# -->
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script type="text/babel" data-presets="react" data-type="module">
#   import { h, render } from "https://unpkg.com/preact?module";
#   render(<h1>Hello World!</h1>, document.body);
# </script>
# <script type="text/babel">
#   <!--
#   alert(1);
#   -->
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_legacy(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script>
# <!--
# alert(1)
# -->
# </script>
# <script>
# <!--
# alert(2)
# //-->
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script>
#   <!--
#   alert(1);
#   -->
# </script>
# <script>
#   <!--
#   alert(2);
#   //-->
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_module(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script type="module">
# import prettier from "prettier/standalone";
# import parserGraphql from "prettier/parser-graphql";
# prettier.format("query { }", {
#                       parser: "graphql",
#   plugins: [
# parserGraphql],
# });
# </script>
# <script type="module">
# async function foo() {
#   let x=10;while(x-->0)console.log(x)
#   await(import('mod'))
# }
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script type="module">
#   import prettier from "prettier/standalone";
#   import parserGraphql from "prettier/parser-graphql";
#   prettier.format("query { }", {
#     parser: "graphql",
#     plugins: [parserGraphql],
#   });
# </script>
# <script type="module">
#   async function foo() {
#     let x = 10;
#     while (x-- > 0) console.log(x);
#     await import("mod");
#   }
# </script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_module_attributes(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script src="foo.wasm" type="module" withtype="webassembly"></script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script src="foo.wasm" type="module" withtype="webassembly"></script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)


# def test_script(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <script type="application/ld+json">
#   {   "json": true }
# </script>
# <script type="application/json">
#   {   "json":true  }
# </script>
# <script type="importmap">
#   {   "json":true  }
# </script>
# <script type="systemjs-importmap">
#   {   "json":true  }
# </script><script type="invalid">
#   {   "json":false  }
# </script>
# <script type="text/html">
#   <div>
#   <p>foo</p>
#   </div>
# </script>
# <script
#   async=""
#   id=""
#   src="/_next/static/development/pages/_app.js?ts=1565732195968"
# ></script><script></script>
# <!-- #8147 -->
# <script lang="vbscript">
# Function hello()
# End Function
# </script>
# <script lang="unknown">
# </script>
#     """
#     ).strip()

#     html_out = (
#         """
# <script type="application/ld+json">
#   { "json": true }
# </script>
# <script type="application/json">
#   { "json": true }
# </script>
# <script type="importmap">
#   { "json": true }
# </script>
# <script type="systemjs-importmap">
#   { "json": true }
# </script>
# <script type="invalid">
#   {   "json":false  }
# </script>
# <script type="text/html">
#   <div>
#     <p>foo</p>
#   </div>
# </script>
# <script
#   async=""
#   id=""
#   src="/_next/static/development/pages/_app.js?ts=1565732195968"
# ></script>
# <script></script>
# <!-- #8147 -->
# <script lang="vbscript">
#   Function hello()
#   End Function
# </script>
# <script lang="unknown"></script>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)
