---
title: "Handlebars テンプレートのリンターとフォーマッター"
description: "djLint で Handlebars テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、handlebars プロファイルを設定してください。"
sidebar:
  label: "Handlebars"
---

djLint で Handlebars テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`handlebars` プロファイルを設定してください。

**[Handlebars とは？](https://handlebarsjs.com/)**

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=handlebars
```

## 設定ファイルで

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```
