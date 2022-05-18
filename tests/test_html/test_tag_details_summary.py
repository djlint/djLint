"""Djlint tests for html details/summary tag.

run:

    pytest tests/test_html/test_tag_details_summary.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_tag_details_summary.py::test_details_summary_tags

"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import write_to_file


def test_details_summary_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<details><summary>summary</summary>body</details>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<details>
    <summary>
        summary
    </summary>
    body
</details>
"""
    )
