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

## 在設定檔中

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
