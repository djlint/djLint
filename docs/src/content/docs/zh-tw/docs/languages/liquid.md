---
title: "Liquid 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Liquid 範本。設定 liquid profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Liquid"
---

djLint 可以 lint 並格式化 Liquid 範本。設定 `liquid` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Liquid？](https://shopify.github.io/liquid/)**

一個 profile 就涵蓋所有 Liquid 方言：Shopify 佈景主題、Jekyll、LiquidJS（Eleventy）和 Fluid（Orchard Core）。

## 使用命令列

```bash
djlint /path/to/templates --profile=liquid
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
