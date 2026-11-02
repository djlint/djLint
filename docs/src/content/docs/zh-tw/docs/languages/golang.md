---
title: "Go 範本 Linter 與格式化工具"
description: "djLint 是 Go 範本 linter，也是 Go 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。"
sidebar:
  label: "Go 範本"
---

djLint 是 Go 範本 linter，也是 Go 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。

**[什麼是 Go 範本？](https://pkg.go.dev/text/template)**

Hugo 佈景主題和 Helm chart 也是以 Go 範本（`text/template`、`html/template`）為基礎，因此它們也請使用同一個 profile。

#### 使用命令列

```bash
djlint /path/to/templates --profile=golang
```

#### 或者，使用設定檔

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
