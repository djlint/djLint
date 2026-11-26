---
title: "集成"
description: "在编辑器中使用 djLint，并通过 pre-commit 运行它。"
---

无论使用哪种编辑器，都请把 djLint 安装在编辑器能找到的位置，最好是项目的虚拟环境中，然后从该环境启动编辑器，或者让编辑器指向该环境中的 `djlint`。这样，编辑器运行的就是项目锁定的版本，结果与 pre-commit 钩子或 CI 中的一致。

如果项目用 [npm](/zh/docs/getting-started/#安装) 安装 djLint，它的命令是项目中的 `node_modules/.bin/djlint`，在 Windows 上是 `node_modules/.bin/djlint.cmd`。下面的编辑器中运行 `djlint` 的地方，请填写这个路径。这是相对路径：如果编辑器不是在包含 `node_modules` 的目录中运行 djLint，请填写完整路径。VS Code 和 Zed 的扩展会自己找到它。

## Visual Studio Code

从 Visual Studio Marketplace 安装 [djLint 扩展](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)。Cursor、Windsurf、VSCodium 等基于 VS Code 的编辑器则从 [Open VSX 安装同一个扩展](https://open-vsx.org/extension/monosans/djlint)。它会在你的环境中查找 djLint，找不到时回退到内置的 djLint；如果你的 djLint 支持语言服务器，它就会使用语言服务器。

其 [README](https://github.com/djlint/djlint-vscode#readme) 介绍了它的设置，以及它运行的是哪个 djLint。

## Zed

[djLint 扩展](https://github.com/djlint/djlint-zed)在 HTML 以及 Django、Jinja、Twig 等模板扩展的语言中运行[语言服务器](#语言服务器)。它还没有进入 Zed 的扩展注册表，所以要作为开发扩展安装：

1. 通过 [rustup](https://rustup.rs) 安装 Rust，Zed 用它构建扩展，并会自动添加 `wasm32-wasip2` 目标。如果 Rust 是用 Homebrew 或 Nix 等其他方式安装的，需要自己添加这个目标。
1. 克隆扩展：

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. 在 Zed 中打开命令面板（macOS 上是 `cmd-shift-p`，其他系统是 `ctrl-shift-p`），运行 **zed: install dev extension**，选择克隆下来的 `djlint-zed` 文件夹。

要更新它，在该文件夹中运行 `git pull`，然后运行 **zed: rebuild dev extension**。

需要 PATH 中或项目里用 npm 安装的 djLint 1.49 或更新版本，或者有 [uv](https://docs.astral.sh/uv/)，它无需安装即可运行 djLint。其 [README](https://github.com/djlint/djlint-zed#readme) 介绍了如何把它设为某个语言的格式化工具，以及它的设置。

## Neovim

Neovim 不会给一些模板扩展名设置文件类型。无论你使用下面哪种方式，都请先注册它们：

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### 内置 LSP 客户端（推荐）

Neovim 0.11 及更高版本可以直接与 djLint 的[语言服务器](#语言服务器)通信，无需任何插件。这样可以在输入时得到检查结果，并带有下划线标出的范围，还能用 `vim.lsp.buf.format()` 格式化。

v2.12.0 之后的 [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) 自带它的配置，装了它只需一行：

```lua
vim.lsp.enable("djlint")
```

如果项目用 npm 安装了 djLint，请在这一行之前加上 `vim.lsp.config("djlint", { cmd = { "node_modules/.bin/djlint", "--lsp" } })`（Windows 上用 `"node_modules/.bin/djlint.cmd"`）。

不用 nvim-lspconfig 或版本较旧时，请自行定义配置：

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

要在保存时格式化，请在同一配置中添加以下内容：

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

请参阅[设置](#设置)。

### conform.nvim 和 nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) 负责格式化，[nvim-lint](https://github.com/mfussenegger/nvim-lint) 负责代码检查，两者都以命令的形式运行 djLint。检查结果没有下划线标出的范围，并且只有在你让 nvim-lint 执行检查时才会出现。预设和命令行一样，来自项目的[配置](/zh/docs/configuration/#profile)。此示例需要 djLint 1.49 或更高版本。

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

- [GitHub 仓库](https://github.com/nvimtools/none-ls.nvim)
- [代码检查](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [格式化](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [npm 包](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains IDE

在 PyCharm 以及其他基于 IntelliJ 的 IDE 中，请使用免费的 [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) 插件：

1. 从 Marketplace 安装 LSP4IJ。
1. 打开 LSP Consoles 工具窗口，添加一个新的语言服务器。
1. 在 **Server** 选项卡中，将名称设为 `djLint`，将命令设为 `djlint --lsp`；如果它不在 PATH 中，请使用项目虚拟环境中 `djlint` 的完整路径。
1. 在 **Mappings** 选项卡中，添加你的模板的文件名模式。如果项目的配置中没有设置[预设](/zh/docs/configuration/#profile)，就由每个模式的语言 ID 来选择预设：

   | 模式                                  | 语言 ID                          |
   | ------------------------------------- | -------------------------------- |
   | `*.html`, `*.htm`                     | `html`，Django 中为 `htmldjango` |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                          |
   | `*.njk`, `*.twig`                     | `nunjucks`                       |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                     |
   | `*.liquid`                            | `liquid`                         |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                         |
   | `*.tera`                              | `tera`                           |
   | `*.mako`                              | `mako`                           |

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

通过 Package Control 安装 SublimeLinter 和 [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint)。djLint 必须位于 Sublime Text 所见的 PATH 中。

## Helix

Helix 可以通过 `languages.toml` 运行[语言服务器](#语言服务器)。`language-servers` 列表会替换 Helix 为该语言设置的列表，所以请在 `djlint` 之后保留 Helix 自带的服务器：

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

Helix 本身不会把任何文件当作 `htmldjango` 打开。在 Django 项目中，请在项目的 `.helix/languages.toml` 里为这一项添加 `file-types = ["html"]`。

## Emacs

使用 Emacs 29 及更高版本自带的 Eglot：

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

然后在模板中运行 `M-x eglot`。`eglot-format-buffer` 可以格式化该模板。`html-mode`、`mhtml-mode` 和 `web-mode` 不表明模板语言，因此在这些模式中，预设来自项目的[配置](/zh/docs/configuration/#profile)。

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

`--sarif` 只会向 stdout 写入一个 SARIF 2.1.0 文档，不输出其他任何内容，因此可以像上面那样重定向。其中会列出每条已启用的规则及其文档链接，每条检查结果都带有行号和列号；配合 `--check` 使用时，需要重新格式化的文件会在 `formatting` 规则下报告。

## pre-commit

djLint 可以用作 [pre-commit](https://pre-commit.com) 钩子，既能做代码检查，也能做格式化。

下表中的每个预设都有一个做代码检查的钩子（列在表中），以及一个做格式化的钩子，名称相同但带有 `reformat`：例如 `djlint-django` 对应 `djlint-reformat-django`。它们会设置 `--profile` 以及 pre-commit 传入的文件。`angular` 没有自己的钩子：请给 `djlint` 或 `djlint-reformat` 设置 `args: [--profile=angular]`。

| 钩子                | 预设       | 文件                                 |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | 无         | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

对于使用其他扩展名的模板，请在配置中覆盖 `files`；如果钩子设置了 `types_or`，也要一并覆盖，因为 pre-commit 要求两者都匹配。请参阅 [pre-commit 文档](https://pre-commit.com/#pre-commit-configyaml---hooks)。

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

[MegaLinter](https://megalinter.io) 已内置 djLint。运行 `npx mega-linter-runner --install` 进行设置，选项请参阅[其 djLint 页面](https://megalinter.io/latest/descriptors/html_djlint/)。
