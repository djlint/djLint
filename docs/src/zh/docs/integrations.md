---
description: 将 djLint 与您喜爱的编辑器集成。使用 Pre-Commit 自动格式化您的模板。在 SublimeText 中进行代码检查（Lint）。
title: 集成支持
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 集成支持, 语言服务器, lsp, neovim, helix
---

# 集成支持

有多个为 djLint 开发的编辑器集成方案。

无论使用哪种编辑器，都请把 djLint 安装在编辑器能找到的位置，最好是项目的虚拟环境中，并从该环境启动编辑器，或让编辑器指向该环境中的 `djlint`。这样编辑器运行的就是项目固定的版本，结果与 pre-commit 钩子或 CI 一致。

## Visual Studio Code

安装 [djLint 扩展](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)，或者在 VSCodium 中使用 [Open VSX 上的版本](https://open-vsx.org/extension/monosans/djlint)。它会在你的环境中查找 djLint，找不到时使用内置版本，并在你的 djLint 支持时使用语言服务器。

它的代码位于 [GitHub](https://github.com/djlint/djlint-vscode)。

## Neovim

djLint 可以在 Neovim 中用作代码检查和格式化工具。### 内置 LSP 客户端（推荐）

Neovim 0.11 或更高版本无需插件即可直接使用 djLint 的[语言服务器](#语言服务器)。这样可以在输入时看到带下划线范围的检查结果，并通过 `vim.lsp.buf.format()` 进行格式化：

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

要在保存时格式化，请在同一配置中添加：

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

请参阅[设置](#设置)。下面的插件则是把 djLint 作为命令运行。

### conform.nvim 和 nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) 负责格式化，[nvim-lint](https://github.com/mfussenegger/nvim-lint) 负责检查，它们都把 djLint 作为命令运行。检查结果没有下划线范围，并且只有在你让 nvim-lint 检查时才会出现。

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

::: content

- [GitHub 仓库](https://github.com/nvimtools/none-ls.nvim)
- [代码检查](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [代码格式化](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

### efm-langserver

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

### coc.nvim

::: content

- [npm package](https://www.npmjs.com/package/coc-htmldjango)
  :::

## JetBrains IDE

在 PyCharm 和其他基于 IntelliJ 的 IDE 中，使用免费的 [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) 插件：

1. 从 Marketplace 安装 LSP4IJ。
1. 打开 LSP Consoles 工具窗口，添加新的语言服务器。
1. 在 **Server** 选项卡中，将名称设为 `djLint`，命令设为 `djlint --lsp`；如果 `djlint` 不在 PATH 中，请使用项目虚拟环境中的完整路径。
1. 在 **Mappings** 选项卡中，为模板添加文件名模式，例如 `*.html`。对于 Django 项目，将语言 ID 设为 `htmldjango`，以便选择正确的[配置](/zh/docs/configuration/#profile)。
1. 在 **Configuration** 选项卡中，可以用 JSON 在 `djlint` 键下填写[设置](#设置)。

检查结果会显示在编辑器中，**Reformat Code** 也可以对这些文件使用服务器。

## Sublime Text

### LSP（推荐）

[LSP](https://packagecontrol.io/packages/LSP) 包运行[语言服务器](#语言服务器)，可在输入时显示检查结果并进行格式化。

运行 **Preferences: LSP Server Configurations** 并添加：

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

djLint 也可用作 SublimeText 的代码检查插件。你可以通过 [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) 安装。

::: content

1. `cmd + shift + p`
2. 安装 SublimeLinter
3. 安装 SublimeLinter-contrib-djlint
   :::

确保 djLint 安装在你的全局 python 中，或你的 `PATH` 变量中。

## Helix

Helix 可以通过 `languages.toml` 运行[语言服务器](#语言服务器)：

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

使用 Emacs 29 及更高版本自带的 Eglot：

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

然后在模板中运行 `M-x eglot`。`eglot-format-buffer` 用于格式化。

## 语言服务器

`djlint --lsp` 通过 stdio 将 djLint 作为语言服务器运行。它会持续运行，因此编辑器可以在输入时获得检查结果，并且格式化文档时无需每次启动新进程。

它报告检查结果并格式化整个文档，不需要额外的软件包。 其他支持 LSP 的编辑器都可以用同一命令运行它。

### 设置

服务器像命令行一样读取项目的[配置](/zh/docs/configuration/)，从每个文件所在的文件夹向上查找。编辑器的设置优先于它，但与命令行一样，只能开启选项或设置值：`false` 不会关闭项目已开启的选项。设置名称与[命令行选项](/zh/docs/configuration/)相同，可使用下划线或 camelCase，逗号分隔的值可以写成列表：

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

服务器通过 `workspace/configuration` 请求 `djlint` 部分。无法响应的编辑器可以在 `initializationOptions` 中发送相同的键。

有两个设置没有对应的命令行选项：

- `use_editor_indentation`：使用编辑器的制表符大小而不是 `indent` 进行格式化。
- `python_rules`：设为 `false` 时跳过带有 `python_module` 的自定义规则，这样不会运行项目中的代码。

如果两处都没有设置 `profile`，则由文档的语言决定：例如 `htmldjango` 使用 `django` 配置。

### 工作方式

- 检查结果会在输入短暂停顿后到达。支持拉取诊断的编辑器会主动请求，其他编辑器则由服务器推送。
- `exclude`、`extend_exclude` 和 `use_gitignore` 对打开的文档生效。被排除的文档没有检查结果，也不会被格式化。
- 如果编辑器支持监视文件，服务器会在 `pyproject.toml`、`djlint.toml`、`.djlint.toml`、`.djlintrc`、`.djlint_rules.yaml`、`.editorconfig` 或 `.gitignore` 变化时重新加载配置；否则在打开或保存文档时重新加载。`configuration` 或 `rules` 指定的文件会在打开或保存文档时重新读取。修改自定义规则的 `python_module` 代码后需要重启。
- 服务器一次只做一件事，因此较慢的规则会延迟后续操作。

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

## MegaLinter

djLint 已集成到 [MegaLinter](https://megalinter.io) 的百余个代码检查工具中。

运行 `npx mega-linter-runner --install` 并根据提示来安装它。

::: content

- [GitHub 仓库](https://github.com/oxsecurity/megalinter)
- [djlint - MegaLinter 文档](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
