---
title: "Python API"
description: "通过 djLint API 在你自己的 Python 代码中格式化和检查模板。"
---

`djlint.api` 可以在 Python 程序中格式化和检查文本，结果与命令行完全相同。它面向编辑器、构建工具以及其他在内存中持有模板的程序。包中的其他部分在任何版本中都可能发生变化，因此请使用这个模块，而不要使用 `djlint.settings` 或 `djlint.lint`。[自定义规则示例](/zh/docs/linter/#python-模块规则)导入的辅助函数 `djlint.lint.get_line`、`djlint.helpers.inside_ignored_rule` 和 `djlint.helpers.inside_ignored_linter_block` 也会继续可用。

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, on_warning=None, **options)` 读取适用于某个文件夹中文件的配置。它从该文件夹开始向上查找配置，与命令行从传给它的第一个路径开始[查找](/zh/docs/configuration/)的方式相同，并且不会改变当前目录。

选项使用命令行选项的名称，但写成下划线形式，作用也与命令行中相同：设置了的值优先于配置文件，而 `False`、空字符串，以及对大多数选项而言的 `0`，都视为未指定。路径以 `pathlib.Path` 的形式给出。

读取配置需要一些时间，因此只要读取配置的那些文件没有变化，就应保留并复用结果。同一个结果可以用于任意数量的文本。

设置 `python_rules=False` 时，不会加载带有 `python_module` 的自定义规则，从而避免运行你不信任的项目中的代码。这些规则的名称会列在 `config.skipped_rules` 中。

`on_warning` 是一个接收消息的函数，会收到有关设置的每一条警告，例如名称拼错，或者某个规则代码没有对应的规则。不设置时，每条警告在每个进程中只会向 stderr 输出一次。无法读取的配置文件或无效的值会引发 `click.UsageError`。

## format_text

`format_text(config, text)` 返回格式化后的文本。第一行以 CRLF 结尾的文本，返回时使用 CRLF，其他文本则使用 LF。设置了 `require_pragma` 时，不含 pragma 的文本会原样返回。它从适用于传给 `load_config` 的文件夹的 `.editorconfig` 中读取 `indent` 和 `max_line_length`，而命令行则按每个文件的路径分别读取它们。

## lint_text

`lint_text(config, text, filename="-")` 返回一个 `Finding` 列表，按其在文档中出现的顺序排列。`per-file-ignores` 匹配的是 `filename`。设置了 `require_pragma` 时，不含 pragma 的文本不会有任何检查结果。

`Finding` 是一个具名元组，包含以下字段：

- `code`：规则代码，例如 `H013`。
- `message`：规则给出的消息。
- `match`：所发现文本的开头部分，最多 20 个字符。
- `line`、`column`：检查结果的起始位置。行号从 1 开始计数，列号从 0 开始计数。
- `end_line`、`end_column`：紧接在结束位置之后的位置，可能位于后面的某一行。

列按字符计数，而不是按字节或 UTF-16 码元计数。

## is_excluded

`is_excluded(config, path)` 判断某个文件是否会像在命令行中那样，被 `exclude`、`extend_exclude` 或 gitignore 排除。`format_text` 和 `lint_text` 本身不会检查这一点。

## 规则模块

自定义规则的 `python_module` 在每个进程中只导入一次，从配置所在的项目根目录导入。要读取另一个项目的规则，长期运行的程序必须从 `sys.modules` 中移除它从第一个项目导入的所有内容，并从 `sys.path` 的末尾移除该项目的根目录。
