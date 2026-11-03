---
title: "Tera 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Tera 範本。設定 tera profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Tera"
---

djLint 可以 lint 並格式化 Tera 範本。設定 `tera` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Tera？](https://keats.github.io/tera/)**

## 使用命令列

```bash
djlint /path/to/templates --profile=tera
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
