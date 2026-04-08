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

    assert result.exit_code == 0

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

    assert result.exit_code == 0

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
    assert result.exit_code == 0

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
    """Exclude patterns should match relative paths within the search dir,
    not the absolute path. This ensures files are found when the project
    lives under a path containing '.git' (e.g. a git worktree at
    '.git-worktrees/feature/')."""
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


def test_gitignore_does_not_match_parent_path(tmp_path: Path) -> None:
    """Gitignore patterns should be matched against paths relative to the
    project root, not absolute paths. When a project lives under a path
    like .claude/worktrees/<name>/, a gitignore pattern such as 'worktrees'
    would incorrectly exclude every file."""
    worktree = tmp_path / ".claude" / "worktrees" / "my-feature"
    templates = worktree / "templates"
    templates.mkdir(parents=True)

    (templates / "index.html").write_text("<div>hello</div>", encoding="utf-8")

    # Create .git dir so find_project_root finds this as root
    (worktree / ".git").mkdir()

    # Gitignore with a pattern that matches a parent directory name
    (worktree / ".gitignore").write_text("worktrees\n", encoding="utf-8")

    config = Config(
        str(templates / "index.html"), use_gitignore=True
    )
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
