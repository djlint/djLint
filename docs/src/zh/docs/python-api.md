---
description: 使用 djLint API 在你自己的 Python 代码中格式化和检查模板。
title: Python API
keywords: 模板 linter, 模板格式化工具, djLint, HTML, 模板, 格式化工具, linter, python, api
---

# Python API

`djlint.api` 可以在 Python 程序中格式化和检查文本，结果与命令行相同。它面向编辑器、构建工具以及任何在内存中持有模板的程序。包中的其他内容可能在任何版本中改变，因此请使用此模块，而不是 `djlint.settings` 或 `djlint.lint`。

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)` 读取适用于某个文件夹中文件的配置。它从该文件夹向上查找，就像命令行从当前目录查找一样，并且不会改变当前目录。

选项名称与命令行选项相同，使用下划线，并优先于配置文件。路径以 `pathlib.Path` 传入。

读取配置需要一些时间，因此只要被读取的文件没有变化，就请保留结果。它可以用于任意数量的文本。

使用 `python_rules=False` 时，不会加载带有 `python_module` 的自定义规则，这样你不信任的项目代码就不会运行。它们的名称保存在 `config.skipped_rules` 中。

## format_text

`format_text(config, text)` 返回格式化后的文本。换行符保持不变。使用 `require_pragma` 时，没有 pragma 的文本会原样返回。

## lint_text

`lint_text(config, text, filename="-")` 按文档顺序返回 `Finding` 列表。`per-file-ignores` 与 `filename` 进行匹配。使用 `require_pragma` 时，没有 pragma 的文本不会有任何结果。

`Finding` 是一个具名元组，包含以下字段：

::: content

- `code`: 规则代码，例如 `H013`。
- `message`: 规则的消息。
- `match`: 找到的文本开头，最多 20 个字符。
- `line`, `column`: 结果开始的位置。行从 1 开始计数，列从 0 开始计数。
- `end_line`, `end_column`: 紧接结束处之后的位置，可能在后面的行。
  :::

列按字符计数，而不是按字节或 UTF-16 代码单元计数。

## 规则模块

自定义规则的 `python_module` 在每个进程中只导入一次，从配置所属的项目根目录导入。长期运行并处理多个项目的程序，需要从 `sys.modules` 中移除该模块才能重新读取它。
