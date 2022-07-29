"""Djlint linter rule tests.

run::

   pytest tests/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   # for a single test

   pytest tests/test_linter/test_linter.py::test_T001

"""
# pylint: disable=C0116,C0103

from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import write_to_file


def test_T001(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{{test }}\n{% test%}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "T001 1:" in result.output
    assert "T001 2:" in result.output

    write_to_file(tmp_file.name, b"{%- test-%}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "nunjucks"])
    assert result.exit_code == 1
    assert "T001 1:" in result.output

    write_to_file(tmp_file.name, b"{%-test -%}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "nunjucks"])
    assert result.exit_code == 1
    assert "T001 1:" in result.output

    write_to_file(tmp_file.name, b"{%- test -%}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "nunjucks"])
    assert result.exit_code == 0

    # this test will pass, because the jinja comment is an ignored block
    write_to_file(tmp_file.name, b"{#-test -#}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert result.exit_code == 0

    write_to_file(tmp_file.name, b"{#- test -#}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert result.exit_code == 0


def test_T002(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% extends 'this' %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "T002 1:" in result.output


def test_T003(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% endblock %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "T003 1:" in result.output


def test_DJ004(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<link src="/static/there">')
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "D004 1:" in result.output

    write_to_file(tmp_file.name, b'<link src="/static/there">')
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert result.exit_code == 1
    assert "J004 1:" in result.output


def test_H005(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<!DOCTYPE html>\n<html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H005 2:" in result.output


def test_H006(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<img alt="test"/>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H006 1:" in result.output
    assert "found 1 error" in result.output


def test_H007(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<html lang="en">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H007 1:" in result.output


def test_H008(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div class='test'>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H008 1:" in result.output


def test_H009(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<H1>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H009 1:" in result.output


def test_H010(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<img HEIGHT="12">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H010 1:" in result.output

    write_to_file(tmp_file.name, b"<li>ID=username</li>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


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
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    write_to_file(tmp_file.name, b"<br >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    # test colgroup tag
    write_to_file(tmp_file.name, b"<colgroup><colgroup asdf></colgroup></colgroup>")
    result = runner.invoke(djlint, [tmp_file.name])
    print(result.output)
    assert result.exit_code == 0
    assert "H017 1:" not in result.output


def test_DJ018(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b'<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n<form action="/Collections"></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "D018 1:" in result.output
    assert "D018 2:" in result.output

    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert result.exit_code == 1
    assert "J018 1:" in result.output
    assert "J018 2:" in result.output

    # test javascript functions
    write_to_file(
        tmp_file.name,
        b'<a href="javascript:abc()">\n<form action="javascript:abc()"></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    # don't check status code. will fail on other rules here.
    assert "D018 1:" not in result.output
    assert "D018 2:" not in result.output

    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    # don't check status code. will fail on other rules here.
    assert "J018 1:" not in result.output
    assert "J018 2:" not in result.output

    # test on_ events
    write_to_file(
        tmp_file.name,
        b'<a href="onclick:abc()">\n<form action="onclick:abc()"></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 0
    assert "D018 1:" not in result.output
    assert "D018 2:" not in result.output
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert "J018 1:" not in result.output
    assert "J018 2:" not in result.output

    # test hash urls
    write_to_file(
        tmp_file.name,
        b'<a href="#">\n<form action="#"><a href="#tab">\n<form action="#go"></form></a></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0

    # test data-src
    write_to_file(
        tmp_file.name,
        b'<div class="em-ajaxLogs" data-src="/table/task/{{ t.id }}/log"></div>',
    )
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "D018 1:" in result.output
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert "J018 1:" in result.output

    # test mailto:
    write_to_file(
        tmp_file.name,
        b'<a href="mailto:joe"></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0

    # test attribute names
    write_to_file(
        tmp_file.name,
        b'<div data-row-selection-action="highlight"></div>',
    )
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 0
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
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


def test_H021(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<div style="asdf"></div>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H021 1:" in result.output

    write_to_file(
        tmp_file.name,
        b'<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet" />',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H021" not in result.output

    write_to_file(
        tmp_file.name,
        b'<acronym title="Cascading Style Sheets">CSS</acronym>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H021" not in result.output


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


def test_H026(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<asdf id="" >')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H026" in result.output

    write_to_file(tmp_file.name, b"<asdf id >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H026" in result.output

    write_to_file(tmp_file.name, b'<asdf class="" >')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H026" in result.output

    write_to_file(tmp_file.name, b'<asdf {% class="" %}></asdf>')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H026" not in result.output

    write_to_file(tmp_file.name, b"<div x-id-y><div id-y><div x-id>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H026" not in result.output


def test_T027(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% blah 'asdf %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "T027" in result.output

    write_to_file(tmp_file.name, b"{% blah 'asdf' %}{{ blah \"asdf\" }}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T027" not in result.output

    write_to_file(tmp_file.name, b"{% blah 'asdf' 'blah %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert result.exit_code == 1
    assert "T027" in result.output

    write_to_file(
        tmp_file.name,
        b'{% trans "Check box if you\'re interested in this location." %}',
    )
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T027" not in result.output

    # test mixed quotes
    write_to_file(
        tmp_file.name,
        b"{% macro rendersubmit(buttons=[], class=\"\", index='', url='', that=\"\" , test='') -%}",
    )
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert "T027" not in result.output


def test_T028(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<a href=\"{% blah 'asdf' -%}\">")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert result.exit_code == 1
    assert "T028" not in result.output

    write_to_file(tmp_file.name, b"<a href=\"{%- if 'asdf' %}\">")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert result.exit_code == 1
    assert "T028" in result.output

    # django should not trigger
    write_to_file(tmp_file.name, b"<a href=\"{%- if 'asdf' %}\">")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "jinja"])
    assert result.exit_code == 1
    assert "T028" in result.output

    write_to_file(tmp_file.name, b"<a href=\"{{- blah 'asdf' }}\">")
    result = runner.invoke(djlint, [tmp_file.name])
    assert "T028" not in result.output

    write_to_file(tmp_file.name, b"<a href=\"{{ blah 'asdf' -}}\">")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T028" not in result.output

    write_to_file(tmp_file.name, b"<a {{ blah 'asdf' }}>")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T028" not in result.output

    write_to_file(tmp_file.name, b"<a {% blah 'asdf' %}>")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T028" not in result.output

    write_to_file(tmp_file.name, b"{% blah 'asdf' %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T028" not in result.output

    write_to_file(tmp_file.name, b"{% for 'asdf' %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T028" not in result.output

    # class should not trigger
    write_to_file(tmp_file.name, b'<input class="{% if %}{% endif %}" />')
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
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


def test_T032(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% static ''  \"  \"  'foo/bar.min.css' %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T032" in result.output

    write_to_file(tmp_file.name, b"{% static  ''  %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T032" in result.output

    write_to_file(tmp_file.name, b"{% static '' \"     \" 'foo/bar.min.css' %}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T032" not in result.output

    write_to_file(tmp_file.name, b"{{ static ''  \"  \"  'foo/bar.min.css' }}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T032" in result.output

    write_to_file(tmp_file.name, b"{{ static  ''  }}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T032" in result.output

    write_to_file(tmp_file.name, b"{{ static '' \"     \" 'foo/bar.min.css' }}")
    result = runner.invoke(djlint, [tmp_file.name, "--profile", "django"])
    assert "T032" not in result.output


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
<p>
{{!-- djlint:on --}}

{{ /* djlint:off H025 */ }}
<p>
{{ /* djlint:on */ }}

""",
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert "H025" not in result.output
