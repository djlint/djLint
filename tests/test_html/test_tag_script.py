"""Test html script tags.

poetry run pytest tests/test_html/test_tag_script.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<div>\n"
            "    <script>console.log();\n"
            "    console.log();\n"
            "\n"
            "    </script>\n"
            "    </div>\n"
        ),
        (
            "<div>\n"
            "    <script>console.log();\n"
            "    console.log();\n"
            "\n"
            "    </script>\n"
            "</div>\n"
        ),
        id="script",
    ),
    pytest.param(
        "<script src=\"{% static 'common/js/foo.min.js' %}\"></script>",
        "<script src=\"{% static 'common/js/foo.min.js' %}\"></script>\n",
        id="script_includes",
    ),
    pytest.param(
        (
            "<script>\n"
            '    $("#x").do({\n'
            "        dataBound: function () {\n"
            '            this.tbody.append($("<td colspan=2\'>X</td>"));\n'
            "        },\n"
            "    });\n"
            "</script>\n"
        ),
        (
            "<script>\n"
            '    $("#x").do({\n'
            "        dataBound: function () {\n"
            '            this.tbody.append($("<td colspan=2\'>X</td>"));\n'
            "        },\n"
            "    });\n"
            "</script>\n"
        ),
        id="complex_js",
    ),
    pytest.param(
        ("<script>{{missing_space}}</script>\n"),
        ("<script>{{missing_space}}</script>\n"),
        id="bad_tag",
    ),
    pytest.param(
        ("<script></script>\n"),
        ("<script></script>\n"),
        id="empty",
    ),
    pytest.param(
        (
            '<script type="text/javascript">\n'
            '  var message = "Alert!";\n'
            "  alert(message);\n"
            "</script>\n"
            '<script type="application/javascript">\n'
            '  var message = "Alert!";\n'
            "  alert(message);\n"
            "</script>\n"
            "<script>\n"
            '  var message = "Alert!";\n'
            "  alert(message);\n"
            "</script>\n"
            '<script type="text/babel">\n'
            "            const    someJS    =   'this should be formatted'\n"
            "</script>\n"
            '<script type="module">\n'
            "      import lib from './lib.js';\n"
            "        function myFunction() { return 'foo'; }\n"
            "  </script>\n"
        ),
        (
            '<script type="text/javascript">\n'
            '  var message = "Alert!";\n'
            "  alert(message);\n"
            "</script>\n"
            '<script type="application/javascript">\n'
            '  var message = "Alert!";\n'
            "  alert(message);\n"
            "</script>\n"
            "<script>\n"
            '  var message = "Alert!";\n'
            "  alert(message);\n"
            "</script>\n"
            "<script type=\"text/babel\">const    someJS    =   'this should be formatted'</script>\n"
            '<script type="module">\n'
            "      import lib from './lib.js';\n"
            "        function myFunction() { return 'foo'; }\n"
            "</script>\n"
        ),
        id="js",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <head>\n"
            "    <title>Sample styled page</title>\n"
            "    <script>alert('test');</script>\n"
            "    <script>\n"
            '      var message = "Alert!";\n'
            "      alert(message);\n"
            "    </script>\n"
            "  </head>\n"
            "  <body>\n"
            "    <h1>Sample styled page</h1>\n"
            "    <p>This page is just a demo.</p>\n"
            "  </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <head>\n"
            "        <title>Sample styled page</title>\n"
            "        <script>alert('test');</script>\n"
            "        <script>\n"
            '      var message = "Alert!";\n'
            "      alert(message);\n"
            "        </script>\n"
            "    </head>\n"
            "    <body>\n"
            "        <h1>Sample styled page</h1>\n"
            "        <p>This page is just a demo.</p>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="simple",
    ),
    pytest.param(
        (
            "<script>alert('test');</script>\n"
            "<script>\n"
            '  document.getElementById("demo").innerHTML = "Hello JavaScript!";\n'
            "</script>\n"
        ),
        (
            "<script>alert('test');</script>\n"
            '<script>document.getElementById("demo").innerHTML = "Hello JavaScript!";</script>\n'
        ),
        id="single_script",
    ),
    pytest.param(
        ('<script type="text/template">\n' " <div>\n" "    </div>\n" "</script>\n"),
        ('<script type="text/template">\n' " <div>\n" "    </div>\n" "</script>\n"),
        id="something_else",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "    <head>\n"
            "    </head>\n"
            "    <body>\n"
            "        <script>\n"
            "            function foo() {\n"
            "                return \\`\n"
            "                    <div>\n"
            "                        <p>Text</p>\n"
            "                    </div>\n"
            "                \\`;\n"
            "            }\n"
            "        </script>\n"
            "    </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "    <head></head>\n"
            "    <body>\n"
            "        <script>\n"
            "            function foo() {\n"
            "                return \\`\n"
            "                    <div>\n"
            "                        <p>Text</p>\n"
            "                    </div>\n"
            "                \\`;\n"
            "            }\n"
            "        </script>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="template_literal",
    ),
    pytest.param(
        (
            '<script type="application/x-typescript">\n'
            "  class Student {\n"
            "    fullName: string;\n"
            "    constructor(public firstName: string, public middleInitial: string, public lastName: string) {\n"
            '    this.fullName = firstName + " " + middleInitial + " " + lastName;\n'
            "  }\n"
            "  }\n"
            "  interface Person {\n"
            "    firstName: string;\n"
            "    lastName: string;\n"
            "  }\n"
            "  function greeter(person : Person) {\n"
            '    return "Hello, " + person.firstName + " " + person.lastName;\n'
            "  }\n"
            '  let user = new Student("Jane", "M.", "User");\n'
            "  document.body.innerHTML = greeter(user);\n"
            "</script>\n"
            '<script lang="ts">\n'
            "  class Student {\n"
            "    fullName: string;\n"
            "    constructor(public firstName: string, public middleInitial: string, public lastName: string) {\n"
            '    this.fullName = firstName + " " + middleInitial + " " + lastName;\n'
            "  }\n"
            "  }\n"
            "  interface Person {\n"
            "    firstName: string;\n"
            "    lastName: string;\n"
            "  }\n"
            "  function greeter(person : Person) {\n"
            '    return "Hello, " + person.firstName + " " + person.lastName;\n'
            "  }\n"
            '  let user = new Student("Jane", "M.", "User");\n'
            "  document.body.innerHTML = greeter(user);\n"
            "</script>\n"
            '<script lang="tsx">\n'
            "  class CommentBox extends React.Component<{ url: string, pollInterval: number}, CommentData> {\n"
            "    constructor(){\n"
            "      super()\n"
            "      this.state = { data: [] };\n"
            "    }\n"
            "    fetchComments() {\n"
            "      $.ajax({\n"
            "        url: this.props.url,\n"
            "        dataType: 'json',\n"
            "        cache: false,\n"
            "        success: (data) => this.setState({ data: data }),\n"
            "        error: (xhr, status, err) => console.error(status, err)\n"
            "      })\n"
            "    }\n"
            "    componentDidMount() {\n"
            "      this.fetchComments();\n"
            "      setInterval(this.fetchComments.bind(this), this.props.pollInterval);\n"
            "    }\n"
            "    render() {\n"
            "      let handleCommentSubmit = (comment: { author: string, text: string }) => {\n"
            "        console.warn('comment submitted!', comment);\n"
            "        const updated = this.state.data.slice(0);\n"
            "        updated.push(comment);\n"
            "        this.setState({ data: updated });\n"
            "      }\n"
            "      return (\n"
            '        <div className="commentBox">\n'
            "        <h1>Comments</h1>\n"
            "        <CommentList data={this.state.data}/>\n"
            "      <CommentForm onCommentSubmit={handleCommentSubmit} />\n"
            "      </div>\n"
            "    );\n"
            "    }\n"
            "  }\n"
            "</script>\n"
        ),
        (
            '<script type="application/x-typescript">\n'
            "  class Student {\n"
            "    fullName: string;\n"
            "    constructor(public firstName: string, public middleInitial: string, public lastName: string) {\n"
            '    this.fullName = firstName + " " + middleInitial + " " + lastName;\n'
            "  }\n"
            "  }\n"
            "  interface Person {\n"
            "    firstName: string;\n"
            "    lastName: string;\n"
            "  }\n"
            "  function greeter(person : Person) {\n"
            '    return "Hello, " + person.firstName + " " + person.lastName;\n'
            "  }\n"
            '  let user = new Student("Jane", "M.", "User");\n'
            "  document.body.innerHTML = greeter(user);\n"
            "</script>\n"
            '<script lang="ts">\n'
            "  class Student {\n"
            "    fullName: string;\n"
            "    constructor(public firstName: string, public middleInitial: string, public lastName: string) {\n"
            '    this.fullName = firstName + " " + middleInitial + " " + lastName;\n'
            "  }\n"
            "  }\n"
            "  interface Person {\n"
            "    firstName: string;\n"
            "    lastName: string;\n"
            "  }\n"
            "  function greeter(person : Person) {\n"
            '    return "Hello, " + person.firstName + " " + person.lastName;\n'
            "  }\n"
            '  let user = new Student("Jane", "M.", "User");\n'
            "  document.body.innerHTML = greeter(user);\n"
            "</script>\n"
            '<script lang="tsx">\n'
            "  class CommentBox extends React.Component<{ url: string, pollInterval: number}, CommentData> {\n"
            "    constructor(){\n"
            "      super()\n"
            "      this.state = { data: [] };\n"
            "    }\n"
            "    fetchComments() {\n"
            "      $.ajax({\n"
            "        url: this.props.url,\n"
            "        dataType: 'json',\n"
            "        cache: false,\n"
            "        success: (data) => this.setState({ data: data }),\n"
            "        error: (xhr, status, err) => console.error(status, err)\n"
            "      })\n"
            "    }\n"
            "    componentDidMount() {\n"
            "      this.fetchComments();\n"
            "      setInterval(this.fetchComments.bind(this), this.props.pollInterval);\n"
            "    }\n"
            "    render() {\n"
            "      let handleCommentSubmit = (comment: { author: string, text: string }) => {\n"
            "        console.warn('comment submitted!', comment);\n"
            "        const updated = this.state.data.slice(0);\n"
            "        updated.push(comment);\n"
            "        this.setState({ data: updated });\n"
            "      }\n"
            "      return (\n"
            '        <div className="commentBox">\n'
            "        <h1>Comments</h1>\n"
            "        <CommentList data={this.state.data}/>\n"
            "      <CommentForm onCommentSubmit={handleCommentSubmit} />\n"
            "      </div>\n"
            "    );\n"
            "    }\n"
            "  }\n"
            "</script>\n"
        ),
        id="typescript",
    ),
    pytest.param(
        (
            '<script type="text/babel" data-presets="react" data-type="module">\n'
            "import { h,\n"
            "         render } from 'https://unpkg.com/preact?module';\n"
            "render(\n"
            "<h1>Hello World!</h1>,\n"
            "         document.body\n"
            ");\n"
            "</script>\n"
            '<script type="text/babel">\n'
            "<!--\n"
            "alert(1)\n"
            "-->\n"
            "</script>\n"
        ),
        (
            '<script type="text/babel" data-presets="react" data-type="module">\n'
            "import { h,\n"
            "         render } from 'https://unpkg.com/preact?module';\n"
            "render(\n"
            "<h1>Hello World!</h1>,\n"
            "         document.body\n"
            ");\n"
            "</script>\n"
            '<script type="text/babel">\n'
            "<!--\n"
            "alert(1)\n"
            "-->\n"
            "</script>\n"
        ),
        id="babel",
    ),
    pytest.param(
        (
            "<script>\n"
            "<!--\n"
            "alert(1)\n"
            "-->\n"
            "</script>\n"
            "<script>\n"
            "<!--\n"
            "alert(2)\n"
            "//-->\n"
            "</script>\n"
        ),
        (
            "<script>\n"
            "<!--\n"
            "alert(1)\n"
            "-->\n"
            "</script>\n"
            "<script>\n"
            "<!--\n"
            "alert(2)\n"
            "//-->\n"
            "</script>\n"
        ),
        id="legacy",
    ),
    pytest.param(
        (
            '<script type="module">\n'
            'import prettier from "prettier/standalone";\n'
            'import parserGraphql from "prettier/parser-graphql";\n'
            'prettier.format("query { }", {\n'
            '                      parser: "graphql",\n'
            "  plugins: [\n"
            "parserGraphql],\n"
            "});\n"
            "</script>\n"
            '<script type="module">\n'
            "async function foo() {\n"
            "  let x=10;while(x-->0)console.log(x)\n"
            "  await(import('mod'))\n"
            "}\n"
            "</script>\n"
        ),
        (
            '<script type="module">\n'
            'import prettier from "prettier/standalone";\n'
            'import parserGraphql from "prettier/parser-graphql";\n'
            'prettier.format("query { }", {\n'
            '                      parser: "graphql",\n'
            "  plugins: [\n"
            "parserGraphql],\n"
            "});\n"
            "</script>\n"
            '<script type="module">\n'
            "async function foo() {\n"
            "  let x=10;while(x-->0)console.log(x)\n"
            "  await(import('mod'))\n"
            "}\n"
            "</script>\n"
        ),
        id="module",
    ),
    pytest.param(
        ('<script src="foo.wasm" type="module" withtype="webassembly"></script>\n'),
        ('<script src="foo.wasm" type="module" withtype="webassembly"></script>\n'),
        id="module_attributes",
    ),
    pytest.param(
        (
            '<script type="application/ld+json">\n'
            '  {   "json": true }\n'
            "</script>\n"
            '<script type="application/json">\n'
            '  {   "json":true  }\n'
            "</script>\n"
            '<script type="importmap">\n'
            '  {   "json":true  }\n'
            "</script>\n"
            '<script type="systemjs-importmap">\n'
            '  {   "json":true  }\n'
            '</script><script type="invalid">\n'
            '  {   "json":false  }\n'
            "</script>\n"
            '<script type="text/html">\n'
            "  <div>\n"
            "  <p>foo</p>\n"
            "  </div>\n"
            "</script>\n"
            "<script\n"
            '  async=""\n'
            '  id=""\n'
            '  src="/_next/static/development/pages/_app.js?ts=1565732195968"\n'
            "></script><script></script>\n"
            "<!-- #8147 -->\n"
            '<script lang="vbscript">\n'
            "Function hello()\n"
            "End Function\n"
            "</script>\n"
            '<script lang="unknown">\n'
            "</script>\n"
        ),
        (
            '<script type="application/ld+json">{   "json": true }</script>\n'
            '<script type="application/json">{   "json":true  }</script>\n'
            '<script type="importmap">{   "json":true  }</script>\n'
            '<script type="systemjs-importmap">{   "json":true  }</script>\n'
            '<script type="invalid">{   "json":false  }</script>\n'
            '<script type="text/html">\n'
            "  <div>\n"
            "  <p>foo</p>\n"
            "  </div>\n"
            "</script>\n"
            '<script async=""\n'
            '        id=""\n'
            '        src="/_next/static/development/pages/_app.js?ts=1565732195968"></script><script></script>\n'
            "<!-- #8147 -->\n"
            '<script lang="vbscript">\n'
            "Function hello()\n"
            "End Function\n"
            "</script>\n"
            '<script lang="unknown"></script>\n'
        ),
        id="more_scripts",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
