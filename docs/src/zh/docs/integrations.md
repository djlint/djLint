---
description: 将 djLint 集成到你喜爱的编辑器中。使用 pre-commit 自动格式化模板。在 Sublime Text 中进行代码检查。
title: 集成
keywords: 模板代码检查工具, 模板格式化工具, djLint, HTML, 模板, 格式化工具, 代码检查工具, 集成, 语言服务器, lsp, neovim, helix
---

# 集成

djLint 已有多种编辑器集成。

无论使用哪种编辑器，都请把 djLint 安装在编辑器能找到的位置，最好是项目的虚拟环境中，然后从该环境启动编辑器，或者让编辑器指向该环境中的 `djlint`。这样，编辑器运行的就是项目锁定的版本，结果与 pre-commit 钩子或 CI 中的一致。

## Visual Studio Code

安装 [djLint 扩展](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)；如果使用 VSCodium，则安装 [Open VSX 上的版本](https://open-vsx.org/extension/monosans/djlint)。它会在你的环境中查找 djLint，找不到时回退到内置的 djLint；如果你的 djLint 支持语言服务器，它就会使用语言服务器。

其代码托管在 [GitHub](https://github.com/djlint/djlint-vscode) 上。

## Neovim

在 Neovim 中，djLint 既可以用作代码检查工具，也可以用作格式化工具。

### 内置 LSP 客户端（推荐）

Neovim 0.11 及更高版本可以直接与 djLint 的[语言服务器](#语言服务器)通信，无需任何插件。这样可以在输入时得到检查结果，并带有下划线标出的范围，还能使用 `vim.lsp.buf.format()` 进行格式化：

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

要在保存时格式化，请在同一配置中添加以下内容：

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

请参阅[设置](#设置)。

### conform.nvim 和 nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) 负责格式化，[nvim-lint](https://github.com/mfussenegger/nvim-lint) 负责代码检查，两者都以命令的形式运行 djLint。检查结果没有下划线标出的范围，并且只有在你让 nvim-lint 执行检查时才会出现。

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

::: content

- [GitHub 仓库](https://github.com/nvimtools/none-ls.nvim)
- [代码检查](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [格式化](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
:::

### efm-langserver

::: content

- [GitHub 仓库](https://github.com/mattn/efm-langserver)

1. 通过 Mason 使用 `:MasonInstall efm djlint` 安装 efm-langserver 和 djLint
1. 将 `htmldjango` 添加到 `filetypes` 中。
1. 创建格式化配置：

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. 通过 `htmldjango = { djlint }` 将语言与格式化工具关联起来。

配置示例：

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

- [npm 包](https://www.npmjs.com/package/coc-htmldjango)
:::

## JetBrains IDE

在 PyCharm 以及其他基于 IntelliJ 的 IDE 中，请使用免费的 [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) 插件：

1. 从 Marketplace 安装 LSP4IJ。
1. 打开 LSP Consoles 工具窗口，添加一个新的语言服务器。
1. 在 **Server** 选项卡中，将名称设为 `djLint`，将命令设为 `djlint --lsp`；如果它不在 PATH 中，请使用项目虚拟环境中 `djlint` 的完整路径。
1. 在 **Mappings** 选项卡中，为你的模板添加文件名模式，例如 `*.html`。如果项目的配置中没有设置[预设](/zh/docs/configuration/#profile)，对于 Django 项目，请将语言 ID 设为 `htmldjango`，以便选中正确的预设。
1. 在 **Configuration** 选项卡中，可以以 JSON 格式在 `djlint` 键下填写[设置](#设置)。

检查结果会显示在编辑器中，并且 **Reformat Code** 可以对已映射的文件使用该服务器。

## Sublime Text

### LSP（推荐）

[LSP](https://packagecontrol.io/packages/LSP) 包会运行[语言服务器](#语言服务器)，从而在输入时提供检查结果，并支持格式化。

运行 **Preferences: LSP Server Configurations** 并添加：

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

djLint 可以用作 Sublime Text 的 Linter 插件，可通过 [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) 安装。

::: content

1. `cmd + shift + p`
2. 安装 SublimeLinter
3. 安装 SublimeLinter-contrib-djlint
:::

请确保 djLint 安装在全局 Python 中，或者位于 `PATH` 上。

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

然后在模板中运行 `M-x eglot`。`eglot-format-buffer` 可以格式化该模板。

## 语言服务器

`djlint --lsp` 会通过 stdio 将 djLint 作为语言服务器运行。它会持续运行，因此编辑器可以在你输入时获得检查结果，格式化文档时也无需每次都启动一个进程。

它会报告检查结果，并能格式化整个文档。它不需要额外的包。任何支持 LSP 的编辑器都可以用同一条命令运行它。

### 设置

服务器读取项目[配置](/zh/docs/configuration/)的方式与命令行相同：从每个文件所在的文件夹开始向上查找。编辑器中的设置优先于项目配置，但与命令行一样，它们只能开启某个选项或设置某个值：`false` 无法关闭项目中开启的选项。设置使用[命令行选项](/zh/docs/configuration/)的名称，可以写成下划线形式或 camelCase 形式；以逗号分隔的值可以写成列表：

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

服务器通过 `workspace/configuration` 请求 `djlint` 部分。无法响应该请求的编辑器，可以在 `initializationOptions` 中发送相同的键。

有两项设置没有对应的命令行选项：

- `use_editor_indentation`：使用编辑器的制表符大小进行格式化，而不是使用 `indent`。
- `python_rules`：设为 `false` 可跳过带有 `python_module` 的自定义规则，从而避免运行项目中的代码。

djLint 会从以下来源中第一个设置了 `profile` 的来源获取它：

1. 编辑器的设置。
1. 项目的配置。
1. 文档的语言：例如，`htmldjango` 会使用 `django` 预设。

如果以上都没有设置，它会像在命令行中一样，不使用任何预设运行。在项目配置中设置 `profile` 是最简单的做法：它在所有编辑器中都有效，也无需设置语言 ID。

### 工作方式

- 检查结果会在你停止输入片刻后出现。支持拉取诊断（pull diagnostics）的编辑器会主动请求结果，其他编辑器则由服务器推送。
- `exclude`、`extend_exclude` 和 `use_gitignore` 对已打开的文档同样生效。被排除的文档不会有检查结果，也不会被格式化。
- 当 `pyproject.toml`、`djlint.toml`、`.djlint.toml`、`.djlintrc`、`.djlint_rules.yaml`、`.editorconfig` 或 `.gitignore` 发生变化时，如果编辑器能够监视文件，服务器就会重新加载配置；否则会在打开或保存文档时重新加载。`configuration` 或 `rules` 指定的文件会在打开或保存文档时重新读取。修改自定义规则的 `python_module` 代码后，需要重启服务器。
- 运行缓慢的规则会拖慢其后的处理，因为服务器一次只做一件事。

## GitHub Actions

在 GitHub Actions 工作流中，djLint 会把每条检查结果报告为一个注解（annotation），使其以内联方式显示在拉取请求的差异中。无需任何配置：djLint 会检测到工作流并自动切换输出方式。

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

使用 `--no-github-output` 可以改为输出普通的控制台格式，使用 `--github-output` 则可以在 Actions 之外强制输出注解。

注解只属于某一个拉取请求。如果想把检查结果保留在仓库的 Security 选项卡中，并保留各次运行的历史记录，请将其写成 SARIF 格式并上传该文件：

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

上传步骤需要在作业或工作流上授予 `security-events: write` 权限。

`--sarif` 只会向 stdout 写入一个 SARIF 2.1.0 文档，不输出其他任何内容，因此可以像上面那样重定向。其中会列出每条已启用的规则及其文档链接，每条检查结果都带有行号和列号；配合 `--check` 使用时，需要重新格式化的文件会在 `formatting` 规则下报告。Azure DevOps、GitLab 以及大多数编辑器都能读取这种格式。

## Pre-Commit

djLint 可以用作 [pre-commit](https://pre-commit.com) 钩子，既能做代码检查，也能做格式化。

该仓库为特定的 djLint 预设提供了多个预先配置好的钩子（它们只是预先设置了 `--profile` 参数，并告诉 pre-commit 要查找哪些文件扩展名）：

::: content

- `djlint` 用于代码检查，`djlint-reformat` 用于格式化
  查找匹配 `*.html` 的文件，不设置 `--profile`。
- `djlint-django` 和 `djlint-reformat-django`
  查找匹配 `*.html` 的文件，并设置 `--profile=django`。
- `djlint-jinja` 和 `djlint-reformat-jinja`
  查找匹配 `*.j2`、`*.jinja` 或 `*.jinja2` 的文件，并设置 `--profile=jinja`。
- `djlint-nunjucks` 和 `djlint-reformat-nunjucks`
  查找匹配 `*.njk` 的文件，并设置 `--profile=nunjucks`。
- `djlint-handlebars` 和 `djlint-reformat-handlebars`
  查找匹配 `*.hbs` 的文件，并设置 `--profile=handlebars`。
- `djlint-liquid` 和 `djlint-reformat-liquid`
  查找匹配 `*.html` 的文件，并设置 `--profile=liquid`。
- `djlint-golang` 和 `djlint-reformat-golang`
  查找匹配 `*.gotmpl` 的文件，并设置 `--profile=golang`。
- `djlint-tera` 和 `djlint-reformat-tera`
  查找匹配 `*.html` 的文件，并设置 `--profile=tera`。
- `djlint-askama` 和 `djlint-reformat-askama`
  查找匹配 `*.html` 的文件，并设置 `--profile=askama`。
:::

请注意，这些预定义钩子接受的输入有时过于保守（你的模板可能使用了不同的扩展名），因此 pre-commit 明确允许你覆盖其中任何预定义选项。更多配置请参阅 [pre-commit 文档](https://pre-commit.com/#pre-commit-configyaml---hooks)。

### 默认 Django 示例

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### 使用 .html 而非 .hbs 扩展名的 Handlebars

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

可以使用 `files` 或 `exclude` 参数把每个钩子限定在各自的目录中，从而在同一个仓库中支持多种模板语言。

## MegaLinter

djlint 已原生内置于 [MegaLinter](https://megalinter.io) 的 100 多个代码检查工具之中

要安装它，只需运行 `npx mega-linter-runner --install` 并按照说明操作

::: content

- [GitHub 仓库](https://github.com/oxsecurity/megalinter)
- [MegaLinter 文档中的 djlint](https://megalinter.io/latest/descriptors/html_djlint/)
:::
