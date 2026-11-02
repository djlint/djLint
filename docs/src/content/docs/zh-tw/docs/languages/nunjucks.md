---
title: "Nunjucks 範本 Linter 與格式化工具"
description: "djLint 是 nunjucks 範本 linter，也是 nunjucks 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。"
sidebar:
  label: "Nunjucks"
---

djLint 是 nunjucks 範本 linter，也是 nunjucks 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。

**[什麼是 Nunjucks？](https://mozilla.github.io/nunjucks/)**

Pebble（Java）範本與 Twig 相容，因此它們也請使用同一個 profile。

#### 使用命令列

```bash
djlint /path/to/templates --profile=nunjucks
```

#### 或者，使用設定檔

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
