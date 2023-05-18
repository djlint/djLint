---
description: Integrate djLint with your favorite editor. Auto format your templates with Pre-Commit. Lint with SublimeText.
title: Integrations
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, integrations
---

# Integrations

There are several editor integrations build for djLint.

## Pre-Commit

djLint can be used as a [pre-commit](https://pre-commit.com) hook as both a linter and a formatter.

The repo provides multiple pre-configured hooks for specific djLint profiles (it just pre-sets the `--profile` argument and tells pre-commit which file extensions to look for):

::: content

- `djlint` for linting and `djlint-reformat` for formatting
  This will look for files matching `templates/**.html` without setting `--profile`.
- `djlint-django` and `djlint-reformat-django`
  This will look for files matching `templates/**.html` and set `--profile=django`.
- `djlint-jinja` and `djlint-reformat-jinja`
  This will look for files matching `*.j2`,`*.jinja` or `*.jinja2` and set `--profile=jinja`.
- `djlint-nunjucks` and `djlint-reformat-nunjucks`
  This will look for files matching `*.njk` and set `--profile=nunjucks`.
- `djlint-handlebars` and `djlint-reformat-handlebars`
  This will look for files matching `*.hbs` and set `--profile=handlebars`.
- `djlint-golang` and `djlint-reformat-golang`
  This will look for files matching `*.tmpl` and set `--profile=golang`.
  :::

Note that these predefined hooks are sometimes too conservative in the inputs they accept (your templates may be using a different extension) so pre-commit explicitly allows you to override any of these pre-defined options. See the [pre-commit docs](https://pre-commit.com/#pre-commit-configyaml---hooks) for additional configuration

### Default Django example

```yaml
repos:
  - repo: https://github.com/Riverside-Healthcare/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars with .html extension instead of .hbs

```yaml
repos:
  - repo: https://github.com/Riverside-Healthcare/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-handlebars
        files: "\\.html"
        types_or: ['html']
      - id: djlint-handlebars
        files: "\\.html"
        types_or: ['html']
```

You can use the `files` or `exclude` parameters to constrain each hook to its own directory, allowing you to support multiple template languages within the same repo.

## SublimeText Linter

djLint can be used as a SublimeText Linter plugin. It can be installed via [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shift + p`
2. Install SublimeLinter
3. Install SublimeLinter-contrib-djlint
   :::

Ensure djLint is installed in your global python, or on your `PATH`.

## Visual Studio Code

::: content

- [GitHub repository](https://github.com/monosans/djlint-vscode)
- [VS Marketplace page](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)
- [Open VSX page](https://open-vsx.org/extension/monosans/djlint)
  :::

## neovim

djLint can use used as formatter in neovim using the `null-ls` plugin.

::: content

- [GitHub repository](https://github.com/jose-elias-alvarez/null-ls.nvim/)
- [Config example](https://github.com/shaeinst/roshnivim/blob/5d991fcfa1b8f865f9653a98c6d97a829d4a2add/lua/plugins/null-ls_nvim.lua#L84-L91)
  :::

## coc.nvim

::: content

- [npm package](https://www.npmjs.com/package/coc-htmldjango)
  :::

## null-ls.nvim

::: content

- [GitHub repository](https://github.com/jose-elias-alvarez/null-ls.nvim)
- [Lint](https://github.com/jose-elias-alvarez/null-ls.nvim/blob/main/lua/null-ls/builtins/diagnostics/djlint.lua#L14)
- [Format](https://github.com/jose-elias-alvarez/null-ls.nvim/blob/main/lua/null-ls/builtins/formatting/djlint.lua#L13)

## MegaLinter

djlint is natively embedded within the 100+ linters of [MegaLinter](https://megalinter.io)

To install it, just run `npx mega-linter-runner --install` and follow instructions

::: content

- [GitHub repository](https://github.com/oxsecurity/megalinter)
- [djlint in MegaLinter documentation](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
