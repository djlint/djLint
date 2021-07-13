import tempfile

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    yield CliRunner()


@pytest.fixture
def tmp_file():
    with tempfile.NamedTemporaryFile() as tmp:
        yield tmp
