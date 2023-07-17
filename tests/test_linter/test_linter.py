"""Djlint linter rule tests.

run::

   pytest tests/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   # for a single test

   pytest tests/test_linter/test_linter.py::test_random

Test setup

(html, (list of codes that should file, plus optional line number))


"""
# pylint: disable=C0116,C0103,C0302

from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import write_to_file


def test_H011(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div class=test></div>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H011 1:" in result.output

    # check for no matches inside template tags
    write_to_file(tmp_file.name, b" {{ func( id=html_id,) }}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H011 1:" not in result.output

    # check meta tag
    write_to_file(
        tmp_file.name,
        b'<meta name="viewport" content="width=device-width, initial-scale=1">',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H011 1:" not in result.output

    # check keywords inside template syntax
    write_to_file(
        tmp_file.name,
        b"<a href=\"{{ url_for('connection_bp.one_connection', connection_id=connection.id) }}\">{{ connection }}</a>",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H011 1:" not in result.output


def test_H012(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<div class = "stuff">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H012 1:" in result.output

    # test for not matching random "=" in text
    write_to_file(tmp_file.name, b"<h3>#= title #</h3>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H012 1:" not in result.output

    # test for not matching "=" in template condition
    write_to_file(
        tmp_file.name,
        b"<p>{% if activity.reporting_groups|length <= 0 %}<h3>{% trans 'General' %}</h3>{% endif %}</p>",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    print(result.output)
    assert result.exit_code == 0
    assert "H012 1:" not in result.output

    # space allowed inside attributes.
    write_to_file(
        tmp_file.name,
        b"""<button x-on:click="myVariable = {{ myObj.id }}" class="text-red-600 hover:text-red-800">
<span x-text="showSource == true ? 'Hide source' : 'Show source'"></span>
<button x-on:click="open = !open" class="flex items-center mt-2">""",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H012" not in result.output


def test_H013(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<img height="12" width="12"/>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H013 1:" in result.output
    print(result.output)
    assert "found 1 error" in result.output


def test_H014(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"</div>\n\n\n<p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H014 1:" in result.output


def test_H015(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"</h1><p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H015 1:" in result.output


def test_H016(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H016 1:" in result.output

    write_to_file(tmp_file.name, b"<html>\n<title>stuff</title>\n</html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H016" not in result.output


def test_H017(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<img this >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H017 1:" not in result.output

    write_to_file(tmp_file.name, b"<img this >")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H017"])
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H017 1:" not in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H017"])
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    write_to_file(tmp_file.name, b"<br >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H017 1:" not in result.output

    write_to_file(tmp_file.name, b"<br >")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H017"])
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    # test colgroup tag
    write_to_file(tmp_file.name, b"<colgroup><colgroup asdf></colgroup></colgroup>")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H017"])
    print(result.output)
    assert "H017 1:" not in result.output

    # test template tags inside html
    write_to_file(tmp_file.name, b"<image {{ > }} />")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H017"])
    assert "H017" not in result.output


def test_DJ018(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b'<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n<form action="/Collections"></form></a>',
    )

    # test hash urls
    write_to_file(
        tmp_file.name,
        b'<a href="#">\n<form action="#"><a href="#tab">\n<form action="#go"></form></a></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_H019(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<a href='javascript:abc()'>asdf</a>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H019 1:" in result.output

    write_to_file(tmp_file.name, b"<form action='javascript:abc()'></form>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H019 1:" in result.output


def test_H020(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div></div>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H020 1:" in result.output

    write_to_file(tmp_file.name, b"<span>\n   </span>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H020 1:" in result.output

    write_to_file(tmp_file.name, b"<td></td>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H020" not in result.output


def test_H022(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<a href="http://">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H022 1:" in result.output


def test_H023(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"&mdash;")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H023 1:" in result.output

    write_to_file(tmp_file.name, b"&aacute;")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H023 1:" in result.output

    write_to_file(tmp_file.name, b"&gt;")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0

    write_to_file(tmp_file.name, b'<a href=" &gt; "></a>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0

    write_to_file(tmp_file.name, b'<a href=" foo & bar; "></a>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0

    write_to_file(tmp_file.name, b'<a href=" &aacute; "></a>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H023 1:" in result.output

    write_to_file(tmp_file.name, b"&#63;")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H023 1:" in result.output

    write_to_file(tmp_file.name, b"&#x3F;")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H023 1:" in result.output

    write_to_file(tmp_file.name, b'<a href=" &#63; "></a>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H023 1:" in result.output


def test_H024(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<script type="hare">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H024" not in result.output

    write_to_file(tmp_file.name, b'<script type="text/javascript">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H024" in result.output

    write_to_file(tmp_file.name, b'<script type="text/css">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H024" in result.output


def test_H025(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H025 1:" in result.output

    write_to_file(tmp_file.name, b"<!-- comment -->")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<!DOCTYPE html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<link {% url_for('something') %} />")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<alpha />")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<alpha>\n</alpha>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(
        tmp_file.name,
        b'<script src="{% static \'notifications/notify.js\' %}" type="text/javascript"></script>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(
        tmp_file.name,
        b'<script src="{% static "folder/foo.js" %}?version={% some_version %}"></script>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(
        tmp_file.name,
        b"<script />",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<tr ><td>Foo</td></tr>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<p>Foo\n<p>Foo</p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025 1:" in result.output
    assert "H025 2:" not in result.output

    # test tags inside attributes
    write_to_file(tmp_file.name, b'<span title="<p>Bar</p>">Foo</span>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<col>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<col />")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    # fix issue #164
    write_to_file(
        tmp_file.name,
        b"""<th {{ attrs }}>
    <a href="{% url %}">{{ content }}</a>
</th>""",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    # fix issue #169
    write_to_file(
        tmp_file.name,
        b"""<li{% if is_active %} class="active" {% endif %}>
    some content
</li>""",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    # test {# #} inside tag
    write_to_file(tmp_file.name, b'<div id="example" {# for #}></div>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    # check closing tag inside a comment
    write_to_file(
        tmp_file.name,
        b'<input {# value="{{ driverId|default(\' asdf \') }}" /> #} value="this">',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output

    # issue #447
    write_to_file(
        tmp_file.name,
        b"""<button title="{% trans "text with ONE single ' quote" %}">
</button>""",
    )
    assert "H025" not in result.output


def test_T027(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<a href=\"{{- blah 'asdf' }}\">")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "T028" not in result.output


def test_H029(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<forM method="Post">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H029" in result.output

    write_to_file(tmp_file.name, b'<forM method="post">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H029" not in result.output

    write_to_file(tmp_file.name, b'<a method="post">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H029" not in result.output


def test_H030(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H030 1:" in result.output

    write_to_file(
        tmp_file.name, b'<html>\n<meta name="description" content="nice"/>\n</html>'
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H030" not in result.output


def test_H031(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H031 1:" in result.output

    write_to_file(
        tmp_file.name, b'<html>\n<meta name="keywords" content="nice"/>\n</html>'
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H031" not in result.output


def test_H033(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name, b"<form action=\" {% url 'foo:bar' %} \" ...>...</form>"
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H033" in result.output

    write_to_file(
        tmp_file.name,
        b"<form action=\" {% url 'foo:bar' %} {{ asdf}} \" ...>...</form>",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H033" in result.output

    write_to_file(
        tmp_file.name, b"<form action=\" {% url 'foo:bar' %} \" ...>...</form>"
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H033" in result.output

    write_to_file(tmp_file.name, b'<form action=" {{ asdf}} " ...>...</form>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H033" in result.output

    write_to_file(
        tmp_file.name, b"<form action=\"{% url 'foo:bar' %} \" ...>...</form>"
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H033" in result.output

    write_to_file(tmp_file.name, b'<form action="asdf " ...>...</form>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H033" in result.output

    write_to_file(tmp_file.name, b'<form action=" asdf " ...>...</form>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H033" in result.output


def test_H035(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<meta this >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H035 1:" not in result.output

    write_to_file(tmp_file.name, b"<meta this >")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H035"])
    assert result.exit_code == 1
    assert "H035 1:" in result.output

    write_to_file(tmp_file.name, b"<meta>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H035 1:" not in result.output

    write_to_file(tmp_file.name, b"<meta>")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H035"])
    assert result.exit_code == 1
    assert "H035 1:" in result.output


def test_H036(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<br><br ><br />")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H036" not in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H036"])
    assert result.exit_code == 1
    assert "H036" in result.output

    write_to_file(tmp_file.name, b"<br />")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H036"])
    assert result.exit_code == 1
    assert "H036" in result.output

    write_to_file(tmp_file.name, b"<br/>")
    result = runner.invoke(djlint, [tmp_file.name, "--include", "H036"])
    assert result.exit_code == 1
    assert "H036" in result.output


def test_rules_not_matched_in_ignored_block(
    runner: CliRunner, tmp_file: TextIO
) -> None:
    write_to_file(tmp_file.name, b"<script><div class=test></script>")
    result = runner.invoke(djlint, [tmp_file.name])

    assert result.exit_code == 0
    assert "H011 1:" not in result.output


def test_output_for_no_linebreaks(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<a\n    class='asdf'></a>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "<a\n" not in result.output

    write_to_file(tmp_file.name, b"<h1>asdf</h1>\n    <h2>asdf</h2>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1

    assert "</h1>\n" not in result.output


def test_output_order(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<h1>asdf</h2>\n    <h3>asdf</h4>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1

    assert (
        """H025 1:0 Tag seems to be an orphan. <h1>
H015 1:8 Follow h tags with a line break. </h2> <h3
H025 1:8 Tag seems to be an orphan. </h2>
H025 2:4 Tag seems to be an orphan. <h3>
H025 2:12 Tag seems to be an orphan. </h4>"""
        in result.output
    )


def test_ignoring_rules(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""{# djlint:off H025,H026 #}
<p>
{# djlint:on #}

<!-- djlint:off H025-->
<p>
<!-- djlint:on -->

{% comment %} djlint:off H025 {% endcomment %}
<p>
{% comment %} djlint:on {% endcomment %}

{{!-- djlint:off H025 --}}
<p style="color:red">
{{!-- djlint:on --}}

{{ /* djlint:off H025 */ }}
<p>
{{ /* djlint:on */ }}

""",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output
    assert "H021" in result.output  # other codes should still show

    # using tabs
    write_to_file(
        tmp_file.name,
        b"""<div>

\t\t{# djlint:off H006 #}

\t\t<img src="{{ variable }}.webp" alt="stuff" />

\t\t{# djlint:on #}

</div>
""",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H006" not in result.output


def test_statistics_empty(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"")
    result = runner.invoke(djlint, [tmp_file.name, "--statistics"])

    assert result.exit_code == 0


def test_statistics_with_results(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div>")
    result = runner.invoke(djlint, [tmp_file.name, "--statistics"])

    assert result.exit_code == 1
