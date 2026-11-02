---
title: "Jinja 範本 Linter 與格式化工具"
description: "djLint 是 jinja 範本 linter，也是 jinja 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。"
sidebar:
  label: "Jinja"
---

djLint 是 jinja 範本 linter，也是 jinja 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。

**[什麼是 Jinja？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 範本與 Jinja2 完全相容，因此請使用同一個 `jinja` profile。

HubSpot 的 Jinjava 範本也是 jinja 風格，因此它們也請使用這個 profile。

#### 使用命令列

```bash
djlint /path/to/templates --profile=jinja
```

#### 或者，使用設定檔

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
