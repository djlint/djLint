---
title: "Nunjucks 模板代码检查与格式化工具"
description: "djLint 是一款 Nunjucks 模板代码检查工具，也是一款 Nunjucks 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。"
sidebar:
  label: "Nunjucks"
---

djLint 是一款 Nunjucks 模板代码检查工具，也是一款 Nunjucks 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。

**[什么是 Nunjucks？](https://mozilla.github.io/nunjucks/)**

Pebble（Java）模板与 Twig 兼容，因此也请为它们使用这个预设。

#### 使用命令行

```bash
djlint /path/to/templates --profile=nunjucks
```

#### 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[查看配置指南，了解所有选项！](/zh/docs/configuration/)
:::
