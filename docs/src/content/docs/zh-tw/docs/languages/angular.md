---
title: "Angular 範本 Linter"
description: "djLint 是 Angular 範本 linter！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。"
sidebar:
  label: "Angular"
---

djLint 是 Angular 範本 linter！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。

**[什麼是 Angular？](https://angular.io/guide/template-syntax)**

#### 使用命令列

```bash
djlint /path/to/templates --profile=angular
```

#### 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

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
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
