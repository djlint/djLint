"""Test djlintrc config.

uv run pytest tests/test_config/test_djlintrc

"""

from __future__ import annotations

from pathlib import Path

from djlint.settings import Config


def test_default() -> None:
    config = Config(str(Path(__file__).parent / "blank.html"))

    assert config.exclude == ".venv | venv | .tox | .eggs | ... | .custom"
    assert config.blank_line_after_tag == "load,extends,include"
    assert config.blank_line_before_tag == "load,extends,include"
    assert config.custom_blocks == r"|endexample\b|endtoc\b|example\b|toc\b"
    assert config.custom_html == r"|mjml|simple-greeting|mj-\w+"
    assert config.extension == "html.dj"
    assert config.files == ["index.html"]
    assert config.format_attribute_template_tags is True
    assert config.format_attribute_js_json_min_props == 3
    assert config.format_css is True
    assert config.format_js is True
    assert config.ignore == "H014,H015"
    assert config.ignore_blocks == r"endexample\b|endraw\b|example\b|raw\b"
    assert config.ignore_case is True
    assert config.include == "H014,H015"
    assert config.indent == 3 * " "
    assert (
        config.linter_output_format
        == "{filename}:{line}: {code} {message} {match}"
    )
    assert config.max_attribute_length == 10
    assert config.max_line_length == 120
    assert config.preserve_blank_lines is True
    assert config.preserve_class_newlines is True
    assert config.preserve_leading_space is True
    assert config.profile == "django"
    assert config.require_pragma is True
    assert config.use_gitignore is True

    assert config.js_config == {"indent_size": 5}
    assert config.css_config == {"indent_size": 5}

    assert config.per_file_ignores == {
        "file.html": "H026,H025",
        "file_two.html": "H001",
    }


def test_dot_djlint_toml(tmp_path: Path) -> None:
    html_file = tmp_path / "templates" / "blank.html"
    html_file.parent.mkdir()
    html_file.write_text("<div></div>", encoding="utf-8")
    (tmp_path / ".djlint.toml").write_text(
        'extension = "html.j2"\nignore = "H014,H015"', encoding="utf-8"
    )

    config = Config(str(html_file))

    assert config.project_root == tmp_path
    assert config.extension == "html.j2"
    assert config.ignore == "H014,H015"


def test_djlint_toml_precedes_dot_djlint_toml(tmp_path: Path) -> None:
    html_file = tmp_path / "blank.html"
    html_file.write_text("<div></div>", encoding="utf-8")
    (tmp_path / "djlint.toml").write_text('ignore = "H014"', encoding="utf-8")
    (tmp_path / ".djlint.toml").write_text('ignore = "H015"', encoding="utf-8")

    config = Config(str(html_file))

    assert config.ignore == "H014"
