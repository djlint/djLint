"""Djlint test config."""
import os
import tempfile
from pathlib import Path
from typing import Generator, TextIO

import pytest
from click.testing import CliRunner

from src.djlint import main as djlint


@pytest.fixture()
def runner() -> CliRunner:
    """Click runner for djlint tests."""
    return CliRunner()


@pytest.fixture()
def tmp_file() -> Generator:
    """Create a temp file for formatting."""
    # pylint: disable=R1732
    tmp = tempfile.NamedTemporaryFile(delete=False)
    yield tmp
    tmp.close()
    os.unlink(tmp.name)


def write_to_file(the_file: str, the_text: bytes) -> None:
    """Shortcode for write some bytes to a file."""
    with open(the_file, mode="w+b") as open_file:
        open_file.write(the_text)


def reformat(the_file: TextIO, runner: CliRunner, the_text: bytes) -> dict:
    write_to_file(the_file.name, the_text)
    result = runner.invoke(djlint, [the_file.name, "--reformat"])
    return {"text": Path(the_file.name).read_text(), "exit_code": result.exit_code}
