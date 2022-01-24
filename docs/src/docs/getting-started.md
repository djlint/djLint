---
description: Getting started with djLint for HTML Template Linting and Formatting. Take advantage of the easy cli interface and many formatter options.
title: Getting Started
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, usage
---

# Getting Started

## Installation from [Pypi](https://pypi.org/project/djlint/)

djLint is build with [Python 3](https://python.org), it can be installed by simply running:

```bash
pip install djlint
```

## CLI Usage

djLint is a command line application. See `configuration` for advanced configuration.

```bash
Usage: python -m djlint [OPTIONS] SRC ...

  djLint · lint and reformat HTML templates.

Options:
  --version             Show the version and exit.
  -e, --extension TEXT  File extension to check [default: html]
  -i, --ignore TEXT     Codes to ignore. ex: "H014,H017"
  --reformat            Reformat the file(s).
  --check               Check formatting on the file(s).
  --indent INTEGER      Indent spacing. [default: 4]
  --quiet               Do not print diff when reformatting.
  --profile TEXT        Enable defaults by template language. ops: django,
                        jinja, nunjucks, handlebars, golang
  --require-pragma      Only format or lint files that starts with a comment
                        with the text 'djlint:on'
  --lint                Lint for common issues. [default option]
  --use-gitignore       Use .gitignore file to extend excludes.
  -h, --help            Show this message and exit.
```

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
