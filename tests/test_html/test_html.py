"""Djlint tests specific to html.

run::

   pytest tests/test_html.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

missing tests:

- self closing should have a /> > meta, link, img, source, param
- smart quotes
- missing quotes are added to single word attributes <p title=Title>String</p> >> <p title="Title">String</p>
- tags and attributes should be made lowercase

"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint

from ..conftest import reformat, write_to_file


def test_front_matter(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""---
layout: <div><div></div></div>
---
<div></div>""",
    )
    assert output.exit_code == 0


def test_pre_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    # added for https://github.com/Riverside-Healthcare/djLint/issues/187
    output = reformat(
        tmp_file,
        runner,
        b"""{% if a %}
    <div>
        <pre><code>asdf</code></pre>
        <pre><code>asdf
            </code></pre>
        <!-- other html -->
        <h2>title</h2>
    </div>
{% endif %}""",
    )
    assert output.exit_code == 0


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
    # check double nesting
    output = reformat(
        tmp_file,
        runner,
        b"""<div>
    <div class="field">
        <textarea>asdf</textarea>
    </div>
</div>
""",
    )

    assert output.exit_code == 0

    # check attributes
    output = reformat(
        tmp_file,
        runner,
        b"""<div>
    <div class="field">
        <textarea class="this"
                  name="that">asdf</textarea>
    </div>
</div>
""",
    )

    assert (
        output.text
        == """<div>
    <div class="field">
        <textarea class="this" name="that">asdf</textarea>
    </div>
</div>
"""
    )


def test_a_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<p>
    some nice text <a href="this">asdf</a>, ok
</p>""",
    )

    assert output.exit_code == 0

    # test added for https://github.com/Riverside-Healthcare/djLint/issues/189
    output = reformat(
        tmp_file,
        runner,
        b"""<a>
    <span>hi</span>hi</a>
<div>
    <h4>{{ _("Options") }}</h4>
</div>
""",
    )

    assert output.exit_code == 0


def test_script_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <script>console.log();\n    console.log();\n\n    </script>\n</div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text()
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


def test_html_comments_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <!-- asdf--><!--\n multi\nline\ncomment--></div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text()
        == """<div>
    <!-- asdf--><!--
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


def test_hr_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<div>
    <div>
        <hr>
    </div>
</div>
""",
    )
    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<div>
    <div>
        <hr />
    </div>
</div>
""",
    )

    assert output.exit_code == 0


def test_span_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span>
"""
    )

    # issue #171, span is an inline tag
    output = reformat(
        tmp_file,
        runner,
        b"""<div class="hi">
    <div class="poor">
        <p class="format">
            <strong>H</strong>ello stranger, <strong>do not wrap span</strong>, <strong>pls</strong>.
            <span class="big">H</span>ello stranger, <strong>do not wrap span</strong>, <span class="big">pls</span>.
        </p>
    </div>
</div>""",
    )  # noqa: E501
    assert output.exit_code == 0


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

    assert output.exit_code == 1

    assert (
        output.text
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
        b"""<!-- djlint:off -->
<div><p><span></span></p></div>
<!-- djlint:on -->
{# djlint:off #}
<div><p><span></span></p></div>
{# djlint:on #}
{% comment %} djlint:off {% endcomment %}
<div><p><span></span></p></div>
{% comment %} djlint:on {% endcomment %}
{{ /* djlint:off */ }}
<div><p><span></span></p></div>
{{ /* djlint:on */ }}
{{!-- djlint:off --}}
<div><p><span></span></p></div>
{{!-- djlint:on --}}
""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""{# djlint: off #}<meta name="description" content="{% block meta_content %}Alle vogelkijkhutten van Nederland{% endblock %}">{# djlint:on #}
""",
    )

    assert output.exit_code == 0

    # check script tag
    output = reformat(
        tmp_file,
        runner,
        b"""<script>
    <div><p><span></span></p></div>
</script>
""",
    )

    assert output.exit_code == 0

    assert (
        """<script>
    <div><p><span></span></p></div>
</script>
"""
        in output.text
    )

    # check inline script includes
    output = reformat(
        tmp_file,
        runner,
        b"""<html>
    <head>
        <link href="{% static  'foo/bar.css' %}" rel="stylesheet"/>
        <!--JS-->
        <script src="{% static  'foo/bar.js' %}"></script>
    </head>
</html>
""",
    )
    print(output.text)
    assert output.exit_code == 0


def test_style_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<style>
    {# override to fix text all over the place in media upload box #}
    .k-dropzone .k-upload-status {
        color: #a1a1a1;
    }
</style>
""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<style>
 .k-dropzone .k-upload-status {
       color: #a1a1a1;
           }
</style>
""",
    )

    assert output.exit_code == 0

    # check style includes
    output = reformat(
        tmp_file,
        runner,
        b"""<link href="{% static 'common/js/foo.min.js' %}"/>""",
    )

    assert output.exit_code == 0


def test_self_closing_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<p><span>Hello</span> <br /><input /><link /><img /><source /><meta /> <span>World</span></p>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<p>
    <span>Hello</span>
    <br />
    <input />
    <link />
    <img />
    <source />
    <meta />
    <span>World</span>
</p>
"""
    )


def test_void_self_closing_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<p><span>Hello</span> <br><input><link><img><source><meta> <span>World</span></p>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """<p>
    <span>Hello</span>
    <br>
    <input>
    <link>
    <img>
    <source>
    <meta>
    <span>World</span>
</p>
"""
    )
