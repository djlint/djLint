---
description: Run djLint as a language server, for findings as you type and formatting in any editor that speaks LSP.
title: Language server
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, language server, lsp, neovim, zed, helix
---

# Language server

`djlint --lsp` runs djLint as a language server over stdio. It stays running, so an editor gets findings as you type and formats a document without starting a process each time.

It reports findings, and formats whole documents. It needs no extra packages.

Whichever editor you use, install djLint where the editor can find it, ideally in the project's virtual environment, and start the editor from there or point it at the `djlint` of that environment. That way the editor runs the version your project pins, with the same results as your pre-commit hook or CI.

## Visual Studio Code

Install the [djLint extension](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), or [the one on Open VSX](https://open-vsx.org/extension/monosans/djlint) for VSCodium. It finds djLint in your environment, falls back to a bundled one, and uses the language server when your djLint has it.

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

To format on save, add this to the same configuration:

```lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = {
    "*.html", "*.jinja", "*.jinja2", "*.j2",
    "*.hbs", "*.handlebars", "*.liquid", "*.gotmpl",
  },
  callback = function(args)
    vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
  end,
})
```

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
language-servers = ["djlint", "vscode-html-language-server"]
```

## JetBrains IDEs

In PyCharm and the other IntelliJ-based IDEs, use the free [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) plugin:

1. Install LSP4IJ from the Marketplace.
1. Open the LSP Consoles tool window and add a new language server.
1. On the **Server** tab, set the name to `djLint` and the command to `djlint --lsp`, with the full path of the `djlint` in the project's virtual environment if it isn't on PATH.
1. On the **Mappings** tab, add a file name pattern for your templates, such as `*.html`. Set the language ID to `htmldjango` for a Django project, so the right [profile](/docs/configuration/#profile) is picked.
1. On the **Configuration** tab, you can set [settings](#settings) as JSON, under a `djlint` key.

Findings appear in the editor, and **Reformat Code** can use the server for the mapped files.

## Sublime Text

With the [LSP](https://packagecontrol.io/packages/LSP) package, run **Preferences: LSP Server Configurations** and add:

```json
{
  "djlint": {
    "enabled": true,
    "command": ["djlint", "--lsp"],
    "selector": "text.html"
  }
}
```

## Emacs

Eglot, which comes with Emacs 29 and newer:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Then run `M-x eglot` in a template. `eglot-format-buffer` formats it.

## Settings

The server reads the project's [configuration](/docs/configuration/) as the command line does, from the folder of each file upward. Settings from the editor win over it, but as on the command line, they can only turn an option on or set a value: `false` doesn't turn off what the project turns on. They take the names of the [command line options](/docs/configuration/), with underscores or in camelCase, and lists can be used for comma-separated values:

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
- It reloads the configuration when `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` or `.gitignore` change, if the editor can watch files, and otherwise when a document is opened or saved. A change to the code of a custom rule's `python_module` needs a restart.
- A slow rule holds up what comes after it, because the server does one thing at a time.
