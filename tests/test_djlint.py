"""
Djlint Tests.

run::

    coverage erase; coverage run -m pytest; coverage report -m

or::

    tox
"""

from pathlib import Path

from src.djlint import main as djlint


def write_to_file(the_file, the_text):
    with open(the_file, mode="w+b") as open_file:
        open_file.write(the_text)


def test_help(runner):
    result = runner.invoke(djlint, ["-h"])
    assert result.exit_code == 0
    assert "Djlint django template files." in result.output


def test_bad_args(runner):
    result = runner.invoke(djlint, ["-a"])
    assert result.exit_code == 2
    assert "Error: No such option: -a" in result.output

    result = runner.invoke(djlint, ["--aasdf"])
    assert result.exit_code == 2
    assert "Error: No such option: --aasdf" in result.output


def test_bad_file(runner):
    result = runner.invoke(djlint, ["not_a_file.html"])
    assert result.exit_code == 2
    assert "Path 'not_a_file.html' does not exist." in result.output


def test_good_file(runner):
    result = runner.invoke(djlint, ["tests/bad.html"])
    assert result.exit_code == 0
    assert str(Path("tests/bad.html")) in result.output


def test_bad_path(runner):
    result = runner.invoke(djlint, ["tests/nowhere"])
    assert result.exit_code == 2
    assert "does not exist." in result.output


def test_good_path_with_ext(runner):
    result = runner.invoke(djlint, ["tests/", "-e", "html"])
    assert result.exit_code == 0
    assert str(Path("tests/bad.html")) in result.output

    result = runner.invoke(djlint, ["tests/", "--extension", "html*"])
    assert result.exit_code == 0
    assert str(Path("tests/bad.html")) in result.output
    assert str(Path("tests/bad.html.dj")) in result.output


def test_good_path_with_bad_ext(runner):
    result = runner.invoke(djlint, ["tests/", "-e", "html.alphabet"])
    assert result.exit_code == 0
    assert "No files to check!" in result.output


def test_empty_file(runner, tmp_file):
    write_to_file(tmp_file.name, b"")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_E001(runner, tmp_file):
    write_to_file(tmp_file.name, b"{{test }}\n{% test%}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "E001 1:" in result.output
    assert "E001 2:" in result.output


def test_E002(runner, tmp_file):
    write_to_file(tmp_file.name, b"{% extends 'this' %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "E002 1:" in result.output


def test_W003(runner, tmp_file):
    write_to_file(tmp_file.name, b"{% endblock %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W003 1:" in result.output


def test_W004(runner, tmp_file):
    write_to_file(tmp_file.name, b'<link src="/static/there">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W004 1:" in result.output


def test_W005(runner, tmp_file):
    write_to_file(tmp_file.name, b"<!DOCTYPE html>\n<html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W005 2:" in result.output


def test_W006(runner, tmp_file):
    write_to_file(tmp_file.name, b"<img />")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W006 1:" in result.output


def test_W007(runner, tmp_file):
    write_to_file(tmp_file.name, b'<html lang="en">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W007 1:" in result.output


def test_W008(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div class='test'>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W008 1:" in result.output


def test_W009(runner, tmp_file):
    write_to_file(tmp_file.name, b"<H1>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W009 1:" in result.output


def test_W010(runner, tmp_file):
    write_to_file(tmp_file.name, b'<img HEIGHT="12">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W010 1:" in result.output


def test_W011(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div class=test></div>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W011 1:" in result.output


def test_W012(runner, tmp_file):
    write_to_file(tmp_file.name, b'<div class = "stuff">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W012 1:" in result.output


def test_W013(runner, tmp_file):
    open(tmp_file.name, mode="wb").write(
        b"this is a very long line of random long text that is very long and should not be so long, hopefully it thows an error somwhere"
    )
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W013 1:" in result.output


def test_W014(runner, tmp_file):
    write_to_file(tmp_file.name, b"</div>\n\n\n<p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W014 1:" in result.output


def test_W015(runner, tmp_file):
    write_to_file(tmp_file.name, b"</h1><p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W015 1:" in result.output


def test_W016(runner, tmp_file):
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W016 1:" in result.output


def test_W017(runner, tmp_file):
    write_to_file(tmp_file.name, b"<img this >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W017 1:" in result.output


def test_W018(runner, tmp_file):
    write_to_file(
        tmp_file.name,
        b'<a class="drop-link" href="/Collections?handler=RemoveAgreement&id=@a.Id">',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W018 1:" in result.output


def test_check(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div></div>")
    result = runner.invoke(djlint, [tmp_file.name], "--check")
    assert result.exit_code == 0
    # assert "Linting 1 file!" in result.output
    # assert "Linted 1 file, found 0 errors" in result.output


def test_check_non_existing_file(runner, tmp_file):
    result = runner.invoke(djlint, "tests/nothing.html", "--check")
    assert result.exit_code == 2


def test_check_non_existing_folder(runner, tmp_file):
    result = runner.invoke(djlint, "tests/nothing", "--check")
    assert result.exit_code == 2


def test_check_django_ledger(runner, tmp_file):
    # source from https://github.com/arrobalytics/django-ledger
    result = runner.invoke(djlint, "tests/django_ledger", "--check")
    assert result.exit_code == 0
    # assert "Linting 120 files!" in result.output
    # assert "0 files were updated." in result.output
