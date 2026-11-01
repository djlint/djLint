---
description: Run djLint as a language server, for findings as you type and formatting in any editor that speaks LSP.
title: Language server
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, language server, lsp, neovim, zed, helix
---

# Language server

`djlint --lsp` runs djLint as a language server over stdio. It stays running, so an editor gets findings as you type and formats a document without starting a process each time.

It reports findings, and formats whole documents. It needs no extra packages.

## Neovim

With Neovim 0.11 or newer:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

To format on command, call `vim.lsp.buf.format()`.

## Zed

Install the [djLint extension](https://github.com/djlint/zed-djlint).

## Helix

In `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["vscode-html-language-server", "djlint"]
formatter = { command = "djlint", args = ["--reformat", "--quiet", "-"] }
```

## Settings

The server reads the project's [configuration](/docs/configuration/) as the command line does, from the folder of each file upward. Settings from the editor win over it. They take the names of the [command line options](/docs/configuration/), with underscores or in camelCase, and lists can be used for comma-separated values:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

The server asks for the `djlint` section with `workspace/configuration`. An editor that can't answer can send the same keys in `initializationOptions`.

Two settings have no command line option:

- `use_editor_indentation`: Format with the tab size of the editor, instead of `indent`.
- `python_rules`: Set it to `false` to skip custom rules with a `python_module`, which keeps the project's code from running.

Without a `profile` from either place, the language of the document picks one: `htmldjango` runs the `django` profile, for example.

## What it does

- Findings arrive after a short pause in typing. An editor with pull diagnostics asks for them, and any other gets them pushed.
- `exclude`, `extend_exclude` and `use_gitignore` apply to open documents. An excluded document has no findings and isn't formatted.
- It reloads the configuration when `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc` or `.gitignore` change, if the editor can watch files.
