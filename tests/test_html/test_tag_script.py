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


def test_script_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <script>console.log();\n    console.log();\n\n    </script>\n</div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<div>
    <script>console.log();
    console.log();

    </script>
</div>
"""
    )

    # check script includes
    output = reformat(
        tmp_file,
        runner,
        b"""<script src="{% static 'common/js/foo.min.js' %}"></script>""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<script>
    $("#x").do({
        dataBound: function () {
            this.tbody.append($("<td colspan=2'>X</td>"));
        },
    });
</script>
""",
    )

    assert output.exit_code == 0

    # check bad template tags inside scripts
    output = reformat(
        tmp_file,
        runner,
        b"""<script>{{missing_space}}</script>\n""",
    )

    assert output.exit_code == 0
