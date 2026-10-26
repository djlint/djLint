---
title: "Django 模板检查与格式化"
description: "djLint是一个 django 模板的代码检查与格式化工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。"
sidebar:
  label: "Django"
---

djLint是一个 django 模板的代码检查与格式化工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。

**[Django简介](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### 使用命令行

```bash
djlint /path/to/templates --profile=django
```

#### 使用配置文件

在你项目中的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
详情请参考 [配置](/zh/docs/configuration/) 章节
:::
