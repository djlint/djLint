---
title: "Go 模板代码检查与格式化工具"
description: "djLint 可以检查和格式化 Go 模板。设置 golang 预设，让规则和格式化方式适合这类模板。"
sidebar:
  label: "Go 模板"
---

djLint 可以检查和格式化 Go 模板。设置 `golang` 预设，让规则和格式化方式适合这类模板。

**[什么是 Go 模板？](https://pkg.go.dev/text/template)**

Hugo 主题和 Helm chart 同样基于 Go 模板（`text/template`、`html/template`），因此也请为它们使用这个预设。

## 使用命令行

```bash
djlint /path/to/templates --profile=golang
```

## 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[查看配置指南，了解所有选项！](/zh/docs/configuration/)
:::
