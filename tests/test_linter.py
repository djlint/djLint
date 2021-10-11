"""Djlint linter rule tests.

run::

   pytest tests/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   # for a single test

   pytest tests/test_linter.py::test_H025 --cov=src/djlint --cov-branch \
         --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116,C0103

from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint

from .conftest import write_to_file


def test_T001(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{{test }}\n{% test%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "T001 1:" in result.output
    assert "T001 2:" in result.output

    write_to_file(tmp_file.name, b"{%- test-%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "T001 1:" in result.output

    write_to_file(tmp_file.name, b"{%-test -%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "T001 1:" in result.output

    write_to_file(tmp_file.name, b"{%- test -%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_T002(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% extends 'this' %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "T002 1:" in result.output


def test_T003(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% endblock %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "T003 1:" in result.output


def test_DJ004(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<link src="/static/there">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "D004 1:" in result.output
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
    assert result.exit_code == 0
    assert "H017 1:" not in result.output


def test_DJ018(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b'<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n<form action="/Collections"></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "D018 1:" in result.output
    assert "J018 1:" in result.output
    assert "D018 2:" in result.output
    assert "J018 2:" in result.output

    # test javascript functions
    write_to_file(
        tmp_file.name,
        b'<a href="javascript:abc()">\n<form action="javascript:abc()"></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    # don't check status code. will fail on other rules here.
    assert "D018 1:" not in result.output
    assert "J018 1:" not in result.output
    assert "D018 2:" not in result.output
    assert "J018 2:" not in result.output

    # test on_ events
    write_to_file(
        tmp_file.name,
        b'<a href="onclick:abc()">\n<form action="onclick:abc()"></form></a>',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "D018 1:" not in result.output
    assert "J018 1:" not in result.output
    assert "D018 2:" not in result.output
    assert "J018 2:" not in result.output

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

    write_to_file(tmp_file.name, b"<tr ><td>Foo</td></tr>")
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


def test_rules_not_matched_in_ignored_block(
    runner: CliRunner, tmp_file: TextIO
) -> None:
    write_to_file(tmp_file.name, b"<script><div class=test></script>")
    result = runner.invoke(djlint, [tmp_file.name])
    print(result.output)
    assert result.exit_code == 0
    assert "H011 1:" not in result.output


def test_custom_rules(runner: CliRunner, tmp_file: TextIO) -> None:
    result = runner.invoke(djlint, ["tests/custom_rules"])
    assert """Linting""" in result.output
    assert """1/1""" in result.output
    assert """T001 1:""" in result.output
    assert result.exit_code == 1


def test_custom_rules_bad_config(runner: CliRunner, tmp_file: TextIO) -> None:
    result = runner.invoke(djlint, ["tests/custom_rules_bad"])
    assert """Linting""" in result.output
    assert """1/1""" in result.output
    assert """T001 1:""" in result.output
    assert result.exit_code == 1
