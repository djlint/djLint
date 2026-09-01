# ruff: noqa: N802
"""Djlint linter rule tests.

run::

   pytest tests/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   # for a single test

   pytest tests/test_linter/test_linter.py::test_random

Test setup

(html, (list of codes that should file, plus optional line number))


"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint
from djlint.output import build_stats_output
from tests.conftest import write_to_file

if TYPE_CHECKING:
    from tempfile import _TemporaryFileWrapper

    import pytest
    from click.testing import CliRunner

    from djlint.settings import Config
    from djlint.types import LintError


def test_H011(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div class=test></div>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H011 1:" in result.output

    # check for no matches inside template tags
    write_to_file(tmp_file.name, b" {{ func( id=html_id,) }}")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0
    assert "H011 1:" not in result.output

    # check meta tag
    write_to_file(
        tmp_file.name,
        b'<meta name="viewport" content="width=device-width, initial-scale=1">',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H011 1:" not in result.output

    # check keywords inside template syntax
    write_to_file(
        tmp_file.name,
        b"<a href=\"{{ url_for('connection_bp.one_connection', connection_id=connection.id) }}\">{{ connection }}</a>",
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H011 1:" not in result.output


def test_H012(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<div class = "stuff">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H012 1:" in result.output

    # test for not matching random "=" in text
    write_to_file(tmp_file.name, b"<h3>#= title #</h3>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0
    assert "H012 1:" not in result.output

    # test for not matching "=" in template condition
    write_to_file(
        tmp_file.name,
        b"<p>{% if activity.reporting_groups|length <= 0 %}<h3>{% trans 'General' %}</h3>{% endif %}</p>",
    )
    result = runner.invoke(djlint, (tmp_file.name,))
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
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H012" not in result.output


def test_H013(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<img height="12" width="12"/>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H013 1:" in result.output
    print(result.output)
    assert "found 1 error" in result.output

    # a name that merely ends in "alt" is a different attribute
    write_to_file(tmp_file.name, b'<img src="a" data-alt="b"/>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H013 1:" in result.output

    # and an "alt=" written inside a value is not an attribute at all
    write_to_file(tmp_file.name, b'<img src="a" title="alt=x"/>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H013 1:" in result.output

    write_to_file(tmp_file.name, b'<img src="a" alt="b"/>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H013" not in result.output

    write_to_file(tmp_file.name, b'<img src="a" alt = "b"/>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H013" not in result.output


def test_H014(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    # the report points at the first blank line, not the content line above
    write_to_file(tmp_file.name, b"</div>\n\n\n<p>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H014 2:" in result.output

    # a line holding only whitespace is a blank line too
    write_to_file(tmp_file.name, b"</div>\n\n   \n<p>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H014 2:" in result.output

    # one blank line is a paragraph break rather than an extra
    write_to_file(tmp_file.name, b"</div>\n\n<p>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H014" not in result.output

    # the threshold follows the options, so the formatter's own output is
    # never rejected
    write_to_file(tmp_file.name, b"</div>\n\n\n<p>")
    result = runner.invoke(djlint, (tmp_file.name, "--max-blank-lines", "2"))
    assert "H014" not in result.output

    result = runner.invoke(djlint, (tmp_file.name, "--preserve-blank-lines"))
    assert "H014" not in result.output


def test_H015(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"</h1><p>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H015 1:" in result.output


def test_H016(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H016 1:" in result.output

    write_to_file(tmp_file.name, b"<html>\n<title>stuff</title>\n</html>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H016" not in result.output

    write_to_file(
        tmp_file.name,
        b"""\
        <html>
        <title id="title-reload-with-htmx" data-foo="bar">stuff</title>
        </html>""",
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H016" not in result.output


def test_H017(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<img this >")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H017 1:" not in result.output

    write_to_file(tmp_file.name, b"<img this >")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    # H017 and H018 enforce opposite conventions
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017,H018"))
    assert "H017 and H018 enforce opposite void tag styles" in result.output

    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    assert "conflicts" not in result.output

    # obsolete elements are no longer styled
    write_to_file(tmp_file.name, b"<keygen><command><menuitem>")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    assert "H017" not in result.output

    write_to_file(tmp_file.name, b"<keygen/><command/><menuitem/>")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    assert "H018" not in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H017 1:" not in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    write_to_file(tmp_file.name, b"<br >")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H017 1:" not in result.output

    write_to_file(tmp_file.name, b"<br >")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    write_to_file(tmp_file.name, b'<meta charset="utf-8">')
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    assert result.exit_code == 1
    assert "H017 1:" in result.output

    # test colgroup tag
    write_to_file(
        tmp_file.name, b"<colgroup><colgroup asdf></colgroup></colgroup>"
    )
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    print(result.output)
    assert "H017 1:" not in result.output

    # test template tags inside html
    write_to_file(tmp_file.name, b"<image {{ > }} />")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
    assert "H017" not in result.output


def test_H018(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<img this />")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H018 1:" not in result.output

    write_to_file(tmp_file.name, b"<img this />")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    assert result.exit_code == 1
    assert "H018 1:" in result.output

    write_to_file(tmp_file.name, b"<br/>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H018 1:" not in result.output

    write_to_file(tmp_file.name, b"<br/>")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    assert result.exit_code == 1
    assert "H018 1:" in result.output

    write_to_file(tmp_file.name, b"<br />")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H018 1:" not in result.output

    write_to_file(tmp_file.name, b"<br />")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    assert result.exit_code == 1
    assert "H018 1:" in result.output

    write_to_file(tmp_file.name, b'<meta charset="utf-8" />')
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    assert result.exit_code == 1
    assert "H018 1:" in result.output

    # test svg path tag
    write_to_file(tmp_file.name, b'<svg><path d="M0 0" /></svg>')
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    assert "H018" not in result.output

    # test colgroup tag
    write_to_file(
        tmp_file.name, b"<colgroup><colgroup asdf></colgroup></colgroup>"
    )
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    print(result.output)
    assert "H018 1:" not in result.output

    # test template tags inside html
    write_to_file(tmp_file.name, b"<image {{ /> }} >")
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H018"))
    assert "H018" not in result.output


def test_DJ018(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(
        tmp_file.name,
        b'<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n<form action="/Collections"></form></a>',
    )

    # test hash urls
    write_to_file(
        tmp_file.name,
        b'<a href="#">\n<form action="#"><a href="#tab">\n<form action="#go"></form></a></form></a>',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0


def test_H019(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<a href='javascript:abc()'>asdf</a>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H019 1:" in result.output

    write_to_file(tmp_file.name, b"<form action='javascript:abc()'></form>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H019 1:" in result.output


def test_H020(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div></div>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H020 1:" in result.output

    write_to_file(tmp_file.name, b"<span>\n   </span>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H020 1:" in result.output

    write_to_file(tmp_file.name, b"<td></td>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0
    assert "H020" not in result.output

    # https://github.com/djlint/djLint/issues/866
    write_to_file(tmp_file.name, b"<slot></slot>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0
    assert "H020" not in result.output


def test_H022(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<a href="http://">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H022 1:" in result.output


def test_H023(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    for reported in (b"&mdash;", b"&aacute;", b"&#63;", b"&#x3F;", b"&copy;"):
        write_to_file(tmp_file.name, reported)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert result.exit_code == 1
        assert "H023 1:" in result.output

    # syntax, and characters that cannot be reviewed as a literal, are allowed
    for quiet in (
        b"&gt;",
        b"&amp;",
        b"&apos;",
        b"&shy;",
        b"&nbsp;",
        b"&zwnj;",
        b"&zwj;",
        b"&lrm;",
        b"&hairsp;",
        b"&#8203;",
        b"&#x200c;",
        b"&#160;",
        b"&#xfeff;",
        b'<a href=" foo & bar; "></a>',
    ):
        write_to_file(tmp_file.name, quiet)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H023" not in result.output

    write_to_file(tmp_file.name, b'<a href=" &#63; "></a>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H023 1:" in result.output


def test_H024(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<script type="hare">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H024" not in result.output

    write_to_file(tmp_file.name, b'<script type="text/javascript">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H024" in result.output

    write_to_file(tmp_file.name, b'<script type="text/css">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H024" in result.output


def test_H025(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H025 1:" in result.output

    write_to_file(tmp_file.name, b"<!-- comment -->")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<!DOCTYPE html>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<link {% url_for('something') %} />")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<br>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<alpha />")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<alpha>\n</alpha>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(
        tmp_file.name,
        b'<script src="{% static \'notifications/notify.js\' %}" type="text/javascript"></script>',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(
        tmp_file.name,
        b'<script src="{% static "folder/foo.js" %}?version={% some_version %}"></script>',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<script />")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<tr ><td>Foo</td></tr>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<p>Foo\n<p>Foo</p>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025 1:" in result.output
    assert "H025 2:" not in result.output

    write_to_file(
        tmp_file.name,
        b"""<p>Here comes a paragraph
