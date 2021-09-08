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


def test_E001(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{{test }}\n{% test%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "E001 1:" in result.output
    assert "E001 2:" in result.output

    write_to_file(tmp_file.name, b"{%- test-%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "E001 1:" in result.output

    write_to_file(tmp_file.name, b"{%-test -%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "E001 1:" in result.output

    write_to_file(tmp_file.name, b"{%- test -%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_E002(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% extends 'this' %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "E002 1:" in result.output


def test_W003(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"{% endblock %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W003 1:" in result.output


def test_W004(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<link src="/static/there">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W004 1:" in result.output


def test_W005(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<!DOCTYPE html>\n<html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W005 2:" in result.output


def test_W006(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<img />")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W006 1:" in result.output
    assert "found 1 error" in result.output


def test_W007(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<html lang="en">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W007 1:" in result.output


def test_W008(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div class='test'>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W008 1:" in result.output


def test_W009(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<H1>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W009 1:" in result.output


def test_W010(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<img HEIGHT="12">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W010 1:" in result.output

    write_to_file(tmp_file.name, b"<li>ID=username</li>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_W011(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div class=test></div>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W011 1:" in result.output


def test_W012(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b'<div class = "stuff">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W012 1:" in result.output


def test_W013(runner: CliRunner, tmp_file: TextIO) -> None:
    # pylint: disable=C0301
    write_to_file(
        tmp_file.name,
        b"this is a very long line of random long text that is very long and should not be so long, hopefully it thows an error somewhere",
    )  # noqa: E501
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W013 1:" in result.output


def test_W014(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"</div>\n\n\n<p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W014 1:" in result.output


def test_W015(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"</h1><p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W015 1:" in result.output


def test_W016(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W016 1:" in result.output


def test_W017(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<img this >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W017 1:" in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W017 1:" in result.output

    write_to_file(tmp_file.name, b"<br >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W017 1:" in result.output


def test_W018(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b'<a class="drop-link" href="/Collections?handler=RemoveAgreement&id=@a.Id">',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W018 1:" in result.output
