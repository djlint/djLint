"""Djlint tests specific to html.

run::

   pytest tests/test_html.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html.py::test_front_matter --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing


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
