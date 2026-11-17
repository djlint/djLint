---
title: "Jinja 模板代码检查与格式化工具"
description: "djLint 可以检查和格式化 Jinja 模板。设置 jinja 预设，让规则和格式化方式适合这类模板。"
sidebar:
  label: "Jinja"
---

djLint 可以检查和格式化 Jinja 模板。设置 `jinja` 预设，让规则和格式化方式适合这类模板。

**[什么是 Jinja？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 遵循 Jinja2 的语法，HubSpot 的 Jinjava 模板也是 Jinja 风格，因此两者都请使用 `jinja` 预设。

## 使用命令行

```bash
djlint /path/to/templates --profile=jinja
```

## 在配置文件中

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

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
