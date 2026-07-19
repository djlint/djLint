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
