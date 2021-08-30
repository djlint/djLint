"""
Djlint Tests.

run::

    pytest --cov=src/djlint --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

for a single test::

    pytest tests/test_djlint.py::test_W010 --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

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


def test_nonexisting_file(runner):
    result = runner.invoke(djlint, ["not_a_file.html"])
    assert result.exit_code == 2
    assert "Path 'not_a_file.html' does not exist." in result.output


def test_existing_file(runner):
    result = runner.invoke(djlint, ["tests/bad.html"])
    assert result.exit_code == 1
    assert str(Path("tests/bad.html")) in result.output


def test_bad_path(runner):
    result = runner.invoke(djlint, ["tests/nowhere"])
    assert result.exit_code == 2
    assert "does not exist." in result.output


def test_good_path_with_ext(runner):
    result = runner.invoke(djlint, ["tests/", "-e", "html"])
    assert result.exit_code == 1
    assert str(Path("tests/bad.html")) in result.output

    result = runner.invoke(djlint, ["tests/", "--extension", "html*"])
    assert result.exit_code == 1
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
    assert result.exit_code == 1
    assert "E001 1:" in result.output
    assert "E001 2:" in result.output


def test_E002(runner, tmp_file):
    write_to_file(tmp_file.name, b"{% extends 'this' %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "E002 1:" in result.output


def test_W003(runner, tmp_file):
    write_to_file(tmp_file.name, b"{% endblock %}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W003 1:" in result.output


def test_W004(runner, tmp_file):
    write_to_file(tmp_file.name, b'<link src="/static/there">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W004 1:" in result.output


def test_W005(runner, tmp_file):
    write_to_file(tmp_file.name, b"<!DOCTYPE html>\n<html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W005 2:" in result.output


def test_W006(runner, tmp_file):
    write_to_file(tmp_file.name, b"<img />")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W006 1:" in result.output
    assert "found 1 error" in result.output


def test_W007(runner, tmp_file):
    write_to_file(tmp_file.name, b'<html lang="en">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W007 1:" in result.output


def test_W008(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div class='test'>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W008 1:" in result.output


def test_W009(runner, tmp_file):
    write_to_file(tmp_file.name, b"<H1>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W009 1:" in result.output


def test_W010(runner, tmp_file):
    write_to_file(tmp_file.name, b'<img HEIGHT="12">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W010 1:" in result.output

    write_to_file(tmp_file.name, b"<li>ID=username</li>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_W011(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div class=test></div>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W011 1:" in result.output


def test_W012(runner, tmp_file):
    write_to_file(tmp_file.name, b'<div class = "stuff">')
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W012 1:" in result.output


def test_W013(runner, tmp_file):
    open(tmp_file.name, mode="wb").write(
        b"this is a very long line of random long text that is very long and should not be so long, hopefully it thows an error somwhere"
    )
    tmp_file.seek(0)
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W013 1:" in result.output


def test_W014(runner, tmp_file):
    write_to_file(tmp_file.name, b"</div>\n\n\n<p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W014 1:" in result.output


def test_W015(runner, tmp_file):
    write_to_file(tmp_file.name, b"</h1><p>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W015 1:" in result.output


def test_W016(runner, tmp_file):
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W016 1:" in result.output


def test_W017(runner, tmp_file):
    write_to_file(tmp_file.name, b"<img this >")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W017 1:" in result.output


def test_W018(runner, tmp_file):
    write_to_file(
        tmp_file.name,
        b'<a class="drop-link" href="/Collections?handler=RemoveAgreement&id=@a.Id">',
    )
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 1
    assert "W018 1:" in result.output


def test_handlebars_else(runner, tmp_file):
    write_to_file(tmp_file.name, b"{{^}}")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0
    assert "Linted 1 file, found 0 errors." in result.output


# assert "asdf" in result.output


def test_check(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--check"])
    assert result.exit_code == 0
    # assert "Linting 1 file!" in result.output
    # assert "Linted 1 file, found 0 errors" in result.output


def test_check_non_existing_file(runner, tmp_file):
    result = runner.invoke(djlint, ["tests/nothing.html", "--check"])
    assert result.exit_code == 2


def test_check_non_existing_folder(runner, tmp_file):
    result = runner.invoke(djlint, ["tests/nothing", "--check"])
    assert result.exit_code == 2


def test_check_django_ledger(runner, tmp_file):
    # source from https://github.com/arrobalytics/django-ledger
    runner.invoke(djlint, ["tests/django_ledger", "--check"])
    # assert result.exit_code == 1
    # assert "Linting 120 files!" in result.output
    # assert "0 files were updated." in result.output


def test_check_reformatter_simple_error(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--check"])
    assert result.exit_code == 1
    assert "1 file would be updated." in result.output


def test_reformatter_simple_error(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert result.exit_code == 1
    assert "1 file was updated." in result.output


def test_check_reformatter_simple_error_quiet(runner, tmp_file):
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--check", "--quiet"])
    assert result.exit_code == 1
    assert "1 file would be updated." in result.output


def test_check_reformatter_no_error(runner, tmp_file):
    write_to_file(
        tmp_file.name, b"<div>\n    <p>\n        nice stuff here\n    </p>\n</div>"
    )
    result = runner.invoke(djlint, [tmp_file.name, "--check"])
    assert result.exit_code == 0
    assert "0 files would be updated." in result.output


def test_reformat_asset_tag(runner, tmp_file):
    write_to_file(
        tmp_file.name,
        b"""{% block css %}{% assets "css_error" %}<link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />{% endassets %}{% endblock css %}""",
    )
    result = runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        open(tmp_file.name).read()
        == """{% block css %}
    {% assets "css_error" %}
        <link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />
    {% endassets %}
{% endblock css %}
"""
    )
    assert result.exit_code == 1


def test_textarea_tag(runner, tmp_file):
    write_to_file(tmp_file.name, b"""<div><textarea>\nasdf\n  asdf</textarea></div>""")
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        open(tmp_file.name).read()
        == """<div>
<textarea>
asdf
  asdf</textarea>
</div>
"""
    )


def test_script_tag(runner, tmp_file):
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <script>console.log();\n    console.log();\n\n    </script>\n</div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        open(tmp_file.name).read()
        == """<div>
    <script>
console.log();
    console.log();

    </script>
</div>
"""
    )


def test_html_comments_tag(runner, tmp_file):
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <!-- asdf-->\n\n   <!--\n multi\nline\ncomment--></div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        open(tmp_file.name).read()
        == """<div>
    <!-- asdf-->
   <!--
 multi
line
comment-->
</div>
"""
    )


def test_dj_comments_tag(runner, tmp_file):
    write_to_file(
        tmp_file.name,
        b"""{# comment #}\n{% if this %}<div></div>{% endif %}""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        open(tmp_file.name).read()
        == """{# comment #}\n{% if this %}<div></div>{% endif %}\n"""
    )
