"""Test djlintrc custom config.

poetry run pytest tests/test_config/test_djlintrc_custom

"""
from pathlib import Path

from src.djlint.settings import Config


def test_custom() -> None:
    config = Config(
        str(Path(__file__).parent / "blank.html"),
        configuration=str(Path(__file__).parent / ".djlint-cust"),
    )

    print(config.exclude)
    assert config.exclude == ".venv,venv,.tox,.egg,... | .customs"
    assert config.blank_line_after_tag == "load,extends,include"
    assert config.blank_line_before_tag == "load,extends,include"
    assert config.custom_blocks == r"|endexample\b|endtoc\b|example\b|toc\b"
    assert config.custom_html == r"|mjml|simple-greeting|mj-\w+"
    assert config.extension == "html.dj"
    assert config.files == ["index.html"]
    assert config.format_attribute_template_tags is True
    assert config.format_css is True
    assert config.format_js is True
    assert config.ignore == "H014,H015"
    assert config.ignore_blocks == r"endexample\b|endraw\b|example\b|raw\b"
    assert config.ignore_case is True
    assert config.include == "H014,H015"
    assert config.indent == 4 * " "
    assert config.linter_output_format == "{filename}:{line}: {code} {message} {match}"
    assert config.max_attribute_length == 10
    assert config.max_line_length == 120
    assert config.preserve_blank_lines is True
    assert config.preserve_leading_space is True
    assert config.profile == "django"
    assert config.require_pragma is True
    assert config.use_gitignore is True

    assert config.js_config == {"indent_size": 4}
    assert config.css_config == {"indent_size": 4}

    assert config.per_file_ignores == {
        "file.html": "H026,H025",
        "file_two.html": "H001",
    }
