---
title: "Mako 範本 Linter 與格式化工具"
description: "djLint 可以 lint 並格式化 Mako 範本。設定 mako profile，讓規則與格式化方式符合這類範本。"
sidebar:
  label: "Mako"
---

djLint 可以 lint 並格式化 Mako 範本。設定 `mako` profile，讓規則與格式化方式符合這類範本。

**[什麼是 Mako？](https://www.makotemplates.org/)**

使用 mako profile 時，`% if x:` 這類控制行和 `##` 註解一定會單獨佔一行；屬性取決於控制行的標籤會保持原樣。Python 區塊以及 `<%doc>` 和 `<%text>` 的內容不會被更動；在 `--format-js` 或 `--format-css` 下，含有 Mako 語法的 script 或 style 也會保持原樣。`% if` 與 `% endif` 之間的行，以及各自單獨佔一行的 `<%block>` 或 `<%def>` 標籤與其結束標籤之間的行，會像其他區塊一樣縮排。`${}` 運算式中的程式碼保持原樣。

## 使用命令列

```bash
djlint /path/to/templates --profile=mako
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::
