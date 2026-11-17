---
title: "Nunjucks 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Nunjucks 範本。設定 nunjucks profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Nunjucks"
---

djLint 可以 lint 並格式化 Nunjucks 範本。設定 `nunjucks` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Nunjucks？](https://mozilla.github.io/nunjucks/)**

## 使用命令列

```bash
djlint /path/to/templates --profile=nunjucks
```

## 在設定檔中

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
