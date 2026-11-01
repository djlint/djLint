---
description: 将 djLint 与您喜爱的编辑器集成。使用 Pre-Commit 自动格式化您的模板。在 SublimeText 中进行代码检查（Lint）。
title: 集成支持
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 集成支持
---

# 集成支持

有多个为 djLint 开发的编辑器集成方案。

## GitHub Actions

在 GitHub Actions 工作流中，djLint 会将每条结果输出为注解（annotation），直接显示在拉取请求的差异视图中。无需任何配置：djLint 会自动识别工作流并切换输出格式。

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

使用 `--no-github-output` 可恢复普通的控制台输出，使用 `--github-output` 可在 Actions 之外强制输出注解。

注解只属于某一个拉取请求。若要把结果保存在仓库的 Security 标签页中，并保留多次运行的历史记录，可以将其输出为 SARIF 并上传该文件：

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

上传步骤需要在 job 或 workflow 上授予 `security-events: write` 权限。

`--sarif` 只向 stdout 输出一个 SARIF 2.1.0 文档，不输出其他内容，因此可以像上面那样重定向到文件。文档列出所有已启用的规则及其文档链接，每条结果都带有行号和列号；配合 `--check` 使用时，需要重新格式化的文件会归入 `formatting` 规则下报告。Azure DevOps、GitLab 和大多数编辑器都能读取这种格式。

## Pre-Commit

djLint 可以集成到 [pre-commit](https://pre-commit.com) hook 作为代码检查工具和格式化工具。

该代码仓库为特定的 djLint 配置文件（profile）提供了多个预先配置好的 hook（这些 hook 只是预先设置了 `--profile` 参数，并告知 pre-commit 需要查找哪些文件扩展名）：

::: content

- 使用 `djlint` 进行代码检查并使用 `djlint-reformat` 进行代码格式化。
  在未设置 `--profile` 时会查找 `*.html`。
- 使用 `djlint-django` 和 `djlint-reformat-django`。
  这时会查找 `*.html` 并设置 `--profile=django`。
- 使用 `djlint-jinja` 和 `djlint-reformat-jinja`。
  这时会查找 `*.j2` 、 `*.jinja` 或 `*.jinja2` 并设置 `--profile=jinja`。
- 使用 `djlint-nunjucks` 和 `djlint-reformat-nunjucks`。
  这时会查找 `*.njk` 并设置 `--profile=nunjucks`。
- 使用 `djlint-handlebars` 和 `djlint-reformat-handlebars`。
  这时会查找 `*.hbs` 并设置 `--profile=handlebars`。
- 使用 `djlint-liquid` 和 `djlint-reformat-liquid`。
  这时会查找 `*.html` 并设置 `--profile=liquid`。
- 使用 `djlint-golang` 和 `djlint-reformat-golang`。
  这时会查找 `*.gotmpl` 并设置 `--profile=golang`。
- 使用 `djlint-tera` 和 `djlint-reformat-tera`。
  这时会查找 `*.html` 并设置 `--profile=tera`。
- 使用 `djlint-askama` 和 `djlint-reformat-askama`。
  这时会查找 `*.html` 并设置 `--profile=askama`。
  :::

请注意，这些预定义的 hook 在它们接受的输入方面有时会过于保守（您的模板可能使用了不同的扩展名），因此 pre-commit 明确允许您覆盖这些预定义的选项。有关额外的配置信息，请参阅 [pre-commit 的文档](https://pre-commit.com/#pre-commit-configyaml---hooks)。

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

您可以使用 `files` 或 `exclude` 参数将每个 hook 限制在其自身的目录范围内，从而允许您在同一个代码仓库中支持多种模板语言。

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

Neovim 0.11 或更高版本无需插件即可直接使用 djLint 的[语言服务器](/zh/docs/language-server/)。这样可以在输入时看到带下划线范围的检查结果，并通过 `vim.lsp.buf.format()` 进行格式化：

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

设置请参阅[语言服务器](/zh/docs/language-server/#设置)。下面的插件则是把 djLint 作为命令运行。

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

使用 `efm-langserver`。

::: content

- [GitHub 仓库](https://github.com/mattn/efm-langserver)

1. 通过 Mason 安装 efm-langserver 和 djLint：`:MasonInstall efm djlint`
1. 将 `htmldjango` 添加到 `filetypes`。
1. 创建格式化配置：

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. 使用 `htmldjango = { djlint }` 将语言连接到格式化工具。

示例配置：

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

:::

## Zed

安装 [djLint 扩展](https://github.com/djlint/zed-djlint)，它会运行[语言服务器](/zh/docs/language-server/)。

## Helix

Helix 可以通过 `languages.toml` 运行[语言服务器](/zh/docs/language-server/)：

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["vscode-html-language-server", "djlint"]
```

## JetBrains IDE、Sublime Text 和 Emacs

它们同样通过[语言服务器](/zh/docs/language-server/)工作。请参阅如何设置 [JetBrains IDE](/zh/docs/language-server/#jetbrains-ide)、[Sublime Text](/zh/docs/language-server/#sublime-text) 和 [Emacs](/zh/docs/language-server/#emacs)。

## MegaLinter

djLint 已集成到 [MegaLinter](https://megalinter.io) 的百余个代码检查工具中。

运行 `npx mega-linter-runner --install` 并根据提示来安装它。

::: content

- [GitHub 仓库](https://github.com/oxsecurity/megalinter)
- [djlint - MegaLinter 文档](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
