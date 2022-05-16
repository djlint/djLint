"""Djlint tests for html figure tag.

run:

    pytest tests/test_html/test_tag_fig_caption.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_tag_fig_caption.py::test_figure_figcaption_tags


"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import write_to_file


def test_figure_figcaption_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<figure><img src="" alt=""><figcaption>caption</figcaption></figure>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<figure>
    <img src="" alt="">
    <figcaption>
        caption
    </figcaption>
</figure>
"""
    )
