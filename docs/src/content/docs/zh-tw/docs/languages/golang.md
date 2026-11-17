---
title: "Go 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Go 範本。設定 golang profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Go 範本"
---

djLint 可以 lint 並格式化 Go 範本。設定 `golang` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Go 範本？](https://pkg.go.dev/text/template)**

Hugo 佈景主題和 Helm chart 也是以 Go 範本（`text/template`、`html/template`）為基礎，因此它們也請使用同一個 profile。

## 使用命令列

```bash
djlint /path/to/templates --profile=golang
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

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
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
