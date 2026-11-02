---
title: "Jinja 模板代码检查与格式化工具"
description: "djLint 是一款 Jinja 模板代码检查工具，也是一款 Jinja 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。"
sidebar:
  label: "Jinja"
---

djLint 是一款 Jinja 模板代码检查工具，也是一款 Jinja 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。

**[什么是 Jinja？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 模板与 Jinja2 完全兼容，因此同样使用这个 `jinja` 预设。

HubSpot 的 Jinjava 模板同样是 Jinja 风格，因此也请为它们使用这个预设。

#### 使用命令行

```bash
djlint /path/to/templates --profile=jinja
```

#### 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile="jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile="jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[查看配置指南，了解所有选项！](/zh/docs/configuration/)
:::
