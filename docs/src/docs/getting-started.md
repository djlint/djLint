---
description: Getting started with djLint for HTML Template Linting and Formatting. Take advantage of the easy cli interface and many formatter options.
title: Getting Started
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, usage
---

# Getting Started

## Installation

djLint is built with [Python](https://python.org), it can be installed from [PyPI](https://pypi.org/project/djlint/) by simply running:

```bash
pip install djlint
```

Or as a standalone tool with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install djlint
```

Or with [pipx](https://pipx.pypa.io/):

```bash
pipx install djlint
```

Or with the community-maintained [Homebrew formula](https://formulae.brew.sh/formula/djlint) on macOS or Linux:

```bash
brew install djlint
```

_Or with npm - **warning**: the npm package is only a wrapper, its install script runs `pip install --upgrade djlint` on whatever `python3` is on your system path. npm will not manage or uninstall the actual package - prefer pip directly when possible._

```bash
npm i djlint
```

## CLI Usage

djLint is a command line application. See `configuration` for advanced configuration.

{% include 'src/_includes/cli.md' %}

{% admonition
   "note",
   "Note",
   "If the command `djlint` is not found, ensure sure that Python is [in your path](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)."
%}

## Using Path vs Stdin

djLint works with a path or stdin.

Running with a path -

```bash
djlint /path/to/templates --lint
```

Or a specific file -

```bash
djlint /path/to/this.mustache --lint
```

Or with stdin -

```bash
echo "<div></div>" | djlint -
```

Stdin can also be used to reformat code. The output will be only the formatted code without messages.

```bash
echo "<div></div>" | djlint - --reformat
```

Output -

```html
<div></div>
```

When reading from stdin, djLint has no real path to match against `per-file-ignores` or to show in messages, so it uses `-` by default. Pass `--stdin-filename` to tell djLint the real path of the piped content, for example when an editor integration pipes a file's contents in on save.

```bash
echo "<div></div>" | djlint - --stdin-filename templates/index.html
```

## Exit Codes

| Code | Meaning                                                                                                                          |
| ---- | -------------------------------------------------------------------------------------------------------------------------------- |
| `0`  | Everything djLint was asked to check is clean, or every file it found was skipped by your configuration.                         |
| `1`  | djLint found linting errors, or files that need reformatting. `--warn` reports these as warnings and exits `0` instead.          |
| `2`  | djLint did not check what you asked it to: the paths matched no files, the command line or config was invalid, or djLint failed. |

Only code `1` means djLint looked at your templates and did not like what it found. Code `2` always means the run itself did not deliver, so a pipeline can treat the two differently instead of guessing.

Code `2` is what catches a run that checked nothing at all: a wrong path, an `--extension` that no longer matches, or templates that have moved. Without it such a run passes silently, having looked at none of your templates.

Files that djLint _did_ find and then skipped on purpose, through `exclude`, `extend_exclude`, `use_gitignore` or `require_pragma`, are not an error. That run exits `0`, because the configuration did exactly what it was told to. It is also what lets `exclude` work under pre-commit, which passes the names of your staged files whether or not you want djLint to look at them.

If a path that legitimately has no templates is normal for your pipeline, turn code `2` off with `allow_empty_input`:

```bash
djlint /path/to/templates --lint --allow-empty-input
```