<ul>
    <li>First Item</li>
</ul>
</p>""",
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert (
        "H025 2:0 List tags should not be nested inside p tags. <ul>"
        in result.output
    )

    # test tags inside attributes
    write_to_file(tmp_file.name, b'<span title="<p>Bar</p>">Foo</span>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    # issue #364
    write_to_file(
        tmp_file.name,
        b'{% if tag|startswith:"<del>" %}\n{% if tag|startswith:"<ins>" %}\n{% endif %}\n{% endif %}',
    )
    result = runner.invoke(djlint, (tmp_file.name, "--profile=django"))
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<div><span>x</span>{# <div> #}</div>")
    result = runner.invoke(djlint, (tmp_file.name, "--profile=django"))
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(
        tmp_file.name,
        b"""<div
    data-x="{{Func
        "a"}}">
</div>""",
    )
    result = runner.invoke(djlint, (tmp_file.name, "--profile=golang"))
    assert result.exit_code == 0
    assert "H025" not in result.output

    write_to_file(
        tmp_file.name,
        b"""  <div class="list-group-item">
    <h3 class="mb-3 text-center">
    </h3>
    <form method="post" action="{% url 'account_login' %}">
        <input type="hidden"
               value="{{ redirect_field_value }}" />
      <div class="mb-3 text-center">
      </div>
      <button type="submit" class="btn btn-primary w-100">
      </button>
    </form>
  </div>
  <div class="list-group-item text-center">
      <a href="{{ signup_url }}"
         class="link-underline link-underline-opacity-0 link-underline-opacity-100-hover">sign up</a>.
  </div>""",
    )
    result = runner.invoke(djlint, (tmp_file.name, "--profile=django"))
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<col>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"<col />")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    # fix issue #164
    write_to_file(
        tmp_file.name,
        b"""<th {{ attrs }}>
    <a href="{% url %}">{{ content }}</a>
