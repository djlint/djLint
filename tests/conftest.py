import os
import tempfile

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    yield CliRunner()


@pytest.fixture
def tmp_file():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    yield tmp
    os.unlink(tmp.name)
