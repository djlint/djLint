"""Djlint tests specific to django.

run::

   pytest tests/test_django.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_django.py::test_comment --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_with(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% with total=business.employees.count %}{{ total }}<div>employee</div>{{ total|pluralize }}{% endwith %}""",
    )
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{% with total=business.employees.count %}
    {{ total }}
    <div>employee</div>
    {{ total|pluralize }}
{% endwith %}
"""
    )
