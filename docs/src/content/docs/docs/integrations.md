---
title: "Integrations"
description: "Use djLint in your editor and run it with pre-commit."
---

Whichever editor you use, install djLint where the editor can find it, ideally in the project's virtual environment, and start the editor from there or point it at the `djlint` of that environment. That way the editor runs the version your project pins, with the same results as your pre-commit hook or CI.

If the project installs djLint with [npm](/docs/getting-started/#installation), its command is `node_modules/.bin/djlint` in the project, or `node_modules/.bin/djlint.cmd` on Windows. Where an editor below runs `djlint`, give it that path. The path is relative: if the editor runs djLint from a folder other than the one with `node_modules`, give the full path. The VS Code and Zed extensions find it by themselves.

## Visual Studio Code

Install the [djLint extension](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) from the Visual Studio Marketplace. Cursor, Windsurf, VSCodium and other editors built on VS Code install [the same extension from Open VSX](https://open-vsx.org/extension/monosans/djlint). It finds djLint in your environment, falls back to a bundled one, and uses the language server when your djLint has it.

Its [README](https://github.com/djlint/djlint-vscode#readme) covers its settings and which djLint it runs.

## Zed

The [djLint extension](https://github.com/djlint/djlint-zed) runs the [language server](#language-server) in HTML and in the languages of the template extensions, such as Django, Jinja and Twig. It isn't in Zed's extension registry yet, so install it as a dev extension:

1. Install Rust through [rustup](https://rustup.rs): Zed builds the extension with it and adds the `wasm32-wasip2` target itself. With a Rust from elsewhere, such as Homebrew or Nix, add that target yourself.
1. Clone the extension:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. In Zed, open the command palette (`cmd-shift-p` on macOS, `ctrl-shift-p` elsewhere), run **zed: install dev extension** and pick the cloned `djlint-zed` folder.

To update it, run `git pull` in that folder, then **zed: rebuild dev extension**.

It needs djLint 1.49 or newer on PATH or installed in the project with npm, or [uv](https://docs.astral.sh/uv/), which runs djLint with no install. Its [README](https://github.com/djlint/djlint-zed#readme) shows how to make it the formatter of a language, and its settings.

## Neovim

Neovim gives some template extensions no filetype. Whichever option below you use, register them first:

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### Built-in LSP client (recommended)

Neovim 0.11 or newer can talk to the [language server](#language-server) of djLint directly, with no plugin. That gives findings as you type, with underlined ranges, and `vim.lsp.buf.format()` for formatting.

[nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) after v2.12.0 ships its configuration, so with it one line is enough:

```lua
vim.lsp.enable("djlint")
```

For djLint installed with npm in the project, put `vim.lsp.config("djlint", { cmd = { "node_modules/.bin/djlint", "--lsp" } })` before that line, with `"node_modules/.bin/djlint.cmd"` on Windows. The path is relative to the directory Neovim runs in, so start Neovim in the project root.

Without nvim-lspconfig, or with an older one, define the configuration yourself:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = {
    "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
    "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
  },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

To format on save, add this to the same configuration:

```lua
local group = vim.api.nvim_create_augroup("djlint_format", {})
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    if vim.lsp.get_client_by_id(args.data.client_id).name ~= "djlint" then
      return
    end
    vim.api.nvim_clear_autocmds({ group = group, buffer = args.buf })
    vim.api.nvim_create_autocmd("BufWritePre", {
      group = group,
      buffer = args.buf,
      callback = function()
        vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
      end,
    })
  end,
})
```

See [Settings](#settings).

### conform.nvim and nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formats and [nvim-lint](https://github.com/mfussenegger/nvim-lint) lints, by running djLint as a command. Findings have no underlined range, and arrive only when you ask nvim-lint to lint. The profile comes from the project's [configuration](/docs/configuration/#profile), as on the command line. This example needs djLint 1.49 or newer.

```lua
local formatters, linters = {}, {}
for _, filetype in ipairs({
  "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
  "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
}) do
  formatters[filetype] = { "djlint" }
  linters[filetype] = { "djlint" }
end
require("conform").setup({
  formatters_by_ft = formatters,
  formatters = { djlint = { prepend_args = { "--stdin-filename", "$FILENAME" } } },
})
local lint = require("lint")
lint.linters_by_ft = linters
vim.list_extend(lint.linters.djlint.args, {
  "--stdin-filename",
  function()
    return vim.api.nvim_buf_get_name(0)
  end,
})
```

### none-ls

- [GitHub repository](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Format](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [npm package](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains IDEs

In PyCharm and the other IntelliJ-based IDEs, use the free [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) plugin:

1. Install LSP4IJ from the Marketplace.
1. Open the LSP Consoles tool window and add a new language server.
1. On the **Server** tab, set the name to `djLint` and the command to `djlint --lsp`, with the full path of the `djlint` in the project's virtual environment if it isn't on PATH.
1. On the **Mappings** tab, add the file name patterns of your templates. When the project's configuration has no [profile](/docs/configuration/#profile), the language ID of a pattern picks it:

   | Patterns                              | Language ID                       |
   | ------------------------------------- | --------------------------------- |
   | `*.html`, `*.htm`                     | `html`, or `htmldjango` in Django |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                           |
   | `*.njk`, `*.twig`                     | `nunjucks`                        |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                      |
   | `*.liquid`                            | `liquid`                          |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                          |
   | `*.tera`                              | `tera`                            |
   | `*.mako`                              | `mako`                            |

1. On the **Configuration** tab, you can set [settings](#settings) as JSON, under a `djlint` key.

Findings appear in the editor, and **Reformat Code** can use the server for the mapped files.

## Sublime Text

### LSP (recommended)

The [LSP](https://packagecontrol.io/packages/LSP) package runs the [language server](#language-server), which gives findings as you type and formatting.

Run **Preferences: LSP Server Configurations** and add:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

Install SublimeLinter and [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) with Package Control. djLint has to be on the PATH that Sublime Text sees.

## Helix

Helix can run the [language server](#language-server) from `languages.toml`. A `language-servers` list replaces the one Helix has for that language, so keep its own servers after `djlint`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server", "superhtml"]

[[language]]
name = "htmldjango"
language-servers = ["djlint", "djlsp", "vscode-html-language-server", "superhtml"]

[[language]]
name = "gotmpl"
language-servers = ["djlint", "gopls"]

[[language]]
name = "jinja"
language-servers = ["djlint"]

[[language]]
name = "nunjucks"
language-servers = ["djlint"]

[[language]]
name = "twig"
language-servers = ["djlint"]

[[language]]
name = "tera"
language-servers = ["djlint"]
```

Helix opens no file as `htmldjango` by itself. In a Django project, add `file-types = ["html"]` to that entry in the project's `.helix/languages.toml`.

## Emacs

Eglot, which comes with Emacs 29 and newer:

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

Then run `M-x eglot` in a template. `eglot-format-buffer` formats it. `html-mode`, `mhtml-mode` and `web-mode` name no template language, so in them the profile comes from the project's [configuration](/docs/configuration/#profile).

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

djLint takes the `profile` from the first of these that has one:

1. The settings of the editor.
1. The project's configuration.
1. The language of the document: `htmldjango` runs the `django` profile, for example.

With none of them, it runs with no profile, as on the command line. A `profile` in the project's configuration is the simplest choice: it works in every editor, with no language ID to set up.

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

`--sarif` writes a SARIF 2.1.0 document to stdout and nothing else, so it can be redirected as above. Every enabled rule is listed with a link to its documentation, each finding carries its line and column, and with `--check` a file that would be reformatted is reported under a `formatting` rule.

## pre-commit

djLint can be used as a [pre-commit](https://pre-commit.com) hook as both a linter and a formatter.

These profiles each have a hook that lints, listed here, and one that formats, named the same with `reformat`: `djlint-reformat-django` for `djlint-django`. They set `--profile` and the files pre-commit passes. `angular` has no hooks of its own: give `djlint` or `djlint-reformat` `args: [--profile=angular]`.

| Hook                | Profile    | Files                                |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | none       | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

For templates with other extensions, override `files` in your config, and `types_or` too where the hook sets it, since pre-commit needs both to match. See the [pre-commit docs](https://pre-commit.com/#pre-commit-configyaml---hooks).

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

[MegaLinter](https://megalinter.io) includes djLint. Run `npx mega-linter-runner --install` to set it up, and see [its djLint page](https://megalinter.io/latest/descriptors/html_djlint/) for the options.
