---
title: "Twig 模板检查与格式化"
description: "djLint是一个 twig 模板的代码检查与格式化工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。"
sidebar:
  label: "Twig"
---

djLint是一个 twig 模板的代码检查与格式化工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。

**[Twig简介](https://twig.symfony.com/)**

Pebble（Java）模板与 Twig 兼容，请为其使用同一个配置。

#### 使用命令行

```bash
djlint /path/to/templates --profile=nunjucks
```

#### 使用配置文件

在你项目中的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
详情请参考 [配置](/zh/docs/configuration/) 章节
:::
