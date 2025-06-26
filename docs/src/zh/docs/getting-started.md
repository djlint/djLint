---
description: Getting started with djLint for HTML Template Linting and Formatting. Take advantage of the easy cli interface and many formatter options.
title: Getting Started
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, usage
---

# Getting Started

## Installation from [Pypi](https://pypi.org/project/djlint/)

djLint is build with [Python](https://python.org), it can be installed by simply running:

```bash
pip install djlint
```

_Or with the npm experimental install - Note, this requires python and pip to be on your system path._

```bash
npm i djlint
```

## CLI Usage

djLint is a command line application. See `configuration` for advanced configuration.

{% include 'src/\_includes/cli.md' %}

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
