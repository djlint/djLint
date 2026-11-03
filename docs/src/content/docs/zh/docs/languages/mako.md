---
title: "Mako 模板代码检查与格式化工具"
description: "djLint 可以检查和格式化 Mako 模板。设置 mako 预设，让规则和格式化方式适合这类模板。"
sidebar:
  label: "Mako"
---

djLint 可以检查和格式化 Mako 模板。设置 `mako` 预设，让规则和格式化方式适合这类模板。

**[什么是 Mako？](https://www.makotemplates.org/)**

使用 mako 预设时，`% if x:` 这样的控制行和 `##` 注释始终独占一行；属性由控制行决定的标签会保持原样。Python 块以及 `<%doc>` 和 `<%text>` 的内容不会被改动；在 `--format-js` 或 `--format-css` 下，含有 Mako 语法的 script 或 style 也保持原样。`% if` 与 `% endif` 之间的行，以及各自独占一行的 `<%block>` 或 `<%def>` 标签与其结束标签之间的行，会像其他块一样缩进。`${}` 表达式中的代码保持原样。

## 使用命令行

```bash
djlint /path/to/templates --profile=mako
```

## 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[查看配置指南，了解所有选项！](/zh/docs/configuration/)
:::
