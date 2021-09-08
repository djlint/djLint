"""Djlint tests specific to html.

run::

   pytest tests/test_html.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint

from .conftest import reformat, write_to_file


def test_textarea_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"""<div><textarea>\nasdf\n  asdf</textarea></div>""")
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<div>
<textarea>
asdf
  asdf</textarea>
</div>
"""
    )


def test_script_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <script>console.log();\n    console.log();\n\n    </script>\n</div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<div>
    <script>
console.log();
    console.log();

    </script>
</div>
"""
    )


def test_html_comments_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <!-- asdf-->\n\n   <!--\n multi\nline\ncomment--></div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<div>
    <!-- asdf-->
   <!--
 multi
line
comment-->
</div>
"""
    )


def test_long_attributes(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<input type="text" class="class one class two" disabled="true" value="something pretty long goes here"
       style="width:100px;cursor: text;border:1px solid pink"
       required="true" />""",
    )

    assert output["exit_code"] == 1

    assert (
        output["text"]
        == """<input type="text"
       class="class one class two"
       disabled="true"
       value="something pretty long goes here"
       style="width:100px;cursor: text;border:1px solid pink"
       required="true"/>
"""
    )
