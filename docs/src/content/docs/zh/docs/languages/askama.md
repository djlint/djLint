---
title: "Askama 模板代码检查与格式化工具"
description: "djLint 可以检查和格式化 Askama 模板。设置 askama 预设，让规则和格式化方式适合这类模板。"
sidebar:
  label: "Askama"
---

djLint 可以检查和格式化 Askama 模板。设置 `askama` 预设，让规则和格式化方式适合这类模板。

**[什么是 Askama？](https://askama.readthedocs.io/)**

## 使用命令行

```bash
djlint /path/to/templates --profile=askama
```

## 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[查看配置指南，了解所有选项！](/zh/docs/configuration/)
:::
