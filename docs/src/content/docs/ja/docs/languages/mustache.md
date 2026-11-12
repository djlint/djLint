---
title: "Mustache テンプレートのリンターとフォーマッター"
description: "djLint で Mustache テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、handlebars プロファイルを設定してください。"
sidebar:
  label: "Mustache"
---

djLint で Mustache テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`handlebars` プロファイルを設定してください。

**[Mustache とは？](https://mustache.github.io/mustache.5.html)**

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=handlebars
```

## または、設定ファイルを使う

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

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
