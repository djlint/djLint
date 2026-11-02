---
title: "Nunjucks 模板代码检查与格式化工具"
description: "djLint 可以检查和格式化 Nunjucks 模板。设置 nunjucks 预设，让规则和格式化方式适合这类模板。"
sidebar:
  label: "Nunjucks"
---

djLint 可以检查和格式化 Nunjucks 模板。设置 `nunjucks` 预设，让规则和格式化方式适合这类模板。

**[什么是 Nunjucks？](https://mozilla.github.io/nunjucks/)**

Pebble（Java）模板与 Twig 兼容，因此也请为它们使用这个预设。

## 使用命令行

```bash
djlint /path/to/templates --profile=nunjucks
```

## 或者，使用配置文件

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
