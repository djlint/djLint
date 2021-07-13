"""Djlint Tests.

run::

    coverage erase; coverage run -m pytest; coverage report -m

or::

    tox
"""


from src.djlint import main as djlint


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
    assert "tests/bad.html" in result.output


def test_bad_path(runner):
    result = runner.invoke(djlint, ["tests/nowhere"])
    assert result.exit_code == 2
    assert "Path 'tests/nowhere' does not exist." in result.output


def test_good_path_with_ext(runner):
    result = runner.invoke(djlint, ["tests/", "-e", "html"])
    assert result.exit_code == 0
    assert "tests/bad.html" in result.output

    result = runner.invoke(djlint, ["tests/", "--extension", "html*"])
    assert result.exit_code == 0
    assert "tests/bad.html" in result.output
    assert "tests/bad.html.dj" in result.output


def test_good_path_with_bad_ext(runner):
    result = runner.invoke(djlint, ["tests/", "-e", "html.alphabet"])
    assert result.exit_code == 0
    assert "No files to lint!" in result.output


def test_empty_file(runner, tmp_file):
    tmp_file.write(b"")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_E001(runner, tmp_file):
    tmp_file.write(b"{{test }}\n{% test%}")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "E001 1:" in result.output
    assert "E001 2:4" in result.output


def test_E002(runner, tmp_file):
    tmp_file.write(b"{% extends 'this' %}")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "E002 1:" in result.output


def test_W003(runner, tmp_file):
    tmp_file.write(b"{% endblock %}")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W003 1:" in result.output


def test_W004(runner, tmp_file):
    tmp_file.write(b'<link src="/static/there">')
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W004 1:" in result.output


def test_W005(runner, tmp_file):
    tmp_file.write(b"<!DOCTYPE html>\n<html>")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W005 2:" in result.output


def test_W006(runner, tmp_file):
    tmp_file.write(b"<img />")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W006 1:" in result.output


def test_W007(runner, tmp_file):
    tmp_file.write(b'<html lang="en">')
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W007 1:" in result.output


def test_W008(runner, tmp_file):
    tmp_file.write(b"<div class='test'>")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W008 1:" in result.output


def test_W009(runner, tmp_file):
    tmp_file.write(b"<H1>")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W009 1:" in result.output


def test_W010(runner, tmp_file):
    tmp_file.write(b'<img HEIGHT="12">')
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W010 1:" in result.output


def test_W011(runner, tmp_file):
    tmp_file.write(b"<div class=test></div>")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W011 1:" in result.output


def test_W012(runner, tmp_file):
    tmp_file.write(b'<div class = "stuff">')
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W012 1:" in result.output


def test_W013(runner, tmp_file):
    tmp_file.write(
        b"this is a very long line of random long text that is very long and should not be so long, hopefully it thows an error somwhere"
    )
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W013 1:" in result.output


def test_W014(runner, tmp_file):
    tmp_file.write(b"</div>\n\n\n<p>")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W014 1:" in result.output


def test_W015(runner, tmp_file):
    tmp_file.write(b"</h1><p>")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W015 1:" in result.output


def test_W016(runner, tmp_file):
    tmp_file.write(b"<html>\nstuff\n</html>")
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "W016 1:" in result.output
