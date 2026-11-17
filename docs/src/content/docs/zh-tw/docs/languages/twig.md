---
title: "Twig 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Twig 範本。設定 nunjucks profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Twig"
---

djLint 可以 lint 並格式化 Twig 範本。設定 `nunjucks` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Twig？](https://twig.symfony.com/)**

Pebble（Java）範本與 Twig 相容，因此它們也請使用同一個 profile。

## 使用命令列

```bash
djlint /path/to/templates --profile=nunjucks
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

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
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
