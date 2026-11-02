---
title: "Liquid 模板代码检查与格式化工具"
description: "djLint 是一款 Liquid 模板代码检查工具，也是一款 Liquid 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。"
sidebar:
  label: "Liquid"
---

djLint 是一款 Liquid 模板代码检查工具，也是一款 Liquid 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。

**[什么是 Liquid？](https://shopify.github.io/liquid/)**

一个预设即可涵盖所有 Liquid 方言：Shopify 主题、Jekyll、LiquidJS（Eleventy）和 Fluid（Orchard Core）。

#### 使用命令行

```bash
djlint /path/to/templates --profile=liquid
```

#### 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile="liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile="liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[查看配置指南，了解所有选项！](/zh/docs/configuration/)
:::
