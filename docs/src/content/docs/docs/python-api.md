---
title: "Python API"
description: "Format and lint templates from your own Python code with the djLint API."
---

`djlint.api` formats and lints text from a Python program, with the same results as the command line. It is meant for editors, build tools and anything else that holds a template in memory. Everything else in the package can change in any release, so use this module rather than `djlint.settings` or `djlint.lint`. The helpers the [custom rule example](/docs/linter/#python-module-rules) imports, `djlint.lint.get_line`, `djlint.helpers.inside_ignored_rule` and `djlint.helpers.inside_ignored_linter_block`, keep working too.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, on_warning=None, **options)` reads the configuration that applies to the files of a folder. It looks for it upward from the folder, as the command line [does](/docs/configuration/) from the first path it is given, and it doesn't change the current directory.

Options take the names of the command line options, with underscores, and work as they do there: a value that is set wins over the configuration file, while `False`, an empty string and, for most options, `0` count as not given. Paths are given as `pathlib.Path`.

Reading the configuration takes some time, so keep the result for as long as the files it was read from don't change. It can be used for any number of texts.

With `python_rules=False`, custom rules with a `python_module` aren't loaded, which keeps the code of a project you don't trust from running. Their names are in `config.skipped_rules`.

`on_warning`, a function that takes a message, gets every warning about the settings, such as a misspelled name or a rule code no rule has. Without it, each warning goes to stderr once per process. A config file that can't be read, or a value that isn't valid, raises `click.UsageError`.

## format_text

`format_text(config, text)` returns the formatted text. A text whose first line ends in CRLF comes back in CRLF, and any other in LF. With `require_pragma`, a text without the pragma comes back unchanged. Where neither the options of `load_config` nor the config file set `indent` or `max_line_length`, it takes them from the `.editorconfig` sections that apply to a file of the configured extension in the folder given to `load_config`, while the command line takes them for each file by its path.

## lint_text

`lint_text(config, text, filename="-")` returns a list of `Finding`, in document order. `filename` is what `per-file-ignores` is matched against. With `require_pragma`, a text without the pragma has no findings.

`Finding` is a named tuple with these fields:

- `code`: The code of the rule, such as `H013`.
- `message`: What the rule says.
- `match`: The start of the text it found, up to 20 characters.
- `line`, `column`: Where the finding starts. Lines count from 1, and columns from 0.
- `end_line`, `end_column`: Just past where it ends, which can be on a later line.

Columns count characters, not bytes or UTF-16 code units.

## is_excluded

`is_excluded(config, path)` tells whether `exclude`, `extend_exclude` or the gitignore leave out a file, as the command line does. `format_text` and `lint_text` don't check this themselves.

## Rule modules

A custom rule's `python_module` is imported once per process, from the project root of the configuration. To read another project's rules, a program that stays running has to remove from `sys.modules` everything it imported from the first project, and remove that project's root from the end of `sys.path`.
