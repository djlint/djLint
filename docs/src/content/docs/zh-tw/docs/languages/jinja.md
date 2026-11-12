---
title: "Jinja 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Jinja 範本。設定 jinja profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Jinja"
---

djLint 可以 lint 並格式化 Jinja 範本。設定 `jinja` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Jinja？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 範本與 Jinja2 完全相容，因此請使用同一個 `jinja` profile。

HubSpot 的 Jinjava 範本也是 jinja 風格，因此它們也請使用這個 profile。

## 使用命令列

```bash
djlint /path/to/templates --profile=jinja
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
