"""Djlint tests specific to django.

run::

   pytest tests/test_django.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_django.py::test_alpine_js --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_blocktranslate(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktranslate %}The width is: {{ width }}{% endblocktranslate %}""",
    )
    assert output.exit_code == 0
    assert (
        output.text
        == r"""{% blocktranslate %}The width is: {{ width }}{% endblocktranslate %}
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktranslate trimmed %}The width is: {{ width }}{% endblocktranslate %}""",
    )
    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktrans %}The width is: {{ width }}{% endblocktrans %}""",
    )
    assert output.exit_code == 0
    assert (
        output.text
        == r"""{% blocktrans %}The width is: {{ width }}{% endblocktrans %}
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktrans trimmed %}The width is: {{ width }}{% endblocktrans %}""",
    )
    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<p>
    {% blocktrans %}If you have not created an account yet, then please
    <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}
</p>\n""",
    )
    assert output.exit_code == 0


# def test_trans(runner: CliRunner, tmp_file: TextIO) -> None:
#     output = reformat(
#         tmp_file, runner, b"""<p>{% trans 'Please do <b>Blah</b>.' %}</p>"""
#     )
#     assert output.exit_code == 1
#     assert (
#         """<p>
#     {% trans 'Please do <b>Blah</b>.' %}
# </p>
# """
#         in output.text
#     )
