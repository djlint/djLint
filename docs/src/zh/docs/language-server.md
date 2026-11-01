---
description: 将 djLint 作为语言服务器运行，在任何支持 LSP 的编辑器中边输入边检查并格式化。
title: 语言服务器
keywords: 模板 linter, 模板格式化工具, djLint, HTML, 模板, 格式化工具, linter, 语言服务器, lsp, neovim, zed, helix
---

# 语言服务器

`djlint --lsp` 通过 stdio 将 djLint 作为语言服务器运行。它会持续运行，因此编辑器可以在输入时获得检查结果，并且格式化文档时无需每次启动新进程。

它报告检查结果并格式化整个文档，不需要额外的软件包。

## Neovim

在 Neovim 0.11 或更高版本中：

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

要格式化文档，请调用 `vim.lsp.buf.format()`。

## Zed

安装 [djLint 扩展](https://github.com/djlint/zed-djlint)。

## Helix

在 `languages.toml` 中：

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["vscode-html-language-server", "djlint"]
formatter = { command = "djlint", args = ["--reformat", "--quiet", "-"] }
```

## 设置

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

## 工作方式

- 检查结果会在输入短暂停顿后到达。支持拉取诊断的编辑器会主动请求，其他编辑器则由服务器推送。
- `exclude`、`extend_exclude` 和 `use_gitignore` 对打开的文档生效。被排除的文档没有检查结果，也不会被格式化。
- 如果编辑器支持监视文件，服务器会在 `pyproject.toml`、`djlint.toml`、`.djlint.toml`、`.djlintrc` 或 `.gitignore` 变化时重新加载配置。
