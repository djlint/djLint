---
title: "Django 範本 Linter 與格式化工具"
description: "djLint 是 django 範本 linter，也是 django 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。"
sidebar:
  label: "Django"
---

djLint 是 django 範本 linter，也是 django 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。

**[什麼是 Django？](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### 使用命令列

```bash
djlint /path/to/templates --profile=django
```

#### 或者，使用設定檔

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
