"""Djlint tests specific to html.

run::

   pytest tests/test_html.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html.py::test_front_matter --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing


"""
# pylint: disable=C0116
from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_long_attributes(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<input type="text" class="class one class two" disabled="true" value="something pretty long goes here"
       style="width:100px;cursor: text;border:1px solid pink"
       required="true" />""",
    )

    assert output.exit_code == 1

    assert (
        output.text
        == """<input type="text"
       class="class one class two"
       disabled="true"
       value="something pretty long goes here"
       style="width:100px;cursor: text;border:1px solid pink"
       required="true"/>
"""
    )

    # check styles
    output = reformat(
        tmp_file,
        runner,
        b"""<div class="my long classes"
     required="true"
     checked="checked"
     data-attr="some long junk"
     style="margin-left: 90px;
            display: contents;
            font-weight: bold;
            font-size: 1.5rem;">
""",
    )

    assert output.exit_code == 0

    # check styles when tag is first
    output = reformat(
        tmp_file,
        runner,
        b"""<div>
    <div style="margin-left: 90px;
                display: contents;
                font-weight: bold;
                font-size: 1.5rem;"
         data-attr="stuff"
         class="my long class goes here">
    </div>
</div>
""",
    )
    assert output.exit_code == 0


def test_ignored_attributes(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<div
    class="a long list of meaningless classes"
    id="somthing_meaning_less_is_here"
    required
    checked="checked"
    json-data='{"menu":{"header":"SVG Viewer","items":[{"id":"Open"}]}}'>
    </div>""",
    )

    assert output.exit_code == 1
    print(output.text)
    assert (
        output.text
        == """<div class="a long list of meaningless classes"
     id="somthing_meaning_less_is_here"
     required
     checked="checked"
     json-data='{"menu":{"header":"SVG Viewer","items":[{"id":"Open"}]}}'>\n</div>
"""
    )
