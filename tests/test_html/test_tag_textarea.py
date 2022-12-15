"""Djlint tests for html textarea tag.

run:

    pytest tests/test_html/test_tag_textarea.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_tag_textarea.py::test_a_tag


"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import reformat, write_to_file


def test_textarea_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"""<div><textarea>\nasdf\n  asdf</textarea></div>""")
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<div>
    <textarea>
asdf
  asdf</textarea>
</div>
"""
    )
    # check double nesting
    output = reformat(
        tmp_file,
        runner,
        b"""<div>
    <div class="field">
        <textarea>asdf</textarea>
    </div>
</div>
""",
    )

    assert output.exit_code == 0

    # check attributes
    output = reformat(
        tmp_file,
        runner,
        b"""<div>
    <div class="field">
        <textarea class="this"
                  name="that">asdf</textarea>
    </div>
</div>
""",
    )

    assert (
        output.text
        == """<div>
    <div class="field">
        <textarea class="this" name="that">asdf</textarea>
    </div>
</div>
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""<div><textarea type="textarea" id="messageContent" name="adContent" maxlength="300" class="form-control class_two" rows="10">{{ adContent|default }}</textarea></div>
""",
    )

    assert (
        output.text
        == """<div>
    <textarea type="textarea"
              id="messageContent"
              name="adContent"
              maxlength="300"
              class="form-control class_two"
              rows="10">{{ adContent|default }}</textarea>
</div>
"""
    )


def test_a_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<p>
    some nice text <a href="this">asdf</a>, ok
</p>""",
    )

    assert output.exit_code == 0

    # test added for https://github.com/Riverside-Healthcare/djLint/issues/189
    output = reformat(
        tmp_file,
        runner,
        b"""<a>
    <span>hi</span>hi</a>
<div>
    <h4>{{ _("Options") }}</h4>
</div>
""",
    )

    assert output.exit_code == 0
