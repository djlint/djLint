---
title: "Askama 範本 Linter 與格式化工具"
description: "djLint 是 Askama 範本 linter，也是 Askama 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。"
sidebar:
  label: "Askama"
---

djLint 是 Askama 範本 linter，也是 Askama 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。

**[什麼是 Askama？](https://askama.readthedocs.io/)**

#### 使用命令列

```bash
djlint /path/to/templates --profile=askama
```

#### 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