</th>""",
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    # fix issue #169
    write_to_file(
        tmp_file.name,
        b"""<li{% if is_active %} class="active" {% endif %}>
    some content
</li>""",
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    # test {# #} inside tag
    write_to_file(tmp_file.name, b'<div id="example" {# for #}></div>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    # check closing tag inside a comment
    write_to_file(
        tmp_file.name,
        b'<input {# value="{{ driverId|default(\' asdf \') }}" /> #} value="this">',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H025" not in result.output

    # issue #447
    write_to_file(
        tmp_file.name,
        b"""<button title="{% trans "text with ONE single ' quote" %}">
</button>""",
    )
    assert "H025" not in result.output

    write_to_file(tmp_file.name, b"</p></p>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H025 1:0" in result.output
    assert "H025 1:4" in result.output

    write_to_file(tmp_file.name, b"</p><p></p></p>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H025 1:0" in result.output
    assert "H025 1:11" in result.output

    # issue #483: the same tag opened in both branches of a conditional
    # shares one close tag.
    write_to_file(
        tmp_file.name,
        b"""{% if foo.bar %}
<tr class="foo">
{% else %}
<tr>
{% endif %}
    <td>Foo</td>
</tr>""",
    )
    result = runner.invoke(djlint, (tmp_file.name, "--profile=jinja"))
    assert result.exit_code == 0
    assert "H025" not in result.output

    # a close tag in each branch of a conditional shares one open tag
    write_to_file(
        tmp_file.name,
        b"""<div>
{% if x %}
</div>
{% else %}
</div>
{% endif %}""",
    )
    result = runner.invoke(djlint, (tmp_file.name, "--profile=django"))
    assert result.exit_code == 0
    assert "H025" not in result.output

    # issue #787: mis-nested tags
    write_to_file(
        tmp_file.name, b"<h1>blah <b>bold</h1>\n<p>blah</b> blah blah</p>"
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H025 1:9" in result.output
    assert "H025 2:7" in result.output

    # tags conditionally opened and closed in separate conditionals are
    # not mis-nesting
    write_to_file(
        tmp_file.name,
        b"{% if a %}<b>{% else %}<i>{% endif %}text"
        b"{% if a %}</b>{% else %}</i>{% endif %}",
    )
    result = runner.invoke(djlint, (tmp_file.name, "--profile=django"))
    assert result.exit_code == 0
    assert "H025" not in result.output


def test_T027(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<a href=\"{{- blah 'asdf' }}\">")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "T028" not in result.output


def test_H029(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<forM method="Post">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H029" in result.output

    write_to_file(tmp_file.name, b'<forM method="post">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H029" not in result.output

    write_to_file(tmp_file.name, b'<a method="post">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H029" not in result.output


def test_H030(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<html>\nstuff\n</html>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H030 1:" in result.output

    write_to_file(
        tmp_file.name,
        b'<html>\n<meta name="description" content="nice"/>\n</html>',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H030" not in result.output

    # a name that merely ends in "name" does not carry the description
    write_to_file(
        tmp_file.name,
        b'<html>\n<meta data-name="description" content="nice"/>\n</html>',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H030 1:" in result.output


def test_H036(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    for reported in (
        b"<p>a<br><br>b</p>",
        b"<p>a<br />\n<br />b</p>",
        b"<p><br>a</p>",
        b"<div>a<br></div>",
        b"<li>a<br/></li>",
    ):
        write_to_file(tmp_file.name, reported)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert result.exit_code == 1, reported
        assert "H036 1:" in result.output

    # a break that is part of the content, as the html specification puts it
    for quiet in (
        b"<p>Acme Ltd<br>1 High St<br>Springfield</p>",
        b"<address>a<br>b</address>",
        b"<br>",
    ):
        write_to_file(tmp_file.name, quiet)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H036" not in result.output, quiet


def test_rules_not_matched_in_ignored_block(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<script><div class=test></script>")
    result = runner.invoke(djlint, (tmp_file.name,))

    assert result.exit_code == 0
    assert "H011 1:" not in result.output


def test_output_for_no_linebreaks(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<a\n    class='asdf'></a>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "<a\n" not in result.output

    write_to_file(tmp_file.name, b"<h1>asdf</h1>\n    <h2>asdf</h2>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1

    assert "</h1>\n" not in result.output


def test_output_order(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<h1>asdf</h2>\n    <h3>asdf</h4>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1

    assert (
        """H025 1:0 Tag seems to be an orphan. <h1>
