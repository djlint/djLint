"""Djlint tests specific to jinja.

run::

   pytest tests/test_jinja/test_call.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_jinja/test_call.py::test_call --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_call(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"{% call 'cool' %}<div>some html</div>{% endcall %}"
    )
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{% call 'cool' %}
    <div>some html</div>
{% endcall %}
"""
    )

    output = reformat(
        tmp_file, runner, b"{% call('cool') %}<div>some html</div>{% endcall %}"
    )
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{% call('cool') %}
    <div>some html</div>
{% endcall %}
"""
    )

    # tags inside template tags should not be formatted.
    output = reformat(tmp_file, runner, b"{% call (a, b) render_form(form, '<hr>'>) %}")
    assert output.exit_code == 0
