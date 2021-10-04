"""Djlint linter rule tests.

run::

   pytest tests/test_linter.py --cov=src/djlint --cov-branch \
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
    write_to_file(tmp_file.name, b"<img />")
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


def test_H012(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<div class = "stuff">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "H012 1:" in result.output


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
    write_to_file(tmp_file.name, b"<colgroup><colgroup asdf>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "H017 1:" not in result.output


def test_DJ018(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b'<a class="drop-link" href="/Collections?handler=RemoveAgreement&id=@a.Id">',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "D018 1:" in result.output
    assert "J018 1:" in result.output
