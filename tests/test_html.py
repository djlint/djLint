"""Djlint tests specific to html.

run::

   pytest tests/test_html.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html.py::test_ignored_block --cov=src/djlint --cov-branch \
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


def test_small_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<small>text</small>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<small>text</small>
"""
    )


def test_dd_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<dd>text</dd>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<dd>
    text
</dd>
"""
    )


def test_dt_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<dt>text</dt>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<dt>
    text
</dt>
"""
    )


def test_details_summary_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<details><summary>summary</summary>body</details>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<details>
    <summary>
        summary
    </summary>
    body
</details>
"""
    )


def test_figure_figcaption_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<figure><img src="" alt=""><figcaption>caption</figcaption></figure>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<figure>
    <img src="" alt="">
    <figcaption>
        caption
    </figcaption>
</figure>
"""
    )


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

    assert output["exit_code"] == 1

    assert (
        output["text"]
        == """<div class="a long list of meaningless classes"
     id="somthing_meaning_less_is_here"
     required
     checked="checked"
     json-data='{"menu":{"header":"SVG Viewer","items":[{"id":"Open"}]}}'></div>
"""
    )


def test_picture_source_img_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""\
<picture><source media="(max-width:640px)"
srcset="image.jpg"><img src="image.jpg" alt="image"></picture>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<picture>
    <source media="(max-width:640px)" srcset="image.jpg">
    <img src="image.jpg" alt="image">
</picture>
"""
    )


def test_ignored_block(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<!-- <span> -->
    <div><p><span></span></p></div>
    <!-- <div> -->
    """,
    )

    assert output["exit_code"] == 1

    assert (
        output["text"]
        == """<!-- <span> -->
<div>
    <p>
        <span></span>
    </p>
</div>
<!-- <div> -->
"""
    )

    # check custom ignore tag {# djlint:off #} {# djlint:on #}
    output = reformat(
        tmp_file,
        runner,
        b"""{% djlint:off %}
    <div><p><span></span></p></div>
    {% djlint:on %}
""",
    )

    assert output["exit_code"] == 0

    assert (
        output["text"]
        == """{% djlint:off %}
    <div><p><span></span></p></div>
    {% djlint:on %}
"""
    )

    # check script tag
    output = reformat(
        tmp_file,
        runner,
        b"""<script>
    <div><p><span></span></p></div>
</script>
""",
    )

    assert output["exit_code"] == 0

    assert (
        output["text"]
        == """<script>
    <div><p><span></span></p></div>
</script>
"""
    )
