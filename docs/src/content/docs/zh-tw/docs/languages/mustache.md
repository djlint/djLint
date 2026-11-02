---
title: "Mustache 範本 Linter 與格式化工具"
description: "djLint 是 mustache 範本 linter，也是 mustache 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。"
sidebar:
  label: "Mustache"
---

djLint 是 mustache 範本 linter，也是 mustache 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。

**[什麼是 Mustache？](https://mustache.github.io/mustache.5.html)**

#### 使用命令列

```bash
djlint /path/to/templates --profile=handlebars
```

#### 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
