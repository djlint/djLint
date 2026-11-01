---
title: "Integrations"
description: "Integrate djLint with your favorite editor. Auto format your templates with Pre-Commit. Lint with SublimeText."
sidebar:
  label: "Integrations"
---

There are several editor integrations built for djLint.

Whichever editor you use, install djLint where the editor can find it, ideally in the project's virtual environment, and start the editor from there or point it at the `djlint` of that environment. That way the editor runs the version your project pins, with the same results as your pre-commit hook or CI.

## Visual Studio Code

Install the [djLint extension](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), or [the one on Open VSX](https://open-vsx.org/extension/monosans/djlint) for VSCodium. It finds djLint in your environment, falls back to a bundled one, and uses the language server when your djLint has it.

Its code is on [GitHub](https://github.com/djlint/djlint-vscode).

## Neovim

djLint can be used as linter and formatter in Neovim.

### Built-in LSP client (recommended)

Neovim 0.11 or newer can talk to the [language server](#language-server) of djLint directly, with no plugin. That gives findings as you type, with underlined ranges, and `vim.lsp.buf.format()` for formatting:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

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

See [Settings](#settings).

### conform.nvim and nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formats and [nvim-lint](https://github.com/mfussenegger/nvim-lint) lints, by running djLint as a command. Findings have no underlined range, and arrive only when you ask nvim-lint to lint.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [GitHub repository](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Format](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [GitHub repository](https://github.com/mattn/efm-langserver)

1. Install efm-langserver and djLint with Mason via `:MasonInstall efm djlint`
1. Add `htmldjango` to `filetypes`.
1. Create format configuration:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Connect language to formatter with `htmldjango = { djlint }`.

Sample configuration:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}

require("lspconfig").efm.setup({
    filetypes = { "htmldjango" },
    init_options = { documentFormatting = true },
    settings = {
        rootMarkers = { ".git/" },
        languages = {
            htmldjango = { djlint },
        },
    },
})
```

### coc.nvim

- [npm package](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains IDEs

In PyCharm and the other IntelliJ-based IDEs, use the free [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) plugin:

1. Install LSP4IJ from the Marketplace.
1. Open the LSP Consoles tool window and add a new language server.
1. On the **Server** tab, set the name to `djLint` and the command to `djlint --lsp`, with the full path of the `djlint` in the project's virtual environment if it isn't on PATH.
1. On the **Mappings** tab, add a file name pattern for your templates, such as `*.html`. Set the language ID to `htmldjango` for a Django project, so the right [profile](/docs/configuration/#profile) is picked.
1. On the **Configuration** tab, you can set [settings](#settings) as JSON, under a `djlint` key.

Findings appear in the editor, and **Reformat Code** can use the server for the mapped files.

## Sublime Text

### LSP (recommended)

The [LSP](https://packagecontrol.io/packages/LSP) package runs the [language server](#language-server), which gives findings as you type and formatting.

Run **Preferences: LSP Server Configurations** and add:

```json
{
  "djlint": {
    "enabled": true,
    "command": ["djlint", "--lsp"],
    "selector": "text.html"
  }
}
```

### SublimeLinter

djLint can be used as a SublimeText Linter plugin. It can be installed via [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

1. `cmd + shift + p`
2. Install SublimeLinter
3. Install SublimeLinter-contrib-djlint

Ensure djLint is installed in your global python, or on your `PATH`.

## Helix

Helix can run the [language server](#language-server) from `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, which comes with Emacs 29 and newer:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Then run `M-x eglot` in a template. `eglot-format-buffer` formats it.

## Language server

`djlint --lsp` runs djLint as a language server over stdio. It stays running, so an editor gets findings as you type and formats a document without starting a process each time.

It reports findings, and formats whole documents. It needs no extra packages. Any other editor that speaks LSP can run it with the same command.

### Settings

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

### What it does

- Findings arrive after a short pause in typing. An editor with pull diagnostics asks for them, and any other gets them pushed.
- `exclude`, `extend_exclude` and `use_gitignore` apply to open documents. An excluded document has no findings and isn't formatted.
- It reloads the configuration when `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` or `.gitignore` change, if the editor can watch files, and otherwise when a document is opened or saved. Files named by `configuration` or `rules` are read again when a document is opened or saved. A change to the code of a custom rule's `python_module` needs a restart.
- A slow rule holds up what comes after it, because the server does one thing at a time.

## GitHub Actions

In a GitHub Actions workflow djLint reports each finding as an annotation, so it shows up inline on the diff of a pull request. No configuration is needed: djLint detects the workflow and switches output automatically.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Use `--no-github-output` to get the plain console output instead, or `--github-output` to force annotations outside of Actions.

Annotations belong to one pull request. To keep findings in the repository's Security tab, with history across runs, write them as SARIF and upload the file:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

The upload step needs the `security-events: write` permission on the job or the workflow.

`--sarif` writes a SARIF 2.1.0 document to stdout and nothing else, so it can be redirected as above. Every enabled rule is listed with a link to its documentation, each finding carries its line and column, and with `--check` a file that would be reformatted is reported under a `formatting` rule. Azure DevOps, GitLab and most editors read the same format.

## Pre-Commit

djLint can be used as a [pre-commit](https://pre-commit.com) hook as both a linter and a formatter.

The repo provides multiple pre-configured hooks for specific djLint profiles (it just pre-sets the `--profile` argument and tells pre-commit which file extensions to look for):

- `djlint` for linting and `djlint-reformat` for formatting
  This will look for files matching `*.html` without setting `--profile`.
- `djlint-django` and `djlint-reformat-django`
  This will look for files matching `*.html` and set `--profile=django`.
- `djlint-jinja` and `djlint-reformat-jinja`
  This will look for files matching `*.j2`,`*.jinja` or `*.jinja2` and set `--profile=jinja`.
- `djlint-nunjucks` and `djlint-reformat-nunjucks`
  This will look for files matching `*.njk` and set `--profile=nunjucks`.
- `djlint-handlebars` and `djlint-reformat-handlebars`
  This will look for files matching `*.hbs` and set `--profile=handlebars`.
- `djlint-liquid` and `djlint-reformat-liquid`
  This will look for files matching `*.html` and set `--profile=liquid`.
- `djlint-golang` and `djlint-reformat-golang`
  This will look for files matching `*.gotmpl` and set `--profile=golang`.
- `djlint-tera` and `djlint-reformat-tera`
  This will look for files matching `*.html` and set `--profile=tera`.
- `djlint-askama` and `djlint-reformat-askama`
  This will look for files matching `*.html` and set `--profile=askama`.

Note that these predefined hooks are sometimes too conservative in the inputs they accept (your templates may be using a different extension) so pre-commit explicitly allows you to override any of these pre-defined options. See the [pre-commit docs](https://pre-commit.com/#pre-commit-configyaml---hooks) for additional configuration.

### Default Django example

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars with .html extension instead of .hbs

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-handlebars
        files: "\\.html"
        types_or: ["html"]
      - id: djlint-handlebars
        files: "\\.html"
        types_or: ["html"]
```

You can use the `files` or `exclude` parameters to constrain each hook to its own directory, allowing you to support multiple template languages within the same repo.

## MegaLinter

djlint is natively embedded within the 100+ linters of [MegaLinter](https://megalinter.io)

To install it, just run `npx mega-linter-runner --install` and follow instructions

- [GitHub repository](https://github.com/oxsecurity/megalinter)
- [djlint in MegaLinter documentation](https://megalinter.io/latest/descriptors/html_djlint/)
