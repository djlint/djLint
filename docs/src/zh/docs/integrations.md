---
description: 将 djLint 与您喜爱的编辑器集成。使用 Pre-Commit 自动格式化您的模板。在 SublimeText 中进行代码检查（Lint）。
title: 集成支持
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 集成支持
---

# 集成支持

有多个为 djLint 开发的编辑器集成方案。

## Pre-Commit

djLint 可以集成到 [pre-commit](https://pre-commit.com) hook 作为代码检查工具和格式化工具。

该代码仓库为特定的 djLint 配置文件（profile）提供了多个预先配置好的 hook（这些 hook 只是预先设置了 --profile 参数，并告知 pre-commit 需要查找哪些文件扩展名）：

::: content

- 使用 `djlint` 进行代码检查并使用 `djlin-reformat` 进行代码格式化。
  在未设置 `--profile` 时会查找 `templates/**.html`。
- 使用 `djlint-django` 和 `djlint-reformat-django`。
  这时会查找 `templates/**.html` 并设置 `--profile=django`。
- 使用 `djlint-jinja` 和 `djlint-reformat-jinja`。
  这时会查找 `*.j2` 、 `*.jinja` 或 `*.jinja2` 并设置 `--profile=jinja`。
- 使用 `djlint-nunjucks` 和 `djlint-reformat-nunjucks`。
  这时会查找 `*.njk` 并设置 `--profile=nunjucks`。
- 使用 `djlint-handlebars` 和 `djlint-reformat-handlebars`。
  这时会查找 `*.hbs` 并设置 `--profile=handlebars`。
- 使用 `djlint-golang` 和 `djlint-reformat-golang`。
  这时会查找 `*.tmpl` 并设置 `--profile=golang`。
  :::

请注意，这些预定义的 hook 在它们接受的输入方面有时会过于保守（您的模板可能使用了不同的扩展名），因此 pre-commit 明确允许您覆盖这些预定义的选项。有关额外的配置信息，请参阅 pre-commit 的文档。

### 默认 Django 示例

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### 使用 .html 后缀而非 .hbs 后缀的 Handlebars

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

您可以使用 files 或 exclude 参数将每个 hook 限制在其自身的目录范围内，从而允许您在同一个代码仓库中支持多种模板语言。

## SublimeText 代码检查

djLint 也可用作 SublimeText 的代码检查插件。你可以通过 [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) 安装。

::: content

1. `cmd + shift + p`
2. 安装 SublimeLinter
3. 安装 SublimeLinter-contrib-djlint
   :::

确保 djLint 安装在你的全局 python 中，或你的 `PATH` 变量中。

## Visual Studio Code

::: content

- [GitHub 仓库](https://github.com/djlint/djlint-vscode)
- [VS Marketplace page](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)
- [Open VSX page](https://open-vsx.org/extension/monosans/djlint)
  :::

## neovim

djLint 可以在 neovim 中检查或格式化代码。

使用 `none-ls` 插件。

::: content

- [GitHub 仓库](https://github.com/nvimtools/none-ls.nvim)
- [代码检查](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [代码格式化](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

使用 `coc.nvim`。

::: content

- [npm package](https://www.npmjs.com/package/coc-htmldjango)
  :::

## MegaLinter

djLint 已集成到 [MegaLinter](https://megalinter.io) 的百余个代码检查工具中。

运行 `npx mega-linter-runner --install` 并根据提示来安装它。

::: content

- [GitHub 仓库](https://github.com/oxsecurity/megalinter)
- [djlint - MegaLinter 文档](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
