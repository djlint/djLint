---
title: "Jinja 模板检查与格式化"
description: "djLint是一个 jinja 模板的代码检查与格式化工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。"
sidebar:
  label: "Jinja"
---

djLint是一个 jinja 模板的代码检查与格式化工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。

**[Jinja简介](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 模板与 Jinja2 完全兼容，请使用同一个 `jinja` 配置。

HubSpot 的 Jinjava 模板也是 jinja 风格，也请使用此配置。

#### 使用命令行

```bash
djlint /path/to/templates --profile=jinja
```

#### 使用配置文件

在你项目中的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile="jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile="jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
详情请参考 [配置](/zh/docs/configuration/) 章节
:::
