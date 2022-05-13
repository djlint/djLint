"""DjLint tests for yaml front matter.

run:

    pytest tests/test_html/test_yaml.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_yaml.py

"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import reformat, write_to_file

def test_invalid(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""---
    invalid:
invalid:
---



<html><head></head><body></body></html>""",
    )
    assert output.text == """---
    invalid:
invalid:
---
<html>
    <head>
    </head>
    <body>
    </body>
</html>
"""


def test_valid(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""
---
hello:     world
---
<html><head></head><body></body></html>""",
    )
    assert output.text == """---
hello:     world
---
<html>
    <head>
    </head>
    <body>
    </body>
</html>
"""

def test_more(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""---
layout: <div><div></div></div>
---
<div></div>""",
    )
    assert output.exit_code == 0
