"""Djlint tests for basic stuff.

Some tests may be from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   poetry run pytest tests/test_html/test_basics.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   poetry run pytest tests/test_html/test_basics.py::test_brocken_html

"""
# pylint: disable=C0116
from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat

# def test_brocken_html(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <!--
# #7241,
# reproduction:
# two different element,
# linebreak
# \\`<\\`
# extra space(s)
# -->
# <div><span>
# <
#     """
#     ).strip()

#     html_out = (
#         """
# <!--
# #7241,
# reproduction:
# two different element,
# linebreak
# \\`<\\`
# extra space(s)
# -->
# <div>
#    <span> <
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


def test_comment(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<!--hello world-->""",
    )

    assert (
        output.text
        == """<!--hello world-->
"""
    )


# def test_emtpy_doc(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <!doctype html>
# <html>
# <head></head>
# <body></body>
# </html>
#     """
#     ).strip()

#     html_out = (
#         """
# <!DOCTYPE html>
# <html>
#     <head></head>
#     <body></body>
# </html>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


def test_empty(runner: CliRunner, tmp_file: TextIO) -> None:

    output = reformat(
        tmp_file,
        runner,
        b"",
    )

    assert (
        output.text
        == """
"""
    )


# def test_form(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <form>
#   <div class="form-group">
#     <label for="exampleInputEmail1">Email address</label>
#     <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email">
#     <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
#   </div>
#   <div class="form-group">
#     <label for="exampleInputPassword1">Password</label>
#     <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
#   </div>
#   <div class="form-group">
#     <label for="exampleSelect1">Example select</label>
#     <select class="form-control" id="exampleSelect1">
#       <option>1</option>
#       <option>2</option>
#       <option>3</option>
#       <option>4</option>
#       <option>5</option>
#     </select>
#   </div>
#   <div class="form-group">
#     <label for="exampleSelect2">Example multiple select</label>
#     <select multiple class="form-control" id="exampleSelect2">
#       <option>1</option>
#       <option>2</option>
#       <option>3</option>
#       <option>4</option>
#       <option>5</option>
#     </select>
#   </div>
#   <div class="form-group">
#     <label for="exampleTextarea">Example textarea</label>
#     <textarea class="form-control" id="exampleTextarea" rows="3"></textarea>
#   </div>
#   <div class="form-group">
#     <label for="exampleInputFile">File input</label>
#     <input type="file" class="form-control-file" id="exampleInputFile" aria-describedby="fileHelp">
#     <small id="fileHelp" class="form-text text-muted">This is some placeholder block-level help text for the above input. It's a bit lighter and easily wraps to a new line.</small>
#   </div>
#   <fieldset class="form-group">
#     <legend>Radio buttons</legend>
#     <div class="form-check">
#       <label class="form-check-label">
#         <input type="radio" class="form-check-input" name="optionsRadios" id="optionsRadios1" value="option1" checked>
#         Option one is this and that&mdash;be sure to include why it's great
#       </label>
#     </div>
#     <div class="form-check">
#       <label class="form-check-label">
#         <input type="radio" class="form-check-input" name="optionsRadios" id="optionsRadios2" value="option2">
#         Option two can be something else and selecting it will deselect option one
#       </label>
#     </div>
#     <div class="form-check disabled">
#       <label class="form-check-label">
#         <input type="radio" class="form-check-input" name="optionsRadios" id="optionsRadios3" value="option3" disabled>
#         Option three is disabled
#       </label>
#     </div>
#   </fieldset>
#   <div class="form-check">
#     <label class="form-check-label">
#       <input type="checkbox" class="form-check-input">
#       Check me out
#     </label>
#   </div>
#   <button type="submit" class="btn btn-primary">Submit</button>
# </form>
#     """
#     ).strip()

#     html_out = (
#         """
# <form>
#     <div class="form-group">
#         <label for="exampleInputEmail1">Email address</label>
#             <input
#               type="email"
#               class="form-control"
#               id="exampleInputEmail1"
#               aria-describedby="emailHelp"
#               placeholder="Enter email"
#             />
#             <small id="emailHelp" class="form-text text-muted"
#               >We'll never share your email with anyone else.</small
#             >
#     </div>
#     <div class="form-group">
#         <label for="exampleInputPassword1">Password</label>
#         <input
#           type="password"
#           class="form-control"
#           id="exampleInputPassword1"
#           placeholder="Password"
#         />
#     </div>
#     <div class="form-group">
#         <label for="exampleSelect1">Example select</label>
#         <select class="form-control" id="exampleSelect1">
#             <option>1</option>
#             <option>2</option>
#             <option>3</option>
#             <option>4</option>
#             <option>5</option>
#         </select>
#     </div>
#     <div class="form-group">
#         <label for="exampleSelect2">Example multiple select</label>
#         <select multiple class="form-control" id="exampleSelect2">
#             <option>1</option>
#             <option>2</option>
#             <option>3</option>
#             <option>4</option>
#             <option>5</option>
#         </select>
#     </div>
#     <div class="form-group">
#         <label for="exampleTextarea">Example textarea</label>
#         <textarea class="form-control" id="exampleTextarea" rows="3"></textarea>
#     </div>
#     <div class="form-group">
#         <label for="exampleInputFile">File input</label>
#         <input
#             type="file"
#             class="form-control-file"
#             id="exampleInputFile"
#             aria-describedby="fileHelp"
#         />
#         <small id="fileHelp" class="form-text text-muted"
#             >This is some placeholder block-level help text for the above input. It's
#             a bit lighter and easily wraps to a new line.</small
#         >
#     </div>
#     <fieldset class="form-group">
#         <legend>Radio buttons</legend>
#         <div class="form-check">
#             <label class="form-check-label">
#                 <input
#                     type="radio"
#                     class="form-check-input"
#                     name="optionsRadios"
#                     id="optionsRadios1"
#                     value="option1"
#                     checked
#                 />
#                 Option one is this and that&mdash;be sure to include why it's great
#             </label>
#         </div>
#         <div class="form-check">
#             <label class="form-check-label">
#                 <input
#                     type="radio"
#                     class="form-check-input"
#                     name="optionsRadios"
#                     id="optionsRadios2"
#                     value="option2"
#                 />
#                 Option two can be something else and selecting it will deselect option
#                 one
#             </label>
#         </div>
#         <div class="form-check disabled">
#             <label class="form-check-label">
#                 <input
#                     type="radio"
#                     class="form-check-input"
#                     name="optionsRadios"
#                     id="optionsRadios3"
#                     value="option3"
#                     disabled
#                 />
#                 Option three is disabled
#             </label>
#         </div>
#     </fieldset>
#     <div class="form-check">
#         <label class="form-check-label">
#             <input type="checkbox" class="form-check-input" />
#             Check me out
#         </label>
#     </div>
#     <button type="submit" class="btn btn-primary">Submit</button>
# </form>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


def test_hello_world(runner: CliRunner, tmp_file: TextIO) -> None:

    output = reformat(
        tmp_file,
        runner,
        b"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
    </head>
    <body>
        <!-- A comment -->
        <h1>Hello World</h1>
    </body>
</html>
""",
    )

    assert output.exit_code == 0


def test_html_comments(runner: CliRunner, tmp_file: TextIO) -> None:

    output = reformat(
        tmp_file,
        runner,
        b"""<!-- htmlhint attr-lowercase: false -->
<html>
    <body>
        <a href="#">Anchor</a>
        <div hidden class="foo" id=bar></div>
    </body>
</html>
""",
    )

    assert output.exit_code == 0


# def test_html5_boilerplate(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <!doctype html>
# <html class="no-js" lang="">
#   <head>
#     <meta charset="utf-8">
#     <meta http-equiv="x-ua-compatible" content="ie=edge">
#     <title></title>
#     <meta name="description" content="">
#     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
#     <link rel="manifest" href="site.webmanifest">
#     <link rel="apple-touch-icon" href="icon.png">
#     <!-- Place favicon.ico in the root directory -->
#     <link rel="stylesheet" href="css/normalize.css">
#     <link rel="stylesheet" href="css/main.css">
#   </head>
#   <body>
#     <!--[if lte IE 9]>
#     <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
#     <![endif]-->
#     <!-- Add your site or application content here -->
#     <p>Hello world! This is HTML5 Boilerplate.</p>
#     <script src="js/vendor/modernizr-3.6.0.min.js"></script>
#     <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
#     <script>window.jQuery || document.write('<script src="js/vendor/jquery-3.3.1.min.js"><\\/script>')</script>
#     <script src="js/plugins.js"></script>
#     <script src="js/main.js"></script>
#     <!-- Google Analytics: change UA-XXXXX-Y to be your site's ID. -->
#     <script>
#       window.ga = function () { ga.q.push(arguments) }; ga.q = []; ga.l = +new Date;
#       ga('create', 'UA-XXXXX-Y', 'auto'); ga('send', 'pageview')
#     </script>
#     <script src="https://www.google-analytics.com/analytics.js" async defer></script>
#   </body>
# </html>
#     """
#     ).strip()

#     html_out = (
#         """
# <!DOCTYPE html>
# <html class="no-js" lang="">
#     <head>
#         <meta charset="utf-8" />
#         <meta http-equiv="x-ua-compatible" content="ie=edge" />
#         <title></title>
#         <meta name="description" content="" />
#         <meta
#             name="viewport"
#             content="width=device-width, initial-scale=1, shrink-to-fit=no"
#         />
#         <link rel="manifest" href="site.webmanifest" />
#         <link rel="apple-touch-icon" href="icon.png" />
#         <!-- Place favicon.ico in the root directory -->
#         <link rel="stylesheet" href="css/normalize.css" />
#         <link rel="stylesheet" href="css/main.css" />
#     </head>
#     <body>
#         <!--[if lte IE 9]>
#             <p class="browserupgrade">
#                 You are using an <strong>outdated</strong> browser. Please
#                 <a href="https://browsehappy.com/">upgrade your browser</a> to improve
#                 your experience and security.
#             </p>
#         <![endif]-->
#         <!-- Add your site or application content here -->
#         <p>Hello world! This is HTML5 Boilerplate.</p>
#         <script src="js/vendor/modernizr-3.6.0.min.js"></script>
#         <script
#             src="https://code.jquery.com/jquery-3.3.1.min.js"
#             integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
#             crossorigin="anonymous"
#         ></script>
#         <script>
#           window.jQuery ||
#             document.write(
#               '<script src="js/vendor/jquery-3.3.1.min.js"><\\/script>'
#             );
#         </script>
#         <script src="js/plugins.js"></script>
#         <script src="js/main.js"></script>
#         <!-- Google Analytics: change UA-XXXXX-Y to be your site's ID. -->
#         <script>
#           window.ga = function () {
#             ga.q.push(arguments);
#           };
#           ga.q = [];
#           ga.l = +new Date();
#           ga("create", "UA-XXXXX-Y", "auto");
#           ga("send", "pageview");
#         </script>
#         <script
#           src="https://www.google-analytics.com/analytics.js"
#           async
#           defer
#         ></script>
#     </body>
# </html>
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


# def test_issue_9368_2(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <strong>a</strong>-<strong>b</strong>-
#     """
#     ).strip()

#     html_out = (
#         """
# <strong>a</strong>-<strong>b</strong>-
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


def test_issue_9368_3(runner: CliRunner, tmp_file: TextIO) -> None:

    output = reformat(
        tmp_file,
        runner,
        b"""a track<strong>pad</strong>, or a <strong>gyro</strong>scope.
""",
    )

    assert output.exit_code == 0


def test_issue_9368(runner: CliRunner, tmp_file: TextIO) -> None:

    output = reformat(
        tmp_file,
        runner,
        b"""<strong>a</strong>-&gt;<strong>b</strong>-&gt;
""",
    )

    assert output.exit_code == 0


# def test_more_html(runner: CliRunner, tmp_file: TextIO) -> None:

#     output = reformat(
#         tmp_file,
#         runner,
#         b"""
# <html>
# <head></head>
# <body>
#     <a href="#">Anchor</a>
#     <div hidden class="foo" id=bar></div>
# </body>
# </html>
#     """
#     )

#     assert output.text == """<html>
#     <head></head>
#     <body>
#         <a href="#">Anchor</a>
#         <div hidden class="foo" id="bar"></div>
#     </body>
# </html>
# """


def test_void_elements(runner: CliRunner, tmp_file: TextIO) -> None:

    output = reformat(
        tmp_file,
        runner,
        b"""<html>
    <head>
        <meta charset="UTF-8" />
        <link rel="stylesheet" href="code-guide.css" />
    </head>
    <body></body>
</html>
""",
    )

    assert output.exit_code == 0


# def test_void_elements_2(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <video controls width="250">
#     <source src="/media/examples/flower.webm"
#             type="video/webm">
#     <source src="/media/examples/flower.mp4"
#             type="video/mp4"
# ></video>text after
# <!-- #8626 -->
# <object data="horse.wav"><param name="autoplay" value="true"
# ><param name="autoplay" value="true"
# ></object>1
# <span><img  src="1.png"
# ><img src="1.png"
# ></span>1
#     """
#     ).strip()

#     html_out = (
#         """
# <video controls width="250">
#     <source src="/media/examples/flower.webm" type="video/webm" />
#     <source src="/media/examples/flower.mp4" type="video/mp4" /></video
# >text after
# <!-- #8626 -->
# <object data="horse.wav">
#     <param name="autoplay" value="true" />
#     <param name="autoplay" value="true" /></object
# >1
# <span><img src="1.png" /><img src="1.png" /></span>1
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out


# def test_with_colon(runner: CliRunner, tmp_file: TextIO) -> None:

#     html_in = (
#         b"""
# <!-- unknown tag with colon -->
# <div>
# <foo:bar>
# <div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>
# <div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>
# <pre> pre pr
# e</pre>
# <textarea> pre-wrap pr
# e-wrap </textarea>
# <span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>
# <span> inline </span><span> inline </span> <span> inline </span><span> inline </span>
# <html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>
# <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>
# <html:pre> pre pr
# e</html:pre>
# <html:textarea> pre-wrap pr
# e-wrap </html:textarea>
# <html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>
# <html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo:bar>
# </div>
# <!-- block tag with colon -->
# <div>
# <foo:div>
# <div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>
# <div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>
# <pre> pre pr
# e</pre>
# <textarea> pre-wrap pr
# e-wrap </textarea>
# <span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>
# <span> inline </span><span> inline </span> <span> inline </span><span> inline </span>
# <html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>
# <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>
# <html:pre> pre pr
# e</html:pre>
# <html:textarea> pre-wrap pr
# e-wrap </html:textarea>
# <html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>
# <html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo:div>
# </div>
# <!-- inline tag with colon -->
# <div>
# <foo:span>
# <div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>
# <div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>
# <pre> pre pr
# e</pre>
# <textarea> pre-wrap pr
# e-wrap </textarea>
# <span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>
# <span> inline </span><span> inline </span> <span> inline </span><span> inline </span>
# <html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>
# <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>
# <html:pre> pre pr
# e</html:pre>
# <html:textarea> pre-wrap pr
# e-wrap </html:textarea>
# <html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>
# <html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo:span>
# </div>
# <!-- unknown -->
# <div>
# <foo-bar>
# <div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>
# <div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>
# <pre> pre pr
# e</pre>
# <textarea> pre-wrap pr
# e-wrap </textarea>
# <span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>
# <span> inline </span><span> inline </span> <span> inline </span><span> inline </span>
# <html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>
# <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>
# <html:pre> pre pr
# e</html:pre>
# <html:textarea> pre-wrap pr
# e-wrap </html:textarea>
# <html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>
# <html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo-bar>
# </div>
# <!-- without colon -->
# <div>
# <div>
# <div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>
# <div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>
# <pre> pre pr
# e</pre>
# <textarea> pre-wrap pr
# e-wrap </textarea>
# <span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>
# <span> inline </span><span> inline </span> <span> inline </span><span> inline </span>
# <html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>
# <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>
# <html:pre> pre pr
# e</html:pre>
# <html:textarea> pre-wrap pr
# e-wrap </html:textarea>
# <html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>
# <html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></div>
# </div>
# <!-- #7236 -->
# <with:colon>
#   <div><h1> text  text  text  text  text  text  text  text  text  text  text  text  text  text </h1></div>
#   <script>
#   const func = function() { console.log('Hello, there');}
#   </script>
#   </with:colon>
# <!-- script like -->
# <with:colon>
# <style>.a{color:#f00}</style>
#   <SCRIPT>
#   const func = function() { console.log('Hello, there');}
#   </SCRIPT>
# <STYLE>.A{COLOR:#F00}</STYLE>
# <html:script>const func = function() { console.log('Hello, there');}</html:script>
# <html:style>.a{color:#f00}</html:style>
# <svg><style>.a{color:#f00}</style></svg>
# <svg><style>.a{color:#f00}</style></svg>
# </with:colon>
# <html:script>const func = function() { console.log('Hello, there');}</html:script>
# <html:style>.a{color:#f00}</html:style>
#     """
#     ).strip()

#     html_out = (
#         """
# <!-- unknown tag with colon -->
# <div>
#     <foo:bar>
#         <div>
#             looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#         </div>
#         <div>block</div>
#         <div>BLOCK</div>
#         <div>block</div>
#         <div>block</div>
#         <div>block</div>
#         <pre>
#  pre pr
# e</pre
#         >
#         <textarea>
#  pre-wrap pr
# e-wrap </textarea
#         >
#         <span>
#             looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#         </span>
#         <span> inline </span><span> inline </span> <span> inline </span
#         ><span> inline </span>
#         <html:div>
#             looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#         </html:div>
#         <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>
#         <html:div> block </html:div><html:div> block </html:div
#         ><html:div> block </html:div>
#         <html:pre> pre pr e</html:pre>
#         <html:textarea> pre-wrap pr e-wrap </html:textarea>
#         <html:span>
#           looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#         </html:span>
#         <html:span> inline </html:span><html:span> inline </html:span>
#         <html:span> inline </html:span><html:span> inline </html:span></foo:bar
#         >
#     </div>
# <!-- block tag with colon -->
# <div>
#   <foo:div>
#     <div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </div>
#     <div>block</div>
#     <div>BLOCK</div>
#     <div>block</div>
#     <div>block</div>
#     <div>block</div>
#     <pre>
#  pre pr
# e</pre
#     >
#     <textarea>
#  pre-wrap pr
# e-wrap </textarea
#     >
#     <span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </span>
#     <span> inline </span><span> inline </span> <span> inline </span
#     ><span> inline </span>
#     <html:div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </html:div>
#     <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>
#     <html:div> block </html:div><html:div> block </html:div
#     ><html:div> block </html:div>
#     <html:pre> pre pr e</html:pre>
#     <html:textarea> pre-wrap pr e-wrap </html:textarea>
#     <html:span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span></foo:div
#   >
# </div>
# <!-- inline tag with colon -->
# <div>
#   <foo:span>
#     <div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </div>
#     <div>block</div>
#     <div>BLOCK</div>
#     <div>block</div>
#     <div>block</div>
#     <div>block</div>
#     <pre>
#  pre pr
# e</pre
#     >
#     <textarea>
#  pre-wrap pr
# e-wrap </textarea
#     >
#     <span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </span>
#     <span> inline </span><span> inline </span> <span> inline </span
#     ><span> inline </span>
#     <html:div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </html:div>
#     <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>
#     <html:div> block </html:div><html:div> block </html:div
#     ><html:div> block </html:div>
#     <html:pre> pre pr e</html:pre>
#     <html:textarea> pre-wrap pr e-wrap </html:textarea>
#     <html:span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span></foo:span
#   >
# </div>
# <!-- unknown -->
# <div>
#   <foo-bar>
#     <div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </div>
#     <div>block</div>
#     <div>BLOCK</div>
#     <div>block</div>
#     <div>block</div>
#     <div>block</div>
#     <pre>
#  pre pr
# e</pre
#     >
#     <textarea>
#  pre-wrap pr
# e-wrap </textarea
#     >
#     <span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </span>
#     <span> inline </span><span> inline </span> <span> inline </span
#     ><span> inline </span>
#     <html:div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </html:div>
#     <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>
#     <html:div> block </html:div><html:div> block </html:div
#     ><html:div> block </html:div>
#     <html:pre> pre pr e</html:pre>
#     <html:textarea> pre-wrap pr e-wrap </html:textarea>
#     <html:span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span></foo-bar
#   >
# </div>
# <!-- without colon -->
# <div>
#   <div>
#     <div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </div>
#     <div>block</div>
#     <div>BLOCK</div>
#     <div>block</div>
#     <div>block</div>
#     <div>block</div>
#     <pre>
#  pre pr
# e</pre
#     >
#     <textarea>
#  pre-wrap pr
# e-wrap </textarea
#     >
#     <span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </span>
#     <span> inline </span><span> inline </span> <span> inline </span
#     ><span> inline </span>
#     <html:div>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block
#     </html:div>
#     <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>
#     <html:div> block </html:div><html:div> block </html:div
#     ><html:div> block </html:div>
#     <html:pre> pre pr e</html:pre>
#     <html:textarea> pre-wrap pr e-wrap </html:textarea>
#     <html:span>
#       looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline
#     </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span>
#     <html:span> inline </html:span><html:span> inline </html:span>
#   </div>
# </div>
# <!-- #7236 -->
# <with:colon>
#   <div>
#     <h1>
#       text text text text text text text text text text text text text text
#     </h1>
#   </div>
#   <script>
#     const func = function () {
#       console.log("Hello, there");
#     };
#   </script>
# </with:colon>
# <!-- script like -->
# <with:colon>
#   <style>
#     .a {
#       color: #f00;
#     }
#   </style>
#   <script>
#     const func = function () {
#       console.log("Hello, there");
#     };
#   </script>
#   <style>
#     .A {
#       color: #f00;
#     }
#   </style>
#   <html:script
#     >const func = function() { console.log('Hello, there');}</html:script
#   >
#   <html:style
#     >.a{color:#f00}</html:style
#   >
#   <svg>
#     <style>
#       .a {
#         color: #f00;
#       }
#     </style>
#   </svg>
#   <svg>
#     <style>
#       .a {
#         color: #f00;
#       }
#     </style>
#   </svg>
# </with:colon>
# <html:script
#   >const func = function() { console.log('Hello, there');}</html:script
# >
# <html:style
#   >.a{color:#f00}</html:style
# >
#         """
#     ).strip()

#     output = reformat(tmp_file, runner, html_in)

#     assert output.text == html_out
