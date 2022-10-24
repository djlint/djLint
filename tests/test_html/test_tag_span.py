"""Djlint tests for html span tag.

run:

    pytest tests/test_html/test_tag_span.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_tag_span.py::test_nested_string


"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import reformat, write_to_file


def test_span_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
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


def test_nested_string(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<p><p><span><strong>asdf</strong><br></span></p></p>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<p>
    <p>
        <span><strong>asdf</strong>
            <br>
        </span>
    </p>
</p>
"""
    )

    write_to_file(
        tmp_file.name,
        b"""<ul>
    <li>
        <span>C</span> <a>D</a> <strong>Q</strong>
    </li>
</ul>
""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<ul>
    <li>
        <span>C</span> <a>D</a> <strong>Q</strong>
    </li>
</ul>
"""
    )


def test_span_leading_text(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""{% if this %}<p>Text <span>text</span></p>{% endif %}""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """{% if this %}
    <p>
        Text <span>text</span>
    </p>
{% endif %}
"""
    )

    write_to_file(
        tmp_file.name,
        b"""<p>
    <span class="badge">New</span> You can now use <strong>this feature</strong>
</p>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<p>
    <span class="badge">New</span> You can now use <strong>this feature</strong>
</p>
"""
    )


def test_span_and_template(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""{% block content %}
    <span></span>{% blocktrans %}<div></div>{% endblocktrans %}
    {% endblock content %}
""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """{% block content %}
    <span></span>{% blocktrans %}<div></div>{% endblocktrans %}
{% endblock content %}
"""
    )