H015 1:8 Follow h tags with a line break. </h2> <h3
H025 1:8 Tag seems to be an orphan. </h2>
H025 2:4 Tag seems to be an orphan. <h3>
H025 2:12 Tag seems to be an orphan. </h4>"""
        in result.output
    )


def test_ignoring_rules(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
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
    result = runner.invoke(djlint, (tmp_file.name,))
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
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H006" not in result.output


def test_statistics_empty(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"")
    result = runner.invoke(djlint, (tmp_file.name, "--statistics"))

    assert result.exit_code == 0
    assert "Statistics" in result.output


def test_statistics_with_results(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<div>\n<img src="x">\n<img src="y">\n')
    result = runner.invoke(djlint, (tmp_file.name, "--statistics"))

    assert result.exit_code == 1
    stats = result.output.split("Statistics", 1)[1].splitlines()
    counted = [line for line in stats if line.startswith(("H013", "H025"))]
    assert counted == [
        "H013 2 Img tag should have an alt attribute.",
        "H025 1 Tag seems to be an orphan.",
    ]


def test_statistics_counts_codes_of_custom_modules(
    capsys: pytest.CaptureFixture[str], basic_config: Config
) -> None:
    lint_message: dict[str, list[LintError]] = {
        "source.html": [
            {"code": "MY001a", "line": "1:0", "match": "x", "message": ""}
        ]
    }

    assert build_stats_output((lint_message,), basic_config) == 1
    assert "MY001a 1" in capsys.readouterr().out


def test_H043(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<button>Save</button>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 1
    assert "H043 1:" in result.output

    write_to_file(tmp_file.name, b'<button type="submit">Save</button>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H043" not in result.output

    # a name that merely ends in "type" is a different attribute
    write_to_file(tmp_file.name, b'<button data-type="a">Save</button>')
    result = runner.invoke(djlint, (tmp_file.name, "--include", "H043"))
    assert "H043 1:" in result.output

    # a type given by a template tag counts
    write_to_file(
        tmp_file.name,
        b'<button {% if x %}type="button"{% endif %}>Save</button>',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H043" not in result.output


def test_H016_title_with_attributes(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    document = (
        b'<!DOCTYPE html><html lang="en"><head>%s</head><body>x</body></html>'
    )

    for head in (
        b"<title>P</title>",
        b"<title id='t'>P</title>",
        b'<title hx-swap-oob="true">P</title>',
    ):
        write_to_file(tmp_file.name, document % head)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H016" not in result.output

    write_to_file(tmp_file.name, document % b'<meta charset="utf-8">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H016 1:" in result.output


def test_H022_loopback_and_prose(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<a href="http://example.com">x</a>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H022 1:" in result.output

    for quiet in (
        b'<a href="http://localhost:8000/admin/">x</a>',
        b'<a href="http://127.0.0.1:5432/health">x</a>',
        b'<a href="http://192.168.1.1/">x</a>',
        b'<a href="/docs" title="Set src=\'http://localhost\' in dev.ini">g</a>',
        b'<a data-href="http://example.com">x</a>',
    ):
        write_to_file(tmp_file.name, quiet)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H022" not in result.output


def test_H024_covers_link_and_anchors_the_name(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    for reported in (
        b'<script type="text/javascript" src="app.js"></script>',
        b'<style type="text/css">a{color:red}</style>',
        b'<link rel="stylesheet" type="text/css" href="a.css">',
    ):
        write_to_file(tmp_file.name, reported)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H024 1:" in result.output

    for quiet in (
        b'<script type="module" src="a.js"></script>',
        b'<script data-type="text/css" src="a.js"></script>',
    ):
        write_to_file(tmp_file.name, quiet)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H024" not in result.output


def test_D018_only_reports_a_hardcoded_route(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    for quiet in (
        b'<a href="{% url \'profile\' %}" data-src="lazy">p</a>',
        b'<div class="card" data-src="avatar"></div>',
        b"<form action=\" {% url 'search' %}\">f</form>",
        b'<a href="/static/doc.pdf">d</a>',
        b'<a href="/media/uploads/1.png">m</a>',
    ):
        write_to_file(tmp_file.name, quiet)
        result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
        assert "D018" not in result.output

    for reported in (
        b'<a href="/cart">c</a>',
        b'<div data-src="/table/1/log"></div>',
    ):
        write_to_file(tmp_file.name, reported)
        result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
        assert "D018 1:" in result.output


def test_H043_steps_over_a_template_block(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(
        tmp_file.name,
        b'<button {% if n > 5 %}type="button"{% endif %}>S</button>',
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H043" not in result.output


def test_tag_rules_skip_markup_inside_an_attribute_value(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    for quiet in (
        b'<div title="<button>x</button>">y</div>',
        b'<p title="a<br><br>b">x</p>',
        b"<p title=\"an <img src='a.png'>\">y</p>",
    ):
        write_to_file(tmp_file.name, quiet)
        result = runner.invoke(djlint, (tmp_file.name, "--include", "H017"))
        for code in ("H043", "H036", "H013", "H017"):
            assert code not in result.output, (quiet, code)


def test_H029_needs_a_name_boundary(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(
        tmp_file.name, b'<form data-method="POST" method="post"></form>'
    )
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H029" not in result.output

    write_to_file(tmp_file.name, b'<form method="POST"></form>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H029 1:" in result.output


def test_H009_matches_what_the_formatter_fixes(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    # the formatter does not know these, so the rule must not ask for them
    for quiet in (
        b"<svg><G><PATH d='M0 0'/></G></svg>",
        b"<NAME>n</NAME>",
        b"<CACHE>c</CACHE>",
        b"<svg><clipPath id='a'/></svg>",
        b'<p title="x <DIV y">t</p>',
    ):
        write_to_file(tmp_file.name, quiet)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H009" not in result.output, quiet

    for reported in (b"<DIV>d</DIV>", b"<NAV>n</NAV>", b"<Div>x</Div>"):
        write_to_file(tmp_file.name, reported)
        result = runner.invoke(djlint, (tmp_file.name,))
        assert "H009 1:" in result.output, reported


def test_H013_accepts_a_valueless_alt(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<img src="a.png" alt>')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H013" not in result.output

    write_to_file(tmp_file.name, b'<img src="a.png">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H013 1:" in result.output


def test_T034_ignores_a_brace_inside_a_string(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<div>{% trans "Save 50}% today" %}</div>')
    result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
    assert "T034" not in result.output

    write_to_file(tmp_file.name, b"<div>{% if a }%</div>")
    result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
    assert "T034 1:" in result.output


def test_T038_leaves_a_custom_paired_tag_alone(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"{% mytag %}x{% endmytag %}")
    result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
    assert "T038" not in result.output

    # nothing opened it, so this one really is an orphan
    write_to_file(tmp_file.name, b"{% endmytag %}")
    result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
    assert "T038 1:" in result.output


def test_T027_ignores_a_delimiter_inside_a_string(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"{{ x|default('}}') }}")
    result = runner.invoke(djlint, (tmp_file.name, "--profile", "jinja"))
    assert "T027" not in result.output

    write_to_file(tmp_file.name, b'{% trans "oops %}')
    result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
    assert "T027 1:" in result.output


def test_H037_counts_a_valueless_attribute(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<input required required>")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H037 1:" in result.output

    write_to_file(tmp_file.name, b'<input required type="a">')
    result = runner.invoke(djlint, (tmp_file.name,))
    assert "H037" not in result.output


def test_H012_sees_past_a_template_tag(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b'<div {{ attrs }} class = "x">y</div>')
    result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
    assert "H012 1:" in result.output
