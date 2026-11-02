---
title: "Django 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Django 範本。設定 django profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Django"
---

djLint 可以 lint 並格式化 Django 範本。設定 `django` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Django？](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## 使用命令列

```bash
djlint /path/to/templates --profile=django
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
