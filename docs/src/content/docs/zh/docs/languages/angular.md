---
title: "Angular 模板检查"
description: "djLint是一个 angular 模板的代码检查工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。"
sidebar:
  label: "Angular"
---

djLint是一个 angular 模板的代码检查工具！使用内置的预设配置（profile），充分利用djLint来检查并格式化你的模板。

**[Angular简介](https://angular.io/guide/template-syntax)**

#### 使用命令行

```bash
djlint /path/to/templates --profile=angular
```

#### 使用配置文件

在你项目中的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile="angular"
```

```toml title="djlint.toml / .djlint.toml"
profile="angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
详情请参考 [配置](/zh/docs/configuration/) 章节
:::
