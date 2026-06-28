"""Djlint tests specific to gitignore configuration.

run::

   pytest tests/test_config_gitignore.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config_gitignore.py::test_ignored_path --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from djlint import main as djlint
from djlint.settings import Config
from djlint.src import get_src

if TYPE_CHECKING:
    from click.testing import CliRunner


@pytest.mark.xdist_group(name="group1")
def test_cli(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--lint")
    )
    assert result.exit_code == 1

    git_path = Path("tests", "test_config", "test_gitignore", ".git")
    gitignore_path = Path(
        "tests", "test_config", "test_gitignore", ".gitignore"
    )

    # create .git folder to make root
    git_path.mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    gitignore_path.write_text("html_two.html", encoding="utf-8")

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_gitignore/html_two.html",
            "--check",
            "--use-gitignore",
        ),
    )

    assert result.exit_code == 1

    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )
    assert result.exit_code == 1

    try:
        gitignore_path.unlink()
        shutil.rmtree(git_path)
    except Exception as e:
        print("cleanup failed")
        print(e)

    # @pytest.mark.xdist_group(name="group1")
    # def test_pyproject(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )
    assert result.exit_code == 1

    # make a root
    git_path.mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    gitignore_path.write_text("html_two.html", encoding="utf-8")
    pyproject_path = Path(
        "tests", "test_config", "test_gitignore", "pyproject.toml"
    )
    pyproject_path.write_text(
        "[tool]\n[tool.djlint]\nuse_gitignore=true", encoding="utf-8"
    )

    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )

    assert result.exit_code == 1

    pyproject_path.write_text(
        "[tool]\n[tool.djlint]\nuse_gitignore=false", encoding="utf-8"
    )

    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )
    assert result.exit_code == 1

    # verify cli overrides pyproject
    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_gitignore/html_two.html",
            "--check",
            "--use-gitignore",
        ),
    )
    print(result.output)
    assert result.exit_code == 1

    try:
        gitignore_path.unlink()
        pyproject_path.unlink()
        shutil.rmtree(git_path)
    except Exception as e:
        print("cleanup failed")
        print(e)

    # @pytest.mark.xdist_group(name="group1")
    # def test_ignored_path(runner: CliRunner) -> None:
    # test for https://github.com/djlint/djLint/issues/224
    # create .git folder to make root
    git_path.mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    gitignore_path.write_text("var", encoding="utf-8")

    result = runner.invoke(
        djlint, ("-", "--use-gitignore"), input='<div><p id="a"></p></div>'
    )
    print(result.output)
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    try:
        gitignore_path.unlink()
        shutil.rmtree(git_path)
    except Exception as e:
        print("cleanup failed")
        print(e)


def test_exclude_does_not_match_parent_path(tmp_path: Path) -> None:
    """Exclude patterns should not match parent dirs outside the project."""
    # Simulate a worktree path that contains ".git" in a parent directory
    worktree = tmp_path / ".git-worktrees" / "feature"
    templates = worktree / "templates"
    templates.mkdir(parents=True)

    (templates / "index.html").write_text("<div>hello</div>", encoding="utf-8")

    # Also create a real .git exclude target inside the project
    git_dir = worktree / "sub" / ".git" / "objects"
    git_dir.mkdir(parents=True)
    (git_dir / "stale.html").write_text("<div>bad</div>", encoding="utf-8")

    config = Config(str(worktree))
    paths = get_src([worktree], config)

    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    # File under templates/ must be found even though the absolute path
    # contains ".git-worktrees"
    assert "templates/index.html" in resolved_paths

    # File under sub/.git/objects/ must still be excluded by the default
    # exclude pattern
    assert "sub/.git/objects/stale.html" not in resolved_paths

    (worktree / ".git").touch()
    generated = templates / "generated"
    generated.mkdir()
    (generated / "bad.html").write_text("<div>bad</div>", encoding="utf-8")

    config = Config(str(templates), exclude="templates/generated")
    paths = get_src([templates], config)
    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    # Exclude patterns relative to project root must still work when
    # searching only a subdirectory.
    assert "templates/index.html" in resolved_paths
    assert "templates/generated/bad.html" not in resolved_paths


def test_exclude_matches_path_segments_not_substrings(tmp_path: Path) -> None:
    """Exclude paths should not match partial path component names."""
    worktree = tmp_path / "project"
    for directory in ("build", "builds", "build-my-template"):
        path = worktree / directory
        path.mkdir(parents=True)
        (path / "template.html").write_text(
            "<div>hello</div>", encoding="utf-8"
        )

    config = Config(str(worktree), exclude="build")
    paths = get_src([worktree], config)

    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    assert "build/template.html" not in resolved_paths
    assert "builds/template.html" in resolved_paths
    assert "build-my-template/template.html" in resolved_paths


def test_exclude_supports_comma_separated_paths(tmp_path: Path) -> None:
    """Exclude should support documented comma-separated paths."""
    worktree = tmp_path / "project"
    for directory in ("build", "dist", "builds"):
        path = worktree / directory
        path.mkdir(parents=True)
        (path / "template.html").write_text(
            "<div>hello</div>", encoding="utf-8"
        )

    config = Config(str(worktree), exclude="build,dist")
    paths = get_src([worktree], config)

    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    assert "build/template.html" not in resolved_paths
    assert "dist/template.html" not in resolved_paths
    assert "builds/template.html" in resolved_paths


def test_exclude_matches_slash_separated_path_segments(tmp_path: Path) -> None:
    """Exclude paths with slashes should match exact path segments."""
    worktree = tmp_path / "project"
    for directory in (
        "templates/generated",
        "templates/generated-assets",
        "my-templates/generated",
    ):
        path = worktree / directory
        path.mkdir(parents=True)
        (path / "template.html").write_text(
            "<div>hello</div>", encoding="utf-8"
        )

    for exclude in ("templates/generated", "templates/generated/"):
        config = Config(str(worktree), exclude=exclude)
        paths = get_src([worktree], config)

        resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

        assert "templates/generated/template.html" not in resolved_paths
        assert "templates/generated-assets/template.html" in resolved_paths
        assert "my-templates/generated/template.html" in resolved_paths


def test_exclude_trailing_slash_matches_nested_path_segment(
    tmp_path: Path,
) -> None:
    """Exclude paths should still match nested path segments."""
    worktree = tmp_path / "project"
    templates = worktree / "apps" / "account" / "templates" / "user"
    emails = templates / "emails"
    emails.mkdir(parents=True)
    (emails / "test.html").write_text("<div>hello</div>", encoding="utf-8")

    other = templates / "email-assets"
    other.mkdir()
    (other / "test.html").write_text("<div>hello</div>", encoding="utf-8")

    config = Config(str(worktree), exclude="emails/")
    paths = get_src([worktree], config)

    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    assert "apps/account/templates/user/emails/test.html" not in resolved_paths
    assert (
        "apps/account/templates/user/email-assets/test.html" in resolved_paths
    )


def test_exclude_leading_slash_matches_project_root_only(
    tmp_path: Path,
) -> None:
    """Exclude paths with leading slashes should match from the project root."""
    worktree = tmp_path / "project"
    for directory in ("emails", "apps/emails"):
        path = worktree / directory
        path.mkdir(parents=True)
        (path / "test.html").write_text("<div>hello</div>", encoding="utf-8")

    config = Config(str(worktree), exclude="/emails/")
    paths = get_src([worktree], config)

    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    assert "emails/test.html" not in resolved_paths
    assert "apps/emails/test.html" in resolved_paths


def test_exclude_leading_slash_does_not_match_source_root(
    tmp_path: Path,
) -> None:
    """Leading slash excludes should not anchor to the searched directory."""
    worktree = tmp_path / "project"
    (worktree / ".git").mkdir(parents=True)
    templates = worktree / "templates"
    for directory in (worktree / "generated", templates / "generated"):
        directory.mkdir(parents=True)
        (directory / "test.html").write_text(
            "<div>hello</div>", encoding="utf-8"
        )

    config = Config(str(templates), exclude="/generated/")
    paths = get_src([templates], config)
    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    assert "templates/generated/test.html" in resolved_paths

    paths = get_src([worktree], config)
    resolved_paths = {p.relative_to(worktree).as_posix() for p in paths}

    assert "generated/test.html" not in resolved_paths
    assert "templates/generated/test.html" in resolved_paths


def test_gitignore_does_not_match_parent_path(tmp_path: Path) -> None:
    """Gitignore patterns should not match parent dirs outside the project."""
    worktree = tmp_path / ".claude" / "worktrees" / "my-feature"
    templates = worktree / "templates"
    templates.mkdir(parents=True)

    (templates / "index.html").write_text("<div>hello</div>", encoding="utf-8")

    # Create .git dir so find_project_root finds this as root
    (worktree / ".git").mkdir()

    # Gitignore with a pattern that matches a parent directory name
    (worktree / ".gitignore").write_text("worktrees\n", encoding="utf-8")

    config = Config(str(templates / "index.html"), use_gitignore=True)
    # Test single file path (the xargs codepath)
    paths = get_src([templates / "index.html"], config)
    assert len(paths) == 1

    # Test directory path
    paths = get_src([worktree], config)
    resolved = {p.relative_to(worktree).as_posix() for p in paths}
    assert "templates/index.html" in resolved

    # A file that IS inside a worktrees/ dir within the project should
    # still be correctly ignored
    ignored_dir = worktree / "worktrees" / "nested"
    ignored_dir.mkdir(parents=True)
    (ignored_dir / "bad.html").write_text("<div>bad</div>", encoding="utf-8")

    paths = get_src([worktree], config)
    resolved = {p.relative_to(worktree).as_posix() for p in paths}
    assert "templates/index.html" in resolved
    assert "worktrees/nested/bad.html" not in resolved
