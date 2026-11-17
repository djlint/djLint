---
title: "Jinja 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Jinja 範本。設定 jinja profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Jinja"
---

djLint 可以 lint 並格式化 Jinja 範本。設定 `jinja` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Jinja？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 遵循 Jinja2 的語法，HubSpot 的 Jinjava 範本也是 Jinja 風格，因此兩者都請使用 `jinja` profile。J004 和 J018 會建議使用 Flask 的 `url_for`，因此在未使用 Flask 的專案中請忽略它們。

## 使用命令列

```bash
djlint /path/to/templates --profile=jinja
```

## 在設定檔中

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
